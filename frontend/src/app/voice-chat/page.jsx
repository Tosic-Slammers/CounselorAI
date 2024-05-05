"use client"
import React, { useState } from 'react';
import axios from 'axios';

function VoiceChatPage() {
  const [response, setResponse] = useState('');
  const [listening, setListening] = useState(false);

  const handleToggleListening = async () => {
    if (!listening) {
      setListening(true);
      try {
        const result = await axios.post('http://localhost:5001/speech_to_text');
        setResponse(result.data.message);
      } catch (error) {
        setResponse('Error: Failed to fetch data');
        console.error('Error fetching data:', error);
      }
    } else {
      setListening(false); // This will stop listening
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 ">
      <style>
        {`
          @keyframes pulse {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.3); opacity: 0.7; }
            100% { transform: scale(1); opacity: 1; }
          }
        `}
      </style>
      <div className="text-center">
        <h1 className="text-4xl font-semibold text-gray-700">AI Therapist</h1>
        <h2 className="text-2xl text-gray-600 mt-4 mb-8">Start chatting</h2>
        <button
          onClick={handleToggleListening}
          className={`justify-center ml-10 mt-4 w-32 h-32 rounded-full transition duration-300 ease-in-out focus:outline-none
                      ${listening ? 'bg-purple-700 animate-pulse' : 'bg-purple-600'}`}
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
        <p className="mt-6 text-base text-gray-700">{response}</p>
      </div>
    </div>
  );
}

export default VoiceChatPage;
