#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from dramatica.common import CacheDB, logging
from dramatica.timeutils import *

DEFAULT_BLOCK_DURATION = 600


class DramaticaObject(object):
    default = {
        "title" : "Unnamed object"
        }

    def __init__(self, **kwargs):
        self.meta = {}
        self.meta.update(self.default)
        self.meta.update(kwargs)

    def __getitem__(self, key):
        return self.meta.get(key, False)

    def __setitem__(self, key, value):
        self.meta[key] = value


class BlockItem(DramaticaObject):
    default = {
        "title"     : "(dramatica auto object)",
        "item_type" : "auto",
        "duration"  : "0"
        }

    def __init__(self, **kwargs):
        super(BlockItem, self).__init__()
        if "id_asset" in kwargs and "db" in kwargs:
            db = kwargs["db"]
            del(kwargs["db"])
            db.query("SELECT tag, value FROM assets WHERE id_asset = {}".format(kwargs["id_asset"]))
            for tag, value in db.fetchall():
                self.meta[tag] = value
        self.meta.update(kwargs)


    @property
    def duration(self):
        return float(self["duration"])


class Block(DramaticaObject):
    default = {}
    def __init__(self, rundown, **kwargs):
        super(Block, self).__init__(**kwargs)
        self.rundown   = rundown
        self.db          = self.rundown.db
        self.asset       = self.rundown.asset
        self.block_order = len(self.rundown.blocks)
        self.items = []
        self.rendered = False

    @property
    def block_type(self):
        return self.__class__.__name__

    @property
    def duration(self):
        dur = 0
        if self.items:
            for item in self.items:
                dur += item.duration
        else:
            start_time = self.broadcast_start
            end_time   = self.scheduled_end
            dur = self["target_duration"] or end_time - start_time

        return dur

    @property
    def scheduled_start(self):
        if self["start"]:
            return self.rundown.clock(*self["start"])

        elif self.block_order == 0:
            return self.rundown.day_start

        return self.rundown.blocks[self.block_order-1].scheduled_end
        

    @property
    def scheduled_end(self):
        try:
            remaining_blocks = self.rundown.blocks[self.block_order+1:]
        except:
            return self.rundown.day_end

        inter_blocks = 1
        for block in remaining_blocks:
            next_fixed_start = block["start"]
            if next_fixed_start:
                next_fixed_start = self.rundown.clock(*next_fixed_start)
                break
            inter_blocks += 1
        else:
            next_fixed_start = self.rundown.day_end

        scheduled_end = self.scheduled_start + ((next_fixed_start - self.scheduled_start) / inter_blocks)
        if inter_blocks > 1:
            scheduled_end = scheduled_end - (scheduled_end % 300) #Round down to 5 mins
        return scheduled_end



    @property
    def broadcast_start(self):
        if self.block_order == 0:
            return self.rundown.day_start
        return self.rundown.blocks[self.block_order-1].broadcast_end
        

    @property 
    def broadcast_end(self):
        if self.rendered and self.items:
            return self.broadcast_start + self.duration
        else:
            return self.scheduled_end


    def render(self):
        _newitems = [item for item in self.items if item["item_type"] != "placeholder"]
        self.items = _newitems
        self.structure()
        self.rendered = True

    def structure(self):
        """This is going to be reimplemented with actual block structure. Default is placeholder matching block duration"""
        self.add_default_placeholder()
            
    def add(self, item, **kwargs):
        assert type(item) == BlockItem
        self.items.append(item)
        self.items[-1].meta.update(kwargs)

    def add_placeholder(self, **kwargs):
        item = BlockItem(**kwargs)
        item["item_type"] = "placeholder"
        item["title"] = kwargs.get("title", "(DRAMATICA PLACEHOLDER)")
        self.items.append(item)

    def add_default_placeholder(self):
        start_time = self.broadcast_start
        end_time   = self.scheduled_end
        target_duration = self["target_duration"] or end_time - start_time
        self.add_placeholder(duration=target_duration)

    def add_jingle(self):
        if self["jingles"]:
            id_jingle = random.choice(self["jingles"]) # very sophisticated jingle selector
            jingle = self.asset(id_jingle)
            self.add(jingle)
            return True
        return False

    def add_promo(self):
        if self.rundown.promos:
            self.add_jingle()
            
            id_promo = random.choice(self.rundown.promos) # ok. this should be done better
            promo = self.asset(id_promo)
            self.add(promo.meta)
            
            self.add_jingle()
            return True
        return False








class Rundown(DramaticaObject):
    default = {
        "day"        : today(),
        "id_channel" : 1,
        "day_start"  : (6,00)
    }

    def __init__(self, **kwargs):
        super(Rundown, self).__init__(**kwargs)

        self.block_types = {}

        self.blocks = []
        self.promos = []
        self.asset_cache = {}

        self.db = CacheDB(":memory:")
        self.db.query("CREATE TABLE assets  (id_asset INTEGER, tag TEXT, value TEXT);")
        self.db.query("CREATE TABLE history (ts INTEGER PRIMARY KEY, id_asset INTEGER);")
        self.db.commit()


    def clock(self, hh, mm):
        """Converts hour and minute of current day to unix timestamp"""
        ttuple = list(self["day"]) + [hh, mm]
        dt = datetime.datetime(*ttuple)
        tstamp = time.mktime(dt.timetuple())  
        if tstamp < self.day_start:
            tstamp += 3600*24
        return tstamp

    @property
    def dow(self):
        return datetime.datetime(*self["day"]).weekday()

    @property
    def day_start(self):
        ttuple = list(self["day"]) + list(self["day_start"])
        dt = datetime.datetime(*ttuple)
        return time.mktime(dt.timetuple())  

    @property 
    def day_end(self):
        return self.day_start + (24*3600)


    def asset(self, id_asset):
        """Returns BlockItem object created from asset specified by provided id_asset"""
        if not id_asset in self.asset_cache:
            self.asset_cache[id_asset] = BlockItem(id_asset=id_asset, db=self.db)    
        return self.asset_cache[id_asset]

    def add(self, block_type_name, **kwargs):
        block_type = self.block_types.get(block_type_name, Block)
        self.blocks.append(block_type(self, **kwargs))
        self.blocks[-1]["block_type"] = block_type_name
        if self.blocks[-1]["instant_render"]:
            self.blocks[-1].render()
        elif self.blocks[-1]["full_auto"]:
            self.blocks[-1].add_default_placeholder()

    def render(self, force=False):
        self.at_time = self.day_start
        for block in self.blocks:
            if not block.rendered or force:
                block.render()
            self.at_time += block.duration