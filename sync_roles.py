import os
import requests
from supabase import create_client, Client

# Environment Variables
DISCORD_BOT_TOKEN = os.environ.get("MTQ0Mzk2NTQwNDU5Nzk4MTE4NA.GR57mP.msVd3ztOz_MzmCF5cJrQHMVhtWY_MQC09y86fk")
GUILD_ID = "1281968083509972995"  # ඔයාගේ Discord Server ID එක
SUPABASE_URL = "https://thvyutjntfbxtmsewwrk.supabase.co" # ඔයාගේ Supabase URL එක
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not DISCORD_BOT_TOKEN or not SUPABASE_KEY:
    print("❌ Error: Secrets missing!")
    exit(1)

# Supabase Client Initialization
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def sync_discord_roles():
    headers = {"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}
    
    # Discord API එකෙන් Server එකේ Members ලා 1000ක් දක්වා Fetch කිරීම
    url = f"https://discord.com/api/v10/guilds/{GUILD_ID}/members?limit=1000"
    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        print(f"❌ Discord API Error ({res.status_code}):", res.text)
        return

    members = res.json()
    print(f"🔄 Fetched {len(members)} members from Discord.")

    # Current Users Sync & Update
    active_discord_ids = []
    
    for member in members:
        user_id = str(member['user']['id'])
        roles = member.get('roles', [])
        active_discord_ids.append(user_id)

        # Upsert user roles (කලින් තිබුණු Roles වෙනස් වෙලා නම් එය Auto-update වේ)
        supabase.table('discord_user_roles').upsert({
            'discord_id': user_id,
            'roles': roles,
            'updated_at': 'now()'
        }).execute()

    print("✅ Successfully updated member roles in Supabase!")

if __name__ == "__main__":
    sync_discord_roles()
