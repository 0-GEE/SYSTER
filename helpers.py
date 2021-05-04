import json
from discord.member import Member

db_file = "servers.json"

def is_admin(user: Member):
    perms = user.guild_permissions
    if perms.administrator:
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