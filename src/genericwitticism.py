# -*- coding: utf-8 -*-

import time
import httplib, urllib
from threading import Thread
import json

from character import Character
from party import Party

def _squelcher():
    Genericwitticism.pool = []
    pool = Genericwitticism.pool
    
    while True:
        if len(pool):
            func, args = pool.pop()
            func(args)
        
        if Genericwitticism._plz_stop:
            return
        
        time.sleep(0.1)

class Genericwitticism(object):
    pool = []
    t = Thread(target=_squelcher)
    _plz_stop = False
    
    def __init__(self, key,host=None, port=None):
        self.host = host if host else "genericwitticism.com"
        self.port = port if port else 8000
        self.key = key
        self.base_path =  "/api3/?"
        self._party = None
        self._character_template = None
    
    def start(self):
        if not Genericwitticism.t.is_alive():
            Genericwitticism._plz_stop = False
            Genericwitticism.t.start()
        
    def stop(self):
        if Genericwitticism.t.is_alive():
            Genericwitticism._plz_stop = True
            
    def _call_api(self, args):
        if not Genericwitticism.t.is_alive():
            raise "Not started!"
            
        command, api_args, callback = args
        
        if api_args:
            path = "%ssession=%s&command=%s&arg=%s" % (self.base_path, self.key, command, api_args)
        else:
            path = "%ssession=%s&command=%s" % (self.base_path, self.key, command)
            
        connection = httplib.HTTPSConnection(self.host, self.port) 
        connection.request("GET", path.encode('latin-1'))
        
        response = connection.getresponse()
        results_json = response.read()
        results = json.loads(results_json)
        
        if "error" in results:
            problem = results["error"]
            if "Could not find valid session from provided api key or session key" in problem:
                raise Exception("No valid session for API key %s" % self.key)

            if "Unable to parse character object" in problem:
                raise Exception("Not able to parse object")
             
            return
        
        connection.close()
        callback(results)
            
    def _pool_append(self, name, args, callback):
        Genericwitticism.pool.append((self._call_api, (name, args, callback)))
        
    def get_party(self, callback=None, force=False, async=True):
        if not force and self._party:
            return self._party
        
        self._party = None
        urp = {"calldone": False}
        
        def _callback(args):
            print "party args", args
            self._party = Party()
            
            for char_id in args["characters"]:
                self.get_character(char_id, force=True, async=False)
            
            urp["calldone"] = True
            if callback:
                callback(args)
        
        self._pool_append("getparty", None, _callback)
        
        if async:
            return None
        
        while not urp["calldone"]:
            time.sleep(0.1)
        
        return self._party
        
        
    def get_character_template(self, callback=None, force=False):
        if not force and self._character_template:
            return self._character_template
        
        self._character_template = None
        
        def _callback(args):
            self._character_template = args
            if callback:
                callback(args)
        
        self._pool_append("getchartemplate", None, _callback)
        
        return None
    
    def create_character(self, name, str=10, dex=10, con=10, int=10, wis=10, callback=None, force=False, async=True):
        t_char = Character()
        t_char.name = name
        t_char.setStrength(15)
        t_char.setConstitution(con)
        t_char.setDexterity(15)
        t_char.setIntelligence(int)
        t_char.setWisdom(wis)
    
        urp = {"calldone": False}
        def _callback(args):
            urp["calldone"] = True
            urp["character"] = args
            print "callback: ", args
            self._party.add_character(Character(args=args))
            
            if callback:
                callback(args)
                
        
        j = '{"name":"'+name+'","str":"15","dex":"15","con":"10","int":"10","wis":"10"}'
        
        self._pool_append("createcharacter", j, _callback)
        
        if async: return None
        
        while not urp["calldone"]: time.sleep(0.1)
        
        return urp["character"]
    
    
    def get_character(self, id, callback=None, force=False, async=True):
        """
            api3/?session=<sessionkey>&command=getcharacter&arg=ri4llrZXK
        """
        if not force and self._party.get_character_by_id(id):
            return self._party.get_character_by_id(id)
        
        self._party.remove_character_by_id(id)
        
        urp = {"calldone": False}
        def _callback(args):
            if not self._party:
                self._party = Party()
            self._party.add_character(Character(args=args))
            urp["calldone"] = True
            urp["character"] = args
            if callback:
                callback(args)
        
        self._pool_append("getcharacter", id, _callback)
        
        if async: return None
        
        while not urp["calldone"]: time.sleep(0.1)
        
        return urp["character"]
    
    def delete_character(self, character, callback=None, force=False, async=True):
        """
            /api3/?session=<sessionkey>&command=deletecharacter&arg=ri4llrZXK
        """
        if not force and not self._party.get_character(name):
            return
        
        urp = {"calldone": False}
        def _callback(args):
            urp["calldone"] = True
            self._party.remove_character(character=character, character_name=None)
            if callback:
                callback(args)
        
        self._pool_append("deletecharacter", character._id, _callback)
        
        if async: return
        
        while not urp["calldone"]: time.sleep(0.1)
        
        return