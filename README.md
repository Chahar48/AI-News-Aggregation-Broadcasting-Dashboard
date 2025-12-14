# AI-News-Aggregation-Broadcasting-Dashboard
Built an AI News Aggregation &amp; Broadcasting Dashboard as an MVP. The system ingests AI-related news, normalizes and deduplicates it, stores it in PostgreSQL, and exposes APIs using FastAPI. A React/Next.js dashboard displays the news feed, allows users to favorite items, and broadcast selected news via Email, LinkedIn, WhatsApp, Blog, or Newsletter

📰 AI News Aggregation & Broadcasting Dashboard (MVP)

Author: Mukesh Kumar
Project Type: MVP Prototype
Backend: FastAPI + PostgreSQL
Frontend: Next.js (React)
AI Integration: Groq (summarization & content generation – mocked where required)

📌 Project Overview

This project is an MVP AI-powered news aggregation dashboard that collects AI-related news from multiple high-signal sources, deduplicates them, displays them in a dashboard, allows users to mark favorites, and broadcast selected news via Email, LinkedIn, WhatsApp, Blog, or Newsletter (mocked).

The goal of this MVP is to demonstrate system design, backend engineering, data handling, and AI integration, not to build a full-scale production scraper.


🎯 Key Features Implemented

✅ AI News Feed Dashboard
✅ Deterministic / Seeded Ingestion (Reliable MVP Mode)
✅ Deduplication Logic
✅ PostgreSQL Database Integration
✅ Favorites System
✅ Broadcast Simulation (Email / LinkedIn / WhatsApp / Newsletter)
✅ Modular Backend Architecture
✅ Frontend Dashboard (React / Next.js)


🧠 Why Seeded Data (Important Design Decision)

Live scraping from 20+ sources is inherently unreliable for interview demos due to:

Rate limits
RSS/API downtime
HTML structure changes

Therefore, this MVP uses deterministic seeded data to ensure:

✔ Dashboard always works
✔ Favorites always work
✔ Broadcast always works
✔ Zero demo risk

The ingestion pipeline is live-ready and can be switched to real sources with minimal changes.

🧩 System Architecture
[Seeded / RSS Sources]
        ↓
[Fetcher Service]
        ↓
[Parser & Normalizer]
        ↓
[Deduplication Logic]
        ↓
[PostgreSQL Database]
        ↓
[FastAPI REST APIs]
        ↓
[Next.js Dashboard]
        ↓
[Broadcast Services (Mocked)]

🗄️ Database Schema (PostgreSQL)
| Table            | Purpose                         |
| ---------------- | ------------------------------- |
| `sources`        | Registered news sources         |
| `news_items`     | Aggregated AI news              |
| `favorites`      | User-favorited news             |
| `broadcast_logs` | Broadcast history               |
| `users`          | Optional user table (MVP-ready) |


🛠 Tech Stack

#Backend

FastAPI
SQLAlchemy ORM
PostgreSQL
Pydantic
Uvicorn

#Frontend

Next.js
React
Tailwind CSS
SWR

#AI

Groq (used for content generation & summaries)
Mocked safely for MVP reliability


```text
ai-news-dashboard/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI app entry point
│   │   ├── config.py                # Environment & app configuration
│   │   │
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── news.py           # News listing & retrieval APIs
│   │   │       ├── favorites.py      # Favorites management APIs
│   │   │       ├── broadcast.py      # Broadcast execution & logs APIs
│   │   │       └── admin.py          # Admin & source management APIs
│   │   │
│   │   ├── models/
│   │   │   ├── db.py                # Database session & engine
│   │   │   ├── orm_models.py        # SQLAlchemy ORM models
│   │   │   └── schemas.py           # Pydantic request/response schemas
│   │   │
│   │   ├── services/
│   │   │   ├── ingestion/
│   │   │   │   ├── fetcher.py       # Source fetching abstraction
│   │   │   │   ├── parsers.py       # RSS / source parsers
│   │   │   │   └── schedule.py      # Ingestion scheduling logic
│   │   │   │
│   │   │   ├── normalizer.py        # Data normalization layer
│   │   │   ├── deduper.py           # Deduplication logic
│   │   │   ├── embedder.py          # Embedding / semantic utilities
│   │   │   ├── summarizer.py        # AI-powered summarization
│   │   │   └── broadcaster.py       # Broadcast engine
│   │   │
│   │   ├── tasks/
│   │   │   ├── worker.py            # Background worker (Celery/RQ-ready)
│   │   │   └── jobs.py              # Async / scheduled jobs
│   │   │
│   │   └── utils/
│   │       ├── logger.py            # Centralized logging
│   │       └── http_client.py       # HTTP utilities & retries
│   │
│   ├── Dockerfile                  # Backend Docker configuration
│   └── requirements.txt            # Python dependencies
│
├── frontend/
│   ├── package.json                # Frontend dependencies
│   ├── next.config.js              # Next.js configuration
│   ├── tailwind.config.js          # Tailwind CSS configuration
│   └── src/
│       ├── pages/
│       │   ├── index.tsx            # News feed page
│       │   └── favorites.tsx        # Favorites page
│       │
│       ├── components/
│       │   ├── NewsCard.tsx         # News item UI component
│       │   └── BroadcastModal.tsx   # Broadcast UI modal
│       │
│       └── lib/
│           └── api.ts               # API client & helpers
│
└── README.md                       # Project documentation
```



