import React from 'react';

interface ScoreCircleProps {
  score: number;
  color: string;
}

const ScoreCircle: React.FC<ScoreCircleProps> = ({ score, color }) => {
  const radius = 50;
  const circumference = 2 * Math.PI * radius;
  const scoreOffset = circumference * (1 - (score > 0 ? score / 100 : 0.1));

  return (
    <div className="relative flex items-center justify-center">
      <svg width="120" height="120" viewBox="0 0 120 120">
        <circle
          cx="60"
          cy="60"
          r={radius}
          stroke="#e5e7eb" // gray-200
          strokeWidth="10"
          fill="transparent"
        />
        <circle
          cx="60"
          cy="60"
          r={radius}
          stroke={color}
          strokeWidth="10"
          fill="transparent"
          strokeDasharray={circumference}
          strokeDashoffset={scoreOffset}
          strokeLinecap="round"
          transform="rotate(-90 60 60)"
        />
      </svg>
      <div className="absolute text-2xl font-bold">{score}</div>
    </div>
  );
};

export default ScoreCircle;
