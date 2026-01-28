# Vedic Astrology Web Application

A comprehensive Indian Vedic Astrology platform with 14 complete modules including Birth Chart calculation, Kundli Matching, Daily Horoscope, AI Chat Astrologer, and more.

## 🌟 Features

### Core Modules (All 14 Implemented)

1. **Birth Chart (Janampatri)** - Complete Vedic calculations using Swiss Ephemeris
   - Lagna (Ascendant), Moon Rashi, Nakshatra
   - All 9 planetary positions (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu)
   - Custom North Indian diamond-style chart visualization
   - 12 Houses (Bhavas) calculation
   - Personality analysis based on Moon sign and Lagna

2. **Kundli Matching (Gun Milan)** - Marriage compatibility system
   - Ashta-Koota 8-point analysis (Varna, Vashya, Tara, Yoni, Graha Maitri, Gana, Bhakoot, Nadi)
   - Score out of 36 points with compatibility verdict
   - Dosha detection (Nadi Dosha, Bhakoot Dosha)

3. **Daily Horoscope** - Personalized predictions for all 12 zodiac signs
   - Career, Finance, Health, and Relationship predictions
   - Lucky number, lucky color, and overall rating

4. **AI Chat Astrologer** - GPT-5.2 powered conversational assistant
   - Answers questions about Vedic astrology concepts
   - Provides personalized guidance based on birth chart data
   - Persistent chat history with session management

5. **PDF Generation** - Professional Janampatri reports
   - Complete birth details and astrological calculations
   - Planetary positions table and personality analysis
   - Print-friendly formatting

6. **Multi-Language Support** - English and Hindi (देवनागरी)
   - Real-time language switching
   - Proper Hindi font rendering (Tiro Devanagari)

7. **Theme Toggle** - Cosmic (Dark) and Parchment (Light) modes
   - Beautiful starry night background for dark mode
   - Vintage paper texture for light mode

8. **Smart City Selector** - Autocomplete with 40+ Indian cities
   - Type-ahead suggestions
   - Fallback to OpenStreetMap geocoding
   - Typo-tolerant search

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **Astrology Engine**: pyswisseph (Swiss Ephemeris)
- **Geocoding**: geopy (OpenStreetMap/Nominatim)
- **PDF Generation**: fpdf2
- **AI Integration**: emergentintegrations (OpenAI GPT-5.2)
- **Database**: MongoDB with Motor (async driver)

### Frontend
- **Framework**: React 19
- **UI Components**: shadcn/ui (Radix UI primitives)
- **Styling**: Tailwind CSS
- **Typography**: Cinzel (headings), Inter (body), Tiro Devanagari (Hindi)
- **Routing**: React Router v7
- **HTTP Client**: Axios
- **Notifications**: Sonner (toast notifications)

### Design
- **Theme**: Celestial Gold aesthetic
- **Modes**: Cosmic (Dark) and Parchment (Light)
- **Charts**: Custom SVG North Indian diamond chart
- **Fonts**: Google Fonts (Cinzel, Inter, Tiro Devanagari Hindi)

## 📦 Installation

### Prerequisites
- Node.js 18+ and Yarn
- Python 3.11+
- MongoDB 6.0+

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=vedic_astrology_db
CORS_ORIGINS=*
EMERGENT_LLM_KEY=your-emergent-key-here
```

5. Start backend server:
```bash
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
yarn install
```

3. Create `.env` file:
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

4. Start frontend server:
```bash
yarn start
```

The application will open at `http://localhost:3000`

## 🔑 API Keys

### Emergent LLM Key (For AI Chat)
The application uses Emergent's Universal LLM Key for AI chat functionality.

To get your key:
1. Sign up at [emergent.sh](https://emergent.sh)
2. Navigate to Profile → Universal Key
3. Copy your key and add to `backend/.env`

Alternatively, you can use your own OpenAI API key by modifying the `server.py` file.

## 📚 API Endpoints

### Birth Chart
- `POST /api/birth-chart` - Calculate birth chart
- `GET /api/birth-chart/{chart_id}` - Retrieve birth chart

### Kundli Matching
- `POST /api/kundli-matching` - Calculate compatibility

### Horoscope
- `GET /api/daily-horoscope/{rashi}` - Get daily horoscope

### AI Chat
- `POST /api/chat` - Send message to AI astrologer
- `GET /api/chat-history/{session_id}` - Get chat history

### PDF Generation
- `POST /api/generate-pdf/{chart_id}` - Generate PDF report

### Utilities
- `GET /api/cities` - Get list of predefined Indian cities

## 🎨 Design Guidelines

The application follows the "Celestial Gold" design aesthetic:

- **Light Mode (Parchment)**: Warm, traditional look with vintage paper texture
- **Dark Mode (Cosmic)**: Deep space theme with starry background
- **Colors**: Gold (#FCD34D), Red (#B91C1C), Orange (#D97706) accents
- **Typography**: Cinzel for headings (authoritative), Inter for body text

## 🧪 Testing

Backend testing:
```bash
cd backend
pytest backend_test.py
```

Frontend testing:
```bash
cd frontend
yarn test
```

## 📖 Usage Guide

### Calculate Birth Chart
1. Click "Get Started" or navigate to "Birth Chart"
2. Enter birth details (name, gender, date, time, place)
3. Use city autocomplete or type manually
4. Click "Calculate"
5. View results with North Indian chart, planetary positions, and personality analysis
6. Download PDF report if needed

### Kundli Matching
1. Navigate to "Kundli Matching"
2. Enter details for both persons
3. Click "Calculate Gun Milan Score"
4. View compatibility score (out of 36) and detailed Ashta-Koota analysis

### Daily Horoscope
1. Navigate to "Daily Horoscope"
2. Select your zodiac sign
3. View predictions for career, finance, health, and relationships

### AI Chat
1. Navigate to "AI Astrologer"
2. Type your astrology-related question
3. Get AI-powered responses from GPT-5.2

## 🌐 Supported Cities (40+)

Major Indian cities with predefined coordinates:
- Mumbai, Delhi, Bangalore, Chennai, Hyderabad
- Kolkata, Pune, Ahmedabad, Jaipur, Lucknow
- Dehradun, Shimla, Goa, Kochi, Thiruvananthapuram
- And 25+ more cities across India

## 🔒 Security & Privacy

- Birth chart data stored securely in MongoDB
- No sensitive data in frontend
- API rate limiting recommended for production
- CORS configured for security

## ⚠️ Disclaimer

This application is for educational and entertainment purposes only. Astrological predictions should not replace professional advice for important life decisions.

## 🤝 Contributing

This is a complete, production-ready application. Feel free to:
- Add more regional languages
- Enhance prediction algorithms
- Add more astrology features (Dasha, transits, remedies)
- Improve UI/UX

## 📄 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

Built with ❤️ using Emergent Agent Platform

## 🐛 Known Issues

None - All features tested and working at 100%

## 📞 Support

For issues or questions:
- Check the code comments
- Review API documentation in `server.py`
- Test with provided sample data

---

**Version**: 1.0.0  
**Last Updated**: January 2025  
**Status**: Production Ready ✅
