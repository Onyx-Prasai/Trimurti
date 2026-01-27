# bloodhub Nepal - Quick Start Guide

## 🚀 Get Started in 5 Minutes

This guide will help you set up and run bloodhub Nepal on your local machine.

---

## ⚡ Quick Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-repo/bloodhub-nepal.git
cd bloodhub-nepal
```

### Step 2: Backend Setup (2 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment (choose one)
python -m venv tri          # Windows
python3 -m venv tri         # Linux/Mac

# Activate virtual environment
tri\Scripts\activate        # Windows
source tri/bin/activate     # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create admin user (follow prompts)
python manage.py createsuperuser

# Start server
python manage.py runserver
```

✅ Backend running at: `http://localhost:8000`

### Step 3: Frontend Setup (2 minutes)

Open a **new terminal** window:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

✅ Frontend running at: `http://localhost:5173`

---

## 🎯 First Steps

### Access the Application

1. **Public Dashboard**: http://localhost:5173
2. **Admin Panel**: http://localhost:8000/admin
   - Login with your superuser credentials
3. **API Documentation**: http://localhost:8000/api/

### Create a Demo Hospital

```bash
cd backend
python manage.py shell
```

Then run this in the Django shell:

```python
from api.models import Hospital
from api.authentication import hash_api_key
import secrets

# Generate API key
raw_key = secrets.token_urlsafe(32)
print(f"API Key (save this!): {raw_key}")

# Create hospital
hospital = Hospital.objects.create(
    code="DEMO-HOSPITAL",
    name="Demo Hospital Kathmandu",
    city="Kathmandu",
    address="Kathmandu, Nepal",
    latitude=27.7172,
    longitude=85.3240,
    api_key_hash=hash_api_key(raw_key),
    is_active=True
)

print(f"Hospital created: {hospital.name}")
print(f"Hospital ID: {hospital.id}")
```

**Save the API key!** You'll need it to send transactions.

### Test API Integration

Use the API key from above:

```bash
curl -X POST http://localhost:8000/api/v1/ingest/transaction/ \
  -H "X-API-Key: YOUR_API_KEY_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "blood_group": "O+",
    "units_change": 10,
    "timestamp": "2026-01-27T10:00:00Z",
    "notes": "Initial stock"
  }'
```

Expected response:
```json
{
  "message": "Transaction ingested",
  "transaction": {...},
  "stock": {
    "blood_group": "O+",
    "units_available": 10,
    "updated_at": "..."
  }
}
```

### View Blood Stock

Open browser: http://localhost:5173/blood-stock

Or query API:
```bash
curl http://localhost:8000/api/v1/public/blood-stock/
```

---

## 🧪 Sample Data (Optional)

### Create Multiple Blood Types

```python
# In Django shell (python manage.py shell)
from api.models import Hospital, Transaction, BloodStock
from django.utils import timezone
import uuid

hospital = Hospital.objects.first()  # Get the demo hospital

# Add stock for all blood groups
blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
units = [25, 10, 30, 8, 15, 5, 50, 12]

for bg, units_count in zip(blood_groups, units):
    # Create transaction
    Transaction.objects.create(
        hospital=hospital,
        blood_group=bg,
        units_change=units_count,
        timestamp=timezone.now(),
        notes=f"Initial {bg} stock"
    )
    
    # Create/update stock
    stock, created = BloodStock.objects.get_or_create(
        hospital=hospital,
        blood_group=bg,
        defaults={'units_available': units_count}
    )
    
    if not created:
        stock.units_available = units_count
        stock.save()
    
    print(f"✅ Added {units_count} units of {bg}")

print("Sample data created!")
```

---

## 📊 Explore Features

### 1. Public Dashboard
Visit: http://localhost:5173/blood-stock
- Search by city, blood group
- View real-time availability
- See hospital details

### 2. Admin Panel
Visit: http://localhost:8000/admin
- View all hospitals
- Check transactions
- Monitor blood stock
- Create alerts

### 3. API Testing

**Get all hospitals:**
```bash
curl http://localhost:8000/api/v1/public/hospitals/
```

**Search for O+ blood in Kathmandu:**
```bash
curl "http://localhost:8000/api/v1/public/blood-stock/?city=Kathmandu&blood_group=O%2B"
```

**Get city aggregated data:**
```bash
curl http://localhost:8000/api/v1/public/blood-availability/Kathmandu/
```

---

## 🛠️ Troubleshooting

### Common Issues

#### 1. Port Already in Use

**Backend (8000)**:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

**Frontend (5173)**:
```bash
# Change port in vite.config.js or
npm run dev -- --port 3000
```

#### 2. Module Not Found

```bash
# Backend
pip install -r requirements.txt

# Frontend
rm -rf node_modules package-lock.json
npm install
```

#### 3. Database Locked

```bash
# Reset database (⚠️ loses data)
cd backend
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

#### 4. CORS Errors

Check `backend/bloodhub/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite default
    "http://localhost:3000",  # Alternative
]
```

---

## 📝 Next Steps

### For Development

1. **Read Documentation**:
   - [bloodhub_ARCHITECTURE.md](bloodhub_ARCHITECTURE.md) - System design
   - [DEVELOPMENT_ROADMAP.md](DEVELOPMENT_ROADMAP.md) - Project plan
   - [HOSPITAL_INTEGRATION_GUIDE.md](HOSPITAL_INTEGRATION_GUIDE.md) - API guide

2. **Explore Code**:
   - `backend/api/models.py` - Database models
   - `backend/api/bloodhub_views.py` - bloodhub endpoints
   - `frontend/src/pages/BloodStockDashboard.jsx` - Dashboard UI

3. **Add Features**:
   - Implement map visualization
   - Add real-time WebSocket updates
   - Create mobile app
   - Build ML prediction model

### For Production

1. **Environment Setup**:
   - Create `.env` file with production settings
   - Set `DEBUG=False`
   - Configure database (PostgreSQL)
   - Set up Redis for caching

2. **Security**:
   - Generate strong `SECRET_KEY`
   - Enable HTTPS
   - Set up rate limiting
   - Configure firewall

3. **Deployment**:
   - Use Gunicorn for Django
   - Use Nginx as reverse proxy
   - Set up SSL certificate
   - Configure monitoring

---

## 🔗 Useful Links

- **API Base URL**: http://localhost:8000/api/v1/
- **Admin Panel**: http://localhost:8000/admin/
- **Frontend**: http://localhost:5173/
- **API Docs**: http://localhost:8000/api/ (add Swagger later)

---

## 💡 Tips

1. **Keep virtual environment activated** when working with backend
2. **Use separate terminals** for backend and frontend
3. **Save API keys securely** - never commit to Git
4. **Check console logs** for errors
5. **Use Django Debug Toolbar** for backend debugging
6. **Use React DevTools** for frontend debugging

---

## 🆘 Get Help

- **Issues**: Open a GitHub issue
- **Email**: support@bloodhub.nepal.gov
- **Docs**: Check the documentation files

---

## ✅ Checklist

After completing this guide, you should have:

- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] Admin account created
- [ ] Demo hospital registered
- [ ] Sample blood stock data
- [ ] Successfully tested API
- [ ] Viewed public dashboard

---

**Congratulations! 🎉 bloodhub Nepal is now running on your machine.**

Explore, experiment, and build amazing features to save lives!

---

*Quick Start Guide v1.0*  
*Last Updated: January 27, 2026*
