import json

with open("../steam_data.json", 'r') as f:
    data = json.load(f)

seen_appids = set()
filtered_apps = []

print(len(data['applist']['apps']))

for ele in data['applist']['apps']:
    appid = ele['appid']
    if appid not in seen_appids:
        seen_appids.add(appid)
        filtered_apps.append(ele)

data['applist']['apps'] = filtered_apps

print(len(filtered_apps))

with open("../steam_data.json", 'w') as f:
    json.dump(filtered_apps, f, indent=4)