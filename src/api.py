import json
import logging
import os
import uuid
import requests
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from src.storage import storage

# --- DevOps Setup & Configuration ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
app = FastAPI(title="LLM Ticket Classifier API", version="2.5.0")

# Configure Gemini (Using 2.5 Flash)
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(
        'gemini-2.5-flash', 
        generation_config={"response_mime_type": "application/json"}
    )
else:
    logger.error("GEMINI_API_KEY is missing!")

# --- Data Models ---
class TicketRequest(BaseModel):
    ticket_text: str = Field(..., min_length=1, max_length=2000)

# --- Webhook Alert Function ---
def trigger_alert(ticket_id: str, category: str, text: str):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL") 
    if not webhook_url:
        return
    payload = {
        "content": f"🚨 **CRITICAL TICKET ALERT** 🚨\n**ID:** {ticket_id}\n**Category:** {category.upper()}\n**Issue:** {text[:100]}..."
    }
    try:
        requests.post(webhook_url, json=payload)
    except Exception as e:
        logger.error(f"Failed to send webhook: {e}")

# --- API Endpoints ---
@app.get("/health")
def health(): 
    return {"status": "healthy", "db_mode": "SQLite" if storage.use_sqlite else "MongoDB"}

@app.post("/predict")
def predict_and_store(request: TicketRequest):
    text = request.ticket_text
    logger.info(f"Processing ticket: {text[:20]}...")
    
    prompt = f"""
    Analyze this customer support ticket.
    CATEGORIES ALLOWED: "billing", "technical", "account", "feature_request", "general"
    URGENCY ALLOWED: "low", "medium", "high"
    
    RULES: 
    1. Determine urgency based purely on the tone and severity of the customer's text. Do not default to medium.
    2. Confidence should be a float between 0.0 and 1.0.
    3. Write a polite, professional 2-3 sentence 'draft_response' email addressing the customer's specific issue.
    
    Ticket Text: "{text}"
    
    Return ONLY a valid JSON object matching this schema exactly: 
    {{"category": "...", "urgency": "...", "confidence": 0.0, "draft_response": "..."}}
    """
    
    try:
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        }
        response = model.generate_content(prompt, safety_settings=safety_settings)
        
        # PROPER JSON EXTRACTION FIX:
        # Use regex to find the JSON dictionary, ignoring any markdown backticks
        raw_text = response.text.strip()
        json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        
        if json_match:
            clean_json_string = json_match.group(0)
            result = json.loads(clean_json_string)
        else:
            raise ValueError("No valid JSON found in LLM response.")
        
        category = result.get("category", "general").lower()
        urgency = result.get("urgency", "medium").lower()
        confidence = float(result.get("confidence", 0.90))
        draft = result.get("draft_response", "Thank you for reaching out. An agent will assist you shortly.")
        
    except Exception as e:
        logger.error(f"LLM Error: {e}")
        category, urgency, confidence, draft = "general", "high", 0.50, "System Error generating response."

    payload = {
        "ticket_id": str(uuid.uuid4())[:8],
        "ticket_text": text,
        "category": category,
        "urgency": urgency,
        "confidence": round(confidence, 2),
        "draft_response": draft
    }
    
    if urgency == "high":
        trigger_alert(payload["ticket_id"], category, text)
        
    storage.save_ticket(payload.copy())
    return payload

@app.get("/stats")
def get_stats(): 
    return storage.get_stats()

@app.get("/history")
def get_history(): 
    return storage.get_recent_tickets()

@app.delete("/ticket/{ticket_id}")
def resolve_ticket(ticket_id: str):
    try:
        storage.delete_ticket(ticket_id)
        logger.info(f"Ticket {ticket_id} resolved and deleted.")
        return {"status": "success", "message": f"Ticket {ticket_id} removed."}
    except Exception as e:
        logger.error(f"Failed to delete ticket: {e}")
        raise HTTPException(status_code=500, detail="Database deletion failed.")