# -*- coding: utf-8 -*-

'''
Created on 20 apr 2013

@author: jdw
'''

import node01
import node02
import settings
from threading import Thread
import time

global running
def start_gui():
    global running
    running = True
    eval(settings.GUI).start()
    
    while running:
        time.sleep(0.1)    
        
    eval(settings.GUI).stop()
    
if __name__ == '__main__':
    t = Thread(target=start_gui)
    t.start()
    
    eval(settings.NODE).submain()
    
    global running
    running = False
    
    
    