import json

regions_json = "./regions_details.json"

with open(regions_json, "r", encoding="utf-8") as f:
    regions_data = json.load(f)

def generate_wowpedia_links(regions):
    base_url = "https://wowpedia.fandom.com/wiki/"
    
    for region in regions:
        formatted_name = region["name"].replace(" ", "_") + "_(Classic)"
        region["link"] = base_url + formatted_name
    
    return regions

# Ensure we modify the list directly
regions_data["regions"] = generate_wowpedia_links(regions_data["regions"])

# Output updated JSON
print(json.dumps(regions_data, indent=4))

# Optionally, save the updated JSON back to a file
with open("./linked_regions.json", "w", encoding="utf-8") as f:
    json.dump(regions_data, f, indent=4)
