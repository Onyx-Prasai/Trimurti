# BloodHub Nepal - System Architecture

## 🏭️ System Overview

BloodHub Nepal is a real-time blood inventory management system that collects aggregated, non-personal blood stock data from hospitals and blood banks across Nepal. The system provides a public dashboard for blood availability search while maintaining strict privacy compliance with Nepal's National Blood Policy.

---

## 📐 System Architecture Diagram

```
┌────────────────────────────────────────────────────────────────────┐
│                         BLOODHUB NEPAL                              │
│                   Real-Time Blood Inventory System                   │
└────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                     HOSPITAL / BLOOD BANK LAYER                      │
│                                                                       │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐            │
│  │  Hospital A  │   │  Hospital B  │   │  Blood Bank  │            │
│  │   (Kathmandu)│   │  (Bhaktapur) │   │  (Lalitpur)  │            │
│  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘            │
│         │ API Key           │ API Key           │ API Key            │
│         │ (HTTPS)           │ (HTTPS)           │ (HTTPS)            │
└─────────┼───────────────────┼───────────────────┼────────────────────┘
          │                   │                   │
          ▼                   ▼                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      INTEGRATION MODULE                              │
│                                                                       │
│  • Hospital Management System Plugin/Webhook                         │
│  • Auto-detects blood stock changes (donations, usage)               │
│  • Sends aggregated data only (no personal info)                     │
│  • Encrypted HTTPS transmission                                      │
└─────────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                               │
│                    (Django REST Framework)                           │
│                                                                       │
│  ┌────────────────────────────────────────────────────────┐         │
│  │  Authentication & Authorization                         │         │
│  │  • API Key Validation (SHA-256)                        │         │
│  │  • Hospital ID Verification                            │         │
│  │  • Rate Limiting                                       │         │
│  └────────────────────────────────────────────────────────┘         │
│                                                                       │
│  ┌────────────────────────────────────────────────────────┐         │
│  │  API Endpoints                                         │         │
│  │  POST /api/v1/ingest/transaction                       │         │
│  │  GET  /api/v1/public/blood-stock                       │         │
│  │  GET  /api/v1/public/hospitals                         │         │
│  │  GET  /api/v1/admin/analytics                          │         │
│  └────────────────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     BUSINESS LOGIC LAYER                             │
│                                                                       │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐   │
│  │ Stock Manager    │  │ Alert System     │  │ ML Predictor    │   │
│  │ • Update stocks  │  │ • Low stock      │  │ • Shortage pred │   │
│  │ • Log changes    │  │ • Critical alert │  │ • Demand trends │   │
│  └──────────────────┘  └──────────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      DATABASE LAYER (SQLite/PostgreSQL)              │
│                                                                       │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐          │
│  │  Hospital   │  │  BloodStock  │  │  Transaction      │          │
│  │  Table      │  │  Table       │  │  (Ledger)         │          │
│  │             │  │              │  │                   │          │
│  │ • id        │  │ • hospital   │  │ • hospital        │          │
│  │ • code      │  │ • blood_grp  │  │ • blood_group     │          │
│  │ • name      │  │ • units      │  │ • units_change    │          │
│  │ • api_key   │  │ • updated_at │  │ • timestamp       │          │
│  └─────────────┘  └──────────────┘  └───────────────────┘          │
└─────────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                              │
│                      (React + Vite Frontend)                         │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────┐        │
│  │              PUBLIC WEB DASHBOARD                        │        │
│  │                                                          │        │
│  │  🔍 Search by Blood Type & Location                     │        │
│  │  📊 Real-Time Stock Display                             │        │
│  │  🗺️  Interactive Map View                               │        │
│  │  ⏱️  Last Updated Timestamps                            │        │
│  │  📈 Regional Availability Charts                        │        │
│  └─────────────────────────────────────────────────────────┘        │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────┐        │
│  │              ADMIN PANEL (Health Authorities)            │        │
│  │                                                          │        │
│  │  📊 National Stock Overview                             │        │
│  │  🚨 Critical Shortage Alerts                            │        │
│  │  📈 Historical Trends & Analytics                       │        │
│  │  🏥 Hospital Management                                 │        │
│  │  🔑 API Key Generation                                  │        │
│  └─────────────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      NOTIFICATION LAYER                              │
│                                                                       │
│  📧 Email Alerts   📱 SMS Alerts   🔔 Push Notifications             │
│  • Low stock warnings to hospitals                                   │
│  • Critical shortage alerts to health authorities                    │
│  • Donation drive recommendations                                    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔐 Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. TRANSPORT LAYER                                          │
│     ✓ HTTPS/TLS 1.3 Encryption                             │
│     ✓ Certificate Pinning                                   │
│                                                              │
│  2. AUTHENTICATION LAYER                                     │
│     ✓ API Key per Hospital (SHA-256 hashed)                │
│     ✓ Key Rotation Support                                  │
│     ✓ Rate Limiting (100 req/min per hospital)             │
│                                                              │
│  3. AUTHORIZATION LAYER                                      │
│     ✓ Hospital can only update own data                     │
│     ✓ Public read-only access to aggregated data           │
│     ✓ Admin panel requires authentication                   │
│                                                              │
│  4. DATA PRIVACY LAYER                                       │
│     ✓ No personal data collection                           │
│     ✓ Only aggregated inventory data                        │
│     ✓ Compliance with Nepal National Blood Policy          │
│                                                              │
│  5. INFRASTRUCTURE LAYER                                     │
│     ✓ Database encryption at rest                           │
│     ✓ Regular security audits                               │
│     ✓ CORS configuration                                    │
│     ✓ SQL injection prevention                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Database Schema

### Core Tables

#### 1. **Hospital** (Registered medical facilities)
```sql
CREATE TABLE Hospital (
    id              UUID PRIMARY KEY,
    code            VARCHAR(50) UNIQUE NOT NULL,    -- e.g., "TU-HOSPITAL"
    name            VARCHAR(200) NOT NULL,          -- e.g., "Tribhuvan University Teaching Hospital"
    city            VARCHAR(100) NOT NULL,          -- e.g., "Kathmandu"
    address         TEXT,
    latitude        DECIMAL(9,6),
    longitude       DECIMAL(9,6),
    api_key_hash    VARCHAR(128) NOT NULL,          -- SHA-256 hashed API key
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_hospital_code ON Hospital(code);
CREATE INDEX idx_hospital_active ON Hospital(is_active);
```

#### 2. **BloodStock** (Current inventory snapshot)
```sql
CREATE TABLE BloodStock (
    id              UUID PRIMARY KEY,
    hospital_id     UUID REFERENCES Hospital(id),
    blood_group     VARCHAR(3) NOT NULL,            -- A+, A-, B+, B-, AB+, AB-, O+, O-
    units_available INTEGER DEFAULT 0,
    updated_at      TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(hospital_id, blood_group)
);

CREATE INDEX idx_bloodstock_hospital ON BloodStock(hospital_id);
CREATE INDEX idx_bloodstock_bloodgroup ON BloodStock(blood_group);
CREATE INDEX idx_bloodstock_units ON BloodStock(units_available);
```

#### 3. **Transaction** (Append-only audit log)
```sql
CREATE TABLE Transaction (
    id              UUID PRIMARY KEY,
    hospital_id     UUID REFERENCES Hospital(id),
    blood_group     VARCHAR(3) NOT NULL,
    units_change    INTEGER NOT NULL,               -- +5 (donation), -2 (issued)
    timestamp       TIMESTAMP NOT NULL,             -- When change occurred
    ingested_at     TIMESTAMP DEFAULT NOW(),        -- When we received it
    source_reference VARCHAR(100),                  -- Hospital's internal ref
    notes           VARCHAR(255),
    
    INDEX idx_transaction_hospital(hospital_id),
    INDEX idx_transaction_timestamp(timestamp),
    INDEX idx_transaction_bloodgroup(blood_group)
);
```

#### 4. **StockAlert** (Low stock notifications)
```sql
CREATE TABLE StockAlert (
    id              UUID PRIMARY KEY,
    hospital_id     UUID REFERENCES Hospital(id),
    blood_group     VARCHAR(3) NOT NULL,
    alert_level     VARCHAR(20),                    -- 'low', 'critical', 'emergency'
    threshold       INTEGER,
    current_units   INTEGER,
    triggered_at    TIMESTAMP DEFAULT NOW(),
    resolved_at     TIMESTAMP NULL,
    notified        BOOLEAN DEFAULT FALSE
);
```

#### 5. **DonationDrive** (Suggested campaigns)
```sql
CREATE TABLE DonationDrive (
    id              UUID PRIMARY KEY,
    city            VARCHAR(100),
    blood_groups    TEXT,                           -- JSON array: ["O+", "A-"]
    urgency         VARCHAR(20),                    -- 'normal', 'urgent', 'critical'
    target_units    INTEGER,
    collected_units INTEGER DEFAULT 0,
    start_date      DATE,
    end_date        DATE,
    status          VARCHAR(20),                    -- 'planned', 'active', 'completed'
    created_at      TIMESTAMP DEFAULT NOW()
);
```

---

## 🔌 API Endpoint Design

### **1. Hospital Integration API** (Protected - Requires API Key)

#### POST `/api/v1/ingest/transaction`
**Purpose**: Hospital systems send blood stock changes

**Headers**:
```
X-API-Key: <hospital_api_key>
Content-Type: application/json
```

**Request Body**:
```json
{
  "blood_group": "O+",
  "units_change": 5,
  "timestamp": "2026-01-27T14:30:00Z",
  "source_reference": "DON-2026-001234",
  "notes": "Blood donation camp"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "transaction_id": "uuid-here",
  "current_stock": {
    "blood_group": "O+",
    "units_available": 45,
    "updated_at": "2026-01-27T14:30:05Z"
  }
}
```

**Error Responses**:
- `401 Unauthorized`: Invalid API key
- `400 Bad Request`: Invalid data format
- `429 Too Many Requests`: Rate limit exceeded

---

### **2. Public Query API** (Open - No Authentication)

#### GET `/api/v1/public/blood-stock`
**Purpose**: Search available blood inventory

**Query Parameters**:
```
?city=Kathmandu
&blood_group=O+
&min_units=5
```

**Response** (200 OK):
```json
{
  "results": [
    {
      "hospital": {
        "code": "TU-HOSPITAL",
        "name": "Tribhuvan University Teaching Hospital",
        "city": "Kathmandu",
        "address": "Maharajgunj, Kathmandu",
        "latitude": 27.7353,
        "longitude": 85.3320
      },
      "stock": {
        "O+": {"units": 45, "updated_at": "2026-01-27T14:30:05Z"},
        "A+": {"units": 32, "updated_at": "2026-01-27T12:15:00Z"},
        "B+": {"units": 18, "updated_at": "2026-01-27T10:00:00Z"}
      }
    }
  ],
  "total_hospitals": 1,
  "last_sync": "2026-01-27T14:30:05Z"
}
```

#### GET `/api/v1/public/hospitals`
**Purpose**: List all registered hospitals

**Response**:
```json
{
  "hospitals": [
    {
      "code": "TU-HOSPITAL",
      "name": "Tribhuvan University Teaching Hospital",
      "city": "Kathmandu",
      "location": {"lat": 27.7353, "lng": 85.3320}
    }
  ]
}
```

#### GET `/api/v1/public/blood-availability/{city}`
**Purpose**: Get aggregated availability by city

**Response**:
```json
{
  "city": "Kathmandu",
  "total_hospitals": 8,
  "aggregated_stock": {
    "O+": 245,
    "O-": 45,
    "A+": 189,
    "A-": 32,
    "B+": 156,
    "B-": 28,
    "AB+": 78,
    "AB-": 15
  },
  "last_updated": "2026-01-27T14:35:00Z"
}
```

---

### **3. Admin API** (Protected - Admin Authentication)

#### GET `/api/v1/admin/analytics/national`
**Purpose**: National blood stock overview

**Response**:
```json
{
  "total_units": 1245,
  "critical_shortages": [
    {
      "city": "Pokhara",
      "blood_group": "AB-",
      "total_units": 3,
      "hospitals_affected": 2
    }
  ],
  "low_stock_alerts": 12,
  "trend": "declining"
}
```

#### POST `/api/v1/admin/hospitals`
**Purpose**: Register new hospital

**Request**:
```json
{
  "code": "PATAN-HOSPITAL",
  "name": "Patan Hospital",
  "city": "Lalitpur",
  "address": "Lagankhel, Lalitpur"
}
```

**Response**:
```json
{
  "hospital_id": "uuid-here",
  "api_key": "plaintext-key-shown-only-once",
  "message": "Hospital registered successfully. Save the API key securely."
}
```

#### GET `/api/v1/admin/alerts`
**Purpose**: Get active shortage alerts

---

## 🚀 Development Roadmap

### **Phase 1: Foundation (Weeks 1-2)** ✅ Current Stage
- [x] Database schema design
- [x] Core models (Hospital, BloodStock, Transaction)
- [x] API key authentication system
- [ ] Basic API endpoints (ingest, query)
- [ ] Admin panel for hospital registration

### **Phase 2: Integration Module (Weeks 3-4)**
- [ ] Hospital integration SDK/plugin
- [ ] Webhook support for real-time updates
- [ ] Sample integration with popular hospital software
- [ ] API documentation with Swagger/OpenAPI
- [ ] Testing with 2-3 pilot hospitals

### **Phase 3: Public Dashboard (Weeks 5-6)**
- [ ] React frontend with real-time updates
- [ ] Search and filter functionality
- [ ] Interactive map with hospital locations
- [ ] Responsive mobile design
- [ ] Blood availability heat map

### **Phase 4: Alert System (Weeks 7-8)**
- [ ] Low stock detection algorithm
- [ ] Email notification system
- [ ] SMS alerts for critical shortages
- [ ] Donation drive suggestion engine
- [ ] Admin alert dashboard

### **Phase 5: Advanced Features (Weeks 9-12)**
- [ ] ML-based shortage prediction
- [ ] Historical trend analysis
- [ ] Regional analytics dashboard
- [ ] Offline sync for unstable internet
- [ ] Mobile app (React Native)

### **Phase 6: Deployment & Scaling (Weeks 13-14)**
- [ ] Production deployment (AWS/DigitalOcean)
- [ ] SSL certificate setup
- [ ] Database migration to PostgreSQL
- [ ] Load balancing and caching
- [ ] Security audit and penetration testing

### **Phase 7: Nationwide Rollout (Weeks 15+)**
- [ ] Onboard 50+ hospitals across Nepal
- [ ] Partnership with Nepal Red Cross Society
- [ ] Integration with National Blood Transfusion Service
- [ ] Public awareness campaign
- [ ] Training materials for hospital staff

---

## 🔒 Security & Privacy Compliance

### **Nepal National Blood Policy Compliance**

✅ **Data Minimization**
- Only collect aggregated inventory data
- No personal donor information (name, age, contact)
- No patient details
- No medical history

✅ **Transparency**
- Public access to stock availability
- Last updated timestamps visible
- Hospital names and locations disclosed
- Clear data usage policy

✅ **Security Measures**
- HTTPS encryption for all data transfer
- API key authentication (SHA-256 hashed)
- Database encryption at rest
- Regular security audits
- Rate limiting to prevent abuse

✅ **Access Control**
- Hospitals can only update their own data
- Admin panel restricted to health authorities
- Public API is read-only
- Audit logs for all transactions

✅ **Data Retention**
- Transaction logs kept for 2 years (audit trail)
- Old alerts purged after resolution
- Hospital can request data deletion

### **HTTPS Implementation Checklist**
- [ ] Obtain SSL/TLS certificate (Let's Encrypt)
- [ ] Configure HTTPS-only redirects
- [ ] Enable HSTS headers
- [ ] Set secure cookie flags
- [ ] Implement certificate pinning for mobile apps

### **API Security Checklist**
- [x] API key authentication implemented
- [ ] Rate limiting (100 requests/min per hospital)
- [ ] Input validation and sanitization
- [ ] SQL injection prevention (using ORM)
- [ ] CORS configuration
- [ ] API versioning (/api/v1/)

---

## 🏥 Integration Guide for Hospitals

### **Step 1: Registration**
1. Hospital admin contacts bloodhub Nepal
2. Admin registers hospital in system
3. Unique API key generated (shown only once)
4. Hospital securely stores API key

### **Step 2: Integration Options**

#### **Option A: Plugin/Module**
Install bloodhub plugin in existing hospital management system:
```python
# Example Python integration
import bloodhub_client

client = bloodhub_client.Client(api_key="YOUR_API_KEY")

# When blood donation received
client.report_transaction(
    blood_group="O+",
    units_change=5,  # 5 units added
    timestamp="2026-01-27T10:00:00Z"
)

# When blood issued to patient
client.report_transaction(
    blood_group="O+",
    units_change=-2,  # 2 units used
    timestamp="2026-01-27T15:00:00Z"
)
```

#### **Option B: Webhook**
Configure hospital system to POST to bloodhub on stock changes:
```bash
curl -X POST https://bloodhub.nepal.gov/api/v1/ingest/transaction \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "blood_group": "A+",
    "units_change": 3,
    "timestamp": "2026-01-27T14:30:00Z"
  }'
