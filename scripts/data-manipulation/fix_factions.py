import json
import re

# Load the JSON data
with open('regions.json', 'r') as file:
    data = json.load(file)

# Define faction assignment rules
alliance_regions = [
    "Stormwind City", "Ironforge", "Darnassus", "Elwynn Forest", "Westfall", "Redridge Mountains",
    "Dun Morogh", "Loch Modan", "Teldrassil", "Darkshore", "Deeprun Tram", "The Stockade"
]

horde_regions = [
    "Orgrimmar", "Thunder Bluff", "Undercity", "Durotar", "Mulgore", "Tirisfal Glades", "The Barrens",
    "Ragefire Chasm"
]

# Special factions to preserve that were there for some reason
special_factions = {
    "Molten Core": "Hydraxian Waterlords",
    "Ruins of Ahn'Qiraj": "Cenarion Circle"
}

# Define default activities based on region type
default_activities = {
    "Zone": ["Explore the region!", "Take a scenic tour!"],
    "City": ["Visit the local tavern!", "Trade with merchants!"],
    "Raid": ["Defeat the bosses!", "Gather your raid group!"],
    "Dungeon": ["Clear the dungeon!", "Collect rare loot!"],
    "Battleground": ["Join the battle!", "Capture the flag!"],
    "Group": ["Clear the dungeon!", "Collect rare loot!"],  # Treat "Group" like a Dungeon
    "Dwarven fortress": ["Clear the dungeon!", "Collect rare loot!"]  # Treat "Dwarven fortress" like a Dungeon
}

# Function to format the screenshot path
def format_screenshot_path(region_name):
    # Convert to lowercase, replace spaces with dashes, remove apostrophes
    formatted_name = region_name.lower().replace(" ", "-")
    formatted_name = re.sub(r"'", "", formatted_name)  # Remove apostrophes
    return f"/screenshots/{formatted_name}.png"

# Function to update factions, screenshot, and activities
def update_regions(regions):
    updated_regions = []
    for region in regions:
        # Determine faction
        faction = "Neutral"  # Default
        if region["name"] in special_factions:
            faction = special_factions[region["name"]]
        elif region["name"] in alliance_regions:
            faction = "Alliance"
        elif region["name"] in horde_regions:
            faction = "Horde"

        # Format screenshot path
        screenshot_path = format_screenshot_path(region["name"])

        # Determine activities based on type
        activities = default_activities.get(region["type"], ["Explore the area!"])  # Fallback if type not found

        # Create updated region with new fields
        updated_region = {
            **region,
            "faction": faction,
            "screenshot": screenshot_path,
            "activities": activities
        }
        updated_regions.append(updated_region)
    
    return updated_regions

# Update the regions
updated_regions = update_regions(data["regions"])

# Save the updated JSON to a new file
with open('updated_regions.json', 'w') as file:
    json.dump({"regions": updated_regions}, file, indent=2)

print("Updated JSON has been saved to 'updated_regions.json'")