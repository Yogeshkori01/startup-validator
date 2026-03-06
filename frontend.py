import streamlit as st
import requests

API_URL = "https://startup-validator-api.onrender.com/analyze"

st.title("🚀 AI Startup Idea Validator")

st.write("Enter your startup idea and get AI-powered analysis.")

idea = st.text_area("Startup Idea")

if st.button("Analyze Idea"):

    if idea.strip() == "":
        st.warning("Please enter a startup idea.")

    else:

        try:
            response = requests.post(API_URL, json={"idea": idea})

            if response.status_code == 200:

                result = response.json()

                st.subheader("Full API Response")
                st.json(result)

                analysis = result.get("ai_analysis", {})

                st.subheader("Category")
                st.write(analysis.get("category", "Not available"))

                st.subheader("Viability Score")
                st.write(analysis.get("viability_score", "Not available"))

                st.subheader("Difficulty")
                st.write(analysis.get("difficulty", "Not available"))

                st.subheader("Similar Startups")
                for s in analysis.get("similar_startups", []):
                    st.write("-", s)

                st.subheader("Suggestions")
                for sug in analysis.get("suggestions", []):
                    st.write("-", sug)

            else:
                st.error(f"API Error: {response.status_code}")

        except Exception as e:
            st.error(f"Error connecting to API: {e}")