from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CareerRequest(BaseModel):
    user_type: str
    move_type: Optional[str] = None
    career_field: Optional[str] = None
    skills: Optional[list[str]] = None
    interests: Optional[list[str]] = None

@app.get("/")
async def root():
    return {"message": "Career Recommendation API is running!"}

def get_onet_recommendations(skills: list[str], interests: list[str]):
    """Fetch career recommendations from O*NET API"""
    api_key = os.getenv("API")
    base_url = "https://services.onetcenter.org/ws/mnm/"

    try:
        # Example endpoint - adjust based on O*NET's available endpoints
        response = requests.get(
            f"{base_url}careers/recommended",
            params={
                "skills": ",".join(skills),
                "interests": ",".join(interests)
            },
            auth=(api_key, '')  # O*NET uses basic auth with username as API key
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"O*NET API error: {str(e)}")

@app.post("/recommend")
async def get_recommendations(request: CareerRequest):
    if request.user_type == "I don't know what career I want":
        # Example skills and interests - you would collect these from your UI
        default_skills = ["problem_solving", "communication", "teamwork"]
        default_interests = ["technology", "creative", "analytical"]
        
        try:
            onet_data = get_onet_recommendations(default_skills, default_interests)
            return {
                "source": "O*NET",
                "recommendations": [job["title"] for job in onet_data.get("careers", [])[:5]]
            }
        except HTTPException as e:
            return {"recommendations": ["Software Developer", "Data Analyst", "UX Designer"]}
    
    elif request.user_type == "I have a job but want to move":
        direction = "senior" if request.move_type == "Vertical" else "related"
        return {"recommendations": [f"{direction} positions in your field"]}
    
    elif request.user_type == "I want to apply to a specific career field":
        return {"recommendations": [f"Entry-level positions in {request.career_field}"]}
    
    return {"recommendations": ["General career advice"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)