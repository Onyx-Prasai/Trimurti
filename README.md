# BloodHub Nepal 🩸

**Real-Time Blood Inventory Management System for Nepal**

A comprehensive, privacy-compliant platform that automatically collects and displays real-time blood inventory data from hospitals and blood banks across Nepal. Built with React.js frontend and Django REST Framework backend, integrated with AI for health assistance and ML-based shortage prediction.

---

## 🌟 Key Features

### 🏥 BloodHub Nepal Core Features
- **Real-Time Blood Inventory**: Live tracking of blood stock across all registered hospitals
- **Public Search Dashboard**: Citizens can search for blood availability by type and location
- **Secure Hospital Integration**: API-based integration with hospital management systems
- **Privacy-Compliant**: Only aggregated data (NO personal information)
- **Alert System**: Automatic low-stock alerts and donation drive suggestions
- **Interactive Map**: Visual representation of blood availability across Nepal
- **Admin Analytics**: National and regional blood stock analytics for health authorities

### 🎯 Blood Hub Features (Donor Platform)
- 🏠 **Home Page**: Hero section with real-time counters, feature grid, and call-to-action
- 🩸 **Find Blood**: Search for hospitals and blood banks by location, blood type, and name
- 📊 **Dashboard**: Track donations, view 56-day calendar, and earned badges
- 🤖 **AI Health Assistant**: Chat with AI and analyze medical reports with Nepalese dietary recommendations
- 🔔 **Notifications**: Get alerts for critical blood needs
- 🎁 **Points & Rewards**: Earn points for donations, redeem items, and refer friends
- 👤 **Profile**: Manage personal information and view statistics

---

## 🏗️ System Architecture

```
┌─────────────────┐
│   Hospitals     │──┐
│  (API Clients)  │  │
└─────────────────┘  │
                     │  HTTPS + API Key
┌─────────────────┐  │  Authentication
│  Blood Banks    │──┤
└─────────────────┘  │
                     ▼
              ┌──────────────────┐
              │  BloodSync API   │
              │   (Django DRF)   │
              └──────────────────┘
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
    ┌─────────┐ ┌────────┐ ┌────────┐
    │  Stock  │ │ Trans- │ │ Alerts │
    │ Manager │ │ actions│ │ System │
    └─────────┘ └────────┘ └────────┘
          │          │          │
          └──────────┼──────────┘
                     ▼
              ┌──────────────┐
              │   Database   │
              │  (SQLite/PG) │
              └──────────────┘
                     │
                     ▼
              ┌──────────────┐
              │ Public API   │
              └──────────────┘
                     │
                     ▼
              ┌──────────────┐
              │React Frontend│
              │  Dashboard   │
              └──────────────┘
```

---

## 💻 Tech Stack

### Frontend
- **React.js** 18.2.0 - UI framework
- **Tailwind CSS** 3.3.6 - Styling
- **Framer Motion** 10.16.16 - Animations
- **React Router DOM** 6.20.0 - Routing
- **Axios** 1.6.2 - HTTP client
- **Vite** 5.0.8 - Build tool
- **Leaflet** - Map visualization

### Backend
- **Django** 6.0 - Web framework
- **Django REST Framework** 3.16.1 - API framework
- **Django CORS Headers** - Cross-origin requests
- **SQLite** (development) / **PostgreSQL** (production)
- **Celery** + **Redis** (planned for background tasks)

### Security
- Custom API Key Authentication (SHA-256)
- HTTPS/TLS encryption
- Rate limiting
- CORS configuration
- Input validation & sanitization

### AI/ML
- **Google Gemini AI** - Health chatbot
- **Time-series forecasting** (planned) - Shortage prediction

---

## 📋 Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**:
```bash
cd backend
```

2. **Create virtual environment**:
```bash
python -m venv tri
```

3. **Activate virtual environment**:
   - Windows: `tri\Scripts\activate`
   - Linux/Mac: `source tri/bin/activate`

4. **Install dependencies**:
```bash
pip install -r requirements.txt
```

5. **Configure environment variables** (optional):
Create `.env` file in `backend/` directory:
```env
MISTRAL_API_KEY=your-mistral-api-key-here  # Optional for AI features
SECRET_KEY=your-django-secret-key
DEBUG=True
```

6. **Run migrations**:
```bash
python manage.py migrate
```

7. **Create superuser** (admin access):
```bash
python manage.py createsuperuser
```

