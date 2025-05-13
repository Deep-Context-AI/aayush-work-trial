import streamlit as st
import requests

# Configure the backend URL
BACKEND_URL = "http://127.0.0.1:8000/recommend"

st.title("Career Recommendations")

# User input section
user_type = st.radio("Select your situation:", 
                    ["I don't know what career I want", 
                     "I have a job but want to move",
                     "I want to apply to a specific career field"])

move_type = None
career_field = None

if user_type == "I have a job but want to move":
    move_type = st.selectbox("Move type:", ["Vertical", "Horizontal"])
elif user_type == "I want to apply to a specific career field":
    career_field = st.selectbox("Careers", ["Software Developer", "Data Scientist", "UX Designer"])

if st.button("Get Recommendations"):
    # Prepare request data
    data = {
        "user_type": user_type,
        "move_type": move_type,
        "career_field": career_field
    }
    
    try:
        response = requests.post(BACKEND_URL, json=data)
        if response.status_code == 200:
            recommendations = response.json().get("recommendations", [])
            st.success("Recommendations:")
            for rec in recommendations:
                st.write(f"- {rec}")
        else:
            st.error(f"API Error: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Connection failed: {str(e)}")