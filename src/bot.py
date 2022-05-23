import os
import sys
from discord.ext import commands
from dotenv import load_dotenv
from Weather import temp
from Rom import fetch

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='request', help=': (!request (SYSTEM) : (ROM NAME)), fetches the requested rom from vimm.net')
async def request(message):
    response = message.message.content
    print(response)
    await message.send(response)

@bot.command(name='temp')
async def weather(message):
    location = message.message.content.strip("!temp ")
    weather = temp(location)
    response = f"""
{location.upper()}
{"======================================="}
| Date and Time: {weather["Time"]}      |
| Temperature: {weather["Temperature"]} |
| Weather: {weather["Weather"]}     
{"======================================="}
    """
    await message.send(response)


bot.run(TOKEN)
