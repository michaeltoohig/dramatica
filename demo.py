#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
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
        start_time = datestr2ts(date)
        end_time   = start_time + (3600*24)

        day = [int(i) for i in date.split("-")]
        self.rundown["day"] = day
        self.rundown["id_channel"] = id_channel
        self.rundown.structure()


    def on_cleanup(self, date, id_channel):
        for block in self.rundown.blocks:
            if not block.rendered:
                block.render()




if __name__ == "__main__":
    drama = MyLittleSqlitePoweredFakeMAMSystem(PLUGIN_PATH)
    
    drama.load_data()
    
    drama.on_structure(time.strftime("%Y-%m-%d"), 1)
    drama.on_cleanup(time.strftime("%Y-%m-%d"), 1)
    
    drama.show()