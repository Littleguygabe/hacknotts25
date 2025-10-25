import { ArrowUp, ArrowDown } from 'lucide-react';

interface PercentageChangeProps {
  percentageChange: number | null;
}

export function PercentageChange({ percentageChange }: PercentageChangeProps) {
  if (percentageChange === null) {
    return null;
  }

  return (
    <div className={`flex items-center gap-1 ${percentageChange >= 0 ? 'text-green-500' : 'text-red-500'}`}>
      {percentageChange >= 0 ? <ArrowUp size={16} /> : <ArrowDown size={16} />}
      <span>{Math.abs(percentageChange).toFixed(2)}%</span>
    </div>
  );
}