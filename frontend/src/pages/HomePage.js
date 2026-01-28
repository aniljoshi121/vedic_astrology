import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Moon, Sun, Languages } from 'lucide-react';
import { useTheme } from '../contexts/ThemeContext';
import { useLanguage } from '../contexts/LanguageContext';
import { Button } from '../components/ui/button';

const HomePage = () => {
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();
  const { language, toggleLanguage, t } = useLanguage();

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Background */}
      <div 
        className="fixed inset-0 z-0"
        style={{
          backgroundImage: theme === 'dark' 
            ? `url('https://images.unsplash.com/photo-1554842309-fef0d204097e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1NTJ8MHwxfHNlYXJjaHwxfHxteXN0aWNhbCUyMHN0YXJyeSUyMG5pZ2h0JTIwc2t5JTIwZGVlcCUyMGJsdWUlMjBwdXJwbGV8ZW58MHx8fHwxNzY5MzU3NTgxfDA&ixlib=rb-4.1.0&q=85')`
            : `url('https://images.unsplash.com/photo-1737276745714-72fe9d14b427?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2OTF8MHwxfHNlYXJjaHwxfHx2aW50YWdlJTIwcGFwZXIlMjB0ZXh0dXJlJTIwcGFyY2htZW50fGVufDB8fHx8MTc2OTM1NzU4NHww&ixlib=rb-4.1.0&q=85')`,
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        }}
      />
      
      {/* Overlay */}
      <div className="fixed inset-0 bg-background/80 backdrop-blur-sm z-0" />

      {/* Mandala decoration */}
      <div 
        className="fixed top-20 right-20 w-96 h-96 opacity-10 pointer-events-none animate-spin-slow"
        style={{
          backgroundImage: `url('https://images.unsplash.com/photo-1755541608519-3746dbfb11d6?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1NTZ8MHwxfHNlYXJjaHwxfHxnb2xkZW4lMjBtYW5kYWxhJTIwcGF0dGVybiUyMGRhcmslMjBiYWNrZ3JvdW5kfGVufDB8fHx8MTc2OTM1NzU3OXww&ixlib=rb-4.1.0&q=85')`,
          backgroundSize: 'contain',
          backgroundRepeat: 'no-repeat'
        }}
      />

      {/* Header */}
      <nav className="relative z-10 flex justify-between items-center p-6 max-w-7xl mx-auto">
        <div>
          <h1 className="font-cinzel text-3xl font-bold text-primary">Jyotish</h1>
        </div>
        <div className="flex gap-4 items-center">
          <Button
            data-testid="language-toggle-btn"
            variant="ghost"
            size="icon"
            onClick={toggleLanguage}
            className="hover:scale-110 transition-transform"
          >
            <Languages className="h-5 w-5" />
          </Button>
          <Button
            data-testid="theme-toggle-btn"
            variant="ghost"
            size="icon"
            onClick={toggleTheme}
            className="hover:scale-110 transition-transform"
          >
            {theme === 'dark' ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
          </Button>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="relative z-10 max-w-7xl mx-auto px-6 py-20">
        <div className="text-center space-y-8 animate-in fade-in slide-in-from-bottom-8 duration-700">
          <h1 className={`font-cinzel text-5xl md:text-7xl font-bold tracking-tight ${language === 'hi' ? 'font-hindi' : ''}`}>
            {t('welcome')}
          </h1>
          <p className={`text-xl md:text-2xl text-muted-foreground max-w-2xl mx-auto ${language === 'hi' ? 'font-hindi' : ''}`}>
            {t('subtitle')}
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-8">
            <Button
              data-testid="get-started-btn"
              onClick={() => navigate('/birth-chart')}
              className="bg-primary text-primary-foreground hover:bg-primary/90 shadow-lg rounded-full px-8 py-6 font-cinzel tracking-wider text-lg transition-all duration-300 hover:scale-105"
            >
              {t('getStarted')}
            </Button>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mt-20">
          {[
            { title: t('birthChart'), path: '/birth-chart' },
            { title: t('kundliMatching'), path: '/kundli-matching' },
            { title: t('dailyHoroscope'), path: '/daily-horoscope' },
            { title: t('aiChat'), path: '/ai-chat' }
          ].map((feature, idx) => (
            <button
              key={idx}
              data-testid={`feature-card-${idx}`}
              onClick={() => navigate(feature.path)}
              className="backdrop-blur-md bg-white/90 dark:bg-slate-800/90 border-2 border-primary/20 shadow-xl rounded-xl p-8 hover:border-primary hover:shadow-2xl transition-all duration-300 hover:scale-105 group"
            >
              <h3 className={`font-cinzel text-xl font-semibold text-gray-800 dark:text-gray-100 group-hover:text-primary transition-colors ${language === 'hi' ? 'font-hindi' : ''}`}>
                {feature.title}
              </h3>
            </button>
          ))}
        </div>

        {/* Disclaimer */}
        <p className={`text-center text-sm text-muted-foreground mt-16 ${language === 'hi' ? 'font-hindi' : ''}`}>
          {t('disclaimer')}
        </p>
      </main>
    </div>
  );
};

export default HomePage;