🚀 How to Run Locally (Step-by-Step)
1️⃣ Clone the Repository
git clone https://github.com/Chahar48/AI-News-Aggregation-Broadcasting-Dashboard.git
cd AI_News_Dashboard

2️⃣ Backend Setup
Create Virtual Environment
python -m venv venv

Activate Virtual Environment

#Windows
venv\Scripts\activate

#Mac/Linux
source venv/bin/activate

3️⃣ Install Backend Dependencies
cd backend
pip install -r requirements.txt

4️⃣ Setup PostgreSQL

Create a PostgreSQL database (via pgAdmin)
Update DB connection in .env or database.py

Example:

DATABASE_URL=postgresql://postgres:password@localhost:5432/ai_news_db

5️⃣ Run Database Migrations / Create Tables
python -c "from app.models.db import Base, engine; Base.metadata.create_all(bind=engine)"

6️⃣ Start Backend Server
uvicorn app.main:app --reload


Backend will run at:
http://127.0.0.1:8000


Swagger Docs:
http://127.0.0.1:8000/docs

7️⃣ Frontend Setup
cd ../frontend
npm install
npm run dev


Frontend will run at:

http://localhost:3000


🚀 Deployment (Dockerized Setup)

This project is fully containerized and can be run locally or deployed on any Docker-compatible platform (AWS, Render, Fly.io, DigitalOcean).

📦 Services Included

FastAPI Backend – news ingestion, favorites, broadcast APIs
Next.js Frontend – dashboard UI
PostgreSQL – persistent database
RQ Worker – async ingestion & broadcast jobs

🛠 Prerequisites
Docker (v20+)
Docker Compose (v2+)

▶️ Run Locally with Docker

From the project root:
docker-compose up --build

This will:

Build backend & frontend images
Start PostgreSQL with persistent storage
Start FastAPI backend
Start background worker
Start Next.js frontend

🌐 Access URLs
Service	URL
Frontend Dashboard	http://localhost:3000
Backend API	http://localhost:8000
API Docs	http://localhost:8000/docs


🔄 How the System Works (End-to-End)
🔁 Ingestion

/api/v1/news/refresh

Uses seeded data (MVP mode)
Ensures sources exist
Normalizes news
Deduplicates
Saves to DB

📰 News Feed

/api/v1/news

Paginated feed
Displayed on dashboard

⭐ Favorites

/api/v1/favorites
Save/remove favorites
Persistent DB storage

📣 Broadcast

/api/v1/broadcast

Mock Email / LinkedIn / WhatsApp / Newsletter
Logs stored in broadcast_logs

🧪 API Endpoints (Core)
| Method | Endpoint                 | Purpose            |
| ------ | ------------------------ | ------------------ |
| GET    | `/api/v1/news`           | Get news feed      |
| POST   | `/api/v1/news/refresh`   | Refresh ingestion  |
| POST   | `/api/v1/favorites`      | Add favorite       |
| GET    | `/api/v1/favorites`      | List favorites     |
| POST   | `/api/v1/broadcast`      | Broadcast favorite |
| GET    | `/api/v1/broadcast/logs` | Broadcast history  |


Live scraping disabled (seeded data used)
No full-text search
No user authentication

🔮 Future Improvements

Enable live RSS/API ingestion
Background ingestion jobs
Embedding-based deduplication
Full-text search & filters
Docker + CI/CD
Real Email/WhatsApp APIs

🏁 Final Notes

This project was designed as a clean, reliable MVP that demonstrates:

System architecture
Backend engineering
AI integration
Database design
Frontend integration

All design decisions were made intentionally to maximize demo reliability and clarity.

📬 Contact

Mukesh Kumar
📧 chaharmukesh518@gmail.com
🔗 https://github.com/Chahar48 / https://www.linkedin.com/in/mukeshchahar/
