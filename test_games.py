import unittest
import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"

class TestGameAPI(unittest.TestCase):
    def test_get_all_games(self):
        """Tüm oyunları getirme testi"""
        response = requests.get(f"{BASE_URL}/games")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('total', data)
        self.assertIn('games', data)
        print(f"\nToplam oyun sayısı: {data['total']}")

    def test_platform_specific_games(self):
        """Platform bazlı oyun getirme testi"""
        platforms = ['steam', 'epic', 'gog']
        for platform in platforms:
            response = requests.get(f"{BASE_URL}/games?platform={platform}")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            print(f"\n{platform.upper()} oyun sayısı: {data['total']}")
            # Platform kontrolü
            if data['games']:
                self.assertEqual(data['games'][0]['platform'].lower(), platform)

    def test_price_filter(self):
        """Fiyat filtresi testi"""
        price_ranges = [
            (0, 10, "0-10"),
            (10, 50, "10-50"),
            (50, 100, "50-100")
        ]
        
        for min_price, max_price, range_name in price_ranges:
            response = requests.get(
                f"{BASE_URL}/games?min_price={min_price}&max_price={max_price}"
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            print(f"\n{range_name} TL arası oyun sayısı: {data['total']}")
            
            # Fiyat aralığı kontrolü
            if data['games']:
                game_price = float(data['games'][0].get('price', 0))
                self.assertTrue(min_price <= game_price <= max_price)

    def test_search_games(self):
        """Oyun arama testi"""
        search_terms = ['witcher', 'portal', 'doom']
        for term in search_terms:
            response = requests.get(f"{BASE_URL}/games/search?q={term}")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            print(f"\n'{term}' araması sonuç sayısı: {data['total']}")
            
            # Arama sonucu kontrolü
            if data['results']:
                game_name = data['results'][0].get('name', '').lower()
                self.assertIn(term, game_name)

    def test_stats(self):
        """Platform istatistikleri testi"""
        response = requests.get(f"{BASE_URL}/games/stats")
        self.assertEqual(response.status_code, 200)
        stats = response.json()
        
        print("\nPlatform İstatistikleri:")
        print(f"Toplam Oyun: {stats['total_games']}")
        print(f"Steam Oyunları: {stats['platforms']['steam']}")
        print(f"Epic Oyunları: {stats['platforms']['epic']}")
        print(f"GOG Oyunları: {stats['platforms']['gog']}")
        print(f"Ücretsiz Oyunlar: {stats['free_games']}")
        print("\nFiyat Aralıkları:")
        print(f"10 TL altı: {stats['price_ranges']['under_10']}")
        print(f"10-30 TL arası: {stats['price_ranges']['10_to_30']}")
        print(f"30 TL üzeri: {stats['price_ranges']['over_30']}")

def run_tests():
    print("Game API Testleri Başlıyor...\n")
    unittest.main(verbosity=2)

if __name__ == '__main__':
    run_tests() 