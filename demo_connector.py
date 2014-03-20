#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dramatica.common import DB

class NXConnector(object):
    def load_data(self):
        """
        This is site specific - Integration /w MAM system
        """
        rdb = DB("clipcache.db")
        rdb.query("SELECT id_asset, tag, value FROM nx_meta")
        for id_asset, tag, value in rdb.fetchall():
            self.db.query("INSERT INTO assets (id_asset, tag, value) VALUES ({}, '{}', '{}')".format(id_asset, tag, self.db.sanit(value)))


    def publish(self):
        """
        This is site specific - Integration /w MAM system
        """
