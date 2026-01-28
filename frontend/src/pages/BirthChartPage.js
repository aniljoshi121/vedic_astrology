import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { ArrowLeft, Download, Loader2 } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import NorthIndianChart from '../components/NorthIndianChart';
import { useLanguage } from '../contexts/LanguageContext';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const BirthChartPage = () => {
  const navigate = useNavigate();
  const { t, language } = useLanguage();
  const [loading, setLoading] = useState(false);
  const [chartData, setChartData] = useState(null);
  const [cities, setCities] = useState([]);
  const [filteredCities, setFilteredCities] = useState([]);
  const [showCitySuggestions, setShowCitySuggestions] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    gender: 'Male',
    date_of_birth: '',
    time_of_birth: '',
    place_of_birth: ''
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

  const handlePlaceChange = (value) => {
    setFormData({ ...formData, place_of_birth: value });
    
    if (value.length > 1) {
      const filtered = cities.filter(city => 
        city.toLowerCase().includes(value.toLowerCase())
      );
      setFilteredCities(filtered.slice(0, 10));
      setShowCitySuggestions(filtered.length > 0);
    } else {
      setShowCitySuggestions(false);
    }
  };

  const selectCity = (city) => {
    setFormData({ ...formData, place_of_birth: city });
    setShowCitySuggestions(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post(`${API}/birth-chart`, formData);
      setChartData(response.data);
      toast.success('Birth chart calculated successfully!');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to calculate birth chart');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = async () => {
    if (!chartData?.id) return;

    try {
      const response = await axios.post(
        `${API}/generate-pdf/${chartData.id}`,
        {},
        { responseType: 'blob' }
      );

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `janampatri_${chartData.name}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      toast.success('PDF downloaded successfully!');
    } catch (error) {
      toast.error('Failed to download PDF');
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
            {t('birthChart')}
          </h1>
          <div className="w-20" />
        </div>

        {!chartData ? (
          /* Birth Details Form */
          <Card className="max-w-2xl mx-auto">
            <CardHeader>
              <CardTitle className={`font-cinzel text-2xl ${language === 'hi' ? 'font-hindi' : ''}`}>
                Enter Birth Details
              </CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <Label htmlFor="name" className={language === 'hi' ? 'font-hindi' : ''}>
                    {t('name')}
                  </Label>
                  <Input
                    id="name"
                    data-testid="name-input"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    required
                  />
                </div>

                <div>
                  <Label htmlFor="gender" className={language === 'hi' ? 'font-hindi' : ''}>
                    {t('gender')}
                  </Label>
                  <Select
                    value={formData.gender}
                    onValueChange={(value) => setFormData({ ...formData, gender: value })}
                  >
                    <SelectTrigger data-testid="gender-select">
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
                  <Label htmlFor="dob" className={language === 'hi' ? 'font-hindi' : ''}>
                    {t('dateOfBirth')} (DD-MM-YYYY)
                  </Label>
                  <Input
                    id="dob"
                    data-testid="dob-input"
                    placeholder="15-08-1990"
                    value={formData.date_of_birth}
                    onChange={(e) => setFormData({ ...formData, date_of_birth: e.target.value })}
                    required
                  />
                </div>

                <div>
                  <Label htmlFor="time" className={language === 'hi' ? 'font-hindi' : ''}>
                    {t('timeOfBirth')} (HH:MM)
                  </Label>
                  <Input
                    id="time"
                    data-testid="time-input"
                    placeholder="14:30"
                    value={formData.time_of_birth}
                    onChange={(e) => setFormData({ ...formData, time_of_birth: e.target.value })}
                    required
                  />
                </div>

                <div className="relative">
                  <Label htmlFor="place" className={language === 'hi' ? 'font-hindi' : ''}>
                    {t('placeOfBirth')}
                  </Label>
                  <Input
                    id="place"
                    data-testid="place-input"
                    placeholder="Mumbai, Delhi, Bangalore..."
                    value={formData.place_of_birth}
                    onChange={(e) => handlePlaceChange(e.target.value)}
                    onFocus={() => {
                      if (formData.place_of_birth.length > 1) {
                        setShowCitySuggestions(true);
                      }
                    }}
                    onBlur={() => {
                      // Delay to allow click on suggestion
                      setTimeout(() => setShowCitySuggestions(false), 200);
                    }}
                    required
                  />
                  {showCitySuggestions && filteredCities.length > 0 && (
                    <div className="absolute z-10 w-full mt-1 bg-card border border-border rounded-lg shadow-lg max-h-60 overflow-y-auto">
                      {filteredCities.map((city, idx) => (
                        <button
                          key={idx}
                          type="button"
                          onClick={() => selectCity(city)}
                          className="w-full text-left px-4 py-2 hover:bg-muted transition-colors"
                        >
                          {city}
                        </button>
                      ))}
                    </div>
                  )}
                  <p className="text-xs text-muted-foreground mt-1">
                    Start typing to see city suggestions or enter any location
                  </p>
                </div>

                <Button
                  data-testid="calculate-btn"
                  type="submit"
                  disabled={loading}
                  className="w-full bg-primary hover:bg-primary/90 font-cinzel"
                >
                  {loading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Calculating...
                    </>
                  ) : (
                    t('calculate')
                  )}
                </Button>
              </form>
            </CardContent>
          </Card>
        ) : (
          /* Birth Chart Results */
          <div className="space-y-6" data-testid="chart-results">
            {/* Actions */}
            <div className="flex justify-between items-center">
              <Button
                variant="outline"
                onClick={() => setChartData(null)}
              >
                New Chart
              </Button>
              <Button
                data-testid="download-pdf-btn"
                onClick={handleDownloadPDF}
                className="gap-2 bg-primary hover:bg-primary/90"
              >
                <Download className="h-4 w-4" />
                {t('downloadPDF')}
              </Button>
            </div>

            {/* Personal Details */}
            <Card>
              <CardHeader>
                <CardTitle className="font-cinzel">Personal Details</CardTitle>
              </CardHeader>
              <CardContent className="grid md:grid-cols-2 gap-4">
                <div><strong>Name:</strong> {chartData.name}</div>
                <div><strong>Gender:</strong> {chartData.gender}</div>
                <div><strong>Date of Birth:</strong> {chartData.date_of_birth}</div>
                <div><strong>Time of Birth:</strong> {chartData.time_of_birth}</div>
                <div className="md:col-span-2"><strong>Place:</strong> {chartData.place_of_birth}</div>
              </CardContent>
            </Card>

            {/* Astrological Summary */}
            <div className="grid md:grid-cols-4 gap-4">
              <Card>
                <CardHeader>
                  <CardTitle className={`font-cinzel ${language === 'hi' ? 'font-hindi' : ''}`}>
                    {t('lagna')}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-2xl font-semibold text-primary">
                    {language === 'hi' ? chartData.lagna.rashi_hindi : chartData.lagna.rashi}
                  </p>
                  <p className="text-sm text-muted-foreground">{chartData.lagna.degree.toFixed(2)}°</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className={`font-cinzel ${language === 'hi' ? 'font-hindi' : ''}`}>
                    {t('moonSign')}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-2xl font-semibold text-primary">
                    {language === 'hi' ? chartData.moon_rashi_hindi : chartData.moon_rashi}
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className={`font-cinzel ${language === 'hi' ? 'font-hindi' : ''}`}>
                    {t('nakshatra')}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-2xl font-semibold text-primary">
                    {chartData.nakshatra.nakshatra}
                  </p>
                  <p className="text-sm text-muted-foreground">Pada: {chartData.nakshatra.pada}</p>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-secondary/10 to-accent/10">
                <CardHeader>
                  <CardTitle className={`font-cinzel ${language === 'hi' ? 'font-hindi' : ''}`}>
                    Western Zodiac
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {chartData.western_zodiac ? (
                    <>
                      <p className="text-3xl font-semibold text-secondary mb-1">
                        {chartData.western_zodiac.symbol}
                      </p>
                      <p className="text-xl font-semibold text-primary">
                        {language === 'hi' ? chartData.western_zodiac.sign_hindi : chartData.western_zodiac.sign}
                      </p>
                      <p className="text-xs text-muted-foreground mt-1">{chartData.western_zodiac.dates}</p>
                    </>
                  ) : (
                    <p className="text-muted-foreground">Sun Sign</p>
                  )}
                </CardContent>
              </Card>
            </div>

            {/* North Indian Chart */}
            <Card>
              <CardHeader>
                <CardTitle className="font-cinzel">Birth Chart (Kundli)</CardTitle>
              </CardHeader>
              <CardContent>
                <NorthIndianChart houses={chartData.houses} planets={chartData.planets} />
              </CardContent>
            </Card>

            {/* Planetary Positions */}
            <Card>
              <CardHeader>
                <CardTitle className={`font-cinzel ${language === 'hi' ? 'font-hindi' : ''}`}>
                  {t('planets')}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b">
                        <th className="text-left py-2">Planet</th>
                        <th className="text-left py-2">Rashi</th>
                        <th className="text-right py-2">Degree</th>
                      </tr>
                    </thead>
                    <tbody>
                      {Object.entries(chartData.planets).map(([planet, data]) => (
                        <tr key={planet} className="border-b hover:bg-muted/50">
                          <td className="py-2 font-semibold">{planet}</td>
                          <td className="py-2">
                            {language === 'hi' ? data.rashi_hindi : data.rashi}
                          </td>
                          <td className="text-right py-2">{data.degree.toFixed(2)}°</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </CardContent>
            </Card>

            {/* Personality Analysis */}
            {chartData.personality && (
              <>
                {/* Overall Personality Card - Prominent Display */}
                <Card className="border-2 border-primary/20 bg-gradient-to-br from-primary/5 to-secondary/5">
                  <CardHeader>
                    <CardTitle className={`font-cinzel text-2xl ${language === 'hi' ? 'font-hindi' : ''}`}>
                      {t('personality')} - Your Nature & Character
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {/* Core Traits */}
                    {chartData.personality.overall_summary && (
                      <div className="space-y-4">
                        <div>
                          <h3 className="font-semibold text-lg mb-2 flex items-center gap-2">
                            <span className="text-primary">✨</span>
                            Core Personality Traits
                          </h3>
                          <div className="flex flex-wrap gap-2">
                            {(language === 'hi' 
                              ? chartData.personality.overall_summary.core_traits_hindi 
                              : chartData.personality.overall_summary.core_traits
                            )?.map((trait, idx) => (
                              <span key={idx} className="px-4 py-2 bg-primary/10 text-primary rounded-full font-medium">
                                {trait}
                              </span>
                            ))}
                          </div>
                        </div>

                        <div className="grid md:grid-cols-2 gap-4">
                          <div className="p-4 bg-card rounded-lg border">
                            <div className="font-semibold mb-1">Life Approach</div>
                            <div className="text-muted-foreground">{chartData.personality.overall_summary.life_approach}</div>
                          </div>
                          <div className="p-4 bg-card rounded-lg border">
                            <div className="font-semibold mb-1">Dominant Element</div>
                            <div className="text-muted-foreground">{chartData.personality.overall_summary.dominant_element}</div>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Dominant Planet Influence */}
                    {chartData.personality.dominant_planet && (
                      <div className="p-4 bg-secondary/10 rounded-lg border border-secondary/20">
                        <h3 className="font-semibold text-lg mb-2 flex items-center gap-2">
                          <span className="text-secondary">🌟</span>
                          Dominant Planetary Influence: {chartData.personality.dominant_planet.planet}
                        </h3>
                        <p className="text-sm text-muted-foreground mb-2">
                          <strong>{language === 'hi' ? chartData.personality.dominant_planet.influence_hindi : chartData.personality.dominant_planet.influence}</strong>
                        </p>
                        <p className="text-sm">
                          {language === 'hi' ? chartData.personality.dominant_planet.characteristics_hindi : chartData.personality.dominant_planet.characteristics}
                        </p>
                      </div>
                    )}

                    {/* Detailed Analysis */}
                    {chartData.personality.detailed_analysis && (
                      <div className="space-y-3">
                        <h3 className="font-semibold text-lg">Detailed Character Analysis</h3>
                        
                        <div className="space-y-2">
                          <div className="flex items-start gap-2">
                            <span className="text-primary font-bold">🌙</span>
                            <div className="flex-1">
                              <div className="font-medium">Emotional Nature</div>
                              <div className="text-sm text-muted-foreground">{chartData.personality.detailed_analysis.emotional_nature}</div>
                            </div>
                          </div>
                          
                          <div className="flex items-start gap-2">
                            <span className="text-primary font-bold">☀️</span>
                            <div className="flex-1">
                              <div className="font-medium">Core Identity</div>
                              <div className="text-sm text-muted-foreground">{chartData.personality.detailed_analysis.core_identity}</div>
                            </div>
                          </div>
                          
                          <div className="flex items-start gap-2">
                            <span className="text-primary font-bold">⬆️</span>
                            <div className="flex-1">
                              <div className="font-medium">Outer Personality</div>
                              <div className="text-sm text-muted-foreground">{chartData.personality.detailed_analysis.outer_personality}</div>
                            </div>
                          </div>
                        </div>

                        <div className="grid md:grid-cols-2 gap-4 mt-4">
                          <div className="p-3 bg-green-50 dark:bg-green-950/20 rounded-lg border border-green-200 dark:border-green-800">
                            <div className="font-semibold text-green-700 dark:text-green-400 mb-1">💪 Key Strengths</div>
                            <ul className="text-sm space-y-1">
                              {chartData.personality.detailed_analysis.strengths?.map((strength, idx) => (
                                <li key={idx}>• {strength}</li>
                              ))}
                            </ul>
                          </div>
                          <div className="p-3 bg-blue-50 dark:bg-blue-950/20 rounded-lg border border-blue-200 dark:border-blue-800">
                            <div className="font-semibold text-blue-700 dark:text-blue-400 mb-1">🌱 Growth Areas</div>
                            <ul className="text-sm space-y-1">
                              {chartData.personality.detailed_analysis.growth_areas?.map((area, idx) => (
                                <li key={idx}>• {area}</li>
                              ))}
                            </ul>
                          </div>
                        </div>
                      </div>
                    )}
                  </CardContent>
                </Card>

                {/* Detailed Sign-based Personalities */}
                <div className="grid md:grid-cols-3 gap-4">
                  {/* Moon Sign */}
                  {chartData.personality.moon_based && (
                    <Card>
                      <CardHeader>
                        <CardTitle className="font-cinzel text-lg">🌙 Moon Sign Influence</CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-2">
                        <div className="text-xl font-bold text-primary">
                          {language === 'hi' ? chartData.moon_rashi_hindi : chartData.moon_rashi}
                        </div>
                        <div className="text-sm">
                          <strong>Traits:</strong> {chartData.personality.moon_based.traits?.join(', ')}
                        </div>
                        <div className="text-sm text-muted-foreground">
                          {chartData.personality.moon_based.nature}
                        </div>
                      </CardContent>
                    </Card>
                  )}

                  {/* Sun Sign */}
                  {chartData.personality.sun_based && (
                    <Card>
                      <CardHeader>
                        <CardTitle className="font-cinzel text-lg">☀️ Sun Sign Influence</CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-2">
                        <div className="text-xl font-bold text-primary">
                          {language === 'hi' ? chartData.planets.Sun.rashi_hindi : chartData.planets.Sun.rashi}
                        </div>
                        <div className="text-sm">
                          <strong>Traits:</strong> {chartData.personality.sun_based.traits?.join(', ')}
                        </div>
                        <div className="text-sm text-muted-foreground">
                          {chartData.personality.sun_based.nature}
                        </div>
                      </CardContent>
                    </Card>
                  )}

                  {/* Lagna */}
                  {chartData.personality.lagna_based && (
                    <Card>
                      <CardHeader>
                        <CardTitle className="font-cinzel text-lg">⬆️ Lagna Influence</CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-2">
                        <div className="text-xl font-bold text-primary">
                          {language === 'hi' ? chartData.lagna.rashi_hindi : chartData.lagna.rashi}
                        </div>
                        <div className="text-sm">
                          <strong>Traits:</strong> {chartData.personality.lagna_based.traits?.join(', ')}
                        </div>
                        <div className="text-sm text-muted-foreground">
                          {chartData.personality.lagna_based.nature}
                        </div>
                      </CardContent>
                    </Card>
                  )}
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default BirthChartPage;
