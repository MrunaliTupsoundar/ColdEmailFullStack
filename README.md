# CES Full Stack Project

A full stack application with a FastAPI backend and a React frontend. The backend provides APIs for email generation and PDF extraction, while the frontend offers a user-friendly interface.

---

## Features

- **FastAPI Backend:** Handles API requests, email generation, and PDF extraction.
- **React Frontend:** Clean UI for interacting with backend services.
- **File Uploads:** Supports file uploads via API.
- **Environment Configuration:** Uses `.env` for sensitive settings.

---

## Tech Stack

- **Backend:** Python, FastAPI, Uvicorn, pdfminer.six, spaCy, Google Generative AI
- **Frontend:** React (Create React App), JavaScript

---

## Project Structure

```
CES_full_stack/
│
├── README.md
├── LICENSE
├── .gitignore
├── backend/
└── frontend/
```

---

## Installation & Setup

### 1. Clone the Repository

```bash
git https://github.com/MrunaliTupsoundar/ColdEmailFullStack.git
cd ColdEmailFullStack
```

---

### 2. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # On Windows
# source venv/bin/activate   # On Mac/Linux

pip install -r requirements.txt
```

- **Create a `.env` file in the `backend` folder and add your environment variables.**
- **For example:**
    ```
    GOOGLE_API_KEY=your_google_api_key_here
    # Add other environment variables as needed
    ```

#### Run the Backend Server

```bash
uvicorn main:app 
```

---

### 3. Frontend Setup

```bash
cd ../frontend
npm install
```

#### Run the Frontend App

```bash
npm start
```

The frontend will run on [http://localhost:3000](http://localhost:3000) by default.

---

## Usage

- Access the frontend at [http://localhost:3000](http://localhost:3000).
- The frontend communicates with the backend API at [http://localhost:8000](http://localhost:8000).
- Make sure both servers are running.

---

## Notes

- If you run frontend and backend on different ports, ensure CORS is enabled in FastAPI.
- Update API endpoints in the frontend if backend URL changes.
- Sensitive files and folders (like `venv/`, `node_modules/`, `.env`, and caches) are excluded from version control using `.gitignore`.

---

## License

This project is licensed under the MIT License.
