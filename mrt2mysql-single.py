#!/usr/bin/env python

import os
import sys
import time
import json
import pymysql
import IPy
from datetime import datetime
import re

# When the parent dies we are seeing continual newlines, so we only access so many before stopping
counter = 0

conn = pymysql.connect(
    host='localhost',
    user='user',
    passwd='password',
    db='db',
)
cur = conn.cursor()

def getSourceASfromASPath(aspathstring):
    if '{' not in aspathstring:
        aspathlist = aspathstring.split(' ')
        sourceasn = aspathlist[-1]
    else:
        aspathstring = re.sub(' \{.*\}$', '', aspathstring)
        aspathlist = aspathstring.split(' ')
        sourceasn = aspathlist[-1]
    return int(sourceasn)

def lineToMysql(oneline):
    # TYPE|SUBNETS|AS_PATH|NEXT_HOP|ORIGIN|ATOMIC_AGGREGATE|AGGREGATOR|COMMUNITIES|SOURCE|TIMESTAMP|ASN 32 BIT
    (adv_type,subnets,aspath,next_hop,origin,atomic_aggregate,aggregator,communities,source,timestamp,asn32bit) = oneline.split('|')
    sourceasn = getSourceASfromASPath(aspath)
    ts = int(timestamp)
    eventtime = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    prefixes = subnets.split(' ')

    for prefix in prefixes:
        sqlinsert = """
INSERT INTO mrt2mysql VALUES (NULL, '%s', '%s', '%s', %d)
        """ % (eventtime, prefix, aspath, sourceasn)
        #print sqlinsert
        conn.ping(reconnect=True)
        cur.execute(sqlinsert)
        #conn.ping(reconnect=True)
        conn.commit()


while True:
    try:
        line = sys.stdin.readline().strip()
        if line == "":
            counter += 1
            if counter > 100:
                break
            continue

        counter = 0

        lineToMysql(line)
        #conn.commit()
    except KeyboardInterrupt:
        pass
    except IOError:
        # most likely a signal during readline
        pass

