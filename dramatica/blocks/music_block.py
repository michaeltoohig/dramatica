#!/usr/bin/env python
# -*- coding: utf-8 -*-

__manifest__ = {
    "title"       : "Music Block",
    "description" : "Simple music selector",
    "author"      : "martas@imm.cz",
    "type"        : "plugin/dramatica",
    "export"      : "MusicBlock"
}

import random
import dramatica
from dramatica.timeutils import *

DEFAULT_MUSIC_BLOCK_DURATION = 3600
DEFAULT_PROMOTED_RATIO       = (1,2)
DEFAULT_ARTIST_SPAN          = 5
DEFAULT_JINGLE_SPAN          = 600
DEFAULT_PROMO_SPAN           = 1200
POOL_RESERVE                 = 1.2

class MusicBlock(dramatica.Block):
    def __init__(self, rundown, **kwargs):
        super(MusicBlock, self).__init__(rundown, **kwargs)
        self["full_auto"] = True

    def structure(self):
        start_time = self.broadcast_start
        end_time   = self.scheduled_end
        target_duration = self["target_duration"] or end_time - start_time

        print ("{} Target duration is {}".format(self["title"], target_duration))

        ######################################################################
        # Promoted / not promoted .... this should be done much much better

        promoted_ratio = self["promoted_ratio"] or DEFAULT_PROMOTED_RATIO
        jingle_span    = self["jingle_span"] or DEFAULT_JINGLE_SPAN
        promo_span     = self["promo_span"] or DEFAULT_PROMO_SPAN

        if type(self["genre"]) == str:
            genre_cond = "AND  assets.value='{}'".format(self["genre"])
        elif type(self["genre"]) == list:
            genres = ", ".join(["'{}'".format(genre) for genre in self["genre"]])
            genre_cond = "AND  assets.value IN ({})".format(genres)
        else:
            genre_cond = ""

        # SELECT PROMOTED SONGS - HITS
        self.db.query("""SELECT assets.id_asset FROM assets LEFT JOIN history 
                            ON    assets.id_asset = history.id_asset 
                            WHERE assets.tag='genre/music' 
                            {genre_cond}
                            AND   assets.id_asset IN (SELECT id_asset FROM assets WHERE tag='promoted' AND value='1')
                            ORDER BY history.ts ASC, RANDOM()
                            LIMIT 100
                            """.format(genre_cond=genre_cond))

        pool_promoted = [i[0] for i in self.db.fetchall()]

        # SELECT SONGS WHICH JUST WASN'T ON AIR FOR A WHILE... 
        self.db.query("""SELECT assets.id_asset FROM assets LEFT JOIN history 
                            ON    assets.id_asset = history.id_asset 
                            WHERE assets.tag='genre/music' 
                            {genre_cond}
                            AND   assets.id_asset NOT IN (SELECT id_asset FROM assets WHERE tag='promoted' AND value='1')
                            ORDER BY history.ts ASC, RANDOM()
                            LIMIT 100
                            """.format(genre_cond=genre_cond))

        pool_normal = [i[0] for i in self.db.fetchall()]

        song_pool = []
        pool_dur = 0
        while (pool_promoted or pool_normal) and pool_dur < target_duration * POOL_RESERVE:
          
            for i in range(promoted_ratio[0]):
                if pool_promoted:
                    id_asset = pool_promoted.pop(0)
                    asset = self.asset(id_asset)
                    song_pool.append(asset)
                    pool_dur += asset.duration
                else:
                    break

            for i in range(promoted_ratio[1]):
                if pool_normal:
                    id_asset = pool_normal.pop(0)
                    asset = self.asset(id_asset)
                    song_pool.append(asset)
                    pool_dur += asset.duration
                else:
                    break

        print ("SONG POOL", self["title"], len(song_pool))

        # Promoted / not promoted, - song pool generation
        ######################################################################

        if self["intro_jingle"]:
            self.add(self.asset(self["intro_jingle"]))

        last_jingle = 0
        last_promo  = 0
        current_duration = 0


        while song_pool:
            
            # BPM/MOOD SELECTOR GOES HERE
            asset_index = random.randrange(0, len(song_pool))
            asset = song_pool.pop(asset_index)


            self.add(asset)
            current_duration += asset.duration
            remaining = target_duration - current_duration
            pool_dur -= asset.duration
            avg_dur   = pool_dur / len(song_pool)

            if remaining < 0:
                break

            if remaining < avg_dur * 1.5:

                print("{}s remaining. Which is less than {}s maximum".format(remaining, avg_dur))
                asset = sorted(song_pool, key=lambda song: abs(song.duration - remaining ))[0]
                self.add(asset)
                break

            if remaining > promo_span and current_duration - last_promo > promo_span:
                if self.add_promo():
                    last_promo = current_duration
                    last_jingle = current_duration
                    current_duration += self.items[-1].duration

            if remaining > jingle_span and current_duration - last_jingle > jingle_span:
                if self.add_jingle():
                    last_jingle = current_duration
                    current_duration += self.items[-1].duration


        if self["outro_jingle"]:
            self.add(self.asset(self["intro_jingle"]))



