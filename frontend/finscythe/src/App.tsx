import { NavigationMenuDemo } from './components/Header/header'
import { ItemSummary } from './components/PredictionShowdown/SummaryPrediction'
import { PredictionCard } from './components/PredictionShowdown/PredictionCard'
import analystImage from '@/assets/Gemini_Generated_Image_mzgdvomzgdvomzgd-removebg-preview.png'

import retailImage from '@/assets/Frame_1-removebg-preview.png'

import './App.css'
import { ChartAreaWithDateTime } from './components/StockChartPanel/StockChart'
import { ItemFinScythe } from './components/PredictionShowdown/FinScythePrediction'

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
    image: retailImage,
    predictionAnalysis: "The community sentiment is largely positive, with some concerns about upcoming regulations.",
    color: "#3b82f6"
  }

  return (
    <>
      <NavigationMenuDemo />
      <main className="container mx-auto px-4 py-8 flex flex-col gap-8">
        <ChartAreaWithDateTime />
        <ItemSummary />
        <div className="flex justify-center gap-8">
          <PredictionCard {...analystCard} />
          <PredictionCard {...communityCard} />
        </div>
        <ItemFinScythe />
      </main>
    </>
  )
}

export default App;
