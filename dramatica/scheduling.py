#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from dramatica.common import DB, logging
from dramatica.timeutils import *


class EventItem():
    def __init__(self, **kwargs):
        self.meta = {
            "title"    : "-- PLACEHOLDER --",
            "duration" : "0"
            }

        if "id_asset" in kwargs and "db" in kwargs:
            db = kwargs["db"]
            db.query("SELECT tag, value FROM assets WHERE id_asset = {}".format(kwargs["id_asset"]))
            for tag, value in db.fetchall():
                self.meta[tag] = value
        else:
            self.meta.update(kwargs)

    def __getitem__(self, key):
        return self.meta.get(key, False)

    def __setitem__(self, key, value):
        self.meta[key] = value


    def get_duration(self):
        return float(self["duration"])




class ProgrammeEvent():
    args = {}
    """
    BASE ARGS:

    title:       Event title
    description: Event description
    start:       Create event at fixed start time (optional). If not specified, end time of previous event is used.

    OPTIONAL:
    jingles:     array of asset id's for jingle selector
    """
    def __init__(self, programme, **kwargs):
        self.args.update(kwargs)
        self.programme = programme
        self.db = self.programme.db
        self.asset = self.programme.asset
        self.event_order = len(self.programme.events)
        self.items = []
        self.rendered = False

    def __getitem__(self, key):
        return self.args.get(key, False)

    def add(self, **kwargs):
        item = EventItem(**kwargs)
        self.items.append(item)

    def get_duration(self):
        dur = 0
        for item in self.items:
            dur += item.get_duration()
        return dur

    def get_event_start(self):
        if self["start"]:
            return self.programme.clock(*self["start"])
        return self.get_broadcast_start()

    def get_broadcast_start(self):
        if self.event_order == 0:
            return self.programme.day_start
        try:
            return self.programme.events[self.event_order-1].get_event_end()
        except IndexError:
            return self.programme.day_start


    def get_event_end(self):
        try:
            next_fixed_start = self.programme.events[self.event_order+1]["start"]
        except:
            next_fixed_start = (23,59)
        if next_fixed_start:
            return self.programme.clock(*next_fixed_start)
        return self.get_event_start() + self.get_duration()

    def render(self):
        self.structure()
        self.rendered = True

    def structure(self):
        """ This is going to be reimplemented with actual event structure. Default is placeholder matching event duration"""
        start_time = max(self.get_event_start(), self.get_broadcast_start())
        end_time   = self.get_event_end()
        target_duration = self["target_duration"] or end_time - start_time
        self.add(duration=target_duration)


            
    def add_jingle(self):
        if self["jingles"]:
            id_jingle = random.choice(self["jingles"]) # very sophisticated jingle selector
            jingle = self.asset(id_jingle)
            self.add(**jingle.meta)


    def add_promo(self):
        if self.programme.promos:
            self.add_jingle()
            
            id_promo = random.choice(self.programme.promos) # ok. this should be done better
            promo = self.asset(id_promo)
            self.add(**promo.meta)
            
            self.add_jingle()





class Programme():
    args = {}
    def __init__(self, **kwargs):
        self.args.update(kwargs)
        self.dy, self.dm, self.dd  = self.args.get("day", today())
        self.id_channel            = self.args.get("id_channel", 1)
        self.day_start = self.clock(*self.args.get("day_start", (6,00)))
        
        self.dt  = datetime.datetime(self.dy, self.dm, self.dd)
        self.dow = self.dt.weekday()

        self.events = []
        self.promos = []

        self.asset_cache = {}

        self.db = DB(":memory:")
        self.db.query("CREATE TABLE assets (id_asset INTEGER, tag TEXT, value TEXT);")
        self.db.query("CREATE TABLE history (ts INTEGER PRIMARY KEY, id_asset INTEGER);")
        self.db.commit()
        
        logging.debug("Loading data...")
        self.load_data()
        logging.debug("Done")
        

    def asset(self, id_asset):
        if not id_asset in self.asset_cache:
            self.asset_cache[id_asset] = EventItem(id_asset=id_asset, db=self.db)    
        return self.asset_cache[id_asset]

    def clock(self, hh, mm):
        dt = datetime.datetime(self.dy, self.dm, self.dd, hh, mm)
        return time.mktime(dt.timetuple())        

    def add(self, event, **kwargs):
        self.events.append(event(self, **kwargs))

    def set_promo(self, clips=[]):
        self.promos = clips

    def render(self, force=False):
        self.at_time = self.day_start
        for event in self.events:
            if not event.rendered or force:
                event.structure()
            self.at_time += event.get_duration()

    def show(self):
        self.render()
        at_time = self.day_start

        print ("\n******************************************************************")

        for i, event in enumerate(self.events):
            broadcast_start = time.strftime("%H:%M", time.localtime(at_time))
            scheduled_start = time.strftime("%H:%M", time.localtime(event.get_event_start()))
            print ("\n")
            print (scheduled_start, broadcast_start, event["title"])
            print ("------------------------------------------------------------------")
            for item in event.items:
                r = time.strftime("%H:%M", time.localtime(at_time))
                title = item["title"]
                try:
                    print ("      {} {!s}".format(r, title))
                except:
                    print ("      {} {!s}".format(r, item["id_asset"]))
                at_time += item.get_duration()

        print ("\n******************************************************************\n")




    def load_data(self):
        """Use this to load asset pool and schedule history (asset scheduled before current day)"""

    def structure(self):
        pass




