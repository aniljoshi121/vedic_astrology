from fastapi import FastAPI, APIRouter, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone
from astrology_engine import AstrologyEngine
from kundli_matching import KundliMatching
from daily_horoscope import DailyHoroscope
from pdf_generator import JanampatriPDF
from emergentintegrations.llm.chat import LlmChat, UserMessage


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# LLM Configuration
EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY')


# ============ MODELS ============

class BirthDetailsInput(BaseModel):
    name: str
    gender: str
    date_of_birth: str  # DD-MM-YYYY
    time_of_birth: str  # HH:MM
    place_of_birth: str

class BirthChartResponse(BaseModel):
    model_config = ConfigDict(extra="allow")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    gender: str
    date_of_birth: str
    time_of_birth: str
    place_of_birth: str
    latitude: float
    longitude: float
    lagna: Dict[str, Any]
    moon_rashi: str
    moon_rashi_hindi: str
    nakshatra: Dict[str, Any]
    western_zodiac: Dict[str, Any]
    planets: Dict[str, Any]
    houses: List[Dict[str, Any]]
    ayanamsa: float
    personality: Dict[str, Any]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class KundliMatchingInput(BaseModel):
    person1: BirthDetailsInput
    person2: BirthDetailsInput

class KundliMatchingResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    matching_result: Dict[str, Any]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ChatMessage(BaseModel):
    message: str
    session_id: str
    chart_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str


# ============ ROUTES ============

@api_router.get("/")
async def root():
    return {"message": "Vedic Astrology API"}


@api_router.get("/cities")
async def get_cities():
    """Get list of predefined Indian cities"""
    from astrology_engine import AstrologyEngine
    cities = list(AstrologyEngine.INDIAN_CITIES.keys())
    cities.sort()
    return {"cities": [city.title() for city in cities]}


@api_router.post("/birth-chart", response_model=BirthChartResponse)
async def calculate_birth_chart(input_data: BirthDetailsInput):
    """Calculate complete birth chart (Janampatri)"""
    try:
        # Calculate birth chart
        chart = AstrologyEngine.calculate_birth_chart(
            name=input_data.name,
            gender=input_data.gender,
            date_str=input_data.date_of_birth,
            time_str=input_data.time_of_birth,
            place=input_data.place_of_birth
        )
        
        # Get personality analysis
        personality = AstrologyEngine.get_personality_traits(chart)
        
        # Prepare response
        response_data = {**chart, 'personality': personality}
        response_obj = BirthChartResponse(**response_data)
        
        # Save to database
        doc = response_obj.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        await db.birth_charts.insert_one(doc)
        
        return response_obj
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@api_router.get("/birth-chart/{chart_id}")
async def get_birth_chart(chart_id: str):
    """Retrieve a saved birth chart"""
    chart = await db.birth_charts.find_one({'id': chart_id}, {"_id": 0})
    
    if not chart:
        raise HTTPException(status_code=404, detail="Birth chart not found")
    
    if isinstance(chart['created_at'], str):
        chart['created_at'] = datetime.fromisoformat(chart['created_at'])
    
    return chart


@api_router.post("/kundli-matching", response_model=KundliMatchingResponse)
async def calculate_kundli_matching(input_data: KundliMatchingInput):
    """Calculate Kundli matching (Gun Milan) for marriage compatibility"""
    try:
        # Calculate birth charts for both persons
        chart1 = AstrologyEngine.calculate_birth_chart(
            name=input_data.person1.name,
            gender=input_data.person1.gender,
            date_str=input_data.person1.date_of_birth,
            time_str=input_data.person1.time_of_birth,
            place=input_data.person1.place_of_birth
        )
        
        chart2 = AstrologyEngine.calculate_birth_chart(
            name=input_data.person2.name,
            gender=input_data.person2.gender,
            date_str=input_data.person2.date_of_birth,
            time_str=input_data.person2.time_of_birth,
            place=input_data.person2.place_of_birth
        )
        
        # Calculate Gun Milan
        matching_result = KundliMatching.calculate_gun_milan(chart1, chart2)
        
        # Prepare response
        response_obj = KundliMatchingResponse(matching_result=matching_result)
        
        # Save to database
        doc = response_obj.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        await db.kundli_matching.insert_one(doc)
        
        return response_obj
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@api_router.get("/daily-horoscope/{rashi}")
async def get_daily_horoscope(rashi: str, date: Optional[str] = None):
    """Get daily horoscope for a zodiac sign"""
    try:
        horoscope = DailyHoroscope.generate_horoscope(rashi, date)
        return horoscope
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@api_router.post("/generate-pdf/{chart_id}")
async def generate_pdf_report(chart_id: str):
    """Generate PDF Janampatri report"""
    try:
        # Fetch chart from database
        chart = await db.birth_charts.find_one({'id': chart_id}, {"_id": 0})
        
        if not chart:
            raise HTTPException(status_code=404, detail="Birth chart not found")
        
        # Generate PDF
        pdf_path = JanampatriPDF.generate_pdf(chart, chart.get('personality', {}))
        
        return FileResponse(
            pdf_path,
            media_type='application/pdf',
            filename=f"janampatri_{chart['name']}.pdf"
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@api_router.post("/chat", response_model=ChatResponse)
async def chat_with_astrologer(input_data: ChatMessage):
    """AI-powered astrology chat assistant"""
    try:
        # Get chart context if chart_id provided
        chart_context = ""
        if input_data.chart_id:
            chart = await db.birth_charts.find_one({'id': input_data.chart_id}, {"_id": 0})
            if chart:
                chart_context = f"""
User's Birth Chart:
- Name: {chart['name']}
- Moon Sign (Rashi): {chart['moon_rashi']}
- Ascendant (Lagna): {chart['lagna']['rashi']}
- Nakshatra: {chart['nakshatra']['nakshatra']}
- Planetary Positions: {', '.join([f"{p}: {d['rashi']}" for p, d in chart['planets'].items()])}
"""
        
        # System message for AI astrologer
        system_message = f"""You are an expert Vedic astrologer with deep knowledge of Indian Jyotish.
You provide insightful, compassionate guidance based on birth charts and planetary positions.

{chart_context}

Guidelines:
- Explain astrological concepts in simple, accessible language
- Provide both English and Hindi terms when relevant
- Be supportive and encouraging in your guidance
- Avoid making medical or legal claims
- Focus on personality insights, life guidance, and spiritual growth
- If asked about compatibility, doshas, or specific predictions, reference the user's chart data
- Keep responses concise but informative
"""
        
        # Initialize LLM Chat
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=input_data.session_id,
            system_message=system_message
        ).with_model("openai", "gpt-5.2")
        
        # Create user message
        user_message = UserMessage(text=input_data.message)
        
        # Get AI response
        ai_response = await chat.send_message(user_message)
        
        # Save chat history to database
        chat_record = {
            'session_id': input_data.session_id,
            'chart_id': input_data.chart_id,
            'user_message': input_data.message,
            'ai_response': ai_response,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        await db.chat_history.insert_one(chat_record)
        
        return ChatResponse(response=ai_response, session_id=input_data.session_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/chat-history/{session_id}")
async def get_chat_history(session_id: str):
    """Retrieve chat history for a session"""
    history = await db.chat_history.find(
        {'session_id': session_id},
        {"_id": 0}
    ).sort('timestamp', 1).to_list(100)
    
    return {"session_id": session_id, "messages": history}


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
