#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import imp

from dramatica.scheduling import *


class Dramatica():
    def __init__(self, plugin_path): 
        if not os.path.exists(plugin_path):
            logging.error("Dramatica plugin dir does not exist")
            return

        self.rundown = False
        block_types = {}

        for fname in os.listdir(plugin_path):
            mod_name, file_ext = os.path.splitext(fname)
            
            if file_ext != ".py":
                continue

            if mod_name.startswith("rundown_"):
                py_mod = imp.load_source(mod_name, os.path.join(plugin_path, fname))
                #TODO: VALIDATION
                self.rundown = py_mod.Rundown()

            elif mod_name.startswith("block_"):
                py_mod = imp.load_source(mod_name, os.path.join(plugin_path, fname))

                if not "__manifest__" in dir(py_mod):
                    logging.warning("No plugin manifest found in {}".format(fname))
                    continue

                for block_name in py_mod.__manifest__["export"].keys():
                    logging.info("Initializing block plugin {} from module `{}`".format(block_name, py_mod.__manifest__["title"] ))
                    block_types[block_name] = py_mod.__manifest__["export"][block_name]

        if self.rundown:
            self.rundown.block_types = block_types
            #TODO: Add default block types

        else:
            pass

            # TODO: Handle non-existent rundown

    def ftime(self, tstamp):
        return time.strftime("%H:%M:%S", time.localtime(tstamp))

    def show(self):
        print ("\n\nRUNDOWN FOR {}-{}-{}".format(*self.rundown["day"]))
        print ("-"*80, "\n")
        at_time = self.rundown.clock(*self.rundown["day_start"])
        for i, block in enumerate(self.rundown.blocks):
            print ("{}  {} ".format(self.ftime(block.scheduled_start), self.ftime(at_time)),  block["title"])
            print ("="*80)
            for j, item in enumerate(block.items):
                print ("          {} ".format(self.ftime(at_time)),  item["title"])
                at_time += item.duration
            print("\n")
