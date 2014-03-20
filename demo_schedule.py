#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dramatica import *

from demo_blocks import *
from demo_connector import NXConnector

class NXTVProgramme(Programme):
    def structure(self):
        promo = {
            MON : [],
            TUE : [],
            WED : [],
            THU : [],
            FRI : [],
            SAT : [],
            SUN : []
            }


        # Weighted promos - For today and tomorow (2:1 ratio)
        self.set_promo( promo[self.dow] * 2 + promo[(self.dow+1) % 7] )
        
        self.add(RanniSrani)

        if self.dow >= MON and self.dow < SAT:
            self.add(RozhlasPoDrate, start=(10,00))
        else:
            self.add(ProgrammeEvent, title="Vikendove sracky")


        self.add(Crawler, start=(16,55))
        self.add(PostX,  start=(17,00))
        self.add(Zpravy, start=(18,50))

        ### PRIME TIME

        # Tomorow promos only
        self.set_promo(promo[(self.dow+1) % 7])

        if self.dow in [FRI, SAT]:
            self.add(RockingPub, start=(19,00))
            self.add(Nachtmetal, start=(23,59))

        elif self.dow == SUN:
            self.add(ProgrammeEvent, title="Movie of the week")
            self.add(Zpravy)
            self.add(ShortFilm)
            self.add(Nachtmetal) 

        elif self.dow == MON:
            pass

        elif self.dow == TUE:
            pass

        elif self.dow == WED:
            pass

        elif self.dow == THU:
            pass



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



if __name__ == "__main__":
    sch = NXTVProgramme(day=(2013,12,21), id_channel=1)
    sch.structure()
    sch.show()