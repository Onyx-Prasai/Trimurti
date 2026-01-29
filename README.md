# Blood Hub Nepal - Team: Trimurti 

## Introduction
A comprehensive platform designed to streamline blood donation processes, manage blood stock efficiently, and incentivize donors through a robust reward system. It connects donors, hospitals, and blood banks to ensure timely blood availability and foster a community of regular blood donors.

## Features

### 1. Donor Management & Engagement
* **Donor Profiles**: Personalized profiles with blood group, donation history, and eligibility tracking
* **Donation Tracking**: Records donations, awards points (500 per donation), and tracks lives saved
* **Eligibility Check**: 56-day lockout period after each donation with visual calendar
* **Referral System**: 100 bonus points for successful referrals
* **Badges & Recognition**: Milestone-based recognition system
* **Blood Group Selection**: Post-login modal for blood group collection

### 2. Blood Request & Supply Management
* **Hospital Blood Requests**: Hospitals can submit urgent requests with blood type and urgency
* **Blood Stock Dashboard**: Real-time inventory overview across hospitals and blood banks
* **Automated Stock Ingestion**: Hospital API integration via BloodSync for automatic stock updates
* **Low Stock Alerts**: Proactive notifications when inventory falls below thresholds
* **Find Blood Banks**: Locate nearby blood banks with contact and operating hours
* **Blood Needs Prediction**: Time series forecasting for regional blood requirements
* **Donation Drives**: Track and manage blood donation campaigns

### 3. Reward System
* **Points for Donations**: 500 points per successful donation
* **Money Rewards**: Redeem points for cash via Esewa
* **Discount Rewards**: Partner discounts from local businesses
* **Healthcare Product Rewards**: Exchange points for medicines and healthcare items

### 4. AI-Powered Health Assistant
* **Interactive Chatbot**: Powered by Google Gemini API for health tips and donation queries
* **Blood Report Analysis**: Upload and analyze medical reports with personalized health insights
* **Nepalese Dietary Context**: Recommendations tailored to local diet and lifestyle

### 5. Multi-User Architecture
* **Donor Accounts**: Standard user accounts with profile management
* **Hospital Accounts**: Blood request and stock management
* **Blood Bank Accounts**: Inventory and operations management
* **Admin Accounts**: Platform administration and analytics

## How it Works

### Frontend (React)
* **Dashboard**: Donation history, points, badges, and calendar view
* **Blood Search**: Find blood by type and location with map view
* **AI Health**: Chatbot and medical report analysis
* **Rewards**: Browse and redeem points for rewards
* **Profile**: Manage personal info and settings

### Backend (Django REST Framework)
* **Authentication**: Token-based auth with API key support for hospitals
* **Data Models**: Robust ORM models for all entities
* **RESTful APIs**: Comprehensive endpoints for all features
* **BloodSync API**: Hospital integration with transaction ledger
* **SMS Integration**: Emergency notifications to nearby donors
* **Prediction Engine**: Time series forecasting for blood needs

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv tri

# Activate (Windows)
tri\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment (optional)
# Create .env with MISTRAL_API_KEY, SECRET_KEY, DEBUG

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Seed sample data (optional)
python manage.py seed_data
python manage.py seed_bloodsync

# Start server
python manage.py runserver
```

Backend available at `http://localhost:8000`

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend available at `http://localhost:5173`

## 📁 Project Structure

```
Trimurti/
├── backend/
│   ├── api/
│   │   ├── models.py              # Database models
│   │   ├── views.py               # API views
│   │   ├── bloodsync_views.py     # Hospital integration endpoints
│   │   ├── serializers.py         # DRF serializers
│   │   ├── urls.py                # Routes
│   │   ├── authentication.py      # API key auth
│   │   ├── utils.py               # Utilities & alerts
│   │   ├── prediction.py          # Blood needs prediction
│   │   └── admin.py               # Admin config
│   ├── bloodhub/
│   │   ├── settings.py            # Django settings
│   │   └── urls.py                # URL config
│   ├── db.sqlite3                 # Development database
│   └── manage.py                  # Django CLI
├── frontend/
│   ├── src/
│   │   ├── components/            # Reusable React components
│   │   │   ├── Logo.jsx
│   │   │   ├── Navbar.jsx
│   │   │   └── BloodGroupModal.jsx
│   │   ├── pages/                 # Page components
│   │   │   ├── Home.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── FindBlood.jsx
│   │   │   ├── BloodStockDashboard.jsx
│   │   │   ├── AIHealth.jsx
│   │   │   ├── Profile.jsx
│   │   │   ├── Points.jsx
│   │   │   └── Notification.jsx
│   │   ├── utils/
│   │   │   └── api.js             # API client
│   │   ├── App.jsx                # Main component
│   │   └── main.jsx               # Entry point
│   ├── index.html
│   └── package.json
├── BLOODSYNC_ARCHITECTURE.md      # System architecture
├── HOSPITAL_INTEGRATION_GUIDE.md  # Hospital API guide
└── README.md                      # This file
```

## 🔌 API Endpoints

### Public API

```http
GET /api/v1/public/blood-stock/
Query: city, blood_group, min_units

GET /api/v1/public/blood-availability/{city}/

GET /api/v1/public/hospitals/

GET /api/v1/public/map-data/
```

### Hospital Integration (Protected)

```http
POST /api/v1/ingest/transaction/
Headers: X-API-Key, Content-Type: application/json
Body: {
  "blood_group": "O+",
  "units_change": 5,
  "timestamp": "2026-01-27T10:00:00Z",
  "source_reference": "DON-001",
  "notes": "Optional notes"
}
```

### Core Endpoints

* `GET /api/donors/stats/` - Platform statistics
* `GET /api/donors/{id}/` - Donor profile
* `POST /api/donors/{id}/register_donation/` - Register donation
* `GET /api/hospitals/` - List hospitals (filterable)
* `GET /api/hospitals/predictions/` - Blood needs forecast
* `GET /api/bloodbanks/` - List blood banks
* `GET /api/store/` - Reward items
* `POST /api/redemptions/` - Redeem points
* `POST /api/ai-health/chat/` - Chat with AI
* `POST /api/ai-health/analyze_report/` - Analyze medical report
* `GET /api/stock/` - Public stock lookup
* `GET /api/hospital-registry/` - Hospital directory

## 🔐 Security

* **API Key Authentication**: SHA-256 hashed keys per hospital
* **HTTPS Only**: Encrypted data in transit
* **Rate Limiting**: 100 req/min per hospital
* **Input Validation**: SQL injection protection
* **CORS**: Controlled cross-origin access
* **Audit Logs**: Complete transaction history

## 🧪 Testing

```bash
# Backend tests
cd backend
python manage.py test

# API testing with curl
curl http://localhost:8000/api/v1/public/blood-stock/?city=Kathmandu
```

## 📜 License

MIT License

Copyright (c) 2026 Trimurti Team

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## 🔮 Future Enhancements

- [ ] Mobile app (React Native)
- [ ] Blockchain audit trail
- [ ] Multi-language support (Nepali)
- [ ] Offline sync mode
- [ ] WhatsApp bot integration

---

**Together, we can save lives through better blood management in Nepal.**