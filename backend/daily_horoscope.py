from typing import Dict, List
from datetime import datetime, timezone
import random

class DailyHoroscope:
    """Generate daily horoscope based on zodiac sign and current transits"""
    
    RASHIS = [
        'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
        'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    
    # Horoscope templates for each category
    TEMPLATES = {
        'career': {
            'Aries': [
                'Your leadership skills shine today. Take initiative in workplace projects.',
                'A bold career move may present itself. Trust your instincts.',
                'Collaboration with colleagues brings unexpected opportunities.'
            ],
            'Taurus': [
                'Patience and persistence lead to professional recognition today.',
                'Financial stability improves through careful planning.',
                'Your practical approach solves a complex work problem.'
            ],
            'Gemini': [
                'Communication skills open new doors in your career.',
                'Networking brings valuable professional connections.',
                'Adaptability helps you navigate workplace changes smoothly.'
            ],
            'Cancer': [
                'Intuition guides important career decisions today.',
                'Nurturing team relationships creates a positive work environment.',
                'Emotional intelligence helps resolve workplace conflicts.'
            ],
            'Leo': [
                'Creative projects receive well-deserved attention and praise.',
                'Leadership opportunities align with your professional goals.',
                'Confidence attracts beneficial career opportunities.'
            ],
            'Virgo': [
                'Attention to detail impresses superiors and colleagues.',
                'Organizational skills lead to increased productivity.',
                'Analytical thinking solves a challenging work problem.'
            ],
            'Libra': [
                'Diplomatic approach creates harmony in professional relationships.',
                'Balanced decisions lead to positive career outcomes.',
                'Collaboration brings mutual benefits in the workplace.'
            ],
            'Scorpio': [
                'Intense focus drives significant professional progress.',
                'Strategic thinking reveals hidden opportunities.',
                'Transformation in career path brings exciting prospects.'
            ],
            'Sagittarius': [
                'Optimistic outlook attracts positive career developments.',
                'Learning opportunities enhance professional skills.',
                'Adventure in work projects brings satisfaction and growth.'
            ],
            'Capricorn': [
                'Disciplined approach leads to long-term career success.',
                'Responsibility and hard work receive recognition.',
                'Strategic planning sets foundation for future achievements.'
            ],
            'Aquarius': [
                'Innovative ideas gain attention from decision-makers.',
                'Humanitarian approach influences workplace positively.',
                'Technology or progressive methods advance your career.'
            ],
            'Pisces': [
                'Creative intuition guides professional decisions wisely.',
                'Compassionate leadership style inspires team members.',
                'Artistic or spiritual work brings fulfillment and recognition.'
            ]
        },
        'finance': {
            'Aries': [
                'Bold financial decisions may pay off today. Calculate risks carefully.',
                'New income opportunity requires quick action.',
                'Energy invested in financial planning yields positive results.'
            ],
            'Taurus': [
                'Financial stability strengthens through conservative investments.',
                'Material security improves with practical money management.',
                'Long-term savings plans show promising growth.'
            ],
            'Gemini': [
                'Multiple income streams require organized tracking today.',
                'Communication about finances brings clarity and solutions.',
                'Versatile approach to money matters proves beneficial.'
            ],
            'Cancer': [
                'Emotional spending needs mindful attention today.',
                'Intuitive financial decisions protect your resources.',
                'Family-related expenses require budgeting and planning.'
            ],
            'Leo': [
                'Generous impulses balanced with practical considerations.',
                'Investment in personal growth pays dividends.',
                'Confidence attracts financial opportunities.'
            ],
            'Virgo': [
                'Detailed budget analysis reveals savings opportunities.',
                'Practical financial planning secures future stability.',
                'Organized approach to money management brings peace of mind.'
            ],
            'Libra': [
                'Balanced approach to spending and saving recommended.',
                'Partnership finances require fair discussion today.',
                'Aesthetic purchases balanced with financial responsibility.'
            ],
            'Scorpio': [
                'Deep financial analysis uncovers hidden opportunities.',
                'Transformative approach to money management begins.',
                'Strategic investments align with long-term goals.'
            ],
            'Sagittarius': [
                'Optimistic financial outlook attracts abundance.',
                'Learning about investments expands opportunities.',
                'Generous spirit balanced with practical wisdom.'
            ],
            'Capricorn': [
                'Disciplined financial management yields steady growth.',
                'Long-term investment strategies prove successful.',
                'Responsible money decisions build solid foundation.'
            ],
            'Aquarius': [
                'Innovative financial strategies bring unexpected gains.',
                'Technology-based investments show promise.',
                'Progressive approach to money management pays off.'
            ],
            'Pisces': [
                'Intuitive financial decisions guided by inner wisdom.',
                'Compassionate giving balanced with self-care.',
                'Creative income opportunities emerge from unexpected sources.'
            ]
        },
        'health': {
            'Aries': [
                'High energy today - channel it into physical activities.',
                'Headaches possible - stay hydrated and take breaks.',
                'Dynamic exercise routine boosts vitality and mood.'
            ],
            'Taurus': [
                'Steady routine supports physical well-being today.',
                'Throat or neck tension - gentle stretches help.',
                'Comfort foods balanced with nutritious choices recommended.'
            ],
            'Gemini': [
                'Mental activity high - balance with physical movement.',
                'Respiratory health important - breathe deeply and mindfully.',
                'Varied activities keep mind and body engaged.'
            ],
            'Cancer': [
                'Emotional well-being directly impacts physical health today.',
                'Digestive system sensitive - choose foods mindfully.',
                'Nurturing self-care practices restore balance.'
            ],
            'Leo': [
                'Vitality strong - maintain heart health through activity.',
                'Back and spine need attention - posture awareness important.',
                'Radiant energy enhanced by adequate rest and nutrition.'
            ],
            'Virgo': [
                'Digestive health focus - mindful eating practices beneficial.',
                'Detail-oriented wellness routine shows positive results.',
                'Stress management through organization and planning.'
            ],
            'Libra': [
                'Kidney and lower back health need gentle care today.',
                'Balance between rest and activity maintains well-being.',
                'Harmonious environment supports mental and physical health.'
            ],
            'Scorpio': [
                'Intense energy requires healthy outlets for expression.',
                'Reproductive and elimination systems need attention.',
                'Transformation through disciplined health practices.'
            ],
            'Sagittarius': [
                'Outdoor activities boost physical and mental health.',
                'Hip and thigh area - stretching exercises beneficial.',
                'Optimistic mindset supports healing and vitality.'
            ],
            'Capricorn': [
                'Bone and joint health - gentle movement prevents stiffness.',
                'Disciplined health routine yields long-term benefits.',
                'Responsibility to self includes adequate rest and care.'
            ],
            'Aquarius': [
                'Circulation and nervous system need attention today.',
                'Innovative wellness approaches bring positive results.',
                'Social connections support mental and emotional health.'
            ],
            'Pisces': [
                'Feet and immune system require gentle care today.',
                'Intuitive body awareness guides health choices.',
                'Spiritual practices enhance overall well-being.'
            ]
        },
        'relationships': {
            'Aries': [
                'Direct communication strengthens romantic bonds today.',
                'Passionate energy enhances intimate connections.',
                'Independence balanced with partnership needs.'
            ],
            'Taurus': [
                'Loyalty and stability deepen relationship commitment.',
                'Sensual experiences bring partners closer together.',
                'Patient understanding resolves minor conflicts.'
            ],
            'Gemini': [
                'Interesting conversations spark romantic connection.',
                'Versatility in relationships brings fresh perspective.',
                'Communication bridges understanding in partnerships.'
            ],
            'Cancer': [
                'Emotional depth strengthens intimate bonds today.',
                'Nurturing gestures express love and care effectively.',
                'Intuitive understanding of partner\'s needs prevails.'
            ],
            'Leo': [
                'Generous affection brightens partner\'s day.',
                'Romantic gestures appreciated and reciprocated.',
                'Confidence in relationships attracts positive energy.'
            ],
            'Virgo': [
                'Practical support demonstrates love and commitment.',
                'Attention to partner\'s needs strengthens connection.',
                'Helpful gestures speak louder than words today.'
            ],
            'Libra': [
                'Harmony and balance characterize relationship dynamics.',
                'Diplomatic approach resolves partnership challenges.',
                'Beauty and romance flourish in balanced connection.'
            ],
            'Scorpio': [
                'Deep emotional intimacy transforms relationships positively.',
                'Passionate connection reaches new depths today.',
                'Trust and vulnerability strengthen partnership bonds.'
            ],
            'Sagittarius': [
                'Adventurous spirit brings excitement to relationships.',
                'Philosophical discussions deepen mutual understanding.',
                'Freedom and commitment find healthy balance.'
            ],
            'Capricorn': [
                'Commitment and responsibility strengthen partnership.',
                'Long-term relationship goals align and progress.',
                'Mature approach resolves relationship challenges.'
            ],
            'Aquarius': [
                'Friendship forms strong foundation for romance.',
                'Independent togetherness characterizes healthy bond.',
                'Progressive ideas about relationships bring clarity.'
            ],
            'Pisces': [
                'Compassionate understanding deepens emotional connection.',
                'Romantic intuition guides relationship decisions.',
                'Spiritual bond enhances physical and emotional intimacy.'
            ]
        }
    }
    
    @staticmethod
    def generate_horoscope(rashi: str, date: str = None) -> Dict:
        """Generate daily horoscope for a zodiac sign"""
        if date is None:
            date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        
        if rashi not in DailyHoroscope.RASHIS:
            raise ValueError(f"Invalid rashi: {rashi}")
        
        # Use date as seed for consistency within the day
        random.seed(date + rashi)
        
        horoscope = {
            'rashi': rashi,
            'date': date,
            'career': random.choice(DailyHoroscope.TEMPLATES['career'][rashi]),
            'finance': random.choice(DailyHoroscope.TEMPLATES['finance'][rashi]),
            'health': random.choice(DailyHoroscope.TEMPLATES['health'][rashi]),
            'relationships': random.choice(DailyHoroscope.TEMPLATES['relationships'][rashi]),
            'lucky_number': random.randint(1, 100),
            'lucky_color': random.choice(['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Orange', 'White', 'Gold']),
            'overall_rating': random.randint(6, 10)
        }
        
        return horoscope
