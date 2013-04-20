# -*- coding: utf-8 -*-

from character import Character

class Party(object):
    def __init__(self):
        self._character_by_ids = {}
        self._character_by_names = {}
    
    def add_character(self, character):
        assert isinstance(character, Character)
        
        self._character_by_ids[character._id] = character
        self._character_by_names[character.name] = character
        
    def get_character_by_id(self, id):
        return self._character_by_ids[id]
    
    def get_character_by_name(self, name):
        return self._character_by_names[name]
    
    def remove_character_by_id(self, id):
        if id in self._character_by_ids:
            self._character_by_ids.pop(id)
        
    def remove_character_by_name(self, name):
        self._character_by_names.pop(name)
        
