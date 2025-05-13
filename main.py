from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

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

@app.get("/")
async def root():
    return {"message": "Career Recommendation API is running!"}

@app.post("/recommend")
async def get_recommendations(request: CareerRequest):
    # Your recommendation logic here
    if request.user_type == "I don't know what career I want":
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