from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="MannSetu Backend API")

# Frontend cross-origin (CORS) setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development/Demo ke liye open hai
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Schemas (Pydantic Models) ---
class ConsentInput(BaseModel):
    user_id: str
    accepted: bool
    share_peer: bool = True
    share_community: bool = True
    share_professional: bool = False

class CheckinInput(BaseModel):
    user_id: str
    mood: str
    energy: int
    connection: int
    stress: int
    note: Optional[str] = ""

class SupportInput(BaseModel):
    user_id: str
    support_type: str
    language: str = "Hindi"

class FollowupInput(BaseModel):
    user_id: str
    choice: str

# --- Temporary In-Memory Storage (Demo Data) ---
consents_db = {}
checkins_db = {}
followups_db = {}

# --- API Endpoints ---

@app.get("/")
def home():
    return {"status": "MannSetu Backend is Running!"}

# 1. Save Consent API
@app.post("/api/consent")
def save_consent(data: ConsentInput):
    consents_db[data.user_id] = data.dict()
    return {"status": "success", "saved": True, "data": consents_db[data.user_id]}

# 2. Check-in Submission API (With Consent Check & Fallback Rule)
@app.post("/api/checkins")
def create_checkin(data: CheckinInput):
    # Step 6 Rule: Check consent enforcement
    user_consent = consents_db.get(data.user_id)
    if not user_consent or not user_consent.get("accepted"):
        raise HTTPException(
            status_code=403, 
            detail="Consent Missing: Check-in submit karne se pehle Consent Form accept karein."
        )

    # User ke history array mein store karein
    if data.user_id not in checkins_db:
        checkins_db[data.user_id] = []
    
    checkins_db[data.user_id].append(data.dict())
    history = checkins_db[data.user_id]

    # Rule-Based Logic / AI Fallback
    recommend_support = False
    status_msg = "baseline_normal"

    if len(history) == 1:
        status_msg = "baseline_established"
    else:
        # Check rule thresholds
        high_stress = data.stress >= 4
        low_energy = data.energy <= 2
        
        if high_stress or low_energy:
            recommend_support = True
            status_msg = "offer_optional_support"

    return {
        "status": "success",
        "change_detected": recommend_support,
        "recommendation": status_msg,
        "total_checkins": len(history)
    }

# 3. Support Match API
@app.post("/api/support/match")
def match_support(data: SupportInput):
    return {
        "status": "success",
        "match": {
            "peer_id": "peer_demo_01",
            "type": data.support_type,
            "language": data.language,
            "availability": "Available Now"
        }
    }

# 4. Follow-up Preference API
@app.post("/api/followups")
def save_followup(data: FollowupInput):
    followups_db[data.user_id] = data.dict()
    return {
        "status": "success",
        "message": f"Follow-up scheduled for {data.choice}",
        "data": followups_db[data.user_id]
    }