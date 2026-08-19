import os
import requests
from supabase import create_client, Client

# Code එක ඇතුළේ Token එක paste කරන්න එපා. Environment Variable එකෙන් ඒක auto ගන්නවා!
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
GUILD_ID = "1281968083509972995"
SUPABASE_URL = "https://thvyutjntfbxtmsewwrk.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not DISCORD_BOT_TOKEN or not SUPABASE_KEY:
    print("❌ Error: Secrets missing in GitHub Actions!")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def sync_discord_roles():
    headers = {"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}
    url = f"https://discord.com/api/v10/guilds/{GUILD_ID}/members?limit=1000"
    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        print(f"❌ Discord API Error ({res.status_code}):", res.text)
        return

    members = res.json()
    print(f"🔄 Fetched {len(members)} members from Discord.")

    for member in members:
        user_id = str(member['user']['id'])
        roles = member.get('roles', [])

        supabase.table('discord_user_roles').upsert({
            'discord_id': user_id,
            'roles': roles,
            'updated_at': 'now()'
        }).execute()

    print("✅ Successfully updated member roles in Supabase!")

if __name__ == "__main__":
    sync_discord_roles()