```

#### **Option C: Manual Upload**
For hospitals without automation:
- Web interface for manual stock updates
- CSV bulk upload
- Mobile app for quick updates

---

## 📱 Optional Advanced Features

### **1. Low-Stock Alert System**
**Algorithm**:
```python
def check_low_stock():
    for hospital in hospitals:
        for blood_group in ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']:
            stock = get_stock(hospital, blood_group)
            
            if stock < 5:
                alert_level = 'critical'
            elif stock < 15:
                alert_level = 'low'
            else:
                continue
                
            send_alert(hospital, blood_group, stock, alert_level)
```

### **2. Donation Drive Suggestions**
**Trigger Conditions**:
- City-wide shortage detected
- Critical blood type below threshold
- Historical demand patterns

**Auto-generation**:
```python
if regional_stock['O+'] < 100 and trend == 'declining':
    create_donation_drive(
        city='Kathmandu',
        blood_groups=['O+', 'O-'],
        urgency='urgent',
        target_units=200,
        duration_days=7
    )
```

### **3. ML-Based Shortage Prediction**
**Features**:
- Historical stock levels
- Seasonal patterns (festivals, accidents)
- City-wise demand trends
- Weather correlations

**Model**: Time-series forecasting (LSTM/Prophet)

**Output**: 7-day and 30-day shortage predictions

### **4. Regional Heat Map**
**Visualization**:
- Color-coded availability by district
- Green: Surplus (>100 units)
- Yellow: Adequate (50-100 units)
- Orange: Low (20-50 units)
- Red: Critical (<20 units)

### **5. Offline Sync Mode**
**For areas with unstable internet**:
- Local SQLite database in hospital
- Queue transactions when offline
- Auto-sync when connection restored
- Conflict resolution algorithm

---

## 🛠️ Technology Stack

**Backend**:
- Django 6.0 + Django REST Framework
- SQLite (development) / PostgreSQL (production)
- Celery (background tasks)
- Redis (caching)

**Frontend**:
- React 18 + Vite
- TailwindCSS
- Framer Motion (animations)
- Leaflet (maps)
- Chart.js (analytics)

**Authentication**:
- Custom API Key authentication
- Django Admin for staff

**Deployment**:
- Docker containers
- Nginx reverse proxy
- Let's Encrypt SSL
- AWS/DigitalOcean

**Monitoring**:
- Sentry (error tracking)
- Prometheus + Grafana (metrics)
- CloudWatch (logs)

---

## 📝 Summary

bloodhub Nepal provides:
✅ Real-time blood inventory tracking  
✅ Secure API-based hospital integration  
✅ Public search dashboard  
✅ Privacy-compliant (no personal data)  
✅ Alert system for shortages  
✅ ML-powered predictions  
✅ Nationwide scalability  

**Next Steps**:
1. Review and approve architecture
2. Begin Phase 1 implementation
3. Onboard pilot hospitals
4. Launch MVP dashboard
5. Scale nationwide

---

*Document Version: 1.0*  
*Last Updated: January 27, 2026*  
*Contact: bloodhub@nepal.gov*
