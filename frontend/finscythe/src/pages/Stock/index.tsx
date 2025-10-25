import React from 'react';
import { useParams } from 'react-router-dom';
import { useTicker } from '@/context/TickerContext.tsx';
import { ChartAreaWithDateTime } from '@/components/StockChartPanel/StockChart';
import { PredictionShowdownContainer } from '@/components/PredictionShowdown/PredictionShowdownContainer';

const Stock = () => {
  const { ticker: paramTicker } = useParams<{ ticker: string }>();
  const { selectedTicker } = useTicker();

  const currentTicker = paramTicker || selectedTicker;

  if (!currentTicker) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen text-gray-900 dark:text-gray-100">
        <h1 className="text-5xl font-bold mb-4">No Stock Selected</h1>
        <p className="text-xl mb-8">Please select a stock to view details.</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen text-gray-900 dark:text-gray-100 p-4">
      <ChartAreaWithDateTime ticker={currentTicker} />
      <PredictionShowdownContainer ticker={currentTicker} />
    </div>
  );
};

export default Stock;
