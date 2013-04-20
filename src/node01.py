# -*- coding: utf-8 -*-
"""
When logged in to the game system, your browser will have two new cookies set, �devnull_session� and �devnull_apikey�.
The first one is recreated for each login, but the second one will be the same between sessions.
Either one can be used as �session� variable when making a call to the API.

Each team can create a party of up to three player characters, who can explore the dungeons.
To see which characters are in the party (currently none), use the following API call;

/api3/?session=<sessionkey>&command=getparty

To make sure that the server isn�t overloaded during gameplay, create a request dispatcher that squelches requests per second to the
server. 

Demonstrate both that information can be fetched (using the getparty call) and that the squelch works when you try to send more than
10 requests per seconds to the server.
"""

import time
import httplib
from threading import Thread
import json

pool = []
def squelcher():
    global pool
    
    while True:
        if len(pool):
            func, args = pool.pop()
            func(args)
        time.sleep(0.1)

def call_api(args):
    command, callback = args
    host = "genericwitticism.com"
    port = 8000
    base_path =  "/api3/?session=c577eb41-c931-4526-9c52-e9b361eba8c3&command=%s" % command
    print base_path
    connection = httplib.HTTPSConnection(host, port)
    connection.request("GET", base_path)
    results = connection.getresponse().read()
    
    callback(results)
    
def get_party(callback):
    pool.append((call_api, ("getparty",callback)))

def hej(args):
    print args
    
    parsed = json.loads(args)
    print parsed
    
    print "Characters in party: "
    for c in parsed["characters"]:
        print c
     
def submain():
     t = Thread(target=squelcher)
     t.start()
     get_party(hej)
     
     
     
     
     
     
     
     