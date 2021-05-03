import asyncio
from asyncio.windows_events import NULL
from datetime import datetime
import traceback
from discord.abc import GuildChannel
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
import json

# sanitize_files = True

# caution_list = ["gfycat.com"]

# log_channel_name = 'text-chat-logs'

db_file = "servers.json"

class Moderation(commands.Cog):
    def __init__(self, bot : commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg : discord.Message):
        if msg.author == self.bot.user:
            return
        channel : discord.TextChannel = msg.channel
        guilds = dict()
        msg_guild : Guild = msg.guild
        print("message's guild's id: {}".format(msg_guild.id))
        with open(db_file, 'r') as f:
            guilds : dict = json.load(f)
            f.close()
        msg_guild_id = msg_guild.id
        configs : dict = guilds.get(str(msg_guild_id), {})
        if len(configs) == 0:
            print("configs not set!")
            return
        if not bool(configs["crash protection"]):
            print("crash protection is off (false)")
            return
        caution_list = list(configs["caution list"])
        log_channel_id = int(configs["logging channel"])
        print("logging channel's id: {}".format(log_channel_id))
        time = datetime.now()
        time = "timestamp = {}:{}:{}".format(time.hour, time.minute, time.second)
        print(time)
        flagged = False

        messageid = msg.id
        await asyncio.sleep(0.5)
        msg = await channel.fetch_message(messageid)
        try:
            # await asyncio.sleep(0.5)
            embeds : list[discord.Embed] = msg.embeds
            print("embeds:\n  {}".format(str(embeds)))
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
                        log_channel : TextChannel = msg_guild.get_channel(log_channel_id)
                        await log_channel.send("``CRASH GIF DETECTED IN {} SENT BY {}#{}``".format(channel.name,
                                                                                                         msg.author.name,
                                                                                                         msg.author.discriminator))

                        break

        except Exception:
            log_channel : TextChannel = msg_guild.get_channel(log_channel_id)
            await log_channel.send("``{}``".format(traceback.format_exc()))
            # await msg.delete()
            traceback.print_exc()

    @commands.command(name='Ptoggle', help='toggles crash gif protection')
    async def toggle(self, ctx : commands.Context):
        auth : discord.Member = ctx.author
        channel : discord.TextChannel = ctx.channel
        perms = auth.guild_permissions
        if not perms.administrator:
            await ctx.send("you do not have permission for this command.")
            return
        msg_guild : Guild = ctx.guild
        msg_guild_id = msg_guild.id
        guilds = dict()
        with open(db_file, 'r') as f:
            guilds : dict = json.load(f)
            f.close()
        configs : dict = guilds.get(str(msg_guild_id), {})
        log_channel_id = int(configs["logging channel"])
        if len(configs) == 0:
            await ctx.send("Please run 'Setup' command and try again")
            return
        if configs["crash protection"]:
            guilds[str(msg_guild_id)]["crash protection"] = False
            try:
                with open(db_file, 'w') as f:
                    json.dump(guilds, f, indent=4)
                    f.close()
                await ctx.send("Crash gif protection disabled!")
            except Exception:
                logging_channel : TextChannel = msg_guild.get_channel(log_channel_id)
                await logging_channel.send("``{}``".format(traceback.format_exc()))
                await channel.send("``and error occurred.``")
            return
        guilds[str(msg_guild_id)]["crash protection"] = True
        try:
            with open(db_file, 'w') as f:
                json.dump(guilds, f, indent=4)
                f.close()
            await ctx.send("Crash gif protection enabled!")
        except Exception:
            logging_channel : TextChannel = msg_guild.get_channel(log_channel_id)
            await logging_channel.send("``{}``".format(traceback.format_exc()))
            await channel.send("``and error occurred.``")


    

