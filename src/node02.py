# -*- coding: utf-8 -*-
"""
Challenge:

To create a character, you must first retrieve the character template. The template describe which properties of the character object will be sent later, when retrieving the current status of a character. Make the call and display the result in a formatted way that makes it easy to see the properties at a glance;

/api3/?session=<sessionkey>&command=getchartemplate

Now create a character. The properties which can be modified are ‘name’, ‘str’, ‘dex’, ‘con’, ‘int’ and ‘wis’, the latter ones corresponding to the classical role-playing game characteristics of strength, dexterity, constitution, intelligence and wisdom.

In this game intelligence and wisdom is not used and so need not be modified.

In the beginning each character has 10 allocation points. each characteristic (‘str’, for example) have 10 base points and can be allocated up to 8 allocation points for a total of 18.

‘Str’ higher than 15 increases attack damage, ‘dex’ higher than 15 increases chance of attack, defense and speed, ‘con’ higher than 15 gives additional hit points on level up.
Use the following APi call to create a new character;

/api3/?session=<sessionkey>&command=createcharacter&arg={‘name’:’foobar’,’str’:’15’,’dex’:’15’,’con:’10’,’int’:’10’,’wis’:’10’}

Then use the getparty API call to make sure that you have a new character in your party.
The new information will be an id for the new character. Now use the following API call to get the current status of your newly created character (replace ri4llrZXK with your actual character id, obviously :) ;

/api3/?session=<sessionkey>&command=getcharacter&arg=ri4llrZXK

Finally, delete your new character, using the following API call;

/api3/?session=<sessionkey>&command=deletecharacter&arg=ri4llrZXK

And verify that the character is indeed deleted by calling getparty once more.
"""


import genericwitticism
import settings

import time 

def get_character_template_callback(result):
    print result

def submain():
    api = genericwitticism.Genericwitticism(key=settings.KEY)    
    api.start()
    
    party = api.get_party(force=True)
    """
    print "party 1: ", party
    call = 0
    
    api.create_character("Tj0ng")
    
    while not party:
        print "call: ", call
        call += 1
        time.sleep(0.1)
        party = api.get_party()
    
    print "party size: ", party.get_amount_of_party_members()
    print "party members", party
    """
    api.stop()
     
     
     
     
     
     
     
     