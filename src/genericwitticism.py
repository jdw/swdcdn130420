
import time
import httplib
from threading import Thread
import json

def _squelcher():
    Genericwitticism.pool = []
    pool = Genericwitticism.pool
    
    while True:
        if len(pool):
            func, args = pool.pop()
            func(args)
        
        time.sleep(0.1)

class Genericwitticism(object):
    pool = []
    t = Thread(target=_squelcher)
    _is_started = False
    
    def __init__(self, key,host=None, port=None):
        self.host = host if host else "genericwitticism.com"
        self.port = port if port else 8000
        self.key = key
        self.base_path =  "/api3/?session=%s&command=%s"
        
    
    def start(self):
        if not Genericwitticism._is_started:
            Genericwitticism.t.start()
            Genericwitticism._is_started = True
        
    def stop(self):
        pass
            
    def _call_api(self, args):
        if not Genericwitticism._is_started:
            raise "Not started!"
            
        command, callback = args
        base_path = self.base_path % (self.key, command)
        
        connection = httplib.HTTPSConnection(self.host, self.port)
        connection.request("GET", base_path)
        results_json = connection.getresponse().read()
        results = json.loads(results_json)
        callback(results)
        
    def get_party(self, callback):
        Genericwitticism.pool.append((self._call_api, ("getparty",callback)))
