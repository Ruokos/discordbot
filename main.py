#Import of modules needed
import discord, os
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime, timezone, timedelta

#Config for command prefix and also CHANNEL_ID it checks, for now only checks the Victoria 3 channel only
COMMAND_PREFIX = "!"
CHANNEL_ID = 1215322855584301117

if not load_dotenv(): #Get private token for the bot from .env file 
    print("No .env file found, thus the program can't start")

TOKEN = os.environ["DISCORD_TOKEN"]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

TRIGGER_WORDS = ["modlist", "mods", "mod"]

#Sets up the bot with previous variables and configs
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

#Just a test
@bot.event
async def on_ready():
    print("Bot is here :P?")

#This should do the trick :p
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    #Checks if the message is send in the Victoria 3 channel
    if message.channel.id == CHANNEL_ID:
        #Get the member object
        member = message.guild.get_member(message.author.id)
        #Checks if the member has been loaded correctly
        if member is not None:
            current_time = datetime.now(timezone.utc)
            join_date = member.joined_at
            
            #Sends a message to users that joined in the last 10 seconds referring to the pinned messages
            if join_date is not None and (current_time - join_date) <= timedelta(minutes=60):
                if any(trigger_word in message.content.lower() for trigger_word in TRIGGER_WORDS):
                    await message.channel.send(f"Hello {message.author.mention}, The modlist for Victoria 3 is pinned in this channel at the top right, including a short instruction for the installation")

bot.run(TOKEN)
