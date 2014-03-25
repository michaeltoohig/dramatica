#!/usr/bin/env python
# -*- coding: utf-8 -*-

__manifest__ = {
    "title"       : "nxtv",
    "description" : "Programme schema of nxtv.cz project",
    "author"      : "martas@imm.cz",
    "type"        : "dramatica/schedule",
    "export"      : "Programme"
}


from dramatica import *

from .block_movies import *
from .block_music import *
from .block_news import *


class Programme(Programme):
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
        self.add(Zpravy, start=(18,45))


        # Tomorow promos only
        self.set_promo(promo[(self.dow+1) % 7])

        if self.dow in [FRI, SAT]:
            self.add(RockingPub, start=(19,00))
            self.add(Nachtmetal, start=(23,59))
        else:

            self.add(Rocking)

            if self.dow == SUN:
                self.add(ProgrammeEvent, start=(20,00), title="Movie of the week")
                self.add(Zpravy)
                self.add(ShortFilm)
                self.add(Nachtmetal) 

            elif self.dow == MON:
                self.add(Movie, start=(20,00), genre="Drama/Horror")
                self.add(Zpravy)
                self.add(ShortFilm, genre="Drama/Horror")
                self.add(Nachtmetal) 

            elif self.dow == TUE:
                self.add(Movie, start=(20,00), genre=["Political", "Social"])
                self.add(Zpravy)
                self.add(ShortFilm, genre=["Political", "Social"])
                self.add(Nachtmetal) 

            elif self.dow == WED:
                self.add(ProgrammeEvent, start=(20,00), title="Arts")
                self.add(Zpravy)
                self.add(ShortFilm)
                self.add(Nachtmetal) 

            elif self.dow == THU:
                self.add(ProgrammeEvent, start=(20,00), title="Technology")
                self.add(Zpravy)
                self.add(ShortFilm)
                self.add(Nachtmetal) 