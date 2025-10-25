import React, { createContext, useState, useContext, type ReactNode } from 'react';

interface TickerContextType {
  selectedTicker: string;
  setSelectedTicker: (ticker: string) => void;
}

const TickerContext = createContext<TickerContextType | undefined>(undefined);

export const TickerProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [selectedTicker, setSelectedTicker] = useState<string>('AAPL'); // Default to AAPL

  return (
    <TickerContext.Provider value={{ selectedTicker, setSelectedTicker }}>
      {children}
    </TickerContext.Provider>
  );
};

export const useTicker = () => {
  const context = useContext(TickerContext);
  if (context === undefined) {
    throw new Error('useTicker must be used within a TickerProvider');
  }
  return context;
};