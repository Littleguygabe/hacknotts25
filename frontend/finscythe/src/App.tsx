import { NavigationMenuDemo } from './components/Header/header'
import StockTitle from './components/StockChartPanel/stock-title'
import { ButtonGroupDemo } from './components/StockChartPanel/stock-button-group'

import './App.css'

function App() {

  return (
    <>
      <NavigationMenuDemo />
      <div className="flex items-center justify-between mt-8">
        <StockTitle />
        <ButtonGroupDemo />
      </div>
    </>
  )
}

export default App
