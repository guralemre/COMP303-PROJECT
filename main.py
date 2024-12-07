from flask import Flask, jsonify, request
from flask_cors import CORS

#react ile flask arasındaki bağlantı
app = Flask(__name__)
CORS(app)  # React ile Flask arasında CORS sorunu yaşamamak için

@app.route('/api/hello', methods=['GET'])
def hello_world():
    return jsonify(message="Connected from flask!")

if __name__ == '__main__':
    app.run(debug=True)



