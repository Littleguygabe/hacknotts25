import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import ScoreCircle from "./ScoreCircle";

interface PredictionCardProps {
  title: string;
  score: number;
  image: string;
  predictionAnalysis: string;
  color: string;
}

export function PredictionCard({ title, score, image, predictionAnalysis, color }: PredictionCardProps) {
  return (
    <Card className="w-full max-w-sm">
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent className="grid gap-4">
        <div className="flex items-center justify-around gap-4">
          <img src={image} alt={title} className="w-48 h-48 object-contain rounded-md" />
          <ScoreCircle score={score} color={color} />
        </div>
        <p className="text-sm text-muted-foreground">
          {predictionAnalysis}
        </p>
      </CardContent>
    </Card>
  )
}
