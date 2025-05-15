import streamlit as st
import requests
from streamlit_extras.colored_header import colored_header

# Configure the backend URL
BACKEND_URL = "http://127.0.0.1:8000/recommend"

st.title("Career Recommendations")
colored_header(label="Find Your Perfect Career", description="", color_name="blue-70")

# User input section
user_type = st.radio("Select your situation:", 
                    ["I don't know what career I want", 
                     "I have a job but want to move",
                     "I want to apply to a specific career field"])

if user_type == "I have a job but want to move":
    move_type = st.selectbox("Move type:", ["Vertical", "Horizontal"])
elif user_type == "I want to apply to a specific career field":
    career_field = st.selectbox("Select career field:", 
                              ["Information Technology", "Healthcare", 
                               "Business", "Engineering", "Arts"])

# Additional inputs for O*NET recommendations
if user_type == "I don't know what career I want":
    st.subheader("Tell us about yourself")
    skills = st.multiselect("Your top skills:",
                          ["Problem Solving", "Communication", "Teamwork", 
                           "Leadership", "Creativity", "Technical Writing"])
    interests = st.multiselect("Your interests:",
                             ["Technology", "Creative Arts", "Analytical Work",
                              "Helping People", "Management", "Outdoor Activities"])

if st.button("Get Career Recommendations", type="primary"):
    # Prepare request data
    data = {
        "user_type": user_type,
        "move_type": move_type if user_type == "I have a job but want to move" else None,
        "career_field": career_field if user_type == "I want to apply to a specific career field" else None,
        "skills": skills if user_type == "I don't know what career I want" else None,
        "interests": interests if user_type == "I don't know what career I want" else None
    }
    
    with st.spinner("Finding the best career matches..."):
        try:
            response = requests.post(BACKEND_URL, json=data)
            if response.status_code == 200:
                result = response.json()
                st.success("Here are your personalized career recommendations:")
                
                if result.get("source") == "O*NET":
                    st.markdown("🔍 Powered by O*NET data")
                
                for rec in result["recommendations"]:
                    st.markdown(f"🏆 **{rec}**")
                    # Add more details about each career if available
                
                st.markdown("---")
                st.info("Want more details? Visit [O*NET Online](https://www.onetonline.org/)")
            else:
                st.error(f"Error: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Connection failed: {str(e)}")