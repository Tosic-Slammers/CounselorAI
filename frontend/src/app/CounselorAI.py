from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import speech_recognition as sr
import requests
from dotenv import load_dotenv
import os
from model.mongoRAG import *
from pymongo import MongoClient
from langchain_openai import ChatOpenAI


# pip install elevenlabs
from typing import IO
from io import BytesIO
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

app = Flask(__name__)
CORS(app)  

# load environmental variables
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MONGO_URI = os.getenv('MONGO_URI')

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)

# Initialize the recognizer
r = sr.Recognizer()

# model initialization
print("initalize LLM")
llm = ChatOpenAI(model_name="ft:gpt-3.5-turbo-0125:personal:counselorai:9PBfTcd4", temperature=0.3)

'''
try:
    cluster = MongoClient(MONGO_URI)
    print("MongoDB connection established.")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
try:
    client = OpenAI()
    print("OpenAI API initialized.") 
except Exception as e:
    print(f"Failed to initialize OpenAI API: {e}")

'''
# llm prompt initialization
print("initalize prompt template")
custom_rag_prompt = rag_template()

# connect to mongodb
print("initalize mongo connection")
MONGODB_COLLECTION = conn_to_cluster(MONGO_URI)

# get vectorstore
print("initalize vectorstore")
vectorstore = get_vectorstore(MONGODB_COLLECTION)

print("model loaded\n")

@app.route('/counselorai', methods=['POST'])
def counselorai():
    text = request.json.get('text', '')
    llm_output = process(MONGODB_COLLECTION, vectorstore, text,llm)
    response = jsonify({"text": str(llm_output)})
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
            print("message: ", text)
            response = requests.post("http://127.0.0.1:5001/counselorai", json={"text": text})
            response = response.text
            conversation = {"You": text, "Therapist: ": response}
            return jsonify({"message": response})
        except Exception as e:
            return jsonify({"error": str(e)})

@app.route('/text_to_speech', methods=['POST'])
def text_to_speech_stream():
    print("Incoming request data:", request.get_json())
    request_data = request.get_json()

    if not request_data or 'text' not in request_data:
            return jsonify(error="Missing 'text' field in the JSON payload"), 400

    text = request_data.get('text', '')
    print(f"Received text: {text}")

    # Perform the text-to-speech conversion
    response = client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB", # Adam pre-made voice
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2",
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    # Create a BytesIO object to hold the audio data in memory
    audio_stream = BytesIO()

    # Write each chunk of audio data to the stream
    for chunk in response:
        if chunk:
            audio_stream.write(chunk)

    # Reset stream position to the beginning
    audio_stream.seek(0)

    # Return the stream for further use
    return send_file(audio_stream, mimetype='audio/mpeg', as_attachment=False, download_name="audio.mp3")

@app.route('/clear_store', methods=['POST'])
def clear_store_endpoint():
    clear_store()
    return jsonify({"status": "success", "message": "Chat history cleared"}), 200

if __name__ == '__main__':
    app.run(port=5001)
