"use client"
import React, { useState } from 'react';
import axios from 'axios';

function VoiceChatPage() {
  const [response, setResponse] = useState('');
  const [listening, setListening] = useState(false);
  const [conversationHistory, setConversationHistory] = useState([]);

  const handleToggleListening = async () => {
    setListening(current => !current);
    if (!listening) {
      try {
        const result = await axios.post('http://localhost:5001/speech_to_text');
        const message = result.data.message || "No response"; // Ensure there's always a message string.
        const newHistory = [...conversationHistory, { text: message }];
        setConversationHistory(newHistory);
        setResponse(message);
      } catch (error) {
        const newHistory = [...conversationHistory, { text: 'Error: Failed to fetch data' }];
        setConversationHistory(newHistory);
        setResponse('Error: Failed to fetch data');
        console.error('Error fetching data:', error);
      }
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
