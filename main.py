from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import auth, credentials, firestore
import jwt
from passlib.context import CryptContext
import logging
import json




# Firebase Ayarları
cred = credentials.Certificate('firebase_key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Flask ve CORS
app = Flask(__name__)
CORS(app)

# Şifreleme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Ayarları
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# Kullanıcıyı Veritabanından Getirme
def get_user(username: str):
    doc_ref = db.collection('users').document(username)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return None

# Kullanıcı Şifre Doğrulama
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# JWT Oluşturma
def create_access_token(username: str):
    payload = {"sub": username}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Kullanıcı Oluşturma
@app.route('/api/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return jsonify({'error': 'Missing fields'}), 400

        # Şifreyi hashleyip veritabanına kaydetme
        hashed_password = pwd_context.hash(password)
        db.collection('users').document(username).set({
            'email': email,
            'password': hashed_password
        })

        return jsonify({'message': 'User created successfully!'}), 201
    except Exception as e:
        logging.error(f"Error in signup: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# Kullanıcı Girişi
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Missing fields'}), 400

        user = get_user(username)
        if not user or not verify_password(password, user['password']):
            return jsonify({'error': 'Invalid credentials'}), 401

        # JWT oluşturma
        token = create_access_token(username)
        return jsonify({'access_token': token}), 200
    except Exception as e:
        logging.error(f"Error in login: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    
#Password Reset
@app.route('/api/reset', methods=['POST'])
def reset():
    try:
        data = request.json
        email = data.get('email')
        new_password = data.get('password')

        # Alanlar kontrol ediliyor
        if not email or not new_password:
            return jsonify({'error': 'Email ve yeni şifre gerekli'}), 400

        # Kullanıcıyı email ile bul
        users = db.collection('users').where('email', '==', email).stream()
        user_doc = None
        for user in users:
            user_doc = user
            break

        if not user_doc:
            return jsonify({'error': 'Bu email adresi ile kayıtlı kullanıcı bulunamadı'}), 404

        # Yeni şifreyi hashleyip Firestore'da güncelle
        hashed_password = pwd_context.hash(new_password)
        db.collection('users').document(user_doc.id).update({
            'password': hashed_password
        })

        return jsonify({'message': 'Şifre başarıyla güncellendi'}), 200
    except Exception as e:
        logging.error(f"Error in reset: {e}")
        return jsonify({'error': 'Şifre sıfırlama işlemi başarısız oldu'}), 500


# JWT Doğrulama
@app.route('/api/protected', methods=['GET'])
def protected_route():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return jsonify({'error': 'Token is missing'}), 401

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        return jsonify({'message': f'Hello, {username}! This is a protected route.'}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401

# Test Bağlantı
@app.route('/api/hello', methods=['GET'])
def hello_world():
    return jsonify(message="Connected from Flask!")

# JSON dosyalarını oku
def load_platform_data(platform):
    try:
        if platform == 'epic':
            with open('epic_data.json', 'r') as file:
                return json.load(file)
        elif platform == 'gog':
            with open('gog_data.json', 'r') as file:
                return json.load(file)
        elif platform == 'steam':
            with open('steam_full_data.json', 'r') as file:
                return json.load(file)
        else:
            return []
    except Exception as e:
        logging.error(f"Error loading data for platform {platform}: {e}")
        return []


# Favorilere ekle
@app.route('/api/favorites', methods=['POST'])
def add_to_favorites():
    try:
        # Token doğrulama
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')

        if not username:
            return jsonify({'error': 'Invalid token'}), 401

        # İstekten oyun bilgilerini al
        data = request.json
        game_data = {
            'id': data.get('id', ''),
            'name': data.get('name', ''),
            'platform': data.get('platform', ''),
            'price': data.get('price', ''),
            'price_formatted': data.get('price_formatted', '')
        }

        # Favori öğeleri kullanıcıya ekle
        favorites_ref = db.collection('users').document(username).collection('favorites')

        # Öğe kontrolü (önceden eklenmiş mi?)
        existing_items = favorites_ref.where('id', '==', game_data['id']).get()
        
        if list(existing_items):
            return jsonify({'error': 'Game already in favorites'}), 400

        # Oyunu favorilere ekle
        favorites_ref.add(game_data)

        return jsonify({'message': 'Game added to favorites successfully!'}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except Exception as e:
        logging.error(f"Error in add_to_favorites: {e}")
        return jsonify({'error': 'Internal server error'}), 500


# Favorileri Getirme
@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    try:
        username = request.args.get('username')

        if not username:
            return jsonify({'error': 'Missing username'}), 400

        # Kullanıcıyı veritabanından al
        user = get_user(username)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Favorileri al
        favorites_ref = db.collection('users').document(username).collection('favorites')
        favorites = [doc.to_dict() for doc in favorites_ref.stream()]

        return jsonify({'favorites': favorites}), 200
    except Exception as e:
        logging.error(f"Error in get_favorites: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    

# Steam fiyatlarını işleyen fonksiyon
def process_steam_price(price_str):
    """Steam fiyatlarını işlemek için özel fonksiyon"""
    try:
        if not price_str or price_str.lower() in ['free', 'ücretsiz', 'free to play']:
            return 0
        
        # Fiyat string'ini temizle
        price = price_str.replace('₺', '').replace('$', '').replace('TL', '').replace(',', '.').strip()
        
        # Eğer fiyat "xxx.xx" formatında ise
        if price.replace('.', '').isdigit():
            return float(price)
        
        # Eğer fiyat kuruş cinsinden bir sayı ise
        if price.isdigit():
            return float(price) / 100  # Kuruşu TL'ye çevir
            
        return 0
    except Exception as e:
        logging.error(f"Error processing price: {price_str}, {e}")
        return 0

def format_price(price, platform=''):
    """Fiyatı formatlamak için özel fonksiyon"""
    if price == 0:
        return 'Ücretsiz'
    if platform.lower() == 'steam':
        return f'₺{price:.2f}'
    return f'₺{price:.2f}'

def load_game_data():
    try:
        # Steam verileri
        steam_games_dict = {}
        
        # Steam verilerini steam_full_data.json'dan al
        with open('data/steam_full_data.json', 'r', encoding='utf-8') as f:
            steam_data = json.load(f)
            for game in steam_data:
                app_id = str(game.get('appid', ''))
                if app_id:
                    try:
                        # Ham fiyat verisini al
                        raw_price = game.get('price', '')
                        price = 0
                        price_formatted = 'Free'
                        
                        # Ücretsiz oyunları ve demo'ları kontrol et
                        free_indicators = ['free to play', 'free', 'demo', 'prologue']
                        if raw_price and not any(indicator in raw_price.lower() for indicator in free_indicators):
                            try:
                                # Fiyat string'ini temizle
                                clean_price = raw_price.replace('$', '').replace(' USD', '').strip()
                                if clean_price:
                                    price = float(clean_price)
                                    price_formatted = f"${price:.2f}"
                            except Exception as e:
                                logging.debug(f"Price conversion failed for {game.get('name')}: {raw_price}")
                                price = 0
                                price_formatted = 'Free'
                        
                        steam_games_dict[app_id] = {
                            'platform': 'Steam',
                            'name': game.get('name', ''),
                            'price': price,
                            'price_formatted': price_formatted,
                            'discount': game.get('discount'),
                            'appid': app_id
                        }
                        
                    except Exception as e:
                        logging.error(f"Error processing Steam game {app_id}: {e}")
                        continue

        # Dictionary'yi listeye çevir
        processed_steam_games = list(steam_games_dict.values())

        # Debug için
        if processed_steam_games:
            logging.info(f"Total processed Steam games: {len(processed_steam_games)}")
            logging.info("Sample processed games:")
            for game in processed_steam_games[:3]:
                logging.info(f"{game['name']}: {game['price_formatted']}")

        # Epic verileri
        processed_epic_games = []
        try:
            with open('data/epic_data.json', 'r', encoding='utf-8') as f:
                epic_data = json.load(f)
                for game in epic_data:
                    try:
                        price = game.get('price', '0')
                        if isinstance(price, str):
                            if price == 'Ücretsiz':
                                price = 0
                            else:
                                try:
                                    price = float(price.replace('₺', '').replace(',', '.').strip())
                                except:
                                    price = 0
                        
                        processed_epic_games.append({
                            'platform': 'Epic',
                            'name': game.get('name', ''),
                            'price': price,
                            'price_formatted': format_price(price, 'Epic'),
                            'discount': game.get('discount'),
                        })
                    except Exception as e:
                        logging.error(f"Error processing Epic game: {e}")
                        continue
        except Exception as e:
            logging.error(f"Error loading Epic data: {e}")

        # GOG verileri
        processed_gog_games = []
        try:
            with open('data/gog_data.json', 'r', encoding='utf-8') as f:
                gog_data = json.load(f)
                for game in gog_data:
                    try:
                        price = game.get('price', '0')
                        if isinstance(price, str):
                            if price == 'Free':
                                price = 0
                            else:
                                try:
                                    price = float(price.replace('$', '').strip())
                                except:
                                    price = 0
                        
                        processed_gog_games.append({
                            'platform': 'GOG',
                            'name': game.get('name', ''),
                            'price': price,
                            'price_formatted': format_price(price, 'GOG'),
                            'discount': game.get('discount'),
                        })
                    except Exception as e:
                        logging.error(f"Error processing GOG game: {e}")
                        continue
        except Exception as e:
            logging.error(f"Error loading GOG data: {e}")

        # Debug logları
        logging.info(f"Processed games count - Steam: {len(processed_steam_games)}, "
                    f"Epic: {len(processed_epic_games)}, GOG: {len(processed_gog_games)}")

        return processed_steam_games, processed_epic_games, processed_gog_games

    except Exception as e:
        logging.error(f"Error loading game data: {e}")
        logging.exception("Full error trace:")
        return [], [], []



# Oyun verilerini yükle

steam_games, epic_games, gog_games = load_game_data()



@app.route('/api/games', methods=['GET'])
def get_games():
    try:
        platform = request.args.get('platform', 'all').lower()
        search = request.args.get('search', '').lower()
        min_price = float(request.args.get('min_price', 0))
        max_price = float(request.args.get('max_price', float('inf')))
        
        # Platform seçimi
        if platform == 'steam':
            games = steam_games
        elif platform == 'epic':
            games = epic_games
        elif platform == 'gog':
            games = gog_games
        else:
            games = steam_games + epic_games + gog_games

        # Filtreleme
        filtered_games = []
        for game in games:
            try:
                # Fiyat kontrolü
                price = game.get('price', 0)
                if isinstance(price, (int, float)):
                    price = float(price)
                
                if not (min_price <= price <= max_price):
                    continue

                # İsim araması
                name = str(game.get('name', '')).lower()
                if search and search not in name:
                    continue

                # Oyun verisini standartlaştır
                processed_game = {
                    'name': game.get('name', ''),
                    'price': price,
                    'price_formatted': game.get('price_formatted', f'₺{price:.2f}' if price > 0 else 'Ücretsiz'),
                    'platform': game.get('platform', ''),
                    'discount': game.get('discount'),
                    'appid': game.get('appid', '')
                }

                filtered_games.append(processed_game)

            except Exception as e:
                logging.error(f"Error processing game: {e}")
                continue

        # Debug için
        if filtered_games:
            logging.info(f"Sample filtered game: {json.dumps(filtered_games[0], indent=2)}")

        return jsonify({
            'total': len(filtered_games),
            'games': filtered_games
        })

    except Exception as e:
        logging.error(f"Error in get_games: {e}")
        logging.exception("Full error trace:")
        return jsonify({'error': str(e)}), 500


#İstatistikler
@app.route('/api/games/stats', methods=['GET'])
def get_stats():
    try:
        # Fiyat karşılaştırması için yardımcı fonksiyon
        def get_price(game):
            price = game.get('price', 0)
            if isinstance(price, str):
                if price == 'Ücretsiz' or price == 'Free' or not price:
                    return 0
                try:
                    # Fiyat string'ini temizle ve float'a çevir
                    price = price.replace('₺', '').replace('TL', '').replace('$', '').replace(',', '.').strip()
                    return float(price)
                except:
                    return 0
            return float(price) if price else 0

        # Tüm oyunları birleştir
        all_games = steam_games + epic_games + gog_games

        # İstatistikleri hesapla
        stats = {
            'total_games': len(all_games),
            'platforms': {
                'steam': len(steam_games),
                'epic': len(epic_games),
                'gog': len(gog_games)
            },
            'free_games': len([g for g in all_games if get_price(g) == 0]),
            'price_ranges': {
                'under_10': len([g for g in all_games if 0 < get_price(g) <= 10]),
                '10_to_30': len([g for g in all_games if 10 < get_price(g) <= 30]),
                'over_30': len([g for g in all_games if get_price(g) > 30])
            }
        }

        # Debug için
        logging.info(f"Stats calculated: {json.dumps(stats, indent=2)}")

        return jsonify(stats)

    except Exception as e:
        logging.error(f"Error in get_stats: {e}")
        logging.exception("Full error trace:")  # Tam hata izini logla
        return jsonify({'error': str(e)}), 500



@app.route('/api/games/search', methods=['GET'])
def search_games():

    try:

        query = request.args.get('q', '').lower()
        platform = request.args.get('platform', 'all').lower()


        # Platform seçimi

        if platform == 'steam':
            games = steam_games
        elif platform == 'epic':
            games = epic_games
        elif platform == 'gog':
            games = gog_games
        else:
            games = steam_games + epic_games + gog_games



        # Arama

        if query:
            results = []
            for game in games:
                name = game.get('name', '').lower() or game.get('title', '').lower()
                if query in name:
                    results.append(game)

        else:

            results = games



        return jsonify({
            'total': len(results),
            'results': results

        })



    except Exception as e:
        logging.error(f"Error in search_games: {e}")
        return jsonify({'error': str(e)}), 500

# Oyun fiyatlarını karşılaştır
@app.route('/api/games/compare/<game_name>', methods=['GET'])
def compare_game_prices(game_name):
    try:
        game_name = game_name.lower()
        comparison = {
            'name': game_name,
            'prices': {
                'steam': None,
                'epic': None,
                'gog': None
            }
        }

        # Steam'de ara
        steam_game = next(
            (game for game in steam_games 
             if game_name in game.get('name', '').lower()),
            None
        )
        if steam_game:
            comparison['prices']['steam'] = {
                'price': steam_game.get('price', 0),
                'price_formatted': steam_game.get('price_formatted', 'Fiyat bilgisi yok'),
                'discount': steam_game.get('discount', None)
            }

        # Epic'te ara
        epic_game = next(
            (game for game in epic_games 
             if game_name in game.get('name', '').lower()),
            None
        )
        if epic_game:
            price = epic_game.get('price', 0)
            comparison['prices']['epic'] = {
                'price': price,
                'price_formatted': f'₺{price:.2f}' if price > 0 else 'Ücretsiz',
                'discount': epic_game.get('discount', None)
            }

        # GOG'da ara
        gog_game = next(
            (game for game in gog_games 
             if game_name in game.get('name', '').lower()),
            None
        )
        if gog_game:
            price = gog_game.get('price', 0)
            comparison['prices']['gog'] = {
                'price': price,
                'price_formatted': f'₺{price:.2f}' if price > 0 else 'Ücretsiz',
                'discount': gog_game.get('discount', None)
            }

        # Debug için
        logging.info(f"Comparison result: {json.dumps(comparison, indent=2)}")

        # En az bir platformda bulunduysa sonuçları döndür
        if any(comparison['prices'].values()):
            return jsonify(comparison)
        else:
            return jsonify({'error': 'Game not found in any platform'}), 404

    except Exception as e:
        logging.error(f"Error in compare_game_prices: {e}")
        return jsonify({'error': str(e)}), 500

# Favorilerden kaldır
@app.route('/api/favorites/<game_id>', methods=['DELETE'])
def remove_from_favorites(game_id):
    try:
        # Token doğrulama
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')

        if not username:
            return jsonify({'error': 'Invalid token'}), 401

        # Favoriyi bul ve sil
        favorites_ref = db.collection('users').document(username).collection('favorites')
        favorites = favorites_ref.where('id', '==', game_id).get()
        
        for favorite in favorites:
            favorite.reference.delete()

        return jsonify({'message': 'Game removed from favorites successfully!'}), 200

    except Exception as e:
        logging.error(f"Error in remove_from_favorites: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)


