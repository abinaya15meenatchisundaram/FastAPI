
# 🚀 FastAPI Project

A simple FastAPI project with modular routing, database integration, and structured project layout.  
This project demonstrates how to build scalable APIs with FastAPI.

---

## 📂 Project Structure



---

## ⚡ Features

- Modular FastAPI project structure
- RESTful API endpoints
- SQLAlchemy for database models
- Pydantic for request/response validation
- Router-based architecture (`/posts`, `/users`)
- Environment-ready for scaling

---

## 🛠️ Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/fastapi.git
cd fastapi
```
2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```
3. Install dependencies:
 ```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

Start the FastAPI server:
 ```bash
uvicorn app.main:app --reload
```
Server will run at:
👉 http://127.0.0.1:8000

--- 

## 📌 API Endpoints

- GET /posts → Fetch all posts
- POST /posts → Create a new post
- GET /posts/{id} → Fetch a post by ID
- DELETE /posts/{id} → Delete a post by ID
- GET /users → Fetch all users
- POST /users → Create a new user
- GET /users/{id} → Fetch user by ID

---

## 📖 Documentation
Once the server is running, explore the interactive API docs:

- Swagger UI → http://127.0.0.1:8000/docs
- ReDoc → http://127.0.0.1:8000/redoc

---

## ✅ Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- Postman API
- PGAdmin

