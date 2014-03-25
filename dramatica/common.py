#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import sqlite3

if sys.platform == "win32":
    PLATFORM = "windows"
else:
    PLATFORM = "linux"


class CacheDB(object):
    def __init__(self, host):
        self._connect(host)

    def _connect(self, host):    
        self.conn = sqlite3.connect(host)
        self.cur = self.conn.cursor()
    
    def query(self, q, *args):
        self.cur.execute(q,*args)

    def fetchall(self):
        return self.cur.fetchall()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.close()

    def sanit(self, instr):
        try:
            return str(instr).replace("''","'").replace("'","''").decode("utf-8")
        except:
            return instr.replace("''","'").replace("'","''")
    
    def lastid(self):
        r = self.cur.lastrowid
        return r




DEBUG, INFO, WARNING, ERROR, GOOD_NEWS = range(0,5)

class Logging():
    def __init__(self):
        self.formats = {
            DEBUG     : "DEBUG \033[34m {0}\033[0m",
            INFO      : "INFO {0}",
            WARNING   : "\033[33mWARNING\033[0m {0}",
            ERROR     : "\033[31mERROR\033[0m {0}",
            GOOD_NEWS : "\033[32mGOOD NEWS\033[0m {0}"
        }

    def _msgtype(self, code):
        return {
            DEBUG : "DEBUG",
            INFO : "INFO",
            WARNING : "WARNING",
            ERROR : "ERROR",
            GOOD_NEWS : "GOOD NEWS"
        }[code]

    def _typeformat(self, code):
        return self._msgtype(code)

    def _send(self,msgtype,message):
        if PLATFORM == "linux":
            print (self.formats[msgtype].format(message))
        else:
            print ("{0:<10} {1}".format(self._typeformat(msgtype), message))
             
    def debug (self,msg): self._send(DEBUG,msg)
    def info (self,msg): self._send(INFO,msg)
    def warning (self,msg): self._send(WARNING,msg)
    def error (self,msg): self._send(ERROR,msg)
    def goodnews(self,msg): self._send(GOOD_NEWS,msg)

logging = Logging() 