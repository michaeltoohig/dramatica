#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dramatica.scheduling import *
from dramatica.blocks.music_block import MusicBlockEvent


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

class Rocking(MusicBlockEvent):
    args = {
        "title" : "Rocking",
        "genre" : ["Rock", "Pop", "Alt rock"],
        "intro_jingle" : VEDCI_ZJISTILI,
        "jingles" : [VEDCI_ZJISTILI]
        }    
