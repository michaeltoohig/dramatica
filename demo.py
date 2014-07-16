#!/usr/bin/env python
from __future__ import print_statement

import imp
import time

from dramatica.common import DramaticaCache
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
    py_mod = imp.load_source(tpl_name, fname)
    return py_mod.Template


def demo_assets():
    pass # TODO


def make_my_day(day=[2014, 1, 4]):

    cache = DramaticaCache(NX_TAGS)
    cache.load_assets(demo_assets())

    rundown = DramaticaRundown(
                self.cache,
                day=day,
                day_start=DAY_START
                id_channel=ID_CHANNEL
            )

    Template = get_template("demo_template")
    if Template:
        template = Template(rundown)
    else:
        return

    template.apply()
    rundown.solve()
    return rundown
    


if __name__ == "__main__":
    rundown make_my_day()
    print (rundown)