#!/usr/bin/env python
# -*- coding: utf-8 -*-

__manifest__ = {
    "title"       : "Music Block",
    "description" : "Simple music selector",
    "author"      : "martas@imm.cz",
    "type"        : "plugin/dramatica",
    "export"      : "MusicBlockEvent"
}

import random
import dramatica
from dramatica.timeutils import *


DEFAULT_MUSIC_BLOCK_DURATION = 3600
DEFAULT_PROMOTED_RATIO       = (1,2)
DEFAULT_ARTIST_SPAN          = 5
DEFAULT_JINGLE_SPAN          = 600
DEFAULT_PROMO_SPAN           = 1200


class MusicBlock(dramatica.Block):
    def structure(self):
        start_time = max(self.get_event_start(), self.get_broadcast_start())
        end_time   = self.get_event_end()
        target_duration = self["target_duration"] or end_time - start_time
        logging.debug("{}: Music block event /w dur {:0n}s".format(self["title"], target_duration))

        ######################################################################
        # Promoted / not promoted .... this should be done much much better

        # how many promoted songs are used. Default is 1 promoted to 2 not
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
                            AND   assets.id_asset IN (SELECT id_asset FROM assets WHERE tag='qc/state' AND value='2') -- FIXME: This should be handled in programme.load_data
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
                            AND   assets.id_asset IN (SELECT id_asset FROM assets WHERE tag='qc/state' AND value='2') -- FIXME: This should be handled in programme.load_data
                            AND   assets.id_asset NOT IN (SELECT id_asset FROM assets WHERE tag='promoted' AND value='1')
                            ORDER BY history.ts ASC, RANDOM()
                            LIMIT 100
                            """.format(genre_cond=genre_cond))

        pool_normal = [i[0] for i in self.db.fetchall()]

        song_pool =[]
        pool_dur = 0
        while (pool_promoted or pool_normal) and pool_dur < target_duration : #FIXME:.... chce to nejakou rezervu....
          
            for i in range(promoted_ratio[0]):
                if pool_promoted:
                    id_asset = pool_promoted.pop(0)
                    asset = self.asset(id_asset)
                    pool_dur += asset.get_duration()
                    song_pool.append(asset)
                else:
                    break

            for i in range(promoted_ratio[1]):
                if pool_normal:
                    id_asset = pool_normal.pop(0)
                    asset = self.asset(id_asset)
                    pool_dur += asset.get_duration()
                    song_pool.append(asset)
                else:
                    break

        # Promoted / not promoted, - song pool generation
        ######################################################################

        if self["intro_jingle"]:
            self.add(id_asset=self["intro_jingle"], title="{} - Intro Jingle".format(self["title"]))

        last_jingle = 0
        last_promo  = 0


        while self.get_duration() < target_duration:
            i = random.randrange(0,len(song_pool))
            a = song_pool.pop(i)
            self.add(**a.meta)

            remaining = target_duration - self.get_duration()

            if remaining > promo_span and self.get_duration() - last_promo > promo_span:
                self.add_promo()
                last_promo = self.get_duration()
            elif remaining > jingle_span and self.get_duration() - last_jingle > jingle_span:
                self.add_jingle()
                last_jingle = self.get_duration()


        if self["outro_jingle"]:
            self.add(id_asset=self["outro_jingle"], title="{} - Outro Jingle".format(self["title"]))



