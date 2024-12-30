from selenium import webdriver
from selenium.webdriver.common.by import By
import json

game_list = []
p_driver = webdriver.Chrome()
p_driver.get("https://www.gog.com/en/games?hideDLCs=true")
page_number = p_driver.find_element(By.CSS_SELECTOR, "button[selenium-id='smallPaginationPage']")


for i in range(1, int(page_number.text)+1):
    driver = webdriver.Chrome()
    driver.get(f"https://www.gog.com/en/games?hideDLCs=true&page={i}")
    print(f"page{i}")

    page = driver.find_element(By.CSS_SELECTOR, "div[selenium-id='paginatedProductsGrid']")

    elements = page.find_elements(By.CSS_SELECTOR, "product-tile[class='ng-star-inserted']")

    for ele in elements:
        game_dict = {}
        discount = ""
        
        try:
            coming_soon = ele.find_elements(By.CSS_SELECTOR, "span[selenium-id='productPriceComingSoonLabel']")
            if coming_soon:
                continue
        except:
            pass 

        try:
            free = ele.find_elements(By.CSS_SELECTOR, "span[selenium-id='productPriceFreeLabel']")
            if free:
                game_dict['price'] = "Free"
        except:
            pass
        try:
            price = ele.find_element(By.CSS_SELECTOR, "price-value[selenium-id='productPriceValue']")
            if '\n' in price.text:
                price_parts = price.text.split('\n')
                game_dict['price'] = price_parts[1]
            else:
                game_dict['price'] = price.text
        except:
            pass

        name = ele.find_element(By.CSS_SELECTOR, "product-title[selenium-id='productTitle']")
        game_dict['name'] = name.text

        try:
            discount = ele.find_element(By.CSS_SELECTOR, "price-discount[selenium-id='productPriceDiscount']")
            game_dict['discount'] = discount.text
        except:
            pass

        game_list.append(game_dict)
    
    with open("../gog_data.json", "w") as f:
        f.write(json.dumps(game_list,indent=4))

    driver.quit()

p_driver.quit()    