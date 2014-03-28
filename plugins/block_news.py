#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dramatica


class Zpravy(dramatica.Block):
    default = {
        "title" : "Zpravy"
        }

class Crawler(dramatica.Block):
    default = {
        "title" : "Crawler",
        "description" : "Nevíte, kam dnes večer vyrazit? Máme pro vás několik tipů."
        }



__manifest__ = {
    "title"       : "nxtv news blocks",
    "author"      : "martas@imm.cz",
    "type"        : "dramatica/block",
    "export"      : {
                    "Zpravy" : Zpravy,
                    "Crawler" : Crawler
                    }
}
