'''
Need:
    - Command Type (App/Website/Powershell) -> DONE
    - Required Words (.lower their responses) -> DONE
    - Required Words among select words (.lower their responses) -> DONE
    - App Directory or Website Link or Powershell Command -> DONE
    - App/Website/Powershell Name -> DONE
'''
import os
import re
import json

# Get User Input on Command Type
def GetCommandType():
    # Response = User's input
    # Error = Warning message to return
    Response, Error = "", ""

    # Will repeat till the Response provided is valid
    while True:
        os.system("cls") # Clears console everything invalid response is provided
        if Error != "": print(f"\n\033[93m{Error}\033[0m\n"); Error = "" # If previously error given, display the error to user

        # Ask user for command type
        Response = input("System: What is the Command Type?\n"
        "1. App\n"
        "2. Website\n"
        "3. Powershell Command\n\n"
        "You: ").strip()

        # Criterias
        if not Response.isnumeric(): # Make sure response is an integer
            Error = "Response is not a number. Please provide 1, 2, or 3." # Warn user criteria not met
        elif not (1 <= int(Response) <= 3): # Make sure input is 1, 2, or 3
            Error = "Response is not valid. Please provide 1, 2, or 3." # Warn user criteria not met
        else:
            break # If criterias are met
    
    # If all criterias are met.. return value depended on selected application
    if Response == "1":
        return "LaunchApplication"
    elif Response == "2":
        return "LaunchWebsite"
    elif Response == "3":
        return "Powershell"
    else:
        return

# Validate if provided CommandName already exists in database
def CommandNameInUse(CommandName: str):
    # Check Database
    with open('Database.json', 'r+') as file:
        Data = json.load(file)
    return CommandName in Data["Commands"]

# Get User Input on Command Name
def GetCommandName(CommandType: str):
    # System Question = The question displayed to user depending on the Command Type Selected
    # Response = User's input
    # Error = Warning message to return
    SystemQuestion = {
        "LaunchApplication": "What is the app's name?",
        "LaunchWebsite": "What is the website's name?",
        "Powershell": "What is the command's name?"
    }
    Response, Error = "", ""

    # Process SystemQuestion based on provided CommandType
    if CommandType == "LaunchApplication":
        SystemQuestion = "What is the app's name?"
    elif CommandType == "LaunchWebsite":
        SystemQuestion = "What is the website's name?"
    elif CommandType == "Powershell":
        SystemQuestion = "What is the command's name?"

    # Will repeat till the Response provided is valid
    while True:
        os.system("cls") # Clears console everything invalid response is provided
        if Error != "": print(f"\033[93m{Error}\033[0m"); Error = "" # If previously error given, display the error to user

        # Ask user for command name
        Response = input(f"System: {SystemQuestion}\nYou: ").strip()

        # Criterias
        if re.compile(r'[\d\\",]').findall(Response): # Make sure there aren't quotation marks or backslash
            Error = "Response contains prohibited symbols. Please refrain from using quotation marks or backslash." # Warn user criteria not met
        elif CommandNameInUse(Response): # Make sure the command name isn't being used by another
            Error = "Command name already exists in the database" # Warn user criteria not met
        else:
            break

    # If all criterias are met.. return response
    return Response

def GetRequiredWords():
    os.system("cls")
    RequiredWords = []
    Response = ""

    print(f"\033[93mType confirm() to confirm\033[0m")
    while True:
        print(f"\nCurrent Words: {RequiredWords}")
        Response = input(f"System: What is word {len(RequiredWords) + 1} that MUST be included in your voice input:\nYou: ").strip().lower()

        if Response != "confirm()":
            RequiredWords.append(Response)
        else:
            break
    return RequiredWords

