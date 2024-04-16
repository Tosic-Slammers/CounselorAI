"use client"
import React, { useState } from 'react';
import axios from 'axios';

function VoiceChatPage() {
  const [response, setResponse] = useState('');

  const handleSpeechToText = async () => {
    try {
      const result = await axios.post('http://localhost:5000/speech_to_text');
      setResponse(result.data.message);
    } catch (error) {
      setResponse('Failed to fetch data');
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div>
      <h1>Speech to Text Service</h1>
      <button onClick={handleSpeechToText}>Start Listening</button>
      <p>{response}</p>
    </div>
  );
}

export default VoiceChatPage;
