from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import requests
import os
import uvicorn
import logging
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from OnetWebService import OnetWebService
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

username = os.getenv("ONET_USERNAME")
password = os.getenv("ONET_PASSWORD")
onet_ws = OnetWebService(username, password)

def check_for_error(service_result):
    if 'error' in service_result:
        sys.exit(service_result['error'])

class CareerRequest(BaseModel):
    user_type: str
    skills: Optional[List[str]] = []
    interests: Optional[List[str]] = []
    move_type: Optional[str] = None
    current_job: Optional[str] = None
    career_field: Optional[str] = None

vinfo = onet_ws.call('about')
check_for_error(vinfo)
print("Connected to O*NET Web Services version " + str(vinfo['api_version']))
print("")


def fetch_onet_recommendations(skills: List[str], interests: List[str], user_type: str, move_type: str = None, current_job: str = None, career_field: str = None):
    api_key = os.getenv("API_KEY")
    if not api_key:
        logger.error("API key missing from environment variables")
        raise HTTPException(
            status_code=500,
            detail="Server configuration error: Missing API key"
        )

    base_url = "https://services.onetcenter.org/ws/mnm/"
    
    try:
        headers = {
            "Accept": "application/json"
        }

        logger.info(f"Making POST request to O*NET mnm with skills: {skills}, interests: {interests}")

        response = requests.post(
            base_url,
            auth=HTTPBasicAuth(api_key, ""),
            json={
                "user_type": user_type,
                "skills": skills,
                "interests": interests,
                "move_type": move_type,
                "current_job": current_job if user_type == "I have a job but want to move" else None,
                "career_field": career_field
            },
            headers=headers,
            timeout=10
        )

        response.raise_for_status()
        return response.json().get("occupation", [])

    except requests.exceptions.HTTPError as e:
        logger.error(f"O*NET API error: {e.response.status_code} - {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"O*NET API error: {e.response.text}"
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Network error: {str(e)}"
        )

def search_onet_careers(keyword: str):

    onet_ws.call('Search')

    api_key = os.getenv("API_KEY")
    if not api_key:
        logger.error("API key missing from environment variables")
        raise HTTPException(
            status_code=500,
            detail="Server configuration error: Missing API key"
        )
    
    search_url = "https://services.onetcenter.org/ws/mnm/search"
    

    try:
        headers = {
            #"Accept": "application/json"
            "Authorization": f"Basic: {api_key}"

        }

        logger.info(f"Searching O*NET careers with keyword: {keyword}")

        response = requests.post(
            search_url,
            auth=HTTPBasicAuth(api_key, ""),
            json={
                "keyword": keyword,
                "start": 1,
                "end": 5
            },
            headers=headers,
            timeout=10
        )
        
        response.raise_for_status()
        return response.json().get("occupation", [])

    except requests.exceptions.HTTPError as e:
        logger.error(f"O*NET API search error: {e.response.status_code} - {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"O*NET API search error: {e.response.text}"
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Network error: {str(e)}"
        )


@app.post("/recommend")
async def get_recommendations(request: CareerRequest):
    logger.info(f"Received recommendation request: {request}")
    
    if request.user_type == "I don't know what career I want":
        if not request.skills or not request.interests:
            logger.warning("Missing skills or interests in request")
            raise HTTPException(
                status_code=400,
                detail="Please provide both skills and interests"
            )
        
        try:
            occupations = fetch_onet_recommendations(request.skills, request.interests, request.user_type, request.move_type, request.current_job, request.career_field)
            
            recommendations = []
            for occupation in occupations:
                if isinstance(occupation, dict):
                    recommendation = {
                        'title': occupation.get('title', 'Unknown Occupation'),
                        'description': occupation.get('bright_outlook', {}).get('description', ''),
                        'code': occupation.get('code', '')
                    }
                    recommendations.append(recommendation)
            
            logger.info(f"Generated {len(recommendations)} recommendations")
            return {'recommendations': recommendations}
            
        except HTTPException as e:
            logger.error(f"Falling back to default recommendations due to: {str(e)}")
            return {
                'recommendations': [
                    {'title': 'Software Developer', 'description': 'Growing tech field'},
                    {'title': 'Data Analyst', 'description': 'High demand for data skills'}
                ]
            }

    elif request.user_type == "I have a job but want to move":
        # Placeholder recommendations
        onet_ws.call('mnm/interestprofiler/questions_30')
        return {
            "recommendations": [
                {"title": "Project Manager", "description": "Leads teams to meet goals."},
                {"title": "Product Owner", "description": "Oversees product development."}
            ]
        }

    elif request.user_type == "I want to apply to a specific career field":
        recommendations = []
        if not request.career_field:
            raise HTTPException(status_code=400, detail="Please specify a career field.")
        try:
            kwquery = request.career_field
            kwresults = onet_ws.call('online/search',
                                    ('keyword', kwquery),
                                    ('end', 5))
            check_for_error(kwresults)
            if (not 'occupation' in kwresults) or (0 == len(kwresults['occupation'])):
                print("No relevant occupations were found.")
                print("")
            else:
                print("Most relevant occupations for \"" + kwquery + "\":")
                for occ in kwresults['occupation']:
                    if isinstance(occ, dict):
                        title = occ.get('title', 'Unknown Occupation')
                        recommendations.append({
                            "title": title,
                            "description": f"Works in the {request.career_field} field."
                        })
                return {
                    "recommendations": recommendations
                }
        except HTTPException as e:
            logger.error(f"Search fallback due to: {str(e)}")
            return {
                "recommendations": [
                    {"title": f"{request.career_field} Specialist", "description": f"Works in the {request.career_field} field."}
                ]
            }

    raise HTTPException(status_code=400, detail="Invalid user_type")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
