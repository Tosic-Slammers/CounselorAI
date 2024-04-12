
export default function Home() {
  return (
      <div className="min-h-screen bg-gray-50 flex flex-col justify-center items-center px-6">
        <h1 className="text-5xl font-bold text-gray-800 mb-2">
          AI Therapist
        </h1>
        <p className="text-gray-600 text-lg mb-10">
          your personal ai mental health therapist accessible 24/7
        </p>
        <div className="flex space-x-6">
          <a
            href="/text-chat"
            className="bg-purple-600 text-white py-3 px-6 rounded-lg shadow-md hover:bg-purple-700 transition duration-300"
          >
            Text Chat
          </a>
          <a
            href="/voice-chat"
            className="bg-purple-600 text-white py-3 px-6 rounded-lg shadow-md hover:bg-purple-700 transition duration-300"
          >
            Voice Chat
          </a>
        </div>
      </div>
  );
};

