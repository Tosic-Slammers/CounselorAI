from flask import Flask, jsonify, request
from flask_cors import CORS
import speech_recognition as sr

app = Flask(__name__)
CORS(app)  

@app.route('/counselorai', methods=['POST'])
def counselorai():
    text = request.json.get('text', '')
    return text + '\n This works!'

if __name__ == '__main__':
    app.run(port=5001)
