import discord


def is_admin(user : discord.Member):
    perms = user.guild_permissions
    if perms.administrator:
        return True
    return False