# Import modules
import json

# Access the database with word queries and commands to initiate on command
def ReadAppDirectories():
    with open('Database.json', 'r') as file:
        return json.load(file)

# Checks if atleast one of the select words are said (Eg. make sure "launch" or "open" is said before launching a program)
def OneRequiredWordsPresent(InputFromUser, OneRequiredWords):
    for EachRequiredList in OneRequiredWords:
        if not any(word in InputFromUser for word in EachRequiredList): # if not atleast one required word
            return False
    return True # if criterias are met and all words are present, return true
