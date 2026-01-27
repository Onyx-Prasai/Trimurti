# Quick Setup Guide

## Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

## One-Time Setup

### Backend
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed_data  # Optional: Add sample data
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Running the Application

1. Start the backend server (port 8000):
```bash
cd backend
python manage.py runserver
```

2. Start the frontend server (port 3000):
```bash
cd frontend
npm run dev
```

3. Open your browser to `http://localhost:3000`

## Testing the Application

### Create a Test Donor
1. Go to Django admin: `http://localhost:8000/admin`
2. Create a User and DonorProfile
3. Or use the API to create one programmatically

### Test Features
- **Home Page**: View statistics and feature grid
- **Find Blood**: Search for hospitals and blood banks
- **Dashboard**: View donation calendar and badges (requires logged-in donor)
- **AI Health**: Chat with AI assistant
- **Points**: View store and referral system
- **Profile**: Edit personal information

## API Testing

You can test the API endpoints using:
- Browser: `http://localhost:8000/api/donors/stats/`
- Postman or similar tools
- Frontend application

## Troubleshooting

### Backend Issues
- Make sure virtual environment is activated
- Check that `.env` file exists with `GEMINI_API_KEY`
- Run migrations if database errors occur

### Frontend Issues
- Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Check that backend is running on port 8000
- Check browser console for CORS errors

### CORS Errors
- Ensure `corsheaders` is in `INSTALLED_APPS`
- Check `CORS_ALLOWED_ORIGINS` in `settings.py`

