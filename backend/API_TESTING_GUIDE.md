# API Testing Guide - How to Test Endpoints

## Method 1: Using curl (Terminal/Command Prompt)

### Update Donor Location

**Windows PowerShell:**
```powershell
curl -X POST http://localhost:8000/api/donors/1/update_location/ `
  -H "Content-Type: application/json" `
  -d '{\"latitude\": 27.7172, \"longitude\": 85.3240, \"location_consent\": true}'
```

**Windows CMD:**
```cmd
curl -X POST http://localhost:8000/api/donors/1/update_location/ -H "Content-Type: application/json" -d "{\"latitude\": 27.7172, \"longitude\": 85.3240, \"location_consent\": true}"
```

**Linux/Mac:**
```bash
curl -X POST http://localhost:8000/api/donors/1/update_location/ \
  -H "Content-Type: application/json" \
  -d '{"latitude": 27.7172, "longitude": 85.3240, "location_consent": true}'
```

**Note:** Replace `1` with your actual donor ID.

### Create Blood Request

```powershell
curl -X POST http://localhost:8000/api/blood-requests/ `
  -H "Content-Type: application/json" `
  -d '{\"hospital_name\": \"Test Hospital\", \"district\": \"Kathmandu\", \"city\": \"Kathmandu\", \"location\": \"Thamel\", \"latitude\": 27.7172, \"longitude\": 85.3240, \"blood_type\": \"O+\", \"urgency\": \"High\", \"units_needed\": 2, \"contact_number\": \"+9771234567890\"}'
```

## Method 2: Using Python requests (Terminal/Python Script)

### Create a test script

Create a file `test_api.py`:

```python
import requests
import json

# Base URL
BASE_URL = "http://localhost:8000"

# Update Donor Location
def update_donor_location(donor_id, latitude, longitude):
    url = f"{BASE_URL}/api/donors/{donor_id}/update_location/"
    data = {
        "latitude": latitude,
        "longitude": longitude,
        "location_consent": True
    }
    
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

# Create Blood Request
def create_blood_request():
    url = f"{BASE_URL}/api/blood-requests/"
    data = {
        "hospital_name": "Test Hospital",
        "district": "Kathmandu",
        "city": "Kathmandu",
        "location": "Thamel, Kathmandu",
        "latitude": 27.7172,
        "longitude": 85.3240,
        "blood_type": "O+",
        "blood_product": "Whole Blood",
        "urgency": "High",
        "units_needed": 2,
        "contact_number": "+9771234567890",
        "contact_person": "Dr. Test"
    }
    
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

# Run tests
if __name__ == "__main__":
    # First, update location for donor ID 1
    print("Updating donor location...")
    update_donor_location(1, 27.7172, 85.3240)
    
    # Then create a blood request
    print("\nCreating blood request...")
    create_blood_request()
```

**Run it:**
```powershell
python test_api.py
```

## Method 3: Using Django Shell

### Open Django Shell

```powershell
cd "c:\Users\samma\Desktop\Trimurti bh\Trimurti\backend"
python manage.py shell
```

### In the shell:

```python
from api.models import DonorProfile
from django.utils import timezone

# Get a donor (replace 1 with your donor ID)
donor = DonorProfile.objects.get(id=1)

# Update location
donor.latitude = 27.7172
donor.longitude = 85.3240
donor.location_consent = True
donor.location_verified_at = timezone.now()
donor.save()

print(f"Location updated for {donor.user.username}")
print(f"Latitude: {donor.latitude}, Longitude: {donor.longitude}")
```

## Method 4: Using Postman (GUI Tool)

1. **Download Postman**: https://www.postman.com/downloads/

2. **Create a new request:**
   - Method: `POST`
   - URL: `http://localhost:8000/api/donors/1/update_location/`
   - Headers: 
     - Key: `Content-Type`
     - Value: `application/json`
   - Body (raw JSON):
     ```json
     {
         "latitude": 27.7172,
         "longitude": 85.3240,
         "location_consent": true
     }
     ```

3. **Click Send**

## Method 5: Using Frontend (React/JavaScript)

### In your React component:

```javascript
// Update Donor Location
async function updateDonorLocation(donorId, latitude, longitude) {
    try {
        const response = await fetch(
            `http://localhost:8000/api/donors/${donorId}/update_location/`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    latitude: latitude,
                    longitude: longitude,
                    location_consent: true
                })
            }
        );
        
        const data = await response.json();
        console.log('Location updated:', data);
        return data;
    } catch (error) {
        console.error('Error updating location:', error);
    }
}

// Get user's current location and update
navigator.geolocation.getCurrentPosition(
    (position) => {
        const { latitude, longitude } = position.coords;
        updateDonorLocation(1, latitude, longitude);
    },
    (error) => {
        console.error('Error getting location:', error);
    }
);
```

## Quick Test Commands

### 1. Check if Django server is running
```powershell
# Should return something if server is running
curl http://localhost:8000/api/donors/
```

### 2. Get donor list (to find donor ID)
```powershell
curl http://localhost:8000/api/donors/
```

### 3. Update location (replace 1 with actual donor ID)
```powershell
curl -X POST http://localhost:8000/api/donors/1/update_location/ -H "Content-Type: application/json" -d "{\"latitude\": 27.7172, \"longitude\": 85.3240, \"location_consent\": true}"
```

## Important Notes

1. **Django Server Must Be Running:**
   ```powershell
   python manage.py runserver
   ```

2. **Get Donor ID First:**
   - Check your database
   - Or use: `GET /api/donors/` to list all donors

3. **Authentication (if required):**
   - Some endpoints may need authentication
   - Add token to headers: `Authorization: Token your_token_here`

## Troubleshooting

### "Connection refused"
- Make sure Django server is running on port 8000

### "404 Not Found"
- Check the URL is correct
- Make sure the donor ID exists

### "400 Bad Request"
- Check JSON format is correct
- Verify all required fields are provided

### "500 Internal Server Error"
- Check Django console for error messages
- Verify database migrations are run
