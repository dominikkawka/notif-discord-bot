import os
import discord
from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN=os.getenv('DISCORD_TOKEN')
CHANNEL_ID=int(os.getenv('CHANNEL_ID'))
TIMEZONE=ZoneInfo('Europe/London')
MEETING_TIME='15:30'
START_DATE= date.fromisoformat('2026-01-14') #year-month-day
COMMUNITY_AGENDA = os.getenv('COMMUNITY_AGENDA')

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@tasks.loop(minutes=1)
async def check_meeting():
    currentTime = datetime.now(TIMEZONE)

    daysSince = (currentTime.date() - START_DATE).days 

    currentTimeStr = currentTime.strftime("%H:%M")
    thirtyMinReminderStr = (currentTime + timedelta(minutes=30)).strftime("%H:%M")
    channel = bot.get_channel(CHANNEL_ID)

    print("Check meeting started: " + currentTimeStr)

    if not channel:
        return print("channel id doesn't exist or bot not in discord channel: ") #+ str(CHANNEL_ID)

    if daysSince % 14 != 0:
        return print("Meeting not today.")
    
    if currentTimeStr == MEETING_TIME:
        await channel.send(f"🔔 @everyone: The community meeting is starting now! Link to agenda: " + COMMUNITY_AGENDA)

    if thirtyMinReminderStr == MEETING_TIME:
        await channel.send(f"⏲️ @everyone: The community meeting is starting in 30 minutes! Link to agenda: " + COMMUNITY_AGENDA)
    
@bot.event
async def on_ready():
    print("Bot online.")
    check_meeting.start()

bot.run(DISCORD_TOKEN)