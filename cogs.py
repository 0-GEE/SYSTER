import asyncio
from datetime import datetime
import traceback
from discord.channel import TextChannel
from discord.embeds import Embed
from discord.ext import commands
import discord
from discord.ext.commands.context import Context
from discord.guild import Guild
from discord.member import Member
from discord.message import Message
from discord.role import Role
import requests
import pymp4parse
import helpers
from loguru import logger


db_file = "servers.json"

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg: Message):
        if msg.author == self.bot.user:
            return
        channel: discord.TextChannel = msg.channel
        msg_guild: Guild = msg.guild
        print("message's guild's id: {}".format(msg_guild.id))
        msg_guild_id = msg_guild.id
        guilds = helpers.load_guilds()
        configs: dict = guilds.get(str(msg_guild_id), {})
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
            embeds: list[Embed] = msg.embeds
            print("embeds:\n  {}".format(str(embeds)))
            for embed in embeds:
                print(embed.video.url)
                url: str = embed.video.url
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
                        log_channel: TextChannel = msg_guild.get_channel(log_channel_id)
                        await log_channel.send("``CRASH GIF DETECTED IN {} SENT BY {}#{}``".format(channel.name,
                                                                                                   msg.author.name,
                                                                                                   msg.author.discriminator))

                        break

        except Exception:
            log_channel: TextChannel = msg_guild.get_channel(log_channel_id)
            await log_channel.send("``{}``".format(traceback.format_exc()))
            traceback.print_exc()

    @commands.command(name='Ptoggle', help='toggles crash gif protection')
    @logger.catch
    async def toggle(self, ctx: commands.Context):
        auth: discord.Member = ctx.author
        channel: discord.TextChannel = ctx.channel
        if not helpers.is_admin(auth):
            await ctx.send("you do not have permission for this command.")
            return
        msg_guild: Guild = ctx.guild
        msg_guild_id = msg_guild.id
        guilds = helpers.load_guilds()
        configs: dict = guilds.get(str(msg_guild_id), {})  
        if len(configs) == 0:
            await ctx.send("Please run 'Setup' command and try again")
            return
        log_channel_id = int(configs["logging channel"])
        if configs["crash protection"]:
            guilds[str(msg_guild_id)]["crash protection"] = False
            try:
                helpers.save_guilds(guilds)
                await ctx.send("Crash gif protection disabled!")
            except Exception:
                logging_channel: TextChannel = msg_guild.get_channel(log_channel_id)
                await logging_channel.send("``{}``".format(traceback.format_exc()))
                await channel.send("``an error occurred.``")
            return
        guilds[str(msg_guild_id)]["crash protection"] = True
        try:
            helpers.save_guilds(guilds)
            await ctx.send("Crash gif protection enabled!")
        except Exception:
            logging_channel: TextChannel = msg_guild.get_channel(log_channel_id)
            await logging_channel.send("``{}``".format(traceback.format_exc()))
            await channel.send("``an error occurred.``")

