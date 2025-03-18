import json
import requests
from urllib.parse import quote
import time
from requests.exceptions import RequestException

# Function to check if a URL is valid
def check_url_validity(url, max_retries=3):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"Checking {url} - Status: {response.status_code}")
            if response.status_code == 200:
                if "Warcraft Wiki does not have a page with this exact name." in response.text:
                    print(f"  -> Page exists but is a 'not found' page")
                    return False
                return True
            elif response.status_code == 429:
                print(f"  -> Rate limited (429), retrying in {2 ** attempt} seconds...")
                time.sleep(2 ** attempt)  # Exponential backoff: 1s, 2s, 4s
                continue
            else:
                print(f"  -> Non-200 status code: {response.status_code}")
                return False
        except RequestException as e:
            print(f"  -> Request failed: {str(e)}")
            return False
    print(f"  -> Max retries reached for {url}")
    return False

# Load JSON data
with open('linked_regions.json', 'r') as file:
    data = json.load(file)

for region in data['regions']:
    region_name = region['name']
    new_url = f"https://warcraft.wiki.gg/wiki/{quote(region_name)}_(Classic)"
    region['link'] = new_url
    
    print(f"\nTesting {region['name']} with _(Classic):")
    if not check_url_validity(new_url):
        new_url = f"https://warcraft.wiki.gg/wiki/{quote(region_name)}"
        region['link'] = new_url
        
        print(f"Testing {region['name']} without _(Classic):")
        if not check_url_validity(new_url):
            print(f"Warning: No valid page found for {region['name']}")
    
    # Add a delay between regions to avoid hitting rate limits
    time.sleep(5)  # 2-second delay between each region check

# Save the modified JSON
with open('modified_links_regions.json', 'w') as file:
    json.dump(data, file, indent=4)

print("\nJSON file has been updated with new links!")