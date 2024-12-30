import json

with open("./data/steam_data.json", 'r') as f:
    data = json.load(f)


with open("./data/steam_full_data.json", 'r') as f:
    data_2 = json.load(f)

with open("./data/steam_full_data_temp.json", 'r') as f:
    data_3 = json.load(f)

target_appid = data_2[-1]['appid']
index = next((i for i, app in enumerate(data) if app["appid"] == target_appid), None)

print(len(data_2))

print(f"\n{index}/{len(data)}\n")