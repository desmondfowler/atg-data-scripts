import json

with open("./regions.md", "r", encoding="utf-8") as f:
    regions_md = f.read()


# Convert markdown list to a structured JSON format
regions = []
lines = regions_md.split("\n")

for line in lines:
    line = line.strip()
    if line.startswith("- "):
        region_name = line[2:]  # Remove '- ' from beginning
        regions.append({
            "id": len(regions) + 1,  # Ensure ID is sequential
            "name": region_name,
            "description": "",  # Placeholder for future data
            "faction": "",  # Placeholder for faction info (Alliance, Horde, Neutral)
            "type": "",  # Placeholder for type (City, Dungeon, Zone, Battleground, etc.)
        })


# Save to a JSON file
with open("regions.json", "w", encoding="utf-8") as f:
    json.dump({"regions": regions}, f, indent=4, ensure_ascii=False)

print("regions.json file has been created!")
