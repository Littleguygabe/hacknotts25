import { NavigationMenuDemo } from './components/Header/header'
import analystImage from '@/assets/Gemini_Generated_Image_mzgdvomzgdvomzgd-removebg-preview.png'
import finScytheImage from '@/assets/Frame_2-removebg-preview.png'
import retailImage from '@/assets/Gemini_Generated_Image_edpypaedpypaedpy-removebg-preview.png'

import './App.css'
import { ChartAreaWithDateTime } from './components/StockChartPanel/StockChart'
import { useTicker } from './context/TickerContext'
import { PredictionShowdownContainer } from './components/PredictionShowdown/PredictionShowdownContainer'

function App() {
  const { selectedTicker } = useTicker();

  return (
    <>
      <NavigationMenuDemo />
      {/* Added max-w-7xl to main container for better desktop centering and width constraint */}
      <main className="mx-auto px-4 py-8 flex flex-col gap-8 max-w-7xl">
        <ChartAreaWithDateTime ticker={selectedTicker} />
        
        {/* Adjusted title alignment to the start of the container */}
        <div className="flex justify-center items-center">
          <p className="text-2xl font-bold">Predictions</p>
        </div>
        <PredictionShowdownContainer ticker={selectedTicker} />
      </main>
      <footer className="text-center py-4 text-sm text-muted-foreground">
        © 2025 FinScythe. All rights reserved.
      </footer>
    </>
  )
}

export default App;