import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './contexts/ThemeContext';
import { LanguageProvider } from './contexts/LanguageContext';
import { Toaster } from './components/ui/sonner';
import HomePage from './pages/HomePage';
import BirthChartPage from './pages/BirthChartPage';
import KundliMatchingPage from './pages/KundliMatchingPage';
import DailyHoroscopePage from './pages/DailyHoroscopePage';
import AIChatPage from './pages/AIChatPage';
import '@/App.css';

function App() {
  return (
    <ThemeProvider>
      <LanguageProvider>
        <BrowserRouter>
          <div className="App">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/birth-chart" element={<BirthChartPage />} />
              <Route path="/kundli-matching" element={<KundliMatchingPage />} />
              <Route path="/daily-horoscope" element={<DailyHoroscopePage />} />
              <Route path="/ai-chat" element={<AIChatPage />} />
            </Routes>
            <Toaster position="top-center" richColors />
          </div>
        </BrowserRouter>
      </LanguageProvider>
    </ThemeProvider>
  );
}

export default App;
