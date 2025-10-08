# backend/main.py

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.extract import extract_keywords, extract_text_from_pdf
from app.email_generator import generate_email
import tempfile
import shutil
import os

app = FastAPI(title="Cold Email Synthesizer API")

# --- CORS Configuration ---
# Allows the React frontend (typically running on port 3000) to communicate with the FastAPI backend (e.g., port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-email")
async def generate_cold_email(
    resume: UploadFile = File(...),
    job_desc: str = Form(...)
):
    if not job_desc or resume.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid input. Ensure a PDF resume and job description are provided.")

    temp_file_path = None
    try:
        # 1. Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            shutil.copyfileobj(resume.file, tmp_file)
            temp_file_path = tmp_file.name

        # 2. Extract text, keywords, and match
        resume_text = extract_text_from_pdf(temp_file_path)

        if "Error extracting text" in resume_text or "No readable text found" in resume_text:
            raise HTTPException(status_code=500, detail=f"PDF extraction error: {resume_text}")

        resume_keywords = extract_keywords(resume_text)
        matched = [kw for kw in resume_keywords if kw.lower() in job_desc.lower()]

        # 3. Generate email using Gemini
        email = generate_email(resume_text, job_desc, matched)
        
        if "Error generating email" in email:
             raise HTTPException(status_code=500, detail=f"AI generation error: {email}")

        # 4. Return the generated email
        return {"email": email}

    except Exception as e:
        print(f"Server error: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    finally:
        # 5. Cleanup the temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)