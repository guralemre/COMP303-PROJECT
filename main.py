from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import auth, credentials, firestore
import jwt
from passlib.context import CryptContext
import logging

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

if __name__ == '__main__':
    app.run(debug=True)