def GetOneRequiredWords(RequiredWords):
    os.system("cls")
    CurrentWords, OneRequiredWords = [], []
    Response = ""

    print(f"\033[93mType confirm() to confirm\033[0m")
    while True:
        
        while True:
            print(f"\nCurrent Words: {CurrentWords}")
            Response = input(f"System: Please enter word {len(CurrentWords) + 1}. The system will check if it contains at least one of these key words.\nYou: ").strip().lower()

            if Response != "confirm()":
                if Response in RequiredWords:
                    print("Word already exists in required words")
                else:
                    CurrentWords.append(Response)
            else:
                break

        OneRequiredWords.append(CurrentWords)
        CurrentWords = []
        while True:
            Response = input(f"\nSystem: Would you like to confirm the list? (Y/N)\nCurrent List: {OneRequiredWords}\nYou: ").strip()

            if Response.lower() == "y" or Response.lower() == "confirm()":
                return OneRequiredWords
            elif Response.lower() == "n":
                break

def GetCommand(CommandType: str):
    os.system('cls')
    SystemQuestion = {
        "LaunchApplication": "What is the app's directory?",
        "LaunchWebsite": "What is the website's URL?",
        "Powershell": "What is the powershell command?"
    }
    Response = input("System: " + SystemQuestion[CommandType] + ": ").strip().strip('\"')
    if CommandType == "LaunchWebsite" and (not Response.startswith("https://")):
        Response = f"https://{Response}"
    return Response

def GetResponse():
    os.system('cls')
    Response = input("System: What would you like the AI to respond when executing command?\nYou: ").strip()
    return Response

def AddToDatabase():
    Payload = {
    "CommandType": GetCommandType(),
    "RequiredWords": GetRequiredWords()
    }
    Payload["OneRequiredWords"] = GetOneRequiredWords(Payload["RequiredWords"])
    Payload["Response"] = GetResponse()
    Payload["Command"] = GetCommand(Payload["CommandType"])

    while True:
        os.system('cls')
        print(f"System: Do you confirm that the command will have the following data? (Y/N)")
        for Key in Payload:
            print(f"{Key}: {Payload[Key]}")
        Response = input(f"\nYou: ").strip()

        if Response.lower() == "y":
            break
        elif Response.lower() == "n":
            while True:
                Response = input("\nSystem: Do you want to modify the data? (Y/N where N will cancel everything)\nYou: ").strip()
                Error = ""
                if Response.lower() == "y":
                    if Error != "": print(f"\n\033[93m{Error}\033[0m\n"); Error = "" # If previously error given, display the error to user
                    while True:
                        Response = input("\nSystem: Which data would you like to update?\n"
                        "1. Required Words\n"
                        "2. One Required Words\n"
                        "3. Command\n"
                        "4. AI Response\n"
                        "You: ").strip()

                        # Criterias
                        if not Response.isnumeric(): # Make sure response is an integer
                            Error = "Response is not a number. Please provide 1, 2, 3, 4, or 5." # Warn user criteria not met
                        elif not (1 <= int(Response) <= 4): # Make sure input is 1, 2, or 3
                            Error = "Response is not valid. Please provide 1, 2, 3, 4, or 5." # Warn user criteria not met
                        else:
                            break # If criterias are met
                    
                    if Response == "1":
                        Payload["RequiredWords"] = GetRequiredWords()
                    elif Response == "2":
                        Payload["OneRequiredWords"] = GetOneRequiredWords(Payload["RequiredWords"]),
                    elif Response == "3":
                        Payload["Command"] = GetCommand(Payload["CommandType"])
                    elif Response == "4":
                        Payload["Response"] = GetResponse()
                    break
                elif Response.lower() == "n":
                    return
            break
  
    CommandName = GetCommandName(Payload["CommandType"])
    
    with open('Database.json', 'r+') as File:
        Data = json.load(File)
        Data['Commands'][CommandName] = Payload

        for Word in Payload["RequiredWords"]:
            if Word not in Data["WordQuery"]:
                Data["WordQuery"][Word] = []
            Data["WordQuery"][Word].append(CommandName)
        for List in Payload["OneRequiredWords"]:
            for Word in List:
                if Word not in Data["WordQuery"]:
                    Data["WordQuery"][Word] = []
                Data["WordQuery"][Word].append(CommandName)

        File.seek(0) # Should reset file position to the beginning.
        json.dump(Data, File, indent=4)
        File.truncate() # Remove remaining part
    os.system('cls')
    print("System: Database has been updated.\n")

