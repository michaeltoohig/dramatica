#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dramatica import *
from plugins.music_block import MusicBlockEvent


JINGLE_POSTX_INTRO   = 1293
JINGLE_POSTX_OUTRO   = 1299

JINGLE_POSTX1        = 1293
JINGLE_POSTX2        = 1299
JINGLE_POSTX3        = 1300
JINGLE_POSTX4        = 1292
JINGLE_POSTX5        = 1295

JINGLE_METAL_INTRO   = 1298
JINGLE_METAL         = 1294

VEDCI_ZJISTILI       = 1304




class RanniSrani(ProgrammeEvent):
    args = {
        "title" : "Ranní srani",
        "description" : ""
        }

class RozhlasPoDrate(ProgrammeEvent):
    args = {
        "title" : "Rozhlas po drate",
        "description" : "Hrajeme vam k praci"
        }


class Zpravy(ProgrammeEvent):
    args = {
        "title" : "Zprávy"
    }

class ShortFilm(ProgrammeEvent):
    pass



#############################
## Music video blocks

class PostX(MusicBlockEvent):
    args = {
        "title" : "PostX",
        "genre" : "Alt rock",
        "intro_jingle" : JINGLE_POSTX_INTRO,
        "outro_jingle" : JINGLE_POSTX_OUTRO,
        "jingles" : [JINGLE_POSTX1, JINGLE_POSTX2, JINGLE_POSTX3, JINGLE_POSTX4, JINGLE_POSTX5]
    }

class RockingPub(MusicBlockEvent):
    args = {
        "title" : "Rocking Pub",
        "genre" : "Rock",
        "intro_jingle" : VEDCI_ZJISTILI,
        "jingles" : [VEDCI_ZJISTILI]
    }    

class Nachtmetal(MusicBlockEvent):
    args = {
        "title" : "Nachtmetal",
        "genre" : "Metal",
        "intro_jingle" : JINGLE_METAL_INTRO,
        "jingles" : [JINGLE_METAL],
        "target_duration" : dur("02:00:00")
    }    

## Music video blocks
#############################









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
    sch = NXTVProgramme()
    sch.structure()
    sch.show()