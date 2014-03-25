#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dramatica.scheduling import *

class Movie(ProgrammeEvent):
    args = {
        "title" : "Movie"
        }

class ShortFilm(ProgrammeEvent):
    args = {
        "title" : "ShortFilm"
        }
