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
from threading import Thread

pool = []
def squelcher():
    global pool
    
    while True:
        if len(pool):
            func, args = pool.pop()
            func(args)
        time.sleep(1)

def test(args):
    print args
def submain():
     t = Thread(target=squelcher)
     t.start()
     pool.append((test, ("hej", "pa")))
     pool.append((test, ("hesdfsdsdfsdfj", "pa")))
     
     
     
     