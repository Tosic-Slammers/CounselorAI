"use client"
import React, { useState } from 'react';

export default function TextChat() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');

  const handleSendClick = () => {
    if (inputValue.trim() !== '') {
      setMessages([...messages, { text: inputValue, sender: 'user' }]);
      setInputValue('');
    }
  };

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleSendClick();
    }
  };

  return (
      <div className="min-h-screen bg-gray-50 flex flex-col justify-center " >
        <h1 className="text-5xl font-bold text-gray-800 mb-6 mt-10">
           Type to chat with your AI therapist
        </h1>
        <div className="bg-white shadow-lg overflow-hidden rounded-lg mb-6 border-purple-600 border- ">
          <div className="px-4 py-5 sm:p-6 space-y-4">
            {messages.map((message, index) => (
              <div key={index} className={`text-gray-800 text-lg ${message.sender === 'user' ? 'text-right' : ''}`}>
                {message.text}
              </div>
            ))}
          </div>
          <div className="px-4 py-3 bg-gray-50 text-right sm:px-6">
            <textarea
              className="shadow-sm text-black focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-lg border-gray-300 rounded-md h-24 p-4"
              placeholder="Type your message here..."
              value={inputValue}
              onChange={handleInputChange}
              onKeyPress={handleKeyPress}
            />
            <button
              type="button"
              className="inline-flex items-center px-6 py-3 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 mt-4"
              onClick={handleSendClick}
            >
              Send
            </button>
          </div>
        </div>
      </div>
  );
}
