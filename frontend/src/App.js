// frontend/src/App.js

import React, { useState, useRef } from 'react';
import axios from 'axios';
import './App.css'; 

// Assuming FastAPI runs on port 8000
const API_URL = 'http://localhost:8000'; 

function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Ref for the hidden file input
  const fileInputRef = useRef(null); 

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setEmail('');

    if (!resumeFile || !jobDescription) {
      setError("⚠️ Please upload a resume (PDF) and paste the job description.");
      return;
    }
    
    if (resumeFile.type !== 'application/pdf') {
        setError("⚠️ Only PDF files are supported for the resume.");
        return;
    }

    setIsLoading(true);

    const formData = new FormData();
    formData.append('resume', resumeFile);
    formData.append('job_desc', jobDescription);

    try {
      const response = await axios.post(`${API_URL}/generate-email`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setEmail(response.data.email);
    } catch (err) {
      console.error("API Error:", err);
      const errorMessage = err.response?.data?.detail || 'Failed to generate email due to an unknown error.';
      setError(`❌ Error: ${errorMessage}`);
    } finally {
      setIsLoading(false);
    }
  };

  // Function to trigger the click on the hidden file input
  const handleCustomButtonClick = () => {
    fileInputRef.current.click();
  };

  return (
    <div className="container">
      <h1>📧 Cold Email Synthesizer</h1>
      
      <form onSubmit={handleSubmit} className="form-card">
        
        {/* 1. RESUME UPLOAD SECTION */}
        <div className="form-group">
          {/* Main Label for the Resume section */}
          <label htmlFor="resume-upload-section">📄 Resume Upload (PDF only)</label> 
          
          <div className="custom-file-upload-container">
            {/* The Visible, Styled Button */}
            <button 
              type="button" 
              className="custom-file-button" 
              onClick={handleCustomButtonClick}
            >
              ⬆️ Choose Resume File
            </button>

            {/* Display the selected file name for user feedback */}
            <label className="file-name-display">
                {resumeFile ? resumeFile.name : "No file chosen"}
            </label>

            {/* The Actual Hidden Input */}
            <input 
              id="resume-upload"
              type="file" 
              accept=".pdf" 
              ref={fileInputRef} 
              onChange={(e) => setResumeFile(e.target.files[0])} 
              style={{ display: 'none' }} 
            />
          </div>
        </div>
        
        {/* 2. JOB DESCRIPTION PASTE SECTION */}
        <div className="form-group">
          <label htmlFor="job-desc">💼 Paste the job description or company information here</label>
          <textarea
            id="job-desc" // CRITICAL ID for CSS selector
            rows="12"
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="E.g., Senior Python Developer role requiring experience with AWS, Pandas, and machine learning..."
          />
        </div>

        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Processing and Generating...' : '✉️ Generate Cold Email'}
        </button>
      </form>

      {error && <p className="message error-message">{error}</p>}
      {isLoading && <p className="message loading-message">Connecting your resume to the job description...</p>}
      
      {email && (
        <section className="output-card">
          <h2>✅ Generated Cold Email</h2>
          <pre className="email-output">{email}</pre>
        </section>
      )}
    </div>
  );
}

export default App;