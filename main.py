from discord.ext import commands
import cogs
import discord
from dotenv import load_dotenv
import os


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='%')

bot.add_cog(cogs.Moderation(bot))
bot.add_cog(cogs.Util(bot))

bot.run(TOKEN)