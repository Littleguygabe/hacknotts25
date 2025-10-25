import {
  Card,
  CardContent,
} from "@/components/ui/card"
import ScoreCircle from "./ScoreCircle";

interface PredictionCardProps {
  title: string;
  score: number;
  image: string;
  predictionAnalysis: string;
  color: string;
  ticker: string;
}

/**
 * A card component that displays a specific sentiment analysis 
 * (Analyst, Social, or Overall) for a given stock ticker.
 */
export function PredictionCard({ title, score, image, predictionAnalysis, color, }: PredictionCardProps) {
  return (
    <Card className="w-full max-w-xs flex-shrink-0">
      <CardContent className="grid gap-4 p-4">
        <div className="flex gap-2 items-center">
          {/* Left side: Image */}
          <img src={image} alt={title} className="w-32 h-32 object-contain rounded-md" />

          {/* Right side: Title and Score */}
          <div className="flex flex-col gap-2">
            <h3 className="text-lg font-semibold">{title}</h3>
            <ScoreCircle score={score} color={color} />
          </div>
        </div>

        {/* Bottom row: Analysis Text */}
        <p className="text-base text-muted-foreground">
          {predictionAnalysis}
        </p>
      </CardContent>
    </Card>
  )
}