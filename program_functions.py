# Import modules
import os
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

# Createes a database if it doesn't exist
# Source: https://stackoverflow.com/questions/32991069/python-checking-for-json-files-and-creating-one-if-needed
def CreateDatabase():
    if not (os.path.exists("Database.json")):
        data = {"WordQuery": {}, "Commands": {}}
        with open('Database.json', 'w') as file:
            json.dump(data, file)