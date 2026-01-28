import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { ArrowLeft, Heart, Loader2 } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { useLanguage } from '../contexts/LanguageContext';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const KundliMatchingPage = () => {
  const navigate = useNavigate();
  const { t, language } = useLanguage();
  const [loading, setLoading] = useState(false);
  const [matchingResult, setMatchingResult] = useState(null);
  const [cities, setCities] = useState([]);
  const [filteredCities1, setFilteredCities1] = useState([]);
  const [filteredCities2, setFilteredCities2] = useState([]);
  const [showCitySuggestions1, setShowCitySuggestions1] = useState(false);
  const [showCitySuggestions2, setShowCitySuggestions2] = useState(false);
  const [formData, setFormData] = useState({
    person1: {
      name: '',
      gender: 'Male',
      date_of_birth: '',
      time_of_birth: '',
      place_of_birth: ''
    },
    person2: {
      name: '',
      gender: 'Female',
      date_of_birth: '',
      time_of_birth: '',
      place_of_birth: ''
    }
  });

  useEffect(() => {
    // Fetch cities list
    const fetchCities = async () => {
      try {
        const response = await axios.get(`${API}/cities`);
        setCities(response.data.cities);
      } catch (error) {
        console.error('Failed to fetch cities:', error);
      }
    };
    fetchCities();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post(`${API}/kundli-matching`, formData);
      setMatchingResult(response.data.matching_result);
      toast.success('Kundli matching calculated successfully!');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to calculate matching');
    } finally {
      setLoading(false);
    }
  };

  const updatePerson = (person, field, value) => {
    setFormData(prev => ({
      ...prev,
      [person]: { ...prev[person], [field]: value }
    }));
  };

  const handlePlaceChange = (person, value) => {
    updatePerson(person, 'place_of_birth', value);
    
    if (value.length > 1) {
      const filtered = cities.filter(city => 
        city.toLowerCase().includes(value.toLowerCase())
      );
      
      if (person === 'person1') {
        setFilteredCities1(filtered.slice(0, 10));
        setShowCitySuggestions1(filtered.length > 0);
      } else {
        setFilteredCities2(filtered.slice(0, 10));
        setShowCitySuggestions2(filtered.length > 0);
      }
    } else {
      if (person === 'person1') {
        setShowCitySuggestions1(false);
      } else {
        setShowCitySuggestions2(false);
      }
    }
  };

  const selectCity = (person, city) => {
    updatePerson(person, 'place_of_birth', city);
    if (person === 'person1') {
      setShowCitySuggestions1(false);
    } else {
      setShowCitySuggestions2(false);
    }
  };

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-7xl mx-auto">
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
            {t('kundliMatching')}
          </h1>
          <div className="w-20" />
        </div>

        {!matchingResult ? (
          /* Input Form */
          <form onSubmit={handleSubmit} className="space-y-8">
            <div className="grid md:grid-cols-2 gap-8">
              {/* Person 1 */}
              <Card>
                <CardHeader>
                  <CardTitle className={`font-cinzel ${language === 'hi' ? 'font-hindi' : ''}`}>
                    {t('person1')}
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label>{t('name')}</Label>
                    <Input
                      data-testid="person1-name"
                      value={formData.person1.name}
                      onChange={(e) => updatePerson('person1', 'name', e.target.value)}
                      required
                    />
                  </div>
                  <div>
                    <Label>{t('gender')}</Label>
                    <Select
                      value={formData.person1.gender}
                      onValueChange={(value) => updatePerson('person1', 'gender', value)}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Male">{t('male')}</SelectItem>
                        <SelectItem value="Female">{t('female')}</SelectItem>
                        <SelectItem value="Other">{t('other')}</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label>{t('dateOfBirth')} (DD-MM-YYYY)</Label>
                    <Input
                      placeholder="15-08-1990"
                      value={formData.person1.date_of_birth}
                      onChange={(e) => updatePerson('person1', 'date_of_birth', e.target.value)}
                      required
                    />
                  </div>
                  <div>
                    <Label>{t('timeOfBirth')} (HH:MM)</Label>
                    <Input
                      placeholder="14:30"
                      value={formData.person1.time_of_birth}
                      onChange={(e) => updatePerson('person1', 'time_of_birth', e.target.value)}
                      required
                    />
                  </div>
                  <div className="relative">
                    <Label>{t('placeOfBirth')}</Label>
                    <Input
                      placeholder="Mumbai, Delhi, Bangalore..."
                      value={formData.person1.place_of_birth}
                      onChange={(e) => handlePlaceChange('person1', e.target.value)}
                      onFocus={() => {
                        if (formData.person1.place_of_birth.length > 1) {
                          setShowCitySuggestions1(true);
                        }
                      }}
                      onBlur={() => {
                        setTimeout(() => setShowCitySuggestions1(false), 200);
                      }}
                      required
                    />
                    {showCitySuggestions1 && filteredCities1.length > 0 && (
                      <div className="absolute z-10 w-full mt-1 bg-card border border-border rounded-lg shadow-lg max-h-60 overflow-y-auto">
                        {filteredCities1.map((city, idx) => (
                          <button
                            key={idx}
                            type="button"
                            onClick={() => selectCity('person1', city)}
                            className="w-full text-left px-4 py-2 hover:bg-muted transition-colors"
                          >
                            {city}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>

              {/* Person 2 */}
              <Card>
                <CardHeader>
                  <CardTitle className={`font-cinzel ${language === 'hi' ? 'font-hindi' : ''}`}>
                    {t('person2')}
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label>{t('name')}</Label>
                    <Input
                      data-testid="person2-name"
                      value={formData.person2.name}
                      onChange={(e) => updatePerson('person2', 'name', e.target.value)}
                      required
                    />
                  </div>
                  <div>
                    <Label>{t('gender')}</Label>
                    <Select
                      value={formData.person2.gender}
                      onValueChange={(value) => updatePerson('person2', 'gender', value)}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Male">{t('male')}</SelectItem>
                        <SelectItem value="Female">{t('female')}</SelectItem>
                        <SelectItem value="Other">{t('other')}</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label>{t('dateOfBirth')} (DD-MM-YYYY)</Label>
                    <Input
                      placeholder="20-05-1992"
                      value={formData.person2.date_of_birth}
                      onChange={(e) => updatePerson('person2', 'date_of_birth', e.target.value)}
                      required
                    />
                  </div>
                  <div>
                    <Label>{t('timeOfBirth')} (HH:MM)</Label>
                    <Input
                      placeholder="10:00"
                      value={formData.person2.time_of_birth}
                      onChange={(e) => updatePerson('person2', 'time_of_birth', e.target.value)}
                      required
                    />
                  </div>
                  <div className="relative">
                    <Label>{t('placeOfBirth')}</Label>
                    <Input
                      placeholder="Mumbai, Delhi, Bangalore..."
                      value={formData.person2.place_of_birth}
                      onChange={(e) => handlePlaceChange('person2', e.target.value)}
                      onFocus={() => {
                        if (formData.person2.place_of_birth.length > 1) {
                          setShowCitySuggestions2(true);
                        }
                      }}
                      onBlur={() => {
                        setTimeout(() => setShowCitySuggestions2(false), 200);
                      }}
                      required
                    />
                    {showCitySuggestions2 && filteredCities2.length > 0 && (
                      <div className="absolute z-10 w-full mt-1 bg-card border border-border rounded-lg shadow-lg max-h-60 overflow-y-auto">
                        {filteredCities2.map((city, idx) => (
                          <button
                            key={idx}
                            type="button"
                            onClick={() => selectCity('person2', city)}
                            className="w-full text-left px-4 py-2 hover:bg-muted transition-colors"
                          >
                            {city}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            </div>

            <Button
              data-testid="calculate-matching-btn"
              type="submit"
              disabled={loading}
              className="w-full max-w-md mx-auto flex bg-primary hover:bg-primary/90 font-cinzel"
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Calculating...
                </>
              ) : (
                <>
                  <Heart className="mr-2 h-4 w-4" />
                  {t('calculate')} {t('gunMilan')}
                </>
              )}
            </Button>
          </form>
        ) : (
          /* Results */
          <div className="space-y-6" data-testid="matching-results">
            <Button
              variant="outline"
              onClick={() => setMatchingResult(null)}
            >
              New Matching
            </Button>

            {/* Score Card */}
            <Card className="bg-gradient-to-br from-primary/10 to-secondary/10">
              <CardContent className="pt-8 text-center">
                <div className="text-6xl font-bold text-primary mb-4">
                  {matchingResult.total_score} / 36
                </div>
                <div className="text-2xl font-cinzel mb-2">
                  {language === 'hi' ? matchingResult.verdict_hindi : matchingResult.verdict}
                </div>
                <div className="text-muted-foreground">
                  {matchingResult.percentage}% {t('compatibility')}
                </div>
              </CardContent>
            </Card>

            {/* Kootas */}
            <Card>
              <CardHeader>
                <CardTitle className="font-cinzel">Ashta-Koota Analysis</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {matchingResult.kootas.map((koota, idx) => (
                    <div key={idx} className="flex items-center justify-between p-4 rounded-lg border">
                      <div>
                        <div className="font-semibold">
                          {language === 'hi' ? koota.name_hindi : koota.name}
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="font-bold text-lg">
                          {koota.obtained_score} / {koota.max_score}
                        </div>
                        <div className={koota.compatible ? 'text-green-600' : 'text-red-600'}>
                          {koota.compatible ? '✓ Compatible' : '✗ Incompatible'}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Doshas */}
            {matchingResult.doshas && matchingResult.doshas.length > 0 && (
              <Card className="border-destructive">
                <CardHeader>
                  <CardTitle className="font-cinzel text-destructive">Doshas Detected</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {matchingResult.doshas.map((dosha, idx) => (
                      <li key={idx} className="text-destructive">
                        • {language === 'hi' ? dosha.name_hindi : dosha.name}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default KundliMatchingPage;
