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



class Character(object):
    
    _nextId = 0
    
    def __init__(self):
        self.name =""
        self._str = 10
        self._dex = 10
        self._con = 10
        self._int = 10
        self._wis = 10
        self._allocationPoints = 10;
        self._id = Character._nextId
        Character._nextId += 1
        
    def _setAttribute(self, attribute, value):
        if attribute + value <= 18 and attribute + value > 0 and self._allocationPoints >= value:
            attribute += value
            self._allocationPoints -= value
        return attribute
    
    def _increaseAttribute(self, attribute):
        return self._setAttribute(attribute, 1)

    def _decreaseAttribute(self, attribute):
        return self._setAttribute(attribute, -1)

            
    def increaseStrength(self):
        self._str = self._increaseAttribute(self._str);
        
    def increaseDexterity(self):
        self._dex = self._increaseAttribute(self._dex);

    def increaseConstitution(self):
        self._con = self._increaseAttribute(self._con);

    def increaseIntelligence(self):
        self._int = self._increaseAttribute(self._int);

    def increaseWisdom(self):
        self._wis = self._increaseAttribute(self._wis);
        
    def decreaseStrength(self):
        self._str = self._increaseAttribute(self._str);
        
    def decreaseDexterity(self):
        self._dex = self._decreaseAttribute(self._dex);

    def decreaseConstitution(self):
        self._con = self._decreaseAttribute(self._con);

    def decreaseIntelligence(self):
        self._int = self._decreaseAttribute(self._int);

    def decreaseWisdom(self):
        self._wis = self._decreaseAttribute(self._wis);
     
    def getStrength(self):
        return self._str 

    def getDexterity(self):
        return self._dex 

    def getConstitution(self):
        return self._con 

    def getIntelligence(self):
        return self._int 

    def getWisdom(self):
        return self._wis 
    
    def setStrength(self, value):
        self._setAttribute(self._str, value)

    def setDexterity(self, value):
        self._setAttribute(self._dex, value)

    def setConstitution(self, value):
        self._setAttribute(self._con, value)

    def setIntelligence(self, value):
        self._setAttribute(self._int, value)

    def setWisdom(self, value):
        self._setAttribute(self._wis, value)

    @staticmethod
    def test():
        character = Character()
        for i in range(0,8): 
            character.increaseStrength()
        assert character._str == 18
        assert character._allocationPoints == 2
        character.increaseStrength()
        character.increaseDexterity()
        character.increaseConstitution()
        character.increaseIntelligence()
        character.increaseWisdom()
        assert character._str == 18
        assert character._dex == 11
        assert character._con == 11
        assert character._int == 10
        assert character._wis == 10
        assert character._allocationPoints == 0
        print "test passed"
         
if __name__ == '__main__':
    Character.test()
     