import asyncio
from datetime import datetime
import traceback
from discord.channel import TextChannel
from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands import bot
import discord
import os
from discord.guild import Guild
from discord.message import Message
import requests
import pymp4parse

sanitize_files = True

caution_list = ["gfycat.com"]

log_channel_name = 'text-chat-logs'

class Moderation(commands.Cog):
    def __init__(self, bot : commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg : discord.Message):
        if msg.author == self.bot.user or not sanitize_files:
            return
        time = datetime.now()
        time = "{} : {} : {}".format(time.hour, time.minute, time.second)
        print(time)
        flagged = False
        channel : discord.TextChannel = msg.channel
        messageid = msg.id
        await asyncio.sleep(0.5)
        msg = await channel.fetch_message(messageid)
        try:
            # await asyncio.sleep(0.5)
            embeds : list[discord.Embed] = msg.embeds
            print("embeds:")
            print(str(embeds))
            for embed in embeds:
                # print(embed)
                print(embed.video.url)
                url : str = embed.video.url
                if type(url) != str:
                    print("empty embed")
                    continue
                for domain in caution_list:
                    if url.find(domain) != -1:
                        flagged = True
                        break
                print(flagged)
                if not flagged:
                    return
                r = requests.get(url, allow_redirects=True)
                with open('subject.mp4', 'wb') as f:
                    f.write(r.content)
                    f.close()
                boxes = pymp4parse.F4VParser.parse(filename='subject.mp4')
                mdat = False
                for box in boxes:
                    dtype = box.type
                    if dtype == 'mdat':
                        mdat = True
                    elif mdat:
                        await msg.delete()
                        await channel.send("DO NOT SEND CRASH GIFS!")
                        guild : Guild = msg.guild
                        channels = guild.text_channels
                        for pchannel in channels:
                            if pchannel.name == log_channel_name:
                                await pchannel.send("``CRASH GIF DETECTED IN {} SENT BY {} #{}``".format(channel.name,
                                                                                                         msg.author.name,
                                                                                                         msg.author.discriminator))
                                break

                        break

        except Exception:
            # await channel.send("``{}``".format(traceback.format_exc()))
            # await msg.delete()
            traceback.print_exc()

    @commands.command(name='Ptoggle', help='toggles crash gif protection')
    async def toggle(self, ctx : commands.Context):
        auth : discord.Member = ctx.author
        channel : discord.TextChannel = ctx.channel
        # if channel.type i
        perms = auth.guild_permissions
        if not perms.administrator:
            await ctx.send("you do not have permission for this command.")
            return
        global sanitize_files
        if sanitize_files:
            sanitize_files = False
            await ctx.send("Crash gif protection disabled!")
            return
        sanitize_files = True
        await ctx.send("Crash gif protection enabled!")


    

