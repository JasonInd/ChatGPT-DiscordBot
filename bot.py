import discord, os, json, aiohttp
import typing, asyncio, functools
from discord import app_commands
from revChatGPT.V3 import Chatbot

if not os.path.exists("config.json"):
	with open("config.json", "w+") as f:
		json.dump({}, f, indent=4)

def load_config():
	with open("config.json", "r") as f:
		return json.load(f)

config = load_config()
DISCORD_TOKEN = config['discord_bot_token']
OPEN_AI_KEY = config['open_ai_key']


chatbot = Chatbot(api_key=OPEN_AI_KEY)

def to_thread(func: typing.Callable) -> typing.Coroutine:
	@functools.wraps(func)
	async def wrapper(*args, **kwargs):
		return await asyncio.to_thread(func, *args, **kwargs)
	return wrapper

@to_thread
def get_response(message, temperature):
	response = chatbot.ask(message, temperature=temperature)
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
@app_commands.describe(message = "The message you want to say to chatGPT", temperature = "Set temperature from 0-1, 1 is highest (Controls how random output is)")
async def chat(interaction: discord.Interaction, message: str, temperature: float = 0.5):
	await interaction.response.defer()

	try:		
		response = await get_response(message, temperature)

		if len(response) > 3800:
			split_message1 = response[:3800]
			split_message2 = response[3800:].strip()
			embed1 = discord.Embed(description = f"`{message}`\n{split_message1}")
			embed1.set_footer(text=f"Temperature: {temperature} made by github.com/JasonInd")
			embed2 = discord.Embed(description = f"`{message} continued...`\n{split_message2}")
			embed2.set_footer(text=f"Temperature: {temperature} made by github.com/JasonInd")
			await interaction.followup.send(embeds=[embed1,embed2])

		else:
			embed = discord.Embed(description = f"`{message}`\n{response}")
			embed.set_footer(text=f"Temperature: {temperature} made by github.com/JasonInd")
			await interaction.followup.send(embed=embed)
	except Exception as e:
		print(e)
		await interaction.followup.send("Something went wrong, please try again! \nIf the problem persists, let me know on Github: https://github.com/JasonInd/chatGPT-DiscordBot/issues")

@client.tree.command(name="rollback", description="Rollback a conversation by a set amount of messages")
async def refresh(interaction: discord.Interaction, amount: int):
	try:
		chatbot.rollback(amount)
		await interaction.response.send_message(f"Conversation rolled back by {amount}",ephemeral=True)
	except Exception as e:
		await interaction.response.send_message("An error has occured please try again",ephemeral=True)

client.run(DISCORD_TOKEN)
