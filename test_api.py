import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_api():
    # 1. Tüm oyunları test et
    print("\nTesting all games...")
    response = requests.get(f"{BASE_URL}/games")
    if response.status_code == 200:
        data = response.json()
        print(f"Total games: {data['total']}")
        if data['games']:
            print("\nFirst game example:")
            print(json.dumps(data['games'][0], indent=2))

    # 2. Steam oyunlarını test et
    print("\nTesting Steam games...")
    response = requests.get(f"{BASE_URL}/games?platform=steam")
    if response.status_code == 200:
        data = response.json()
        print(f"Total Steam games: {data['total']}")
        if data['games']:
            print("\nFirst Steam game example:")
            print(json.dumps(data['games'][0], indent=2))

    # 3. Fiyat karşılaştırma testi
    print("\nTesting price comparison...")
    game_name = "witcher"  # Test için örnek oyun
    response = requests.get(f"{BASE_URL}/games/compare/{game_name}")
    if response.status_code == 200:
        data = response.json()
        print(f"\nPrice comparison for '{game_name}':")
        print(json.dumps(data, indent=2))

if __name__ == "__main__":
    test_api() 