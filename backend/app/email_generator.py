# app/email_generator.py

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env file for environment variables
load_dotenv()

# Configure Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_email(resume_text, job_description, matched_skills):
    """
    Generate a personalized cold email using Google's Gemini model.
    """

    prompt = f"""
You are an assistant that writes personalized cold emails.

Given the following:

Resume content:
{resume_text}

Job description:
{job_description}

Matched skills:
{matched_skills}

Write a short, professional, and polite cold email that clearly connects the candidate's experience and strengths to the job.
Avoid buzzwords and exaggeration. Keep it natural, concise, and engaging.
"""

    # Use Gemini model (fast and capable for text tasks)
    model = genai.GenerativeModel("models/gemini-2.5-pro")

    try:
        response = model.generate_content(prompt)
        return response.text.strip() if response.text else "No response generated."
    except Exception as e:
        return f"Error generating email: {e}"
