import React from 'react';

const Home = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
      <h1 className="text-5xl font-bold mb-4">Welcome to FinScythe</h1>
      <p className="text-xl mb-8">Your ultimate tool for stock prediction showdowns.</p>
      <div className="flex space-x-4">
        <a href="/discovery" className="px-6 py-3 bg-blue-600 text-white rounded-lg shadow-md hover:bg-blue-700 transition duration-300">
          Explore Stocks
        </a>
        <a href="/about" className="px-6 py-3 border border-gray-300 dark:border-gray-700 rounded-lg shadow-md hover:bg-gray-200 dark:hover:bg-gray-800 transition duration-300">
          Learn More
        </a>
      </div>
    </div>
  );
};

export default Home;
