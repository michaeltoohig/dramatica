#!/usr/bin/env python
#from __future__ import print_statement

import os
#import imp
import importlib
from importlib.machinery import SourceFileLoader
import time
import random

from dramatica.common import DramaticaCache, DramaticaAsset
from dramatica.scheduling import DramaticaRundown
from dramatica.templates import DramaticaTemplate
from dramatica.timeutils import *

DAY_START = [6,0] # Broadcast starts at 6:00
ID_CHANNEL = 1
PLUGINS_DIR = "plugins"

NX_TAGS = [
    (str, "title"),
    (str, "description"),
    (str, "genre"),
    (str, "rights"),
    (str, "source"),
    (str, "role/performer"),
    (str, "role/director"),
    (str, "album"),
    (str, "path"),
    (int, "qc/state"),
    (int, "id_folder"),
    (float, "duration"),
    (float, "mark_in"),
    (float, "mark_out"),
    (float, "audio/bpm")
    ]


def get_template(tpl_name):
    fname = os.path.join(PLUGINS_DIR, "templates", "{}.py".format(tpl_name))
    if not os.path.exists(fname):
        print("Template does not exist")
        return False
    #py_mod = imp.load_source(tpl_name, fname)
    py_mod = SourceFileLoader(tpl_name, fname).load_module()
    return py_mod.Template


def demo_assets():
    assets = []
    # build assets
    for i in list(range(200)):
        if i % 10 == 0:
            path="data/postx_short/{}.webm".format(random.randint(1,4))
            #path=f"data/postx_short/{random.randint(1, 4)}.webm",
        else:
            path="data/{}.webm".format(random.randint(1,14))
            #path=f"data/{random.randint(1, 4)}.webm",
        #a = DramaticaAsset(
        a = dict(
            title=i,
            description="description",
            #description=f"{i} description.",
            genre=random.choice([
                "horror",
                "political",
                "social",
                "conspiracy",
                "arts",
                "technology",
                "rock",
                "rock",
                "drama",
                "comedy",
            ]),
            source="source",
            path=path,
            duration=random.randint(300, 1800),
            mark_in=random.randint(0, 120),
            id_folder=random.randint(2, 8),
            id_object=i,
        )
        a['audio/bpm'] = random.randint(80, 140)
        assets.append(a)

    # movies
    for i in list(range(10)):
        a = dict(
            title=i,
            description="description",
            genre="movie",
            source="source",
            path="data/movies/{}.webm".format(i),
            duration=random.randint(3600, 7200),
            id_folder=1,
            id_object=i + 200,
        ) 
        assets.append(a)

    # fillers
    for i in list(range(100)):
        a = dict(
            title="Filler {}".format(i),
            description="description",
            genre="filler",
            source="source",
            path="data/filler/{}.webm".format(i),
            duration=random.randint(30, 500),
            id_folder=20,
            id_object=i + 210,
        ) 
        assets.append(a)
    return assets

    #a1 = DramaticaAsset(title="1", description="1 video", genre="Music", source="online", path="data/1.webm", duration=10, mark_in=2, mark_out=8, id_object=1)
    #a2 = DramaticaAsset(title="2", description="2 video", genre="Music", source="online", path="data/2.webm", duration=10, mark_in=2, mark_out=8, id_object=2)
    #a3 = DramaticaAsset(title="3", description="3 video", genre="Music", source="online", path="data/3.webm", duration=10, mark_in=2, mark_out=8, id_object=3)
    #a4 = DramaticaAsset(title="4", description="4 video", genre="Music", source="online", path="data/4.webm", duration=10, mark_in=2, mark_out=8, id_object=4)
    #return [a1,a2,a3,a4]


def make_my_day(day=[2014, 1, 4]):

    cache = DramaticaCache(NX_TAGS)
    cache.load_assets(demo_assets())

    #import pdb; pdb.set_trace()
    
    rundown = DramaticaRundown(
                cache,
                day=day,
                day_start=DAY_START,
                id_channel=ID_CHANNEL
            )

    Template = get_template("demo_tv")
    if Template:
        template = Template(rundown)
    else:
        return


    template.apply()
    rundown.solve()
    return rundown
    


if __name__ == "__main__":
    rundown = make_my_day()
    import pdb; pdb.set_trace()
    print (rundown)