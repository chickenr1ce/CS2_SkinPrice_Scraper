import json
import scraper


try:
    with open('config.json', 'r') as f:
        skins_to_track = json.load(f)
except FileNotFoundError:
    print("Error: config.json not found!")
    skins_to_track = []
except json.JSONDecodeError:
    print("Error: config.json is not a valid JSON!")
    skins_to_track = []
