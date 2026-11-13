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

## Deploy on Vercel

The project root is the Vercel root directory. The root `main.py` exposes the
FastAPI app, and the root `requirements.txt` installs the backend dependencies.

Conversation history requires persistent storage. Before deploying, create a
PostgreSQL database (for example, with Neon) and configure these environment
variables in the Vercel project settings:

- `DATABASE_URL`: the database's PostgreSQL connection string. Use the pooled
  connection string if the provider offers one.
- `GEMINI_API_KEY`: a valid Google AI Studio API key.

Do not commit either value. The app rejects SQLite on Vercel because serverless
storage is not durable. `GEMINI_MODEL` and `GEMINI_FALLBACK_MODEL` are optional.

To deploy, import `jerlineharsha/codingbodhi-ai-chatbot` into Vercel, keep the
project root as the root directory, add the environment variables, and deploy.
After deployment, check `/health` and open the site URL to verify the app.
