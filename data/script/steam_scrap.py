import requests
import json
from bs4 import BeautifulSoup

html_url = f"https://store.steampowered.com/app/"

with open("../steam_data.json", 'r') as f:
    data = json.load(f)

with open("../steam_full_data.json", "r") as f:
    scrap_data = json.load(f)

with open("../steam_full_data_temp.json", 'w') as f:
    f.write(json.dumps(scrap_data, indent=4))

target_appid = scrap_data[-1]['appid']
index = next((i for i, app in enumerate(data) if app["appid"] == target_appid), None)

for ele in data[index+1:]:
    appid = ele['appid']
    print(appid)
    response = requests.get(html_url+str(appid), allow_redirects=False)
    if response.url == "https://store.steampowered.com/":
        continue

    if response.status_code == 200:
        pass
    else:
        continue
    print(appid)
    soup = BeautifulSoup(response.text, "html.parser")
    if soup.find("div", class_="game_area_bubble game_area_dlc_bubble"):
        continue
    elif soup.find("div", class_="game_area_mod_bubble game_area_bubble"):
        continue
    elif soup.find("span", class_="not_yet"):
        continue
    elif not soup.find("div", class_="game_area_purchase_game"):
        continue
    elif soup.find("div", class_="game_area_purchase_game").find("div", class_="game_purchase_price price"):
        price = soup.find("div", class_="game_area_purchase_game").find("div", class_="game_purchase_price price")
    elif soup.find("div", class_="game_area_purchase_game").find("div", class_="discount_final_price"):
        price = soup.find("div", class_="game_area_purchase_game").find("div", class_="discount_final_price")
        discount = soup.find("div", class_="game_area_purchase_game").find("div", class_="discount_pct")
        if discount:
            ele["discount"] = discount.text.strip()
    else:
        continue
    print(appid) 
    if price:
        ele["price"] = price.text.strip()
    else:
        continue 
    
    scrap_data.append(ele)
    print("done")
    with open("../steam_full_data.json", 'w') as f:
        f.write(json.dumps(scrap_data, indent=1))

