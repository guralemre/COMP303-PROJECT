import requests
import json

url = f"https://api.steampowered.com/ISteamApps/GetAppList/v2/"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    with open("../steam_data.json", 'w') as f:
        json.dump(data, f,indent=4)
else:
    print(f"Error: {response.status_code}")
        








