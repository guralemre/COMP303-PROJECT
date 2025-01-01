import matplotlib.pyplot as plt
import json
import numpy as np

def load_game_data():
    """Tüm platformlardan oyun verilerini yükle"""
    try:
        # Steam verileri
        with open('data/steam_data.json', 'r', encoding='utf-8') as f:
            steam_data = json.load(f)
            steam_games = {game['name'].lower(): convert_price(game.get('price', '0')) 
                         for game in steam_data}

        # Epic verileri
        with open('data/epic_data.json', 'r', encoding='utf-8') as f:
            epic_data = json.load(f)
            epic_games = {game['name'].lower(): convert_price(game.get('price', '0')) 
                         for game in epic_data}

        # GOG verileri
        with open('data/gog_data.json', 'r', encoding='utf-8') as f:
            gog_data = json.load(f)
            gog_games = {game['name'].lower(): convert_price(game.get('price', '0')) 
                        for game in gog_data}

        return steam_games, epic_games, gog_games
    except Exception as e:
        print(f"Veri yükleme hatası: {e}")
        return {}, {}, {}

def convert_price(price):
    """Fiyatları float'a çevir"""
    try:
        if isinstance(price, (int, float)):
            return float(price)
        if isinstance(price, str):
            price = price.replace('₺', '').replace('$', '').replace(',', '').strip()
            return float(price) if price != 'Ücretsiz' and price != 'Free' else 0
        return 0
    except:
        return 0

def find_common_games():
    """Üç platformda da bulunan oyunları bul"""
    steam_games, epic_games, gog_games = load_game_data()
    
    # Ortak oyunları bul
    common_games = set(steam_games.keys()) & set(epic_games.keys()) & set(gog_games.keys())
    
    # Fiyat karşılaştırması yap
    comparisons = []
    for game in common_games:
        comparisons.append({
            'name': game,
            'steam_price': steam_games[game],
            'epic_price': epic_games[game],
            'gog_price': gog_games[game]
        })
    
    return sorted(comparisons, key=lambda x: max(x['steam_price'], x['epic_price'], x['gog_price']), reverse=True)[:10]

def create_price_comparison_chart():
    """Fiyat karşılaştırma grafiği oluştur"""
    comparisons = find_common_games()
    
    # Grafik verilerini hazırla
    games = [game['name'].title() for game in comparisons]
    steam_prices = [game['steam_price'] for game in comparisons]
    epic_prices = [game['epic_price'] for game in comparisons]
    gog_prices = [game['gog_price'] for game in comparisons]

    # Grafik ayarları
    plt.figure(figsize=(15, 8))
    x = np.arange(len(games))
    width = 0.25

    # Çubukları çiz
    plt.bar(x - width, steam_prices, width, label='Steam', color='#1b2838')
    plt.bar(x, epic_prices, width, label='Epic', color='#2a2a2a')
    plt.bar(x + width, gog_prices, width, label='GOG', color='#5c2d91')

    # Grafik düzenlemeleri
    plt.xlabel('Oyunlar')
    plt.ylabel('Fiyat (TL)')
    plt.title('Platform Bazlı Oyun Fiyatları Karşılaştırması')
    plt.xticks(x, games, rotation=45, ha='right')
    plt.legend()

    # Izgara ekle
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Düzen ayarlamaları
    plt.tight_layout()

    # Grafiği kaydet
    plt.savefig('price_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    create_price_comparison_chart()
    print("Fiyat karşılaştırma grafiği oluşturuldu: price_comparison.png") 