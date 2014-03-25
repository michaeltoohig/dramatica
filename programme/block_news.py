#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dramatica.scheduling import *


class Zpravy(ProgrammeEvent):
    args = {
        "title" : "Zprávy"
        }

class Crawler(ProgrammeEvent):
    args = {
        "title" : "Crawler",
        "description" : "Nevíte, kam dnes večer vyrazit? Máme pro vás několik tipů."
        }
