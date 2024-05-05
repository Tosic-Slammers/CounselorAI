from flask import Flask, jsonify, request
from flask_cors import CORS
import speech_recognition as sr
import requests

app = Flask(__name__)
CORS(app)  


# Initialize the recognizer
r = sr.Recognizer()

@app.route('/counselorai', methods=['POST'])
def counselorai():
    text = request.json.get('text', '')
    print("message: ", text)
    response = jsonify({"text": "Therapist: " + text + " working"})
    return response

@app.route('/speech_to_text', methods=['POST','GET'])
def speech_to_text():
    with sr.Microphone() as source:
        print("Calibrating for background noise. Please wait...")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Please speak into the microphone.")
        # Starts listening
        audio = r.listen(source)
        # Finishes listening
        print("Processing audio...")
        try:
            text = r.recognize_google(audio)
            response = requests.post("http://127.0.0.1:5001/counselorai", json={"text": text})
            return jsonify({"message": "You: " + response.text})
        except Exception as e:
            return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(port=5001)
