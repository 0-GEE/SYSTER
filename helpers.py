import json
from discord.guild import Guild
from discord.member import Member

db_file = "servers.json"

def is_authorized(user: Member):
    perms = user.guild_permissions
    if perms.view_audit_log:
        return True
    return False

def load_guilds():
    try:
        with open(db_file, 'r') as f:
            guilds: dict = json.load(f)
            f.close()
        return guilds
    except Exception:
        return {}
    
def save_guilds(guilds: dict):
    with open(db_file, 'w') as f:
        json.dump(guilds, f, indent=4)
        f.close()

def remove_guild(guild: Guild):
    guilds = load_guilds()
    target_id = str(guild.id)
    guilds.pop(target_id)
    save_guilds(guilds)