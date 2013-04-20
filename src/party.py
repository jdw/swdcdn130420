from character import Character

class Party(object):
    def __init__(self):
        self._characters = {}
    
    def get_character(self, name):
        if not name in self._characters:
            return None
        
        return self._characters[name]
    
    def get_amount_of_party_members(self):
        return len(self._characters)
    
    def add_character(self, character):
        assert isinstance(character, Character)
        
        self._characters[character.name] = character
    
    def remove_character(self, character=None, character_name=None):
        if not character and not character_name:
            raise Exception("Both character and character name can not be 'None'!")
        
        assert isinstance(character, Character)
        
        name = character_name if character_name else character.name
        
        if name in self._characters:
            self._characters.pop(character.name)
        
        
    