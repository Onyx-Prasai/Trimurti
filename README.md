# Trimurti - Blood Management and Donor Reward System

## Introduction
A comprehensive platform designed to streamline blood donation processes, manage blood stock efficiently, and incentivize donors through a robust reward system. It connects donors, hospitals, and blood banks to ensure timely blood availability and foster a community of regular blood donors. 

## Features

### 1. Donor Management & Engagement
*   **Donor Profiles**: Personalized profiles for donors, tracking their blood group, donation history, and eligibility.
*   **Donation Tracking**: Records individual donations, awards points, and provides insights into lives saved.
*   **Eligibility Check**: Automatically determines donor eligibility based on last donation date.
*   **Referral System**: Incentivizes new donor sign-ups through referral bonuses.
*   **Badges & Recognition**: Recognizes and rewards donors with badges based on their donation milestones.
*   **Location-Based Services**: Allows donors to share their location for efficient matching with nearby blood requests, with privacy consent.

### 2. Blood Request & Supply Management
*   **Hospital Blood Requests**: Hospitals can submit urgent blood requests with details on blood type, product, and urgency.
*   **Emergency Blood Requests**: Users can initiate emergency blood requests, triggering SMS notifications to nearby location matching donors.
*   **Blood Stock Dashboard**: Real-time overview of blood stock levels across participating hospitals and blood banks.
*   **Automated Stock Ingestion**: Hospitals can integrate to automatically update blood stock levels via API, recording all transactions.
*   **Low Stock Alerts**: Proactive notifications for hospitals when blood stock falls below critical thresholds.
*   **Find Blood Banks**: Locate nearby blood banks with contact information and operating hours.
*   **Blood Needs Prediction**: Utilizes predictive analysis to forecast regional blood requirements, aiding in proactive resource allocation using time series forecasting.
*   **Donation Drives**: Management and tracking of planned blood donation campaigns, including target collection and progress.

### 3. Reward System
*   **Points for Donations**: Donors earn points for each successful blood donation.
*   **Money Rewards**: Redeem earned points for cash through platforms like Esewa.
*   **Discount Rewards**: Unlock exclusive discounts from various businesses (restaurants, pharmacies, etc.) using points.
*   **Medicine/Healthcare Product Rewards**: Exchange points for essential medicines or healthcare products.

### 4. AI-Powered Health Assistant
*   **Interactive Chatbot**: An AI assistant (powered by Mistral AI) providing health tips, nutritional advice, and answers to blood donation-related queries, with a focus on natural remedies and Nepalese dietary context.
*   **Blood Report Analysis**: Upload blood report images or PDFs for AI-driven analysis, offering personalized health insights, dietary recommendations, lifestyle tips, and wellness advice, while strictly avoiding medical diagnoses or prescriptions.

### 5. Multi-User Architecture
*   **Donor Accounts**: Standard user accounts for blood donors.
*   **Hospital Accounts**: Dedicated accounts for hospitals to manage requests and stock.
*   **Blood Bank Accounts**: Accounts for blood banks to manage their operations.
*   **Admin Accounts**: Administrative access for platform management.

## How it Works

### Frontend (User Interface)
The frontend, built with React, provides an intuitive and responsive user experience:
*   **Dashboard**: A personalized hub for donors to view their donation history, points, badges, and recent activities.
*   **Blood Request/Find Blood**: Interfaces for requesting blood or searching for available blood/blood banks using filters and map views.
*   **AI Health**: A dedicated section for interacting with the AI chatbot and uploading blood reports for analysis.
*   **Rewards**: A catalog of available rewards (money, discounts, medicines) where users can browse and redeem their points.
*   **Profile & Settings**: Users can manage their personal information, location consent, and security settings.

### Backend (API & Business Logic)
The backend, powered by Django REST Framework, handles all data management, business logic, and third-party integrations:
*   **User & Profile Management**: Securely manages user authentication, donor profiles, and specific profiles for hospitals, blood banks, and administrators.
*   **Data Models**: Robust data models (using Django ORM) for Donors, Hospitals, Blood Banks, Donations, Blood Requests, Rewards, Stock, Transactions, and more.
*   **API Endpoints**: A comprehensive set of RESTful APIs to facilitate communication between the frontend and backend, enabling all core functionalities.
*   **SMS Service Integration**: Integrates with an SMS gateway (e.g., Twilio) to send timely notifications to potential donors for emergency blood requests, utilizing location-based matching.
*   **AI Integration**: Connects with Mistral AI for the health assistant chatbot and blood report analysis features, ensuring responsible and health-focused recommendations.
*   **Blood Stock Logic**: Manages the append-only transaction ledger and materialized blood stock views, updating in real-time as hospitals ingest data.
*   **Prediction Engine**: Processes historical data to predict future blood needs, exposed via an API endpoint uses time series forecasting .

## Getting Started

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
- Donor personal information (name, age, contact, blood group)
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
### For Citizens

1. Visit the public dashboard
2. Search for blood by type and location
3. View real-time availability
4. Find nearest hospital with required blood
5. Contact hospital directly
6. If want blood contact hospital and the hospital will call the nearest person for donation

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

## 🔮 Future Enhancements

- [ ] Mobile app (React Native)
- [ ] Blockchain audit trail
- [ ] Multi-language support (Nepali)
- [ ] Offline sync mode
- [ ] WhatsApp bot integration
- [ ] API for third-party apps

---

2
**Together, we can save lives through better blood management in Nepal.**

---

## Blood Group Selection Feature

### Overview
A modal popup appears after user login to collect blood group information. This enhances user onboarding and ensures critical health data is captured.

### User Experience
1. **After Login**: User successfully authenticates
2. **Modal Appears**: Beautiful red-themed modal with blood group options
3. **Selection**: User selects from 8 blood groups (A+, A-, B+, B-, AB+, AB-, O+, O-)
4. **Action**: User can either:
   - Click **"Submit"** to save blood group and proceed to dashboard
   - Click **"Do It Later"** to skip and proceed to dashboard
5. **Future Update**: User can update blood group anytime from profile settings

### Implementation Details

**Frontend Components:**
- `frontend/src/components/BloodGroupModal.jsx` - Modal component with:
  - Blood drop icon header
  - 4-column responsive grid for blood group options
  - Submit and "Do It Later" buttons
  - Smooth slide-in animation
  - Loading state during submission

**Modified Files:**
- `frontend/src/pages/Login.jsx` - Updated login flow to show modal after authentication
- `frontend/src/index.css` - Added slideIn animation keyframes

**Backend API:**
- **Endpoint**: `PUT /api/donor-profile/update-blood-group/`
- **Authentication**: Required (Token-based)
- **Request**: `{ "blood_group": "A+" }`
- **Response**: `{ "message": "Blood group updated successfully", "blood_group": "A+" }`
- **Validation**: Only valid blood groups (A+, A-, B+, B-, AB+, AB-, O+, O-) accepted

## Key Features Implementation

### 56-Day Donation Lockout
The dashboard implements a 56-day lockout period after each donation. The calendar visually shows:
- **Green**: Days when donation is available
- **Yellow**: Days within the 56-day lockout period
- **Gray**: Past dates

### Points System
- 500 points awarded per confirmed donation
- 100 bonus points for successful referrals
- Points can be redeemed for store items

### AI Health Assistant
- Chat interface for health questions
- Medical report analysis with Nepalese dietary recommendations
- Powered by Google Gemini API

### Blood Needs Prediction
The backend includes a prediction model that analyzes:
- Active hospital requests vs. available donors
- Regional blood shortages
- Urgency scores for each blood type and city
- Time series forecasting with auto regression and moving average combined  

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


