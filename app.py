import streamlit as st
import requests

st.title("Career Recommendations")

user_type = st.radio("Select your situation:", 
                    ["I don't know what career I want", 
                     "I have a job but want to move",
                     "I want to apply to a specific career field"])

if user_type == "I have a job but want to move":
    move_type = st.selectbox("Move type:", ["Vertical", "Horizontal"])

if user_type == "I don't know what career I want":
    move_type = st.button("Take the Career Recommender Survey")

if user_type == "I want to apply to a specific career field":
    move_type = st.selectbox("Careers", ["Doctor", "Lawyer", "Engineer", "Teacher", "Software Developer", "Data Scientist", "Nurse", "Pharmacist", "Accountant", "Architect", "Graphic Designer", "Civil Engineer", "Mechanical Engineer", "Electrical Engineer", "Marketing Manager", "Sales Executive", "Financial Analyst", "UX Designer", "Product Manager", "Psychologist", "Therapist", "Dentist", "Veterinarian", "Pilot", "Flight Attendant", "Chef", "Event Planner", "Journalist", "Editor", "Author", "Copywriter", "Social Media Manager", "Human Resources Manager", "Business Analyst", "Entrepreneur", "Real Estate Agent", "Police Officer", "Firefighter", "Paramedic", "Biologist", "Chemist", "Physicist", "Mathematician", "Astronomer", "Statistician", "Environmental Scientist", "Geologist", "Economist", "Historian", "Political Scientist", "Sociologist", "Anthropologist", "Archaeologist", "Librarian", "Software Tester", "Cybersecurity Analyst", "Game Developer", "Web Developer", "Mobile App Developer", "Systems Administrator", "DevOps Engineer", "Machine Learning Engineer", "AI Researcher", "Blockchain Developer", "IT Support Specialist", "Network Engineer", "Database Administrator", "Cloud Architect", "Legal Assistant", "Paralegal", "Judge", "Court Reporter", "Interpreter", "Translator", "Musician", "Actor", "Director", "Producer", "Choreographer", "Dancer", "Photographer", "Videographer", "Interior Designer", "Fashion Designer", "Model", "Personal Trainer", "Fitness Coach", "Dietitian", "Nutritionist", "Life Coach", "Career Counselor", "Electrician", "Plumber", "Carpenter", "Mechanic", "Welder", "Truck Driver", "Construction Manager", "Surveyor", "Urban Planner"
])