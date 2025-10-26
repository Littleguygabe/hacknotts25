import './App.css';
import { Header } from './components/Header/header';
import { TickerProvider } from './context/TickerContext.tsx';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Discovery from './pages/Discovery';
import Stock from './pages/Stock';
import { Footer } from './components/Footer/footer';

function App() {
  return (
    <Router>
      <TickerProvider>
        <Header />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/discovery" element={<Discovery />} />
          <Route path="/stock/:ticker" element={<Stock />} />
        </Routes>
        <Footer />
      </TickerProvider>
    </Router>
  );
}

export default App;