8. **Seed sample data** (optional):
```bash
python manage.py seed_data
python manage.py seed_bloodsync  # Creates demo hospital with API key
```

9. **Run the development server**:
```bash
python manage.py runserver
```

The backend API will be available at `http://localhost:8000`

---

### Frontend Setup

1. **Navigate to frontend directory**:
```bash
cd frontend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Run the development server**:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173` (Vite default port)

---

## 📁 Project Structure

```
Trimurti/
├── backend/
│   ├── api/
│   │   ├── models.py              # Database models (Hospital, BloodStock, Transaction, etc.)
│   │   ├── views.py               # API views
│   │   ├── bloodsync_views.py     # BloodSync Nepal specific endpoints
│   │   ├── serializers.py         # DRF serializers
│   │   ├── urls.py                # API routes
│   │   ├── authentication.py      # API key authentication
│   │   ├── utils.py               # Alert system & utility functions
│   │   ├── admin.py               # Django admin configuration
│   │   └── prediction.py          # ML-based prediction (future)
│   ├── bloodhub/
│   │   ├── settings.py            # Django settings
│   │   └── urls.py                # Main URL configuration
│   ├── db.sqlite3                 # Development database
│   └── manage.py                  # Django management script
├── frontend/
│   ├── src/
│   │   ├── components/            # Reusable React components
│   │   │   ├── Logo.jsx
│   │   │   └── Navbar.jsx
│   │   ├── pages/                 # Page components
│   │   │   ├── Home.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── FindBlood.jsx
│   │   │   ├── BloodStockDashboard.jsx  # ⭐ BloodHub public dashboard
│   │   │   ├── AIHealth.jsx
│   │   │   ├── Profile.jsx
│   │   │   ├── Points.jsx
│   │   │   └── Notification.jsx
│   │   ├── utils/
│   │   │   └── api.js             # API client functions
│   │   ├── App.jsx                # Main app component
│   │   └── main.jsx               # Entry point
│   ├── index.html
│   └── package.json
├── BLOODSYNC_ARCHITECTURE.md      # ⭐ Complete system architecture
├── DEVELOPMENT_ROADMAP.md         # ⭐ Project roadmap & timeline
├── HOSPITAL_INTEGRATION_GUIDE.md  # ⭐ Hospital API integration guide
├── SETUP.md                        # Original setup instructions
└── README.md                       # This file
```

---

## 🔌 API Endpoints

### BloodHub Nepal Public API

#### Query Blood Stock
```http
GET /api/v1/public/blood-stock/
Query Parameters:
  - city: Filter by city
  - blood_group: Filter by blood group (A+, A-, B+, B-, AB+, AB-, O+, O-)
  - min_units: Minimum units required

Example: GET /api/v1/public/blood-stock/?city=Kathmandu&blood_group=O+
```

#### Get Blood Availability by City
```http
GET /api/v1/public/blood-availability/{city}/

Example: GET /api/v1/public/blood-availability/Kathmandu/
```

#### List All Hospitals
```http
GET /api/v1/public/hospitals/
```

#### Get Map Data
```http
GET /api/v1/public/map-data/
Returns: Hospital locations with current stock for map visualization
```

### BloodSync Hospital Integration API (Protected)

#### Ingest Transaction
```http
POST /api/v1/ingest/transaction/
Headers:
  X-API-Key: <hospital-api-key>
  Content-Type: application/json

Body:
{
  "blood_group": "O+",
  "units_change": 5,              // +5 for donation, -2 for usage
  "timestamp": "2026-01-27T10:00:00Z",
  "source_reference": "DON-001",  // Optional
  "notes": "Blood donation camp"  // Optional
}
```

### Admin API (Protected - Admin Only)

#### National Analytics
```http
GET /api/v1/admin/analytics/national/
Returns: National blood stock overview, critical shortages, trends
```

#### View Alerts
```http
GET /api/alerts/
Query Parameters:
  - resolved: true/false
  - alert_level: low/critical/emergency
```

#### Donation Drives
```http
GET /api/donation-drives/
POST /api/donation-drives/
```

---

## 🔐 Security & Privacy

### Data Privacy Compliance

BloodHub Nepal is designed with **privacy-first** principles:

✅ **What We Collect:**
- Total blood units available (aggregated)
- Blood group types
- Hospital name and location
- Timestamps of stock changes

❌ **What We DON'T Collect:**
- Donor personal information (name, age, contact)
- Patient details
- Medical records
- Staff information

### Security Features

