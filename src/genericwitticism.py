
import time
import httplib
from threading import Thread
import json

import character

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
        self.base_path =  "/api3/?session=%s&command=%s"
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
        base_path = self.base_path % (self.key, command)
        if api_args:
            base_path = base_path + api_args
            
        connection = httplib.HTTPSConnection(self.host, self.port)
        connection.request("GET", base_path)
        
        response = connection.getresponse()
        results_json = response.read()
        results = json.loads(results_json)
        
        if "error" in results:
            if "Could not find valid session from provided api key or session key" in results["error"]:
                raise Exception("No valid session for API key %s" % self.key)

            return
        
        connection.close()
        callback(results)
    
    def _pool_append(self, name, args, callback):
        Genericwitticism.pool.append((self._call_api, (name, args, callback)))
        
    def get_party(self, callback=None, force=False):
        if not force and self._party:
            return self._party
        
        self._party = None
        def _callback(args):
            self._party = args
            if callback:
                callback(args)
        
        self._pool_append("getparty", None, _callback)
        
        return None
        
        
    def get_character_template(self, callback, force=False):
        if not force and self._character_template:
            return self._character_template
        
        self._character_template = None
        
        def _callback(args):
            self._character_template = args
            if callback:
                callback(args)
        
        self._pool_append("getchartemplate", None, callback)
        
        return None
    
    def create_character(self, name, str=10, dex=10, con=10, int=10, wis=10, force=False):
        t_char = character.Character()
        t_char.name = name
        
        Genericwitticism.pool.append((self._call_api, ("createcharacter", args, callback)))
    
    