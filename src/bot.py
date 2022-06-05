import os
import sys
from discord.ext import commands
from discord import File, HTTPException
from dotenv import load_dotenv
from weather import temp
from rom import fetch

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='rom', help=': (!rom (SYSTEM): (ROM NAME)), fetches the requested rom from vimm.net')
async def send(message):
    request = message.message.content.replace("!rom ", "")
    print(f"Fetching... {request}")
    try:
        await message.send(file=File(fetch(request)))
    except HTTPException as E:
        print(f"{request} : {E.text}")
        await message.send(f"{request} : {E.text}")
    except Exception as E:
        print(f"{request} : {E}")
        await message.send(f"{request} : {E}")

@bot.command(name='temp')
async def weather(message):
    location = message.message.content.strip("!temp ")
    weather = temp(location)
    response = f"""
{location.upper()}
{"====================================="}
| Date and Time: {weather["Time"]}     |
| Temperature: {weather["Temperature"]}|
| Weather: {weather["Weather"]}
{"====================================="}
    """
    await message.send(response)


bot.run(TOKEN)
