from flask import Flask, jsonify, request
from flask_cors import CORS
import speech_recognition as sr

app = Flask(__name__)
CORS(app)  

@app.route('/speech_to_text', methods=['POST'])
def speech_to_text():
    # Initialize the recognizer
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Calibrating for background noise. Please wait...")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Please speak into the microphone.")
        # Starts listening
        audio = r.listen(source, timeout=10)
        # Finishes listening
        try:
            text = r.recognize_google(audio)
            return jsonify({"message": "You: " + text})
        except Exception as e:
            return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
