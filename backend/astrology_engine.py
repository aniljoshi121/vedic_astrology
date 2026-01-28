import swisseph as swe
from datetime import datetime, timezone
from geopy.geocoders import Nominatim
from typing import Dict, List, Tuple
import math

# Initialize Swiss Ephemeris
swe.set_ephe_path('/usr/share/ephe')

class AstrologyEngine:
    PLANETS = {
        'Sun': swe.SUN,
        'Moon': swe.MOON,
        'Mars': swe.MARS,
        'Mercury': swe.MERCURY,
        'Jupiter': swe.JUPITER,
        'Venus': swe.VENUS,
        'Saturn': swe.SATURN,
        'Rahu': swe.MEAN_NODE,
        'Ketu': swe.MEAN_NODE  # Ketu is 180° opposite to Rahu
    }
    
    RASHIS = [
        'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
        'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    
    RASHIS_HINDI = [
        'मेष', 'वृषभ', 'मिथुन', 'कर्क', 'सिंह', 'कन्या',
        'तुला', 'वृश्चिक', 'धनु', 'मकर', 'कुम्भ', 'मीन'
    ]
    
    # Western Zodiac Signs (Sun Sign based)
    WESTERN_ZODIAC = [
        {'sign': 'Aries', 'hindi': 'मेष', 'dates': 'Mar 21 - Apr 19', 'symbol': '♈'},
        {'sign': 'Taurus', 'hindi': 'वृषभ', 'dates': 'Apr 20 - May 20', 'symbol': '♉'},
        {'sign': 'Gemini', 'hindi': 'मिथुन', 'dates': 'May 21 - Jun 20', 'symbol': '♊'},
        {'sign': 'Cancer', 'hindi': 'कर्क', 'dates': 'Jun 21 - Jul 22', 'symbol': '♋'},
        {'sign': 'Leo', 'hindi': 'सिंह', 'dates': 'Jul 23 - Aug 22', 'symbol': '♌'},
        {'sign': 'Virgo', 'hindi': 'कन्या', 'dates': 'Aug 23 - Sep 22', 'symbol': '♍'},
        {'sign': 'Libra', 'hindi': 'तुला', 'dates': 'Sep 23 - Oct 22', 'symbol': '♎'},
        {'sign': 'Scorpio', 'hindi': 'वृश्चिक', 'dates': 'Oct 23 - Nov 21', 'symbol': '♏'},
        {'sign': 'Sagittarius', 'hindi': 'धनु', 'dates': 'Nov 22 - Dec 21', 'symbol': '♐'},
        {'sign': 'Capricorn', 'hindi': 'मकर', 'dates': 'Dec 22 - Jan 19', 'symbol': '♑'},
        {'sign': 'Aquarius', 'hindi': 'कुम्भ', 'dates': 'Jan 20 - Feb 18', 'symbol': '♒'},
        {'sign': 'Pisces', 'hindi': 'मीन', 'dates': 'Feb 19 - Mar 20', 'symbol': '♓'}
    ]
    
    @staticmethod
    def get_western_zodiac(date_time: datetime) -> Dict:
        """Calculate Western/Tropical zodiac sign based on birth date"""
        month = date_time.month
        day = date_time.day
        
        # Determine zodiac based on date ranges
        if (month == 3 and day >= 21) or (month == 4 and day <= 19):
            idx = 0  # Aries
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            idx = 1  # Taurus
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            idx = 2  # Gemini
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            idx = 3  # Cancer
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            idx = 4  # Leo
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            idx = 5  # Virgo
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
            idx = 6  # Libra
        elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
            idx = 7  # Scorpio
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
            idx = 8  # Sagittarius
        elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
            idx = 9  # Capricorn
        elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
            idx = 10  # Aquarius
        else:  # (month == 2 and day >= 19) or (month == 3 and day <= 20)
            idx = 11  # Pisces
        
        zodiac = AstrologyEngine.WESTERN_ZODIAC[idx]
        return {
            'sign': zodiac['sign'],
            'sign_hindi': zodiac['hindi'],
            'symbol': zodiac['symbol'],
            'dates': zodiac['dates']
        }
    
    NAKSHATRAS = [
        'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
        'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
        'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
        'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
        'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
    ]
    
    # Predefined Indian cities with coordinates (fallback)
    INDIAN_CITIES = {
        'mumbai': (19.0760, 72.8777),
        'delhi': (28.7041, 77.1025),
        'new delhi': (28.6139, 77.2090),
        'bangalore': (12.9716, 77.5946),
        'bengaluru': (12.9716, 77.5946),
        'kolkata': (22.5726, 88.3639),
        'chennai': (13.0827, 80.2707),
        'hyderabad': (17.3850, 78.4867),
        'pune': (18.5204, 73.8567),
        'ahmedabad': (23.0225, 72.5714),
        'jaipur': (26.9124, 75.7873),
        'lucknow': (26.8467, 80.9462),
        'kanpur': (26.4499, 80.3319),
        'nagpur': (21.1458, 79.0882),
        'indore': (22.7196, 75.8577),
        'bhopal': (23.2599, 77.4126),
        'patna': (25.5941, 85.1376),
        'vadodara': (22.3072, 73.1812),
        'ludhiana': (30.9010, 75.8573),
        'agra': (27.1767, 78.0081),
        'nashik': (19.9975, 73.7898),
        'varanasi': (25.3176, 82.9739),
        'srinagar': (34.0837, 74.7973),
        'surat': (21.1702, 72.8311),
        'chandigarh': (30.7333, 76.7794),
        'goa': (15.2993, 74.1240),
        'panaji': (15.4909, 73.8278),
        'kochi': (9.9312, 76.2673),
        'thiruvananthapuram': (8.5241, 76.9366),
        'dehradun': (30.3165, 78.0322),
        'shimla': (31.1048, 77.1734),
        'ranchi': (23.3441, 85.3096),
        'guwahati': (26.1445, 91.7362),
        'bhubaneswar': (20.2961, 85.8245),
        'coimbatore': (11.0168, 76.9558),
        'mysore': (12.2958, 76.6394),
        'jodhpur': (26.2389, 73.0243),
        'madurai': (9.9252, 78.1198),
        'vijayawada': (16.5062, 80.6480),
        'visakhapatnam': (17.6868, 83.2185),
    }
    
    @staticmethod
    def get_coordinates(place_name: str) -> Tuple[float, float]:
        """Convert place name to latitude and longitude with fallback"""
        # First, try predefined cities (case-insensitive, partial match)
        place_lower = place_name.lower().strip()
        
        # Try exact match or partial match in city name
        for city, coords in AstrologyEngine.INDIAN_CITIES.items():
            if city in place_lower or place_lower in city:
                return coords
        
        # If not found in predefined, try geocoding service
        try:
            geolocator = Nominatim(user_agent="vedic_astrology_app", timeout=10)
            
            # Try original query
            location = geolocator.geocode(place_name)
            if location:
                return location.latitude, location.longitude
            
            # Try with "India" appended if not already present
            if 'india' not in place_lower:
                location = geolocator.geocode(f"{place_name}, India")
                if location:
                    return location.latitude, location.longitude
            
            # Try removing state/country and searching city only
            parts = place_name.split(',')
            if len(parts) > 1:
                city_only = parts[0].strip()
                location = geolocator.geocode(f"{city_only}, India")
                if location:
                    return location.latitude, location.longitude
            
            raise ValueError(f"Location not found: {place_name}. Please try entering just the city name (e.g., 'Mumbai' or 'Delhi')")
            
        except Exception as e:
            raise ValueError(f"Unable to find location: {place_name}. Please use a major city name or select from the dropdown.")
    
    @staticmethod
    def get_julian_day(date_time: datetime, lat: float, lon: float) -> Tuple[float, float]:
        """Calculate Julian Day Number"""
        year = date_time.year
        month = date_time.month
        day = date_time.day
        hour = date_time.hour + date_time.minute / 60.0
        
        jd = swe.julday(year, month, day, hour)
        return jd, hour
    
    @staticmethod
    def get_ayanamsa(jd: float) -> float:
        """Get Ayanamsa (precession) for Lahiri system"""
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        return swe.get_ayanamsa(jd)
    
    @staticmethod
    def get_planetary_positions(jd: float, ayanamsa: float) -> Dict:
        """Calculate positions of all planets"""
        positions = {}
        
        for planet_name, planet_id in AstrologyEngine.PLANETS.items():
            result = swe.calc_ut(jd, planet_id)
            # result is a tuple: (longitude, latitude, distance, speed_long, speed_lat, speed_dist)
            longitude = result[0][0] - ayanamsa  # Sidereal position
            
            if longitude < 0:
                longitude += 360
            
            # For Ketu, add 180 degrees to Rahu
            if planet_name == 'Ketu':
                longitude = (longitude + 180) % 360
            
            rashi_num = int(longitude / 30)
            degree = longitude % 30
            
            positions[planet_name] = {
                'longitude': round(longitude, 2),
                'rashi': AstrologyEngine.RASHIS[rashi_num],
                'rashi_hindi': AstrologyEngine.RASHIS_HINDI[rashi_num],
                'degree': round(degree, 2),
                'rashi_num': rashi_num + 1
            }
        
        return positions
    
    @staticmethod
    def get_lagna(jd: float, lat: float, lon: float, ayanamsa: float) -> Dict:
        """Calculate Ascendant (Lagna)"""
        houses = swe.houses(jd, lat, lon, b'P')  # Placidus house system
        ascendant = houses[0][0] - ayanamsa
        
        if ascendant < 0:
            ascendant += 360
        
        rashi_num = int(ascendant / 30)
        degree = ascendant % 30
        
        return {
            'longitude': round(ascendant, 2),
            'rashi': AstrologyEngine.RASHIS[rashi_num],
            'rashi_hindi': AstrologyEngine.RASHIS_HINDI[rashi_num],
            'degree': round(degree, 2),
            'rashi_num': rashi_num + 1
        }
    
    @staticmethod
    def get_houses(jd: float, lat: float, lon: float, ayanamsa: float, lagna_rashi: int) -> List[Dict]:
        """Calculate 12 houses (Bhavas) starting from Lagna"""
        houses = []
        
        for i in range(12):
            house_num = i + 1
            rashi_num = (lagna_rashi + i - 1) % 12
            
            houses.append({
                'house_num': house_num,
                'rashi': AstrologyEngine.RASHIS[rashi_num],
                'rashi_hindi': AstrologyEngine.RASHIS_HINDI[rashi_num],
                'rashi_num': rashi_num + 1
            })
        
        return houses
    
    @staticmethod
    def get_moon_nakshatra(moon_longitude: float) -> Dict:
        """Calculate Nakshatra based on Moon position"""
        nakshatra_num = int(moon_longitude / (360 / 27))
        nakshatra_degree = (moon_longitude % (360 / 27))
        
        # Pada (quarter) calculation
        pada = int(nakshatra_degree / ((360 / 27) / 4)) + 1
        
        return {
            'nakshatra': AstrologyEngine.NAKSHATRAS[nakshatra_num],
            'nakshatra_num': nakshatra_num + 1,
            'pada': pada
        }
    
    @staticmethod
    def calculate_birth_chart(name: str, gender: str, date_str: str, time_str: str, place: str) -> Dict:
        """Main function to calculate complete birth chart"""
        # Parse date and time
        date_time = datetime.strptime(f"{date_str} {time_str}", "%d-%m-%Y %H:%M")
        
        # Get coordinates
        lat, lon = AstrologyEngine.get_coordinates(place)
        
        # Calculate Julian Day
        jd, hour = AstrologyEngine.get_julian_day(date_time, lat, lon)
        
        # Get Ayanamsa
        ayanamsa = AstrologyEngine.get_ayanamsa(jd)
        
        # Calculate Lagna
        lagna = AstrologyEngine.get_lagna(jd, lat, lon, ayanamsa)
        
        # Calculate planetary positions
        planets = AstrologyEngine.get_planetary_positions(jd, ayanamsa)
        
        # Calculate houses
        houses = AstrologyEngine.get_houses(jd, lat, lon, ayanamsa, lagna['rashi_num'])
        
        # Moon Rashi (Zodiac sign)
        moon_rashi = planets['Moon']['rashi']
        moon_rashi_hindi = planets['Moon']['rashi_hindi']
        
        # Nakshatra
        nakshatra = AstrologyEngine.get_moon_nakshatra(planets['Moon']['longitude'])
        
        # Western Zodiac (Sun Sign)
        western_zodiac = AstrologyEngine.get_western_zodiac(date_time)
        
        return {
            'name': name,
            'gender': gender,
            'date_of_birth': date_str,
            'time_of_birth': time_str,
            'place_of_birth': place,
            'latitude': round(lat, 4),
            'longitude': round(lon, 4),
            'lagna': lagna,
            'moon_rashi': moon_rashi,
            'moon_rashi_hindi': moon_rashi_hindi,
            'nakshatra': nakshatra,
            'western_zodiac': western_zodiac,
            'planets': planets,
            'houses': houses,
            'ayanamsa': round(ayanamsa, 2)
        }
    
    @staticmethod
    def get_dominant_planet(planets: Dict) -> str:
        """Determine the dominant planet in the chart"""
        # Simplified logic: planet in its own sign or exalted
        exaltation = {
            'Sun': 'Aries', 'Moon': 'Taurus', 'Mars': 'Capricorn',
            'Mercury': 'Virgo', 'Jupiter': 'Cancer', 'Venus': 'Pisces',
            'Saturn': 'Libra'
        }
        
        own_signs = {
            'Sun': ['Leo'], 'Moon': ['Cancer'], 
            'Mars': ['Aries', 'Scorpio'], 'Mercury': ['Gemini', 'Virgo'],
            'Jupiter': ['Sagittarius', 'Pisces'], 'Venus': ['Taurus', 'Libra'],
            'Saturn': ['Capricorn', 'Aquarius']
        }
        
        for planet, data in planets.items():
            if planet in ['Rahu', 'Ketu']:
                continue
            
            # Check exaltation
            if exaltation.get(planet) == data['rashi']:
                return planet
            
            # Check own sign
            if data['rashi'] in own_signs.get(planet, []):
                return planet
        
        # Default to Sun
        return 'Sun'
    
    @staticmethod
    def get_personality_traits(chart: Dict) -> Dict:
        """Generate comprehensive personality analysis based on birth chart"""
        moon_rashi = chart['moon_rashi']
        lagna_rashi = chart['lagna']['rashi']
        sun_rashi = chart['planets']['Sun']['rashi']
        dominant_planet = AstrologyEngine.get_dominant_planet(chart['planets'])
        
        # Basic personality traits based on Moon Rashi
        rashi_traits = {
            'Aries': {
                'traits': ['Dynamic', 'Energetic', 'Courageous', 'Impulsive'],
                'traits_hindi': ['गतिशील', 'ऊर्जावान', 'साहसी', 'आवेगपूर्ण'],
                'nature': 'Fiery and passionate',
                'nature_hindi': 'अग्नि और जोशीला',
                'guna': 'Rajas',
                'element': 'Fire'
            },
            'Taurus': {
                'traits': ['Stable', 'Patient', 'Practical', 'Reliable'],
                'traits_hindi': ['स्थिर', 'धैर्यवान', 'व्यावहारिक', 'विश्वसनीय'],
                'nature': 'Grounded and steady',
                'nature_hindi': 'ज़मीन से जुड़ा और स्थिर',
                'guna': 'Tamas',
                'element': 'Earth'
            },
            'Gemini': {
                'traits': ['Communicative', 'Versatile', 'Curious', 'Intellectual'],
                'traits_hindi': ['संवादी', 'बहुमुखी', 'जिज्ञासु', 'बौद्धिक'],
                'nature': 'Adaptable and quick-witted',
                'nature_hindi': 'अनुकूलनशील और तेज़-तर्रार',
                'guna': 'Rajas',
                'element': 'Air'
            },
            'Cancer': {
                'traits': ['Emotional', 'Nurturing', 'Intuitive', 'Protective'],
                'traits_hindi': ['भावुक', 'पालन-पोषण करने वाला', 'सहज ज्ञान युक्त', 'सुरक्षात्मक'],
                'nature': 'Sensitive and caring',
                'nature_hindi': 'संवेदनशील और देखभाल करने वाला',
                'guna': 'Sattva',
                'element': 'Water'
            },
            'Leo': {
                'traits': ['Confident', 'Generous', 'Charismatic', 'Creative'],
                'traits_hindi': ['आत्मविश्वासी', 'उदार', 'करिश्माई', 'रचनात्मक'],
                'nature': 'Bold and expressive',
                'nature_hindi': 'साहसी और अभिव्यंजक',
                'guna': 'Sattva',
                'element': 'Fire'
            },
            'Virgo': {
                'traits': ['Analytical', 'Organized', 'Detail-oriented', 'Helpful'],
                'traits_hindi': ['विश्लेषणात्मक', 'संगठित', 'विस्तार-उन्मुख', 'मददगार'],
                'nature': 'Methodical and perfectionist',
                'nature_hindi': 'व्यवस्थित और पूर्णतावादी',
                'guna': 'Rajas',
                'element': 'Earth'
            },
            'Libra': {
                'traits': ['Balanced', 'Diplomatic', 'Harmonious', 'Social'],
                'traits_hindi': ['संतुलित', 'कूटनीतिक', 'सामंजस्यपूर्ण', 'सामाजिक'],
                'nature': 'Peace-loving and fair',
                'nature_hindi': 'शांतिप्रिय और निष्पक्ष',
                'guna': 'Rajas',
                'element': 'Air'
            },
            'Scorpio': {
                'traits': ['Intense', 'Mysterious', 'Passionate', 'Determined'],
                'traits_hindi': ['तीव्र', 'रहस्यमय', 'भावुक', 'दृढ़निश्चयी'],
                'nature': 'Deep and transformative',
                'nature_hindi': 'गहन और परिवर्तनकारी',
                'guna': 'Tamas',
                'element': 'Water'
            },
            'Sagittarius': {
                'traits': ['Optimistic', 'Adventurous', 'Philosophical', 'Independent'],
                'traits_hindi': ['आशावादी', 'साहसिक', 'दार्शनिक', 'स्वतंत्र'],
                'nature': 'Free-spirited and wise',
                'nature_hindi': 'मुक्त-आत्मा और बुद्धिमान',
                'guna': 'Sattva',
                'element': 'Fire'
            },
            'Capricorn': {
                'traits': ['Ambitious', 'Disciplined', 'Responsible', 'Practical'],
                'traits_hindi': ['महत्वाकांक्षी', 'अनुशासित', 'जिम्मेदार', 'व्यावहारिक'],
                'nature': 'Hardworking and goal-oriented',
                'nature_hindi': 'मेहनती और लक्ष्य-उन्मुख',
                'guna': 'Tamas',
                'element': 'Earth'
            },
            'Aquarius': {
                'traits': ['Innovative', 'Humanitarian', 'Independent', 'Progressive'],
                'traits_hindi': ['नवोन्वेषी', 'मानवतावादी', 'स्वतंत्र', 'प्रगतिशील'],
                'nature': 'Visionary and unconventional',
                'nature_hindi': 'दूरदर्शी और अपरंपरागत',
                'guna': 'Tamas',
                'element': 'Air'
            },
            'Pisces': {
                'traits': ['Compassionate', 'Artistic', 'Intuitive', 'Dreamy'],
                'traits_hindi': ['दयालु', 'कलात्मक', 'सहज ज्ञान युक्त', 'स्वप्निल'],
                'nature': 'Sensitive and spiritual',
                'nature_hindi': 'संवेदनशील और आध्यात्मिक',
                'guna': 'Sattva',
                'element': 'Water'
            }
        }
        
        moon_personality = rashi_traits.get(moon_rashi, {})
        lagna_personality = rashi_traits.get(lagna_rashi, {})
        sun_personality = rashi_traits.get(sun_rashi, {})
        
        # Dominant planet traits
        planet_traits = {
            'Sun': {
                'influence': 'Leadership and Authority',
                'influence_hindi': 'नेतृत्व और अधिकार',
                'characteristics': 'Confident, authoritative, natural leader, ego-driven, ambitious',
                'characteristics_hindi': 'आत्मविश्वासी, सत्तावादी, स्वाभाविक नेता, अहंकार-प्रेरित, महत्वाकांक्षी'
            },
            'Moon': {
                'influence': 'Emotions and Intuition',
                'influence_hindi': 'भावनाएँ और अंतर्ज्ञान',
                'characteristics': 'Emotional, intuitive, nurturing, changeable, sensitive to surroundings',
                'characteristics_hindi': 'भावनात्मक, सहज, पोषण करने वाला, परिवर्तनशील, परिवेश के प्रति संवेदनशील'
            },
            'Mars': {
                'influence': 'Energy and Action',
                'influence_hindi': 'ऊर्जा और कार्य',
                'characteristics': 'Energetic, courageous, aggressive, competitive, action-oriented',
                'characteristics_hindi': 'ऊर्जावान, साहसी, आक्रामक, प्रतिस्पर्धी, कार्य-उन्मुख'
            },
            'Mercury': {
                'influence': 'Communication and Intelligence',
                'influence_hindi': 'संचार और बुद्धि',
                'characteristics': 'Intelligent, communicative, analytical, witty, versatile',
                'characteristics_hindi': 'बुद्धिमान, संवादी, विश्लेषणात्मक, मजाकिया, बहुमुखी'
            },
            'Jupiter': {
                'influence': 'Wisdom and Expansion',
                'influence_hindi': 'ज्ञान और विस्तार',
                'characteristics': 'Wise, optimistic, philosophical, generous, knowledge-seeking',
                'characteristics_hindi': 'बुद्धिमान, आशावादी, दार्शनिक, उदार, ज्ञान-खोजी'
            },
            'Venus': {
                'influence': 'Love and Beauty',
                'influence_hindi': 'प्रेम और सौंदर्य',
                'characteristics': 'Artistic, romantic, sensual, harmonious, pleasure-loving',
                'characteristics_hindi': 'कलात्मक, रोमांटिक, कामुक, सामंजस्यपूर्ण, सुख-प्रिय'
            },
            'Saturn': {
                'influence': 'Discipline and Responsibility',
                'influence_hindi': 'अनुशासन और जिम्मेदारी',
                'characteristics': 'Disciplined, responsible, patient, serious, hardworking',
                'characteristics_hindi': 'अनुशासित, जिम्मेदार, धैर्यवान, गंभीर, मेहनती'
            }
        }
        
        # Overall personality summary
        summary_traits = []
        summary_traits_hindi = []
        
        # Combine traits from Moon (emotions), Sun (ego), and Lagna (personality)
        if moon_personality.get('traits'):
            summary_traits.extend(moon_personality['traits'][:2])
        if sun_personality.get('traits'):
            summary_traits.extend([t for t in sun_personality['traits'][:2] if t not in summary_traits])
        if lagna_personality.get('traits'):
            summary_traits.extend([t for t in lagna_personality['traits'][:2] if t not in summary_traits])
        
        # Hindi traits
        if moon_personality.get('traits_hindi'):
            summary_traits_hindi.extend(moon_personality['traits_hindi'][:2])
        if sun_personality.get('traits_hindi'):
            summary_traits_hindi.extend([t for t in sun_personality['traits_hindi'][:2] if t not in summary_traits_hindi])
        if lagna_personality.get('traits_hindi'):
            summary_traits_hindi.extend([t for t in lagna_personality['traits_hindi'][:2] if t not in summary_traits_hindi])
        
        # Life approach
        life_approach_parts = []
        if moon_personality.get('nature'):
            life_approach_parts.append(moon_personality['nature'])
        if lagna_personality.get('nature'):
            life_approach_parts.append(lagna_personality['nature'])
        
        life_approach = f"{life_approach_parts[0]} with {life_approach_parts[1].lower()}" if len(life_approach_parts) == 2 else life_approach_parts[0] if life_approach_parts else "Balanced approach to life"
        
        return {
            'overall_summary': {
                'core_traits': summary_traits[:5],
                'core_traits_hindi': summary_traits_hindi[:5],
                'life_approach': life_approach,
                'dominant_element': moon_personality.get('element', 'Earth'),
                'dominant_guna': moon_personality.get('guna', 'Rajas')
            },
            'moon_based': moon_personality,
            'sun_based': sun_personality,
            'lagna_based': lagna_personality,
            'dominant_planet': {
                'planet': dominant_planet,
                **planet_traits.get(dominant_planet, {})
            },
            'detailed_analysis': {
                'emotional_nature': f"Moon in {moon_rashi}: {moon_personality.get('nature', 'Balanced')}",
                'core_identity': f"Sun in {sun_rashi}: {sun_personality.get('nature', 'Stable')}",
                'outer_personality': f"Lagna in {lagna_rashi}: {lagna_personality.get('nature', 'Harmonious')}",
                'strengths': summary_traits[:3],
                'growth_areas': ['Patience', 'Adaptability', 'Communication'] if moon_personality.get('guna') == 'Rajas' else ['Action', 'Initiative', 'Expression']
            }
        }
