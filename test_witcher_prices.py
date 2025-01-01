import json
import logging

logging.basicConfig(level=logging.INFO)

def test_witcher_prices():
    try:
        # Steam verilerini yükle
        with open('data/steam_full_data.json', 'r', encoding='utf-8') as f:
            steam_data = json.load(f)
            
        # Witcher oyunlarını bul
        witcher_games = []
        for game in steam_data:
            if 'witcher' in game.get('name', '').lower():
                witcher_games.append({
                    'name': game.get('name', ''),
                    'appid': game.get('appid', ''),
                    'price': game.get('price', 'N/A'),
                    'discount': game.get('discount', 'No discount')
                })
        
        # Sonuçları göster
        print("\nWitcher Games on Steam:")
        print("-" * 80)
        
        for game in witcher_games:
            print(f"\nGame: {game['name']}")
            print(f"AppID: {game['appid']}")
            print(f"Price: {game['price']}")
            print(f"Discount: {game['discount']}")
            print("-" * 80)
            
        print(f"\nTotal Witcher games found: {len(witcher_games)}")
        
        # Fiyat formatlarını kontrol et
        print("\nPrice Formats:")
        price_formats = set()
        for game in witcher_games:
            price = game['price']
            price_formats.add(f"{type(price)}: {price}")
        
        for fmt in price_formats:
            print(fmt)
            
    except Exception as e:
        print(f"Error testing Witcher prices: {e}")

if __name__ == "__main__":
    test_witcher_prices() 