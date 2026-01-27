# Blood Hub Nepal

A professional-grade, health-themed blood donation platform for Nepal. Built with React.js frontend and Django REST Framework backend, integrated with Google Gemini AI for health assistance.

## Features

- 🏠 **Home Page**: Hero section with real-time counters, feature grid, and call-to-action
- 🩸 **Find Blood**: Search for hospitals and blood banks by location, blood type, and name and also shows blood prediction where blood is needed and mapping algorithm
- 📊 **Dashboard**: Track donations, view 56-day calendar, and see earned badges
- 🤖 **AI Health Assistant**: Chat with AI and analyze medical reports with Nepalese dietary recommendations
- 🔔 **Notifications**: Get alerts for critical blood needs
- 🎁 **Points & Rewards**: Earn points for donations, redeem items, and refer friends
- 👤 **Profile**: Manage personal information and view statistics
- 🌐 **BloodSync**: Real-time hospital stock ingestion via API key protected endpoint and live public stock lookup

## Tech Stack

### Frontend
- React.js 18.2.0
- Tailwind CSS 3.3.6
- Framer Motion 10.16.16
- React Router DOM 6.20.0
- Axios 1.6.2
- Vite 5.0.8

### Backend
- Django 4.2.7
- Django REST Framework 3.14.0
- Google Gemini API
- SQLite (development) — replace with PostgreSQL for production

### AI/ML 

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the `backend` directory and add your Gemini API key:
```
GEMINI_API_KEY='your-real-api-key'
```
   You can obtain a Gemini API key from the Google AI Platform.


6. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

7. Seed initial data (optional, for development):
```bash
python manage.py seed_data
```

8. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

9. (Optional) Generate a demo hospital + API key for BloodSync ingestion:
```bash
python manage.py seed_bloodsync
```
The command prints a `X-API-Key` value you can use for posting transactions.

10. Run the development server:
```bash
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Project Structure

```
BloodH/
├── backend/
│   ├── api/
│   │   ├── models.py          # Database models
│   │   ├── views.py            # API views
│   │   ├── serializers.py     # DRF serializers
│   │   ├── urls.py            # API routes
│   │   └── prediction.py      # Blood needs prediction
│   ├── bloodhub/
│   │   ├── settings.py        # Django settings
│   │   └── urls.py            # Main URL config
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/             # Page components
│   │   ├── utils/             # API utilities
│   │   └── App.jsx            # Main app component
│   └── package.json
└── README.md
```

## Key Features Implementation

### 56-Day Donation Lockout
The dashboard implements a 56-day lockout period after each donation. The calendar visually shows:
- **Green**: Days when donation is available
- **Yellow**: Days within the 56-day lockout period
- **Gray**: Past dates

### Points System
- 100 points awarded per confirmed donation
- 20 bonus points for successful referrals
- Points can be redeemed for store items

### Gamification Badges
- **First Drop**: Earned after first donation
- **Life Saver**: Earned after 5 donations

### AI Health Assistant
- Chat interface for health questions
- Medical report analysis with Nepalese dietary recommendations
- Powered by Google Gemini API

### Blood Needs Prediction
The backend includes a prediction model that analyzes:
- Active hospital requests vs. available donors
- Regional blood shortages
- Urgency scores for each blood type and city

## API Endpoints

- `GET /api/donors/stats/` - Platform statistics
- `GET /api/donors/{id}/` - Donor profile
- `POST /api/donors/{id}/register_donation/` - Register donation
- `GET /api/hospitals/` - List hospitals (with filters)
- `GET /api/hospitals/predictions/` - Blood needs predictions
- `GET /api/bloodbanks/` - List blood banks
- `GET /api/store/` - Store items
- `POST /api/redemptions/` - Redeem points
- `POST /api/ai-health/chat/` - AI chat
- `POST /api/ai-health/analyze_report/` - Analyze medical report
- `POST /api/ingest/transactions/` - Hospital-side ingestion (headers: `X-API-Key`, body: `hospital_id`, `blood_group`, `units_change`, `timestamp`)
- `GET /api/stock/` - Public stock lookup (filters: `blood_group`, `city`)
- `GET /api/hospital-registry/` - Public registry of participating hospitals
- `GET /api/transactions/` - Read-only transaction ledger (filters: `hospital_id`, `blood_group`)

## BloodSync Prototype Architecture
- **Hospital adapter**: lightweight service/plugin in the hospital’s HIS/LIS that calls `POST /api/ingest/transactions/` on donation received or unit issued events. Only non-personal data is sent.
- **Central ingestion**: API key authentication per hospital, append-only `Transaction` ledger, and materialized `BloodStock` table updated atomically.
- **Public availability**: `GET /api/stock/` serves current units per hospital/blood group for the React dashboard. Polling every ~15s in the prototype; upgradeable to WebSockets/SSE.
- **Data model**: `Hospital` (with hashed API key), `Transaction` (units_change, timestamp), `BloodStock` (current counts).
- **Security**: HTTPS (configure in deployment), per-hospital API key, optional request signing in future, no personal data in payloads.


