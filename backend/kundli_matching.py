from typing import Dict

class KundliMatching:
    """Ashta-Koota (8-point) Gun Milan system for marriage compatibility"""
    
    # Varna classification
    VARNA = {
        'Aries': 'Kshatriya', 'Leo': 'Kshatriya', 'Sagittarius': 'Kshatriya',
        'Taurus': 'Vaishya', 'Virgo': 'Vaishya', 'Capricorn': 'Vaishya',
        'Gemini': 'Shudra', 'Libra': 'Shudra', 'Aquarius': 'Shudra',
        'Cancer': 'Brahmin', 'Scorpio': 'Brahmin', 'Pisces': 'Brahmin'
    }
    
    VARNA_SCORE = {'same': 1, 'compatible': 1, 'incompatible': 0}
    
    # Vashya classification
    VASHYA = {
        'Aries': 'Quadruped', 'Taurus': 'Quadruped', 'Leo': 'Quadruped', 'Sagittarius': 'Human',
        'Gemini': 'Human', 'Virgo': 'Human', 'Libra': 'Human', 'Aquarius': 'Human',
        'Cancer': 'Water', 'Scorpio': 'Insect', 'Pisces': 'Water', 'Capricorn': 'Quadruped'
    }
    
    # Gana classification
    GANA = {
        1: 'Deva', 5: 'Deva', 7: 'Deva', 8: 'Deva', 13: 'Deva', 15: 'Deva', 17: 'Deva', 22: 'Deva', 27: 'Deva',
        2: 'Manushya', 4: 'Manushya', 6: 'Manushya', 11: 'Manushya', 12: 'Manushya', 20: 'Manushya', 21: 'Manushya', 25: 'Manushya', 26: 'Manushya',
        3: 'Rakshasa', 9: 'Rakshasa', 10: 'Rakshasa', 14: 'Rakshasa', 16: 'Rakshasa', 18: 'Rakshasa', 19: 'Rakshasa', 23: 'Rakshasa', 24: 'Rakshasa'
    }
    
    @staticmethod
    def calculate_varna(rashi1: str, rashi2: str) -> Dict:
        """Calculate Varna Koota (1 point)"""
        varna1 = KundliMatching.VARNA.get(rashi1)
        varna2 = KundliMatching.VARNA.get(rashi2)
        
        score = 1 if varna1 == varna2 else 0
        
        return {
            'name': 'Varna',
            'name_hindi': 'वर्ण',
            'max_score': 1,
            'obtained_score': score,
            'compatible': score == 1
        }
    
    @staticmethod
    def calculate_vashya(rashi1: str, rashi2: str) -> Dict:
        """Calculate Vashya Koota (2 points)"""
        vashya1 = KundliMatching.VASHYA.get(rashi1)
        vashya2 = KundliMatching.VASHYA.get(rashi2)
        
        if vashya1 == vashya2:
            score = 2
        elif (vashya1 == 'Human' and vashya2 in ['Human', 'Water']) or \
             (vashya2 == 'Human' and vashya1 in ['Human', 'Water']):
            score = 1
        else:
            score = 0
        
        return {
            'name': 'Vashya',
            'name_hindi': 'वश्य',
            'max_score': 2,
            'obtained_score': score,
            'compatible': score >= 1
        }
    
    @staticmethod
    def calculate_tara(nakshatra1: int, nakshatra2: int) -> Dict:
        """Calculate Tara Koota (3 points)"""
        diff = abs(nakshatra2 - nakshatra1)
        remainder = diff % 9
        
        # Janma (1), Sampat (2), Vipat (3), Kshema (4), Pratyak (5), 
        # Sadhaka (6), Vadha (7), Mitra (8), Parama Mitra (9/0)
        favorable_taras = [2, 4, 6, 8, 0]
        
        score = 3 if remainder in favorable_taras else 0
        
        return {
            'name': 'Tara',
            'name_hindi': 'तारा',
            'max_score': 3,
            'obtained_score': score,
            'compatible': score >= 1.5
        }
    
    @staticmethod
    def calculate_yoni(nakshatra1: int, nakshatra2: int) -> Dict:
        """Calculate Yoni Koota (4 points)"""
        # Simplified yoni calculation based on nakshatra
        yoni_map = {
            1: 'Horse', 2: 'Elephant', 3: 'Sheep', 4: 'Serpent', 5: 'Dog', 6: 'Cat',
            7: 'Rat', 8: 'Cow', 9: 'Buffalo', 10: 'Tiger', 11: 'Hare', 12: 'Monkey',
            13: 'Mongoose', 14: 'Lion', 15: 'Monkey', 16: 'Rat', 17: 'Cow', 18: 'Buffalo',
            19: 'Tiger', 20: 'Hare', 21: 'Monkey', 22: 'Mongoose', 23: 'Lion', 24: 'Monkey',
            25: 'Horse', 26: 'Elephant', 27: 'Sheep'
        }
        
        yoni1 = yoni_map.get(nakshatra1)
        yoni2 = yoni_map.get(nakshatra2)
        
        if yoni1 == yoni2:
            score = 4
        elif yoni1 and yoni2:
            # Friendly yonis get 2 points, neutral 1, enemy 0
            score = 2  # Default neutral
        else:
            score = 0
        
        return {
            'name': 'Yoni',
            'name_hindi': 'योनि',
            'max_score': 4,
            'obtained_score': score,
            'compatible': score >= 2
        }
    
    @staticmethod
    def calculate_graha_maitri(rashi1: str, rashi2: str) -> Dict:
        """Calculate Graha Maitri Koota (5 points)"""
        # Lords of rashis
        lords = {
            'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury', 'Cancer': 'Moon',
            'Leo': 'Sun', 'Virgo': 'Mercury', 'Libra': 'Venus', 'Scorpio': 'Mars',
            'Sagittarius': 'Jupiter', 'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter'
        }
        
        lord1 = lords.get(rashi1)
        lord2 = lords.get(rashi2)
        
        # Simplified friendship - same lord gets max points
        if lord1 == lord2:
            score = 5
        else:
            # Friendly planets
            friends = {
                'Sun': ['Moon', 'Mars', 'Jupiter'],
                'Moon': ['Sun', 'Mercury'],
                'Mars': ['Sun', 'Moon', 'Jupiter'],
                'Mercury': ['Sun', 'Venus'],
                'Jupiter': ['Sun', 'Moon', 'Mars'],
                'Venus': ['Mercury', 'Saturn'],
                'Saturn': ['Mercury', 'Venus']
            }
            
            if lord2 in friends.get(lord1, []):
                score = 4
            else:
                score = 1
        
        return {
            'name': 'Graha Maitri',
            'name_hindi': 'ग्रह मैत्री',
            'max_score': 5,
            'obtained_score': score,
            'compatible': score >= 3
        }
    
    @staticmethod
    def calculate_gana(nakshatra1: int, nakshatra2: int) -> Dict:
        """Calculate Gana Koota (6 points)"""
        gana1 = KundliMatching.GANA.get(nakshatra1, 'Manushya')
        gana2 = KundliMatching.GANA.get(nakshatra2, 'Manushya')
        
        if gana1 == gana2:
            score = 6
        elif (gana1 == 'Deva' and gana2 == 'Manushya') or (gana1 == 'Manushya' and gana2 == 'Deva'):
            score = 5
        elif (gana1 == 'Manushya' and gana2 == 'Rakshasa') or (gana1 == 'Rakshasa' and gana2 == 'Manushya'):
            score = 1
        else:  # Deva-Rakshasa combination
            score = 0
        
        return {
            'name': 'Gana',
            'name_hindi': 'गण',
            'max_score': 6,
            'obtained_score': score,
            'compatible': score >= 3,
            'gana1': gana1,
            'gana2': gana2
        }
    
    @staticmethod
    def calculate_bhakoot(rashi1_num: int, rashi2_num: int) -> Dict:
        """Calculate Bhakoot Koota (7 points)"""
        diff = abs(rashi2_num - rashi1_num)
        
        # Incompatible positions: 2-12, 5-9, 6-8
        incompatible = [2, 5, 6, 7, 8, 10]
        
        if diff == 0:
            score = 7
        elif diff in incompatible:
            score = 0
            dosha = True
        else:
            score = 7
            dosha = False
        
        return {
            'name': 'Bhakoot',
            'name_hindi': 'भकूट',
            'max_score': 7,
            'obtained_score': score,
            'compatible': score >= 3,
            'dosha': diff in incompatible
        }
    
    @staticmethod
    def calculate_nadi(nakshatra1: int, nakshatra2: int) -> Dict:
        """Calculate Nadi Koota (8 points)"""
        # Three Nadis: Aadi, Madhya, Antya
        nadi1 = (nakshatra1 - 1) % 3
        nadi2 = (nakshatra2 - 1) % 3
        
        nadi_names = ['Aadi', 'Madhya', 'Antya']
        nadi_names_hindi = ['आदि', 'मध्य', 'अंत्य']
        
        if nadi1 != nadi2:
            score = 8
            dosha = False
        else:
            score = 0
            dosha = True
        
        return {
            'name': 'Nadi',
            'name_hindi': 'नाड़ी',
            'max_score': 8,
            'obtained_score': score,
            'compatible': score == 8,
            'dosha': dosha,
            'nadi1': nadi_names[nadi1],
            'nadi2': nadi_names[nadi2]
        }
    
    @staticmethod
    def calculate_gun_milan(chart1: Dict, chart2: Dict) -> Dict:
        """Calculate complete Gun Milan (36 points)"""
        rashi1 = chart1['moon_rashi']
        rashi2 = chart2['moon_rashi']
        rashi1_num = chart1['planets']['Moon']['rashi_num']
        rashi2_num = chart2['planets']['Moon']['rashi_num']
        nakshatra1 = chart1['nakshatra']['nakshatra_num']
        nakshatra2 = chart2['nakshatra']['nakshatra_num']
        
        # Calculate all 8 kootas
        varna = KundliMatching.calculate_varna(rashi1, rashi2)
        vashya = KundliMatching.calculate_vashya(rashi1, rashi2)
        tara = KundliMatching.calculate_tara(nakshatra1, nakshatra2)
        yoni = KundliMatching.calculate_yoni(nakshatra1, nakshatra2)
        graha_maitri = KundliMatching.calculate_graha_maitri(rashi1, rashi2)
        gana = KundliMatching.calculate_gana(nakshatra1, nakshatra2)
        bhakoot = KundliMatching.calculate_bhakoot(rashi1_num, rashi2_num)
        nadi = KundliMatching.calculate_nadi(nakshatra1, nakshatra2)
        
        kootas = [varna, vashya, tara, yoni, graha_maitri, gana, bhakoot, nadi]
        
        total_score = sum(k['obtained_score'] for k in kootas)
        
        # Compatibility verdict
        if total_score >= 28:
            verdict = 'Excellent'
            verdict_hindi = 'उत्कृष्ट'
        elif total_score >= 24:
            verdict = 'Very Good'
            verdict_hindi = 'बहुत अच्छा'
        elif total_score >= 18:
            verdict = 'Good'
            verdict_hindi = 'अच्छा'
        elif total_score >= 12:
            verdict = 'Average'
            verdict_hindi = 'औसत'
        else:
            verdict = 'Not Recommended'
            verdict_hindi = 'अनुशंसित नहीं'
        
        # Check for doshas
        doshas = []
        if nadi['dosha']:
            doshas.append({'name': 'Nadi Dosha', 'name_hindi': 'नाड़ी दोष'})
        if bhakoot.get('dosha'):
            doshas.append({'name': 'Bhakoot Dosha', 'name_hindi': 'भकूट दोष'})
        
        return {
            'person1': {
                'name': chart1['name'],
                'rashi': rashi1,
                'nakshatra': chart1['nakshatra']['nakshatra']
            },
            'person2': {
                'name': chart2['name'],
                'rashi': rashi2,
                'nakshatra': chart2['nakshatra']['nakshatra']
            },
            'kootas': kootas,
            'total_score': total_score,
            'max_score': 36,
            'percentage': round((total_score / 36) * 100, 2),
            'verdict': verdict,
            'verdict_hindi': verdict_hindi,
            'doshas': doshas
        }
