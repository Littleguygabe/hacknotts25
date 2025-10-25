import { NavigationMenuDemo } from './components/Header/header'
import { ButtonGroupDemo } from './components/StockChartPanel/stock-button-group'
import { PredictionCard } from './components/PredictionShowdown/PredictionCard'
import analystImage from '@/assets/Gemini_Generated_Image_mzgdvomzgdvomzgd-removebg-preview.png'

import './App.css'
import { ChartAreaInteractive } from './components/StockChartPanel/Stock-Chart'

function App() {

  const analystCard = {
    title: "Analyst Prediction",
    score: 88,
    image: analystImage,
    predictionAnalysis: "Based on market trends and recent company performance, we predict a strong upward movement.",
    color: "#22c55e"
  }

  const communityCard = {
    title: "Community Prediction",
    score: 72,
    image: "https://placehold.co/600x400/E0E0E0/000000/png",
    predictionAnalysis: "The community sentiment is largely positive, with some concerns about upcoming regulations.",
    color: "#3b82f6"
  }

  return (
    <>
      <NavigationMenuDemo />
      <div className="flex items-center justify-between mt-8">
        <ButtonGroupDemo />
      </div>
      <div className="mt-8">
        <ChartAreaInteractive />
      </div>
      <div className="flex justify-center gap-8 mt-8">
        <PredictionCard {...analystCard} />
        <PredictionCard {...communityCard} />
      </div>
    </>
  )
}

export default App;
