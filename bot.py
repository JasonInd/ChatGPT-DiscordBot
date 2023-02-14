import discord, os, json, aiohttp
import typing, asyncio, functools
from discord import app_commands
from revChatGPT.V1 import Chatbot

if not os.path.exists("config.json"):
	with open("config.json", "w+") as f:
		json.dump({}, f, indent=4)

def load_config():
	with open("config.json", "r") as f:
		return json.load(f)

config = load_config()
DISCORD_TOKEN = config['discord_bot_token']
OPEN_AI_EMAIL = config['open_ai_email']
OPEN_AI_PASS = config['open_ai_pass']

chatbot = Chatbot({
  "email": OPEN_AI_EMAIL,
  "password": OPEN_AI_PASS
})

def to_thread(func: typing.Callable) -> typing.Coroutine:
	@functools.wraps(func)
	async def wrapper(*args, **kwargs):
		return await asyncio.to_thread(func, *args, **kwargs)
	return wrapper

@to_thread
def get_response(message, conversationid, parentid):
	response = None
	for data in chatbot.ask(message, conversation_id=conversationid, parent_id=parentid):
		response = data
	return response

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
@app_commands.describe(message = "The message you want to say to chatGPT", conversationid = "Conversation ID to continue a previous conversation (specify a parentid as well)", 
parentid = "ID of the original message (specify a conversationid as well)", new_conversation = "Lets you start a new conversation thread")
async def chat(interaction: discord.Interaction, message: str, conversationid: str = None, parentid: str = None, new_conversation: bool = False):
	await interaction.response.defer()

	try:
		if new_conversation == True:
			chatbot.reset_chat()
		response= await get_response(message, conversationid, parentid)

		if len(response['message']) > 3800:
			split_message1 = response['message'][:3800]
			split_message2 = response['message'][3800:].strip()
			embed1 = discord.Embed(description = f"`{message}`\n{split_message1}")
			embed1.set_footer(text=f"Conversation ID: {response['conversation_id']} Parent ID: {response['parent_id']}")
			embed2 = discord.Embed(description = f"`{message} continued...`\n{split_message2}")
			embed2.set_footer(text=f"Conversation ID: {response['conversation_id']} Parent ID: {response['parent_id']}")
			await interaction.followup.send(embeds=[embed1,embed2])

		else:
			embed = discord.Embed(description = f"`{message}`\n{response['message']}")
			embed.set_footer(text=f"Conversation ID: {response['conversation_id']} Parent ID: {response['parent_id']}")
			await interaction.followup.send(embed=embed)
	except Exception as e:
		print(e)
		await interaction.followup.send("Something went wrong, please try again! \nIf the problem persists, let me know on Github: https://github.com/JasonInd/chatGPT-DiscordBot/issues")

@client.tree.command(name="rollback", description="Rollback a conversation by a set amount of message")
async def refresh(interaction: discord.Interaction, amount: int):
	try:
		chatbot.rollback_conversation(amount)
		await interaction.response.send_message(f"Conversation rolled back by {amount}",ephemeral=True)
	except Exception as e:
		await interaction.response.send_message("An error has occured please try again",ephemeral=True)

@client.tree.command(name="delete-conversation", description="Remove a conversation or all of them")
async def refresh(interaction: discord.Interaction, conversation_id: str, delete_all:bool=False):
	try:
		if delete_all == True:
			chatbot.clear_conversations()
			await interaction.response.send_message("All Conversations deleted",ephemeral=True)
		else:
			chatbot.delete_conversation(conversation_id)
			await interaction.response.send_message("Conversation deleted",ephemeral=True)
	except Exception as e:
		await interaction.response.send_message("An error has occured please try again",ephemeral=True)

client.run(DISCORD_TOKEN)