def RemoveAppFromDatabase():
    Response = input("System: What app would you like to remove from the database?\nYou: ").strip() # Command Name in Database (Eg. Google)

    if not CommandNameInUse(Response):
        print("\n\033[93mApp isn't present in the database. Perhaps try another name or a different app.\033[0m\n")
        return
    
    with open('Database.json', 'r+') as File:
        Data = json.load(File)

        for Word in Data['Commands'][Response]["RequiredWords"]:
            if (Word in Data['WordQuery']) and (Response in Data['WordQuery'][Word]):
                if len(Data['WordQuery'][Word]) < 2:
                    del Data['WordQuery'][Word]
                else:
                    Data['WordQuery'][Word].pop(Data['WordQuery'][Word].index(Response))
        for List in Data['Commands'][Response]["OneRequiredWords"]:
            for Word in List:
                if (Word in Data['WordQuery']) and (Response in Data['WordQuery'][Word]):
                    if len(Data['WordQuery'][Word]) < 2:
                        del Data['WordQuery'][Word]
                    else:
                        Data['WordQuery'][Word].pop(Data['WordQuery'][Word].index(Response))
        del Data['Commands'][Response]

        File.seek(0) # Should reset file position to the beginning.
        json.dump(Data, File, indent=4)
        File.truncate() # Remove remaining part

        print(f"\n\033[93m{Response} has been removed from database.\033[0m\n")

