# Import modules
import os
from dotenv import load_dotenv
from assets.modules.AI import AI_Object

################################# AI/User Data #################################
User_Gender = "Male"

AI_Name = "Jarvis"
AI_Gender = "Male"
AI_Description = f"You are a {AI_Gender} AI, similar to Tony Stark's AI JARVIS with the name {AI_Name}, providing the user ({User_Gender}) with short responses/information (strictly no longer than 75 words)."
################################################################################

# Function to start the program
def main():
    try:
        load_dotenv('./.env') # Load Environmental Variables
        AI_API_KEY = os.environ.get("API_KEY")

        # Create AI Class
        AI = AI_Object(Name=AI_Name, Gender=AI_Gender, Description=AI_Description, AI_API_KEY=AI_API_KEY)

        # Repeatedly listen for the trigger word (AI's name)
        while True:
            InputFromUser = AI.Get_Audio(not AI.AIInitiated) # Listen for user's voice inputs
            if InputFromUser.count(AI.Name.lower()) > 0: # If AI's name is said atleast once
                
                AI.Respond("Yes sir?") # Make AI Respond
                AI.ActivateListening() # Start listening for user's command
    except (KeyboardInterrupt, SystemExit): pass # close the program without errors
    finally: print("\n\033[93mAlright bro, can't believe you're shutting me down..\033[0m") # AI's final words :(

# Start the program if this file is main.py
if __name__ == "__main__":
    main()