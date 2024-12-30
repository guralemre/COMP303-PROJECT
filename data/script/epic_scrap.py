import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

start = 0
count = 100
game_list = []
flag = True

while(flag):
    driver = webdriver.Chrome()
    driver.get(f"https://store.epicgames.com/tr/browse?sortBy=relevancy&sortDir=DESC&category=Game&count={str(count)}&start={str(start)}")
    try:
        name = driver.find_element(By.CLASS_NAME, "css-17qmv99")
        if name.text == "Sonuç bulunamadı":
            flag = False
    except:
        start += count

    page = driver.find_elements(By.CLASS_NAME, "css-lrwy1y")

    for i, ele in enumerate(page):
        game_info = {}

        try:
            price = ele.find_element(By.CLASS_NAME, "css-l24hbj")
            name = ele.find_element(By.CLASS_NAME, "css-lgj0h8")
            game_info['name'] = name.text
            discount = ""
            try:
                discount = ele.find_element(By.CLASS_NAME, "css-1qze2n1")
                game_info['discount'] = discount.text
            except:
                pass 

            if discount != "":
                game_info['price'] = ele.find_elements(By.CLASS_NAME, "css-l24hbj")[3].text
            else:
                game_info['price'] = price.text
        except:
            continue

        game_list.append(game_info)
        with open("../epic_data.json", "w") as f:
            f.write(json.dumps(game_list, indent=4))
    
    driver.quit()

