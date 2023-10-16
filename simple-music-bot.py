import os
import random
import discord
import asyncio
import yt_dlp as youtube_dl
from dotenv import load_dotenv

intents = discord.Intents.all()
intents.members = True

from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
#token loaded from python environment

bot = commands.Bot(command_prefix='$',intents=intents)

yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': "-vn"} 

#Next 3 options are for managing music played by youtube link
@bot.command()
async def play(ctx, url):
        
    if ctx.author.voice is None:
        await ctx.send("You cannot play a video if I'm not in a voice channel.")

    else:

        vc = discord.utils.get(bot.voice_clients, guild=ctx.author.guild)

        if vc is None:
            channel = ctx.author.voice.channel
            vc = await channel.connect()   

        with youtube_dl.YoutubeDL(yt_dl_opts) as ydl:

            song_info = ydl.extract_info(url, download=False)
            vc.play(discord.FFmpegPCMAudio(song_info["url"], before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",options="-vn"))

            while vc.is_playing():
                await asyncio.sleep(1)

@bot.command()
async def pause(ctx):
   ctx.voice_client.pause()
   #await ctx.send("paused")
   
@bot.command()
async def stop(ctx):
   ctx.voice_client.stop()
   #await ctx.send("stopped")    



bot.run(token)