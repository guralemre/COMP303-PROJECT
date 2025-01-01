import matplotlib.pyplot as plt
import json
import numpy as np

def load_game_data():
    """Platformlardan oyun verilerini yükle"""
    try:
        # Steam verileri
        with open('data/steam_data.json', 'r', encoding='utf-8') as f:
            steam_data = json.load(f)
            steam_games = {game['name'].lower(): game.get('price', '0') for game in steam_data}

        # Epic verileri
        with open('data/epic_data.json', 'r', encoding='utf-8') as f:
            epic_data = json.load(f)
            epic_games = {game['name'].lower(): game.get('price', '0') for game in epic_data}

        # GOG verileri
        with open('data/gog_data.json', 'r', encoding='utf-8') as f:
            gog_data = json.load(f)
            gog_games = {game['name'].lower(): game.get('price', '0') for game in gog_data}

        return steam_data, epic_data, gog_data
    except Exception as e:
        print(f"Veri yükleme hatası: {e}")
        return [], [], []

def find_witcher_games():
    """Witcher oyunlarını bul ve fiyatlarını karşılaştır"""
    steam_data, epic_data, gog_data = load_game_data()
    
    witcher_games = {
        'steam': [],
        'epic': [],
        'gog': []
    }
    
    # Her platformda Witcher oyunlarını ara
    for game in steam_data:
        if 'witcher' in game['name'].lower():
            witcher_games['steam'].append({
                'name': game['name'],
                'price': game.get('price', 'N/A')
            })
    
    for game in epic_data:
        if 'witcher' in game['name'].lower():
            witcher_games['epic'].append({
                'name': game['name'],
                'price': game.get('price', 'N/A')
            })
    
    for game in gog_data:
        if 'witcher' in game['name'].lower():
            witcher_games['gog'].append({
                'name': game['name'],
                'price': game.get('price', 'N/A')
            })
    
    return witcher_games

def print_witcher_prices():
    """Witcher oyunlarının fiyatlarını yazdır"""
    witcher_games = find_witcher_games()
    
    print("\nWitcher Oyunları Fiyat Karşılaştırması:")
    print("-" * 50)
    
    for platform, games in witcher_games.items():
        print(f"\n{platform.upper()} Platform:")
        if games:
            for game in games:
                print(f"Oyun: {game['name']}")
                print(f"Fiyat: {game['price']}")
                print("-" * 30)
        else:
            print("Bu platformda Witcher oyunu bulunamadı.")

def create_witcher_price_chart():
    """Witcher oyunları için fiyat karşılaştırma grafiği oluştur"""
    witcher_games = find_witcher_games()
    
    plt.figure(figsize=(12, 6))
    
    platforms = list(witcher_games.keys())
    x = np.arange(len(platforms))
    
    for i, platform in enumerate(platforms):
        games = witcher_games[platform]
        if games:
            prices = []
            names = []
            for game in games:
                try:
                    price = float(str(game['price']).replace('₺', '').replace('$', '').replace(',', '').strip())
                    prices.append(price)
                    names.append(game['name'])
                except:
                    continue
            
            if prices:
                plt.bar([f"{platform}\n{name}" for name in names], prices, label=platform.upper())
    
    plt.title('Witcher Oyunları Fiyat Karşılaştırması')
    plt.xlabel('Platform ve Oyun')
    plt.ylabel('Fiyat')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    plt.savefig('witcher_prices.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    print_witcher_prices()
    create_witcher_price_chart()
    print("\nWitcher fiyat grafiği oluşturuldu: witcher_prices.png") 