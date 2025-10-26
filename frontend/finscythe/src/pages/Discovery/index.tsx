import React from 'react';
import { Link } from 'react-router-dom';
import { Card, CardHeader, CardTitle } from '@/components/ui/card';
import { tickers } from '@/components/Header/SearchStock';

const Discovery = () => {
  return (
    <div className="flex flex-col items-center dark:text-gray-100 p-4">
      <div className="w-full">
        <h1 className="text-5xl font-bold mb-8 text-center">Discover Stocks</h1>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 px-4">
          {tickers.map((ticker) => (
            <Link to={`/stock/${ticker.value}`} key={ticker.value}>
              <Card className="hover:shadow-lg transition-shadow duration-200 ease-in-out flex items-center justify-center h-48">
                <CardHeader className="flex justify-center items-center text-center">
                  <CardTitle className="text-4xl font-bold text-center text-wrap">{ticker.label}</CardTitle>
                </CardHeader>
              </Card>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Discovery;
