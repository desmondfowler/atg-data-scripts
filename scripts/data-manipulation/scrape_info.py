import requests
from bs4 import BeautifulSoup
import json
import time

# Load your JSON file
with open("regions.json", "r") as f:
    data = json.load(f)

# Function to scrape data from Wowpedia
def scrape_region_data(region_name):
    # Replace spaces with underscores for the URL
    url_name = region_name.replace(" ", "_") + '_(Classic)'
    url = f"https://wowpedia.fandom.com/wiki/{url_name}"
    
    try:
        # Fetch the page
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract description (first paragraph after the intro)
        intro = soup.find("div", class_="mw-parser-output")
        if intro:
            paragraphs = intro.find_all("p", recursive=False)
            for p in paragraphs:
                if p.text.strip():  # Get the first non-empty paragraph
                    description = p.text.strip()
                    break
            else:
                description = "No description available."
        else:
            description = "No description available."

        # Extract faction and type (inferred from infobox or content)
        infobox = soup.find("table", class_="infobox")
        faction = "Neutral"  # Default
        region_type = "Zone"  # Default
        
        if infobox:
            rows = infobox.find_all("tr")
            for row in rows:
                header = row.find("th")
                value = row.find("td")
                if header and value:
                    header_text = header.text.strip().lower()
                    value_text = value.text.strip()
                    if "faction" in header_text:
                        if "alliance" in value_text.lower():
                            faction = "Alliance"
                        elif "horde" in value_text.lower():
                            faction = "Horde"
                        elif "neutral" in value_text.lower():
                            faction = "Neutral"
                        else:
                            faction = value_text  # Specific faction if mentioned
                    elif "type" in header_text or "zone type" in header_text:
                        region_type = value_text.split(",")[0].strip()  # First type only
        
        # Fallback logic for type based on name patterns
        if "lair" in region_name.lower() or "core" in region_name.lower() or "depths" in region_name.lower():
            region_type = "Raid" if "Raid" not in region_type else region_type
        elif "city" in region_name.lower() or region_name in ["Ironforge", "Orgrimmar", "Stormwind City", "Darnassus", "Thunder Bluff", "Undercity"]:
            region_type = "City"
        elif "basin" in region_name.lower() or "gulch" in region_name.lower() or "valley" in region_name.lower() and "alterac" not in region_name.lower():
            region_type = "Battleground"

        return {
            "description": description[:500] + "..." if len(description) > 500 else description,  # Limit length
            "faction": faction,
            "type": region_type
        }
    
    except requests.RequestException as e:
        print(f"Error fetching {region_name}: {e}")
        return {"description": "Error retrieving data.", "faction": "Unknown", "type": "Unknown"}

# Process each region
for region in data["regions"]:
    print(f"Scraping {region['name']}...")
    scraped_data = scrape_region_data(region["name"])
    region["description"] = scraped_data["description"]
    region["faction"] = scraped_data["faction"]
    region["type"] = scraped_data["type"]
    time.sleep(1)  # Be polite to the server, avoid overwhelming it

# Save the updated JSON
with open("updated_regions.json", "w") as f:
    json.dump(data, f, indent=4)

print("Done! Check 'updated_regions.json' for results.")