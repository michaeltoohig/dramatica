#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import dramatica

from dramatica.common import CacheDB

PLUGIN_PATH = "plugins"


def datestr2ts(datestr, hh=0, mm=0, ss=0):
    """Converts YYYY-MM-DD string to timestamp"""
    yy,mo,dd = [int(i) for i in datestr.split("-")]
    return int(time.mktime(time.struct_time([yy,mo,dd,hh,mm,ss,False,False,False])))


class MyLittleSqlitePoweredFakeMAMSystem(dramatica.Dramatica):

    def load_data(self):
        src_db = CacheDB("clipcache.db")
        src_db.query("SELECT id_asset, tag, value FROM nx_meta")
        for id_asset, tag, value in src_db.fetchall():
            self.rundown.db.query("INSERT INTO assets (id_asset, tag, value) VALUES ({}, '{}', '{}')".format(id_asset, tag, self.rundown.db.sanit(value)))

    def on_structure(self, date, id_channel):
        self.load_data()

        start_time = datestr2ts(date)
        end_time   = start_time + (3600*24)

        day = [int(i) for i in date.split("-")]
        self.rundown["day"] = day
        self.rundown["id_channel"] = id_channel
        self.rundown.structure()

        print ("\n\nRUNDOWN FOR {}".format(date))
        print ("======================\n")
        for i, block in enumerate(self.rundown.blocks):
            scheduled_start = time.strftime("%H:%M", time.localtime(block.scheduled_start))
            scheduled_end   = time.strftime("%H:%M", time.localtime(block.scheduled_end))
            print (scheduled_start, scheduled_end,  block["title"])
            print ()

        
    def on_cleanup(self, date, id_channel):
        self.load_data(date, id_channel)




if __name__ == "__main__":
    drama = MyLittleSqlitePoweredFakeMAMSystem(PLUGIN_PATH)
    drama.on_structure(time.strftime("%Y-%m-%d"), 1)