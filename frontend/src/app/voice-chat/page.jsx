"use client"
import React, { useState } from 'react';
import axios from 'axios';

function VoiceChatPage() {
  const [response, setResponse] = useState('');
  const [listening, setListening] = useState(false);
  const [conversationHistory, setConversationHistory] = useState([]);
  const [audioURL, setAudioURL] = useState(null);

  const handleToggleListening = async () => {
    setListening(current => !current);
    if (!listening) {
      try {
        const result = await axios.post('http://localhost:5001/speech_to_text');
        let message = result.data.message || "No response"; // Ensure there's always a message string.
        if (message !== "No response"){
          message = JSON.parse(result.data.message).text;
        }
        console.log(message)
        const newHistory = [...conversationHistory, { text: message }];
        setConversationHistory(newHistory);
        setResponse(message);

        await fetchAudio(message);
      } catch (error) {
        const newHistory = [...conversationHistory, { text: 'Error: Failed to fetch data' }];
        setConversationHistory(newHistory);
        setResponse('Error: Failed to fetch data');
        console.error('Error fetching data:', error);
      }
    }
  };

  //TTS
  const fetchAudio = async (text) => {
    try {
        console.log('Sending text-to-speech request...');
        const tts = await fetch('http://localhost:5001/text_to_speech', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text }),
        });
        if (!tts.ok) {
            console.error('TTS request failed', tts.status, tts.statusText);
            return;
        }
        const audioBlob = await tts.blob();
        const newUrl = URL.createObjectURL(audioBlob);
        if (audioURL) {
            URL.revokeObjectURL(audioURL);
        }
        setAudioURL(null);
        setTimeout(() => {
            setAudioURL(newUrl);
        }, 0);
        console.log('New Audio URL:', newUrl);
    } catch (error) {
        console.error('Error fetching audio:', error);
    }
  };


  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <style>
        {`
          @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.2); opacity: 0.8; }
          }
        `}
      </style>
      <div className="flex flex-col items-center">
        <h1 className="text-4xl font-semibold text-gray-700 mb-4">CounselorAI</h1>
        <h2 className="text-2xl text-gray-600">Click the icon to start chatting</h2>
        <button
          onClick={handleToggleListening}
          className={`mt-8 w-32 h-32 rounded-full bg-purple-600 transition duration-300 ease-in-out focus:outline-none
                      ${listening ? 'animate-pulse bg-purple-700' : ''}`}
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
        >
          <div
            className={`${listening ? 'bg-purple-300' : 'bg-purple-200'} w-3/4 h-3/4 rounded-full`}
          ></div>
        </button>
        {audioURL && (
                <audio key={audioURL} controls className="mt-4">
                    <source src={audioURL} type="audio/mpeg" />
                    Your browser does not support the audio element.
                </audio>
            )}
        <div className="mt-6 bg-gray-200 p-6 w-full max-w-xl h-64 overflow-auto text-gray-700 text-lg">
          {conversationHistory.map((entry, index) => (
            <p key={index} className={`text-left ${entry.text && entry.text.startsWith("Error:") ? 'text-red-600' : 'text-blue-600'}`}>
              {entry.text}
            </p>
          ))}
        </div>
      </div>
    </div>
  );
}

export default VoiceChatPage;
