#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dramatica


class Movie(dramatica.Block):
    default = {
        "title" : "Movie"
        }

class ShortFilm(dramatica.Block):
    default = {
        "title" : "ShortFilm"
        }




__manifest__ = {
    "title"       : "nxtv movie blocks",
    "author"      : "martas@imm.cz",
    "type"        : "dramatica/block",
    "export"      : {
                    "Movie" : Movie,
                    "ShortFilm" : ShortFilm
                    }
}