def ModifyDatabase():
    while True:
        Response = input("What is the name of the command? ")
        if not CommandNameInUse(Response):
            os.system("cls")
            print("\n\033[93mApp isn't present in the database. Perhaps try another name or a different app.\033[0m\n")
        else:
            break

    CommandName = Response
    Error = ""

    while True:
        if Error != "": print(f"\n\033[93m{Error}\033[0m\n")
        Response = input("What would you like to modify:\n"
                        "1. Command Name\n"
                        "2. Required Words\n"
                        "3. One Required Words\n"
                        "4. Command\n"
                        "5. AI Response\n"
                        "You: ").strip()

        # Criterias
        if not Response.isnumeric(): # Make sure response is an integer
            Error = "Response is not a number. Please provide 1, 2, 3, 4, or 5." # Warn user criteria not met
        elif not (1 <= int(Response) <= 5): # Make sure input is 1, 2, or 3
            Error = "Response is not valid. Please provide 1, 2, 3, 4, or 5." # Warn user criteria not met
        else:
            break # If criterias are met
    
    if Response == "1":

        # Vector Function, turns [list1, list2] into one list without repeating elements
        def VectorWords(NewRequiredWords):
            VectoredWords = []
            for List in NewRequiredWords:
                for Word in List:
                    if Word not in VectoredWords:
                        VectoredWords.append(Word)
            return VectoredWords

        with open('Database.json', 'r+') as file:
            Data = json.load(file)

            # Vectorise OneRequiredWords
            VectoredList = VectorWords(Data["Commands"][CommandName]["OneRequiredWords"])
            
            # Vectorise [RequiredWords, OneRequiredWords]
            VectoredList = VectorWords([Data["Commands"][CommandName]["RequiredWords"], VectoredList])

            # Ask for the new command name, confirming it doesn't exist
            NewCommandName = GetCommandName(Data["Commands"][CommandName]["CommandType"])

            # Copy old payload to new command name
            Data["Commands"][NewCommandName] = Data["Commands"][CommandName]

            # Iterate over every word, removing old command name, adding updated command name
            for Word in VectoredList:
                Data["WordQuery"][Word].pop(Data["WordQuery"][Word].index(CommandName))
                Data["WordQuery"][Word].append(NewCommandName)

            # Remove old payload
            del Data["Commands"][CommandName]

            # Update database
            file.seek(0) # Should reset file position to the beginning.
            json.dump(Data, file, indent=4)
            file.truncate() # Remove remaining part

        print("The command name has been updated")

    elif Response == "2":

        NewRequiredWords = GetRequiredWords()
        with open('Database.json', 'r+') as file:
            Data = json.load(file)

            # Replace payload
            OldRequiredWords = Data["Commands"][CommandName]["RequiredWords"]
            Data["Commands"][CommandName]["RequiredWords"] = NewRequiredWords # Replace payload

            # Remove old words not present in new word from query -> AnB'
            WordsToRemove = [Word for Word in OldRequiredWords if Word not in set(NewRequiredWords)]
            for Word in WordsToRemove:
                if len(Data['WordQuery'][Word]) < 2:
                    del Data['WordQuery'][Word]
                else:
                    Data['WordQuery'][Word].pop(Data['WordQuery'][Word].index(Response))

            # Add new words not present in old word from query -> AnB'
            WordsToAdd = [Word for Word in NewRequiredWords if Word not in set(OldRequiredWords)]
            for Word in WordsToAdd:
                Data["WordQuery"][Word] = [CommandName]

            file.seek(0) # Should reset file position to the beginning.
            json.dump(Data, file, indent=4)
            file.truncate() # Remove remaining part

        print("Required words have been updated.")
            
    elif Response == "3":
        
        def VectorWords(NewRequiredWords):
            VectoredWords = []
            for List in NewRequiredWords:
                for Word in List:
                    if Word not in VectoredWords:
                        VectoredWords.append(Word)
            return VectoredWords
        

        with open('Database.json', 'r+') as file:
            Data = json.load(file)

            NewRequiredWords = GetOneRequiredWords(Data["Commands"][CommandName]["RequiredWords"])

            # Replace payload
            OldRequiredWords = Data["Commands"][CommandName]["OneRequiredWords"]
            Data["Commands"][CommandName]["OneRequiredWords"] = NewRequiredWords # Replace payload

            # lists of lists of words -> list of words
            OldVectoredWords = VectorWords(OldRequiredWords)
            NewVectoredWords = VectorWords(NewRequiredWords)

            # Remove old words not present in new word from query -> AnB'
            WordsToRemove = [Word for Word in OldVectoredWords if Word not in set(NewVectoredWords)]
            for Word in WordsToRemove:
                if len(Data['WordQuery'][Word]) < 2:
                    del Data['WordQuery'][Word]
                else:
                    Data['WordQuery'][Word].pop(Data['WordQuery'][Word].index(Response))

            # Add new words not present in old word from query -> AnB'
            WordsToAdd = [Word for Word in NewVectoredWords if Word not in set(OldVectoredWords)]
            for Word in WordsToAdd:
                Data["WordQuery"][Word] = [CommandName]

            file.seek(0) # Should reset file position to the beginning.
            json.dump(Data, file, indent=4)
            file.truncate() # Remove remaining part

        print("Required words have been updated.")

    elif Response == "4":
        
        with open('Database.json', 'r+') as file:
            Data = json.load(file)
            NewData = GetCommand(Data["Commands"][CommandName]["CommandType"])
            Data["Commands"][CommandName]["Command"] = NewData
            file.seek(0) # Should reset file position to the beginning.
            json.dump(Data, file, indent=4)
            file.truncate() # Remove remaining part

        print("The Command has been updated.")

    elif Response == "5":

        NewData = GetResponse()
        with open('Database.json', 'r+') as file:
            Data = json.load(file)
            Data["Commands"][CommandName]["Response"] = NewData
            file.seek(0) # Should reset file position to the beginning.
            json.dump(Data, file, indent=4)
            file.truncate() # Remove remaining part

        print("The response has been updated.")

def Choices():
    while True:
        Response = input("What would you like to perform:\n"
        "1. Add an app\n"
        "2. Remove an app\n"
        "3. Modify an app's data\n"
        "You: ").strip()

        if Response == "1":
            AddToDatabase()
        elif Response == "2":
            RemoveAppFromDatabase()
        elif Response == "3":
            ModifyDatabase()
        else:
            os.system("cls")

if __name__ == "__main__":
    Choices()