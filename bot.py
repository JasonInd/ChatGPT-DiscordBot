import discord, os, json, aiohttp
import typing, asyncio, functools
from discord import app_commands
from revChatGPT.Official import AsyncChatbot

if not os.path.exists("config.json"):
    with open("config.json", "w+") as f:
        json.dump({}, f, indent=4)

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

config = load_config()
DISCORD_TOKEN = config['discord_bot_token']
OPEN_AI_KEY = config['open_ai_key']

chatbot = AsyncChatbot(api_key=OPEN_AI_KEY)


class aclient(discord.Client):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!",intents=intents,help_command=None)
        self.tree = app_commands.CommandTree(self)
        self.synced = False

    async def setup_hook(self):
        await self.tree.sync()
        self.synced = True
        print(f"Synced Slash commands for {self.user}")

    async def on_ready(self):
        print(f"Logged in as {self.user}")

client = aclient()

@client.tree.command(name="chat",description="Talk to chatGPT")
@app_commands.describe(message = "The message you want to say to chatGPT", conversation_id = "Specify a previous conversation ID",new_conversation = "Lets you start a new conversation thread")
async def chat(interaction: discord.Interaction, message: str, conversation_id: str = None, new_conversation: bool = False):
    await interaction.response.defer()

    try:
        if new_conversation == True:
            chatbot.reset()
        response = await chatbot.ask(message, conversation_id)

        if len(response['choices'][0]['text']) > 3800:
            split_message1 = response['choices'][0]['text'][:3800]
            split_message2 = response['choices'][0]['text'][3800:].strip()
            embed1 = discord.Embed(description = f"`{message}`\n{split_message1}")
            embed1.set_footer(text=f"Prompt Tokens: {response['usage']['prompt_tokens']} │ Completion Tokens: {response['usage']['completion_tokens']} │ Total Tokens Used: {response['usage']['total_tokens']}")
            embed2 = discord.Embed(description = f"`{message} continued...`\n{split_message2}")
            embed2.set_footer(text=f"Prompt Tokens: {response['usage']['prompt_tokens']} │ Completion Tokens: {response['usage']['completion_tokens']} │ Total Tokens Used: {response['usage']['total_tokens']}")
            await interaction.followup.send(embeds=[embed1,embed2])

        else:
            embed = discord.Embed(description = f"`{message}`\n{response['choices'][0]['text']}")
            embed.set_footer(text=f"Prompt Tokens: {response['usage']['prompt_tokens']} │ Completion Tokens: {response['usage']['completion_tokens']} │ Total Tokens Used: {response['usage']['total_tokens']}")
            await interaction.followup.send(embed=embed)
    except Exception as e:
        print(e)
        await interaction.followup.send("Something went wrong, please try again! \nIf the problem persists, let me know on Github: https://github.com/JasonInd/chatGPT-DiscordBot/issues")

@client.tree.command(name="rollback", description="Go back a specified number of messages")
async def refresh(interaction: discord.Interaction, amount:int):
    try:
        chatbot.rollback(amount)
        #print(f"Rolled back chat history by {amount} messages")
        await interaction.response.send_message(f"Rolled back chat history by {amount} messages",ephemeral=True)
    except Exception as e:
        await interaction.response.send_message("An error has occured please try again",ephemeral=True)

client.run(DISCORD_TOKEN)
