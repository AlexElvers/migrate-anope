#!/usr/bin/env python3

"""
Migrate users from Anope 1.6 to Anope 2.0 (SQLite).
Author: Alexander Elvers
"""

import struct
from pprint import pprint


FILE = "nick.db"


class Unpack:
    def __init__(self, buf):
        self.buf = buf
        self.offset = 0

    def unpack(self, format):
        res = struct.unpack_from(format, self.buf, self.offset)
        self.offset += struct.calcsize(format)
        return res

    def unpack_string(self):
        size = self.unpack(">h")
        s = self.unpack("%ds" % size)[0][:-1]
        return s


# based on nickserv.c/load_ns_dbase
with open(FILE, "rb") as f:
    p = Unpack(f.read())
    (version,) = p.unpack(">i")
    print("Version:", version)

    users = []
    for i in range(1024):
        if p.unpack("b")[0] == 1:
            nc = {}
            nc["display"] = p.unpack_string()
            nc["pass"] = p.unpack_string()
            nc["email"] = p.unpack_string()
            nc["greet"] = p.unpack_string()
            nc["icq"] = p.unpack(">i")[0]
            nc["url"] = p.unpack_string()
            nc["flags"] = p.unpack(">i")[0]
            nc["language"] = p.unpack(">h")[0]
            nc["accesscount"] = p.unpack(">h")[0]
            nc["access"] = []
            for access in range(nc["accesscount"]):
                nc["access"].append(p.unpack_string())
            nc["memos.memocount"] = p.unpack(">h")[0]
            nc["memos.memomax"] = p.unpack(">h")[0]
            nc["memos.memos"] = []
            for memo_i in range(nc["memos.memocount"]):
                memo = {}
                memo["number"] = p.unpack(">i")[0]
                memo["flags"] = p.unpack(">h")[0]
                memo["time"] = p.unpack(">i")[0]
                memo["sender"] = p.unpack_string()
                memo["text"] = p.unpack_string()
            nc["channelcount"] = p.unpack(">h")[0]
            p.unpack(">h")[0]
            if version < 13:
                p.unpack(">h")[0]
                p.unpack(">i")[0]
                p.unpack(">h")[0]
                p.unpack_string()
            users.append(nc)
    pprint(users)
