
# AI Assistant 🤖

Don't use physical inputs and start using AI Assistant, an AI-powered voice assistant. Think of it like your personal butler, providing quick responses with audio feedback and may be tailored to your needs. Automate your workstation through voice commands, and improve productivity.
## Key Features 🔑

**Works Online**: Efficient for lightweight devices.  
**Customisable Experience**: Create your own commands!  
**Open-sourced**: Read the code, change it to your own needs!  
**Custom AI**: Use your own API key
## WARNING ⚠️

The project is currently a prototype used locally by users. There are many improvements to be made such as using SQL for databases to improve scalability. Some personal improvements is encouraged as a learning tool.  

The author is NOT responsible for having API keys leaked, or anything malicious additions by the end user. The project is open-sourced.
## Installation 💾

Before installation, note that the current version is only compatible on Windows, but will soon be compatible with Linux and MacOS.

1. Make sure [**Python**](https://www.python.org/) is installed on your device.
2. Download all of the files.
3. Open terminal and install the dependencies. The command should be something like:
```bash
pip install -r requirements.txt
```
4. Add your [AI's API key](#getting-and-saving-api-keys-) as an environmental variable in "*.env*" file.
5. Rename `main.py` to `main.pyw` if desired to run without a console window.
6. Change the AI's attributes:  open `main.py` in a text editor such as Notepad and change data in "AI/User Data".
7. Run the `main.py*` file and let it initialise (this could take a while depending on your system for the first time).
## Getting and Saving API Keys 🔐

There are many ways to get an API key, but this section will guide you through one way to get an API key.  

1. Go to [OpenRouter](https://openrouter.ai/) and sign up for an account.
2. Go to [Models](https://openrouter.ai/models) and select a preferred model of AI.
3. Go to API and click "Create API key," then create an API key.
4. Copy the API key you have created and store it safely (you won't be able to see this key again).
5. Open the ".env" file in the project and type the following:
*Replace [API_KEY_HERE] with your API Key*
```bash
API_KEY = "Bearer [API_KEY_HERE]"
```
6. Save the ".env" file.
## Usage 🪴

To trigger the AI, simply same the AI's name (default is Jarvis). Provide your input after the AI responds with "Yes sir?" following a beep.

The AI will beep when said its name, and when it asks a question.
## Built-in Commands ⚙️

These commands are coded directly into the program and not in the database.

| Command | Result |
| ------------- | ------------- |
|"[AI Name]" | Assistant responds, and starts listening |  
|"Google [anything]" | Googles whatever is said (doesn't go to default search engine)|  
|"Cancel command" | Assistant will stop listening for inputs|  
|"Terminate AI" | Assistant will shutdown |
|"What's the time?" | Assistant responds "It's [current time in 12 hour format] right now sir!"|

If the Assistant cannot confirm these commands, it will either ask again, run the program through the database for possible answer, or ask your AI model of choice.

These commands can only be overwritten within the code, and is suggested to change to fit different tones, accents, and microphone quality. (I know I had an issue with my accents detecting "cancel" as "council")
## Adding Commands ➕

Use the provided `DatabaseManipulator.py` and select choice "1" to guide you through adding commands.

**The rest of this section will clarify on some of the confusion.**

When asked for words that "MUST be included," be sure to list words that you need to say. E.g., if "tomato" and "potato" are listed, something like "tomato potato" must be said to run the command. Type confirm() to confirm your list of words.  
**Use-case example**: Application's name must be said

In the section for words that "contain at least one of these key word," it will repetitively ask for words until confirm() is typed. As long as one of these words typed is said, the command can run; runs as long as other the words that must be included are also present. After confirming, you can either confirm the final list, or add another list of words with similar intent.  
**Use-case example**: To trigger command with either of two verbs with same meaning such as "open" or "launch"
  
⚠️⚠️⚠️ **WARNING: WHILE USERS MAY ADD POWERSHELL COMMANDS FOR SCRIPTING COMPLEX WORKFLOWS, MALICIOUS ACTORS MAY EXPLOIT ITS PRIVILEGES, SO USE THIS OPTION AS YOUR OWN RISK.** ⚠️⚠️⚠️
## Removing Commands ❌

Use the provided `DatabaseManipulator.py` and select choice "2" to guide you through removing commands.

You must know the name of the command you are trying to remove. If you do not know the name, open `Database.json` file and try looking for it.
## Modifying Commands 🔧

Use the provided `DatabaseManipulator.py` and select choice "3" to guide you through adding commands.

You must know the name of the command you are trying to modify. If you do not know the name, open `Database.json` file and try looking for it. Select the option you'd like to modify, and you will be asked to fill the new data.
