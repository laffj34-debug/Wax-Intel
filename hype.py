import requests
import os
from supabase import create_client

# This connects to the database you already made
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_KEY")
supabase = create_client(url, key)

def run_hype_check():
    # 1. Get your dad's players from the SQL table you made
    cards = supabase.table("cards").select("player_name").execute()
    player_list = [c['player_name'] for c in cards.data]
    
    # 2. Check the live MLB scores
    data = requests.get("https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard").json()
    
    for event in data.get('events', []):
        summary = str(event).lower()
        for player in player_list:
            if player.lower() in summary and "home run" in summary:
                # 3. If found, turn on the "Fire" mode in the database
                supabase.table("cards").update({"is_hype": True}).eq("player_name", player).execute()
                print(f"Hype detected for {player}!")

run_hype_check()