- **API Key Authentication**: SHA-256 hashed keys for hospital access
- **HTTPS Only**: All data encrypted in transit
- **Rate Limiting**: Prevents API abuse (100 req/min per hospital)
- **Input Validation**: SQL injection protection
- **CORS Configuration**: Controlled cross-origin access
- **Audit Logs**: Complete transaction history

---

## 🎯 Usage Guide

### For Hospitals

1. **Register**: Contact BloodHub Nepal for onboarding
2. **Receive API Key**: Securely store your unique API key
3. **Integrate**: Use our client libraries or direct HTTP calls
4. **Report Transactions**: Automatically send stock changes

See [HOSPITAL_INTEGRATION_GUIDE.md](HOSPITAL_INTEGRATION_GUIDE.md) for detailed instructions.

### For Citizens

1. Visit the public dashboard
2. Search for blood by type and location
3. View real-time availability
4. Find nearest hospital with required blood
5. Contact hospital directly

### For Administrators

1. Access admin panel at `/admin/`
2. Register new hospitals
3. Generate API keys
4. Monitor national stock levels
5. View alerts and analytics
6. Manage donation drives

---

## 📊 Database Schema

### Core Models

**Hospital**: Registered medical facilities
- id, code, name, city, address, api_key_hash, is_active

**BloodStock**: Current inventory snapshot
- hospital, blood_group, units_available, updated_at

**Transaction**: Append-only audit ledger
- hospital, blood_group, units_change, timestamp, ingested_at

**StockAlert**: Low stock notifications
- hospital, blood_group, alert_level, threshold, current_units

**DonationDrive**: Blood donation campaigns
- title, city, blood_groups, urgency, target_units, status

See [BLOODSYNC_ARCHITECTURE.md](BLOODSYNC_ARCHITECTURE.md) for complete schema.

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
python manage.py test
```

### API Testing with curl
```bash
# Query blood stock
curl http://localhost:8000/api/v1/public/blood-stock/?city=Kathmandu

# Ingest transaction (requires API key)
curl -X POST http://localhost:8000/api/v1/ingest/transaction/ \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"blood_group":"O+","units_change":5,"timestamp":"2026-01-27T10:00:00Z"}'
```

---

## 🚀 Deployment

### Production Checklist

- [ ] Migrate to PostgreSQL
- [ ] Set up SSL/TLS certificate
- [ ] Configure environment variables
- [ ] Enable production settings (DEBUG=False)
- [ ] Set up Celery + Redis for background tasks
- [ ] Configure email/SMS services for alerts
- [ ] Set up monitoring (Sentry, Prometheus)
- [ ] Database backups
- [ ] Load balancing
- [ ] CDN for static files

### Recommended Stack

- **Web Server**: Nginx
- **App Server**: Gunicorn
- **Database**: PostgreSQL
- **Cache**: Redis
- **Task Queue**: Celery
- **Hosting**: AWS, DigitalOcean, or Heroku
- **Monitoring**: Sentry, Grafana

---

## 📚 Documentation

- **[System Architecture](BLOODSYNC_ARCHITECTURE.md)**: Complete technical design
- **[Development Roadmap](DEVELOPMENT_ROADMAP.md)**: Project timeline and milestones
- **[Hospital Integration Guide](HOSPITAL_INTEGRATION_GUIDE.md)**: API integration instructions
- **[Setup Guide](SETUP.md)**: Original setup documentation

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Coding Standards

- Follow PEP 8 for Python code
- Use ESLint/Prettier for JavaScript
- Write meaningful commit messages
- Add tests for new features
- Update documentation

---

## 📜 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🙏 Acknowledgments

- Nepal Red Cross Society
- National Blood Transfusion Service
- All participating hospitals and blood banks
- Open-source community

---

## 📞 Contact & Support

**Project Maintainer**: [Your Name]  
**Email**: bloodhub@nepal.gov  
**Website**: https://bloodhub.nepal.gov  
**Emergency Hotline**: +977-XXX-XXXXXX

---

## 🔮 Future Enhancements

- [ ] Mobile app (React Native)
- [ ] ML-based shortage prediction
- [ ] SMS alert system
- [ ] Blockchain audit trail
- [ ] Multi-language support (Nepali)
- [ ] Offline sync mode
- [ ] WhatsApp bot integration
- [ ] API for third-party apps

---

## ⭐ Star this project if you find it useful!

**Together, we can save lives through better blood management in Nepal.**

---

*Last Updated: January 27, 2026*
*Version: 2.0.0*

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


