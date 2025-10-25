import React from 'react';

interface ScoreCircleProps {
  score: number;
  color: string;
}

const ScoreCircle: React.FC<ScoreCircleProps> = ({ score, color }) => {
  const radius = 35;
  const circumference = 2 * Math.PI * radius;
  const scoreOffset = circumference * (1 - (score > 0 ? score / 100 : 0.1));

  return (
    <div className="relative flex items-center justify-center">
      <svg width="80" height="80" viewBox="0 0 80 80">
        <circle
          cx="40"
          cy="40"
          r={radius}
          stroke="#e5e7eb" // gray-200
          strokeWidth="8"
          fill="transparent"
        />
        <circle
          cx="40"
          cy="40"
          r={radius}
          stroke={color}
          strokeWidth="8"
          fill="transparent"
          strokeDasharray={circumference}
          strokeDashoffset={scoreOffset}
          strokeLinecap="round"
          transform="rotate(-90 40 40)"
        />
      </svg>
      <div className="absolute text-xl font-bold">{score}</div>
    </div>
  );
};

export default ScoreCircle;