# Import Modules
import sys
import json
import subprocess
import urllib.parse
import re
from datetime import datetime
import requests
import speech_recognition as SR
import edge_tts
from playaudio import playaudio


# Import Local Modules
import assets.modules.program_functions as program_functions

# Main AI Class
class AI_Object:
    # Initialise
    def __init__(self, Name, Gender, Description, AI_API_KEY):
        self.Name = Name
        self.Gender = Gender
        self.AIInitiated = False
        self.Description = Description
        self.AI_API_KEY = AI_API_KEY

        # Create Database if it doesn't exist
        program_functions.CreateDatabase()

        # Import local database for certain words to listen for, and their responses
        print("\n\033[93mReading Database\033[0m")
        self.AppDirectories = program_functions.ReadAppDirectories()

        # Initialise Speech Recognition Module
        print("\n\033[93mInitialising Input Listener\033[0m")
        self.Recogniser = SR.Recognizer()

    # Plays a local file audio
    def PlaySound(self, filename):
        playaudio(filename)

    # Get the user's audio from microphone
    def Get_Audio(self, PlayNotif = True):
        with SR.Microphone() as source: # select a microphone
            self.Recogniser.adjust_for_ambient_noise(source, duration=0.5) # adjust for background noise
            if not self.AIInitiated: self.Respond(self.Name + " has been initiated."); self.AIInitiated = True # if not informed users that AI is initiated, inform them
            if PlayNotif: self.PlaySound('./assets/sounds/listening.wav') # listening tone
            audio = self.Recogniser.listen(source) # start recording for user inputs
            said = "" # variable declaration

            try:
                said = self.Recogniser.recognize_google(audio, language="english") # attempt to transcribe audio to text
            except Exception as e:
                pass # pass no response

        if said.replace(" ", "") != "": print(f"User: {said.strip()}") # ignores silent inputs for printing purposes
        return said.strip().lower() # returns transcribed text

    # Text-to-Speech
    def Respond(self, Response: str):
        Output = edge_tts.Communicate(Response, "en-GB-RyanNeural") # TTS Model
        
        # Convert Response Text to Audio and overwrite to "AI_Response.mp3"
        with open("./assets/sounds/AI_Response.mp3", "wb") as file:
            for chunk in Output.stream_sync():
                if chunk["type"] == "audio":
                    file.write(chunk["data"])

        print(f"{self.Name}: {Response}") # print to console
        self.PlaySound("./assets/sounds/AI_Response.mp3") # play the response

    # Ask AI for a response
    def AI_Response(self, InputFromUser: str, PreviousConversation: dict={}):
        # Create new chat with instructions for the AI
        Messages = [
                {"role": "system", "content": self.Description}
                ]
        
        # If AI referred to this function, PreviousConversation will be provided.
        if PreviousConversation != {}:
            # If provided, restore previous chat history to Messages variable
            for Message in PreviousConversation:
                Messages.append(Message)
        Messages.append({"role": "User", "content": InputFromUser}) # Add the user's latest response to the end of messages

        # Create a POST request to OpenRouter API to get an AI generated response based on Messages
        completion = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": self.AI_API_KEY,
                "Content-Type": "application/json",
                "HTTP-Referer": "<YOUR_SITE_URL>", #  Optional. Site URL for rankings on openrouter.ai.
                "X-Title": "<YOUR_SITE_NAME>", #  Optional. Site title for rankings on openrouter.ai.
            },
            data=json.dumps({
                "model": "deepseek/deepseek-r1:free", # utilises Deepseek's R1 Model
                "messages": Messages
            })
            ).json()
        
        # Get the text content from the response
        content = completion['choices'][0]["message"]["content"] or "Couldn't contact servers. I won't be able to answer this question unfortunately."
        
        # Add AI's response to history
        Messages.append({"role": "AI", "content": content})

        return Messages

    # Process user's microphone input into commands
    def ActivateListening(self, PreviousConversation={}):

        # Listen and collate user's voice input
        InputFromUser = self.Get_Audio()

        if InputFromUser.strip() and InputFromUser.split()[0] == "google": # if user said "google {blah blah blah}"
            URL = f"https://google.com/search?q={urllib.parse.quote_plus(' '.join(InputFromUser.split()[1:]))}" # parse string to google link
            subprocess.run(r'explorer.exe "{}"'.format(URL)) # open link in default browser

        elif "cancel command" in InputFromUser: # cancel listening command

            self.Respond("Cancelling Command.")

        elif "terminate AI" in InputFromUser: # close the program

            self.Respond("Terminating sir.")
            sys.exit()

        elif "what's the time" in InputFromUser: # provides the current time

            self.Respond("It's {} right now sir!".format(datetime.now().strftime("%I:%M %p").lstrip("0")))

        elif InputFromUser.replace(" ", "") == "": # If user's response wasn't heard
            
            self.Respond("Sorry I didn't hear that could you repeat that?")
            self.ActivateListening()

        else: # If no criteria fit, access database's commands

            self.LaunchProgram(InputFromUser, PreviousConversation)

    # Process user's microphone input into executing programs within the database (if failed, asks AI)
    def LaunchProgram(self, InputFromUser, PreviousConversation={}):
        InputWords = re.findall(r'\b\w+\b', InputFromUser) # separates a sentence into words. Eg. "hey darling would you like one?" -> ["hey", "darling", "would", "you", "like", "one"]
        CheckedApps = [] # cache for programs we have already checked
        CheckedWords = [] # cache for words we have already checked

        for Word in InputWords: # for words in user's input
            if not (Word in CheckedWords): # if we haven't checked this word yet
                CheckedWords.append(Word) # cache the word
                if self.AppDirectories["WordQuery"].get(Word): # If the word is related to a stored app
                    for App in self.AppDirectories["WordQuery"][Word]: # Go over every app the word is related to
                        if not (App in CheckedApps): # if we haven't checked this app yet
                            CheckedApps.append(App) # cache the app
                            RequiredWords = self.AppDirectories["Commands"][App]["RequiredWords"] # Words that are required (MUST be in the input)
                            OneRequiredWords = self.AppDirectories["Commands"][App]["OneRequiredWords"] # Words with the need to require only one word. Eg. For [["one, two"], ["three, four"]], one/two AND three/four must be present

                            CommandType = self.AppDirectories["Commands"][App]["CommandType"] # Variable for if the command is a powershell cmd or website link
                            if all(word in InputFromUser for word in RequiredWords): # check if RequiredWords are met
                                if OneRequiredWords == [] or program_functions.OneRequiredWordsPresent(InputFromUser, OneRequiredWords): # check if OneRequiredWords are met

                                    # At this point, the App that user attempted to launch will be confirmed
                                    try:
                                        # AI respond with database response while executing the command
                                        self.Respond(self.AppDirectories["Commands"][App]["Response"])

                                        if CommandType == "LaunchApplication": # Launch App if the Command is a link
                                            AppDirectory = self.AppDirectories["Commands"][App]["Command"]
                                            subprocess.run(r'explorer.exe "{}"'.format(AppDirectory))
                                        elif CommandType == "LaunchWebsite": # Launch Website if the Command is a link
                                            URL = self.AppDirectories["Commands"][App]["Command"]
                                            subprocess.run(r'explorer.exe "{}"'.format(URL))
                                        elif CommandType == "Powershell": # Launch powershell command if command is PS command
                                            subprocess.run(self.AppDirectories["Commands"][App]["Command"])

                                    except: # if error while launching

                                        # warn user that the launch was unsuccessful
                                        self.Respond("Sorry, launch failed.")

                                    return # end function
                                
        # If we get here, it means we couldn't find anything in the database. Thereby, our course of action is to ask AI
        NewConversation = self.AI_Response(InputFromUser, PreviousConversation) # gets chat history for this session
        AI_Response = NewConversation[-1]["content"] # gets AI's response
        self.Respond(AI_Response) # Make TTS respond

        if AI_Response.endswith("?"): # If the AI has left a sort of question
            self.ActivateListening(NewConversation) # Continue the conversation by listening to user's next response
