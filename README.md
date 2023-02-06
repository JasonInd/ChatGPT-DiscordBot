# ChatGPT-DiscordBot

An up to date Discord Bot that generates replies using ChatGPT official API. 
Aimed to be as simple as possible so that people can set it up and modify on their own with ease.

It is currently completely free - that is you will still be able to generate replies regardless of how many tokens you have. This will most likely be fixed on full release of the official API.

## Features

`/chat (message) [conversationID (optional)] [new_conversation (optional)]` Talke to chatGPT and get a response, set new_conversation to true if you want to start a new conversation. You can also specify a previous conversation ID to continue a previous conversation.

`/rollback (amount)` - Go back a select amount of messages from your conversation

![HoggyGPT GIF](https://user-images.githubusercontent.com/72218862/210123549-83357527-0dc9-49a8-bb79-93a6f596850f.gif)

### Only in Versions 0.0.4 and below
`/chat (message) [conversationID (optional)] [parentID (optional)] [new_conversation (optional)]`

Talk to chatGPT and get a response. ConversationID and parentID are optional parameters that allow you to continue a previous conversation if you'd like, keep in mind you must have both to continue a previous conversation. New conversations can be started via setting the new_conversation option to True

`/refresh` - Refresh your session token

## Setup

### Install required modules with pip 

`pip install -r requirements.txt`

### Getting OpenAI API key
1. Create account on OpenAI
2. Go to https://platform.openai.com/account/api-keys
3. Copy API key

### Getting session token (Only required for Versions 0.0.4 and below)

You can get your session token manually from your browser:

1. Go to https://chat.openai.com/api/auth/session
2. Press F12 to open console
3. Go to Application then Cookies
4. Copy the session token value in __Secure-next-auth.session-token
5. Paste it into `config.json` file

You can modify the code to use email and password if you'd like just follow the guide by acheong08 - [chatGPT authentication](https://github.com/acheong08/ChatGPT/wiki/Setup)

### Creating a Discord bot
1. Go to https://discord.com/developers/
2. Create a new application and choose a name
3. Go to the Bot tab and then click Add Bot
4. Copy bot token and put it into the `config.json` file
5. Make sure you turn on the required intents for the bot e.g. Message Intents
6. Invite bot to your server using the OAuth2 URL Generator

### Running the bot
1. Run `python3 bot.py` to start the bot
2. A browser will open up and you will need to press verify you are a human button
3. Use the commands and have fun! 

## License

Released under the [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html) license.

