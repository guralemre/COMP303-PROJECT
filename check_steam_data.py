import json
import logging

logging.basicConfig(level=logging.INFO)

def check_steam_data():
    try:
        with open('data/steam_full_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"\nTotal games in steam_full_data.json: {len(data)}")
            
            if data:
                print("\nFirst 5 games:")
                for game in data[:5]:
                    print("\nGame:", game.get('name'))
                    print("AppID:", game.get('appid'))
                    print("Price (USD):", game.get('price'))
                    print("Discount:", game.get('discount'))
                    print("-" * 50)

                # Fiyat formatlarını kontrol et
                print("\nUnique price formats:")
                price_formats = set()
                for game in data:
                    if 'price' in game:
                        price_formats.add(str(type(game['price'])) + ": " + str(game['price']))
                for fmt in price_formats:
                    print(fmt)

    except Exception as e:
        print(f"Error reading steam_full_data.json: {e}")

if __name__ == "__main__":
    check_steam_data() 