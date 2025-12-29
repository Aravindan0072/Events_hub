backend project - minimal FastAPI + SQLite

Quick start:
1. (Optional) create and activate a virtualenv
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate    # Windows PowerShell

2. Install dependencies:
   pip install -r requirements.txt

3. Seed DB (creates app.db with dummy users):
   python seed.py

4. Run the API:
   uvicorn main:app --reload

Endpoints:
POST /users  -> create user (JSON: { "name": "", "email": "" })
GET  /       -> health check
