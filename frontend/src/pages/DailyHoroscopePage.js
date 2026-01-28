import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { ArrowLeft } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { useLanguage } from '../contexts/LanguageContext';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const RASHIS = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
];

const DailyHoroscopePage = () => {
  const navigate = useNavigate();
  const { t, language } = useLanguage();
  const [selectedRashi, setSelectedRashi] = useState('Aries');
  const [horoscope, setHoroscope] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (selectedRashi) {
      fetchHoroscope();
    }
  }, [selectedRashi]);

  const fetchHoroscope = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/daily-horoscope/${selectedRashi}`);
      setHoroscope(response.data);
    } catch (error) {
      toast.error('Failed to fetch horoscope');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <Button
            data-testid="back-button"
            variant="ghost"
            onClick={() => navigate('/')}
            className="gap-2"
          >
            <ArrowLeft className="h-4 w-4" />
            {t('home')}
          </Button>
          <h1 className={`font-cinzel text-3xl md:text-4xl font-bold ${language === 'hi' ? 'font-hindi' : ''}`}>
            {t('dailyHoroscope')}
          </h1>
          <div className="w-20" />
        </div>

        {/* Rashi Selector */}
        <Card className="mb-6">
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <label className="font-semibold">Select your zodiac sign:</label>
              <Select value={selectedRashi} onValueChange={setSelectedRashi}>
                <SelectTrigger data-testid="rashi-select" className="w-48">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {RASHIS.map(rashi => (
                    <SelectItem key={rashi} value={rashi}>{rashi}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* Horoscope Display */}
        {horoscope && !loading && (
          <div className="space-y-6" data-testid="horoscope-display">
            {/* Overall Info */}
            <Card className="bg-gradient-to-br from-primary/10 to-secondary/10">
              <CardContent className="pt-6 text-center">
                <div className="text-4xl font-cinzel font-bold text-primary mb-2">
                  {horoscope.rashi}
                </div>
                <div className="text-muted-foreground mb-4">{horoscope.date}</div>
                <div className="flex justify-center gap-8">
                  <div>
                    <div className="text-sm text-muted-foreground">Lucky Number</div>
                    <div className="text-2xl font-bold">{horoscope.lucky_number}</div>
                  </div>
                  <div>
                    <div className="text-sm text-muted-foreground">Lucky Color</div>
                    <div className="text-2xl font-bold">{horoscope.lucky_color}</div>
                  </div>
                  <div>
                    <div className="text-sm text-muted-foreground">Rating</div>
                    <div className="text-2xl font-bold">{horoscope.overall_rating}/10</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Career */}
            <Card>
              <CardHeader>
                <CardTitle className={`font-cinzel ${language === 'hi' ? 'font-hindi' : ''}`}>
                  {t('career')}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground leading-relaxed">{horoscope.career}</p>
              </CardContent>
            </Card>

            {/* Finance */}
            <Card>
              <CardHeader>
                <CardTitle className={`font-cinzel ${language === 'hi' ? 'font-hindi' : ''}`}>
                  {t('finance')}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground leading-relaxed">{horoscope.finance}</p>
              </CardContent>
            </Card>

            {/* Health */}
            <Card>
              <CardHeader>
                <CardTitle className={`font-cinzel ${language === 'hi' ? 'font-hindi' : ''}`}>
                  {t('health')}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground leading-relaxed">{horoscope.health}</p>
              </CardContent>
            </Card>

            {/* Relationships */}
            <Card>
              <CardHeader>
                <CardTitle className={`font-cinzel ${language === 'hi' ? 'font-hindi' : ''}`}>
                  {t('relationships')}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground leading-relaxed">{horoscope.relationships}</p>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
};

export default DailyHoroscopePage;
