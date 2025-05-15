import streamlit as st
import requests

# FastAPI endpoint
BACKEND_URL = "http://127.0.0.1:8000/recommend"

st.title("Career Recommendations")

# User input section
user_type = st.radio(
    "Select your situation:",
    [
        "I don't know what career I want", 
        "I have a job but want to move",
        "I want to apply to a specific career field"
    ]
)

# Initialize variables
skills = []
interests = []
move_type = None
career_field = None

# Dynamic form based on user type
if user_type == "I don't know what career I want":
    st.subheader("Tell us about your skills and interests")
    
    # Skill selection
    skills = st.multiselect(
        "Select your top skills:",
        ["Problem Solving", "Communication", "Teamwork", 
         "Leadership", "Creativity", "Technical Writing",
         "Data Analysis", "Programming", "Design"]
    )
    
    # Interest selection
    interests = st.multiselect(
        "Select your interests:",
        ["Technology", "Creative Arts", "Analytical Work",
         "Helping People", "Management", "Outdoor Activities",
         "Science", "Business", "Healthcare"]
    )

elif user_type == "I have a job but want to move":
    current_job = st.selectbox("Select career field:", 
                              ["Information Technology", "Healthcare", 
                               "Business", "Engineering", "Arts"])
    move_type = st.selectbox("Are you looking for a horizontal or vertical move?", ["Vertical", "Horizontal"])

elif user_type == "I want to apply to a specific career field":
    career_field = st.selectbox("Select career field:", 
                              ["Information Technology", "Healthcare", 
                               "Business", "Engineering", "Arts"])

# Submit button
if st.button("Get Recommendations"):
    try:
        response = requests.post(
            BACKEND_URL,
            json={
                "user_type": user_type,
                "skills": [s.lower().replace(" ", "_") for s in skills],
                "interests": [i.lower() for i in interests],
                "move_type": move_type,
                "career_field": career_field
            }
        )
        
        if response.status_code == 200:
            results = response.json()
            if "recommendations" in results:
                st.success("Recommended careers for you:")
                for idx, career in enumerate(results["recommendations"], 1):
                    # Safely access dictionary values
                    title = career.get("title", "Unknown Career")
                    description = career.get("description", "No description available")
                    
                    st.markdown(f"### {idx}. {title}")
                    st.write(description)
                    st.markdown("---")
            else:
                st.error("Unexpected response format from API")
        else:
            st.error(f"API Error: {response.text}")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")