class Util(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    @commands.command(name='setup', 
                      help='perform quick server config for the bot (specify logging server if applicable)')
    @logger.catch
    async def setup(self, ctx: Context, *args):
        auth: Member = ctx.author
        if not helpers.is_admin(auth):
            await ctx.send("you do not have permission for this command")
            return
        try:
            msg_guild: Guild = ctx.guild
            msg_guild_id = msg_guild.id
            guilds = helpers.load_guilds()
            configs: dict = guilds.get(str(msg_guild_id), {})
            if len(configs) != 0:
                await ctx.send("I am already configured for this server!")
                return
            configs["crash protection"] = True
            configs["caution list"] = ["gfycat.com"]
            if len(args) > 0:
                logging_channel_name = str(args[0])
                channels = msg_guild.text_channels
                logging_channel: TextChannel = None
                found = False
                for channel in channels:
                    if channel.name == logging_channel_name:
                        logging_channel = channel
                        found = True
                        break
                if not found:
                    await ctx.send("Channel ``{}`` not found! Configuration aborted.".format(logging_channel_name))
                    return
                configs["logging channel"] = str(logging_channel.id)
            else:
                logging_channel: TextChannel = await msg_guild.create_text_channel(name='sys-log', 
                                                                                   reason="log channel was not specified at 'setup' command call")
                msg_guild_roles: list[Role] = msg_guild.roles
                for role in msg_guild_roles:
                    if not role.permissions.administrator:
                        await logging_channel.set_permissions(target=role, 
                                                              read_messages=False,
                                                              send_messages=False)
                configs["logging channel"] = str(logging_channel.id)
            guilds[str(msg_guild_id)] = configs
            helpers.save_guilds(guilds)
            await ctx.send("Setup success! I am now ready for use in ``{}``".format(msg_guild.name))
        except Exception:
            traceback.print_exc()
            await ctx.send("``an error occured.\n{}``".format(traceback.format_exc()))

    @commands.command(name='setlog', help='set logging channel for the bot')
    @logger.catch
    async def setlog(self, ctx: Context, *args):
        auth: Member = ctx.author
        if not helpers.is_admin(auth):
            await ctx.send("You do not have permission for this command.")
            return
        if len(args) < 1:
            await ctx.send("Please specify a channel by name and try again!")
            return
        guilds = helpers.load_guilds()
        msg_guild: Guild = ctx.guild
        msg_guild_id = msg_guild.id
        configs: dict = guilds.get(str(msg_guild_id), {})
        if len(configs) == 0:
            await ctx.send("Run 'setup' and try again!")
            return
        logging_channel_name = str(args[0])
        logging_channel: TextChannel = None
        found = False
        msg_guild_channels: list[TextChannel] = msg_guild.channels
        for channel in msg_guild_channels:
            if channel.name == logging_channel_name:
                logging_channel = channel
                found = True
                break
        if not found:
            await ctx.send("Channel ``{}`` not found.".format(logging_channel_name))
            return
        configs["logging channel"] = str(logging_channel.id)
        guilds[str(msg_guild_id)] = configs
        try:
            helpers.save_guilds(guilds)
            await ctx.send("Successfully set logging channel to ``{}``!".format(logging_channel_name))
        except Exception:
            await ctx.send("``an error occured.\n{}``".format(traceback.format_exc()))
            traceback.print_exc()

    @commands.command(name='add', help='add a domain to the risk list')
    @logger.catch
    async def add(self, ctx: Context, *args):
        auth: Member = ctx.author
        if not helpers.is_admin(auth):
            await ctx.send("You do not have permission for this command.")
            return
        if len(args) < 1:
            await ctx.send("please specify a domain name and try again")
            return
        try:
            guilds = helpers.load_guilds()
            msg_guild: Guild = ctx.guild
            msg_guild_id = msg_guild.id
            configs: dict = guilds.get(str(msg_guild_id), {})
            if len(configs) == 0:
                await ctx.send("Please run 'setup' command and try again")
                return
            caution_list: list[str] = list(configs["caution list"])
            new_domain = str(args[0]).strip()
            if caution_list.count(new_domain) > 0:
                await ctx.send("Domain is already in list!")
                return
            caution_list.append(new_domain)
            configs["caution list"] = caution_list
            guilds[str(msg_guild_id)] = configs
            helpers.save_guilds(guilds)
            await ctx.send("Succesfully added ``{}`` to the risk list!".format(new_domain))
        except Exception:
            logging_channel: TextChannel = msg_guild.get_channel(int(configs["logging channel"]))
            await logging_channel.send("``and error occurred.\n{}``".format(traceback.format_exc()))
            await ctx.send("something went wrong. Check the log channel for details")
            traceback.print_exc()

    @commands.command(name='remove', help='remove a domain from the risk list')
    @logger.catch
    async def remove(self, ctx: Context, *args):
        auth: Member = ctx.author
        if not helpers.is_admin(auth):
            await ctx.send("You do not have permission for this command")
            return
        if len(args) == 0:
            await ctx.send("Please specify a domain and try again")
            return
        try:
            guilds = helpers.load_guilds()
            msg_guild: Guild = ctx.guild
            msg_guild_id = msg_guild.id
            configs: dict = guilds.get(str(msg_guild_id), {})
            if len(configs) == 0:
                await ctx.send("Please run 'setup' and try again")
                return
            caution_list: list[str] = configs["caution list"]
            target = str(args[0])
            try:
                caution_list.remove(target)
                await ctx.send("Succesfully removed ``{}`` from the risk list!".format(target))
            except Exception:
                await ctx.send("domain ``{}`` not found in risk list".format(target))
            configs["caution list"] = caution_list
            guilds[str(msg_guild_id)] = configs
            helpers.save_guilds(guilds)
        except Exception:
            await ctx.send("something went wrong. Check log channel for details")
            logging_channel: TextChannel = msg_guild.get_channel(int(configs["logging channel"]))
            await logging_channel.send("``an error occurred\n{}``".format(traceback.format_exc()))
            traceback.print_exc()
        
        


    

