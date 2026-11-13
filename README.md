# CodingBodhi AI Chatbot

## Run locally

1. Install Python 3.10 or later.
2. In PowerShell, from the project directory:

   ```powershell
   cd backend
   py -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   if (!(Test-Path .env)) { Copy-Item .env.example .env }
   ```

3. Add a valid `GEMINI_API_KEY` to `backend/.env`.
4. Start the app from `backend`:

   ```powershell
   uvicorn main:app --reload
   ```

5. Open <http://127.0.0.1:8000>. The API health check is at
   <http://127.0.0.1:8000/health>, and interactive API docs are at
   <http://127.0.0.1:8000/docs>.

If `DATABASE_URL` is unset, SQLite is used and the database file is created at
`backend/codingbodhi.db`. If `DATABASE_URL` is set, the app uses that configured
database; for PostgreSQL, provide a SQLAlchemy PostgreSQL URL in `backend/.env`.

The browser keeps an anonymous user ID and the active conversation in local
storage. This supports conversation continuity on that browser, but is not an
account or authentication system.
