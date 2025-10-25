import React, { useEffect, useState } from 'react';
import { PredictionCard } from './PredictionCard';
import analystImage from '@/assets/Gemini_Generated_Image_mzgdvomzgdvomzgd-removebg-preview.png';
import finScytheImage from '@/assets/Frame_2-removebg-preview.png';
import retailImage from '@/assets/Gemini_Generated_Image_edpypaedpypaedpy-removebg-preview.png';

interface HistoryItem {
    Datetime: string;
    Close: number;
}

interface SentimentResponse {
    ticker: string;
    analyst_score: number;
    analyst_summary: string; 
    social_score: number;
    social_summary: string;
    ticker_history: HistoryItem[]; 
}

interface PredictionShowdownContainerProps {
  ticker: string;
}

export function PredictionShowdownContainer({ ticker }: PredictionShowdownContainerProps) {
  const [sentimentData, setSentimentData] = useState<SentimentResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSentimentData = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`http://127.0.0.1:8000/sentiment/synthetic/${ticker}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data: SentimentResponse = await response.json();
        setSentimentData(data);
      } catch (e: any) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };

    if (ticker) {
      fetchSentimentData();
    }
  }, [ticker]);

  if (loading) {
    return <div>Loading predictions...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!sentimentData) {
    return <div>No prediction data available.</div>;
  }

  // Analyst Card Data
  const analystCard = {
    title: "Analyst",
    score: sentimentData.analyst_score,
    image: analystImage,
    predictionAnalysis: sentimentData.analyst_summary,
    color: "#3b82f6"
  }

  // Community Card Data
  const communityCard = {
    title: "Community",
    score: sentimentData.social_score,
    image: retailImage,
    predictionAnalysis: sentimentData.social_summary,
    color: "#FF6701"
  }

  // FinScythe Card Data (assuming it uses a combination or average)
  const finScytheScore = Math.round((sentimentData.analyst_score + sentimentData.social_score) / 2);
  const finScytheSummary = `Analyst View: ${sentimentData.analyst_summary} | Social View: ${sentimentData.social_summary}`;

  const finScytheCard = {
    title: "FinScythe",
    score: finScytheScore,
    image: finScytheImage,
    predictionAnalysis: finScytheSummary,
    color: "#22c55e"
  }

  return (
    <div className="flex justify-center items-start gap-4 flex-wrap lg:flex-nowrap lg:justify-center">
      <PredictionCard {...analystCard} ticker={ticker} />
      <PredictionCard {...communityCard} ticker={ticker} />
      <PredictionCard {...finScytheCard} ticker={ticker} />
    </div>
  );
}