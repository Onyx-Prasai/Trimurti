# Location-Based SMS System Guide

## ✅ What Was Implemented

A complete location-based SMS notification system that:
1. **Stores user phone numbers** during registration
2. **Captures and stores user location** (latitude/longitude)
3. **Uses expanding radius search** (500m → 1km → 2km → 5km → 10km)
4. **Sends custom location-aware SMS** to nearby donors

## 🎯 Features

### 1. Phone Number Storage
- Phone numbers are stored in both `User.phone_number` and `DonorProfile.phone`
- If phone is provided during registration, it's automatically stored
- Existing phone numbers are preserved (won't overwrite)

### 2. Location Storage
- Users can enable location consent
- Latitude and longitude are stored in `DonorProfile`
- Location is verified when consent is given

### 3. Location-Based Matching
- Starts with **500m radius**
- Expands to **1km, 2km, 5km, 10km** if needed
- Only matches donors with:
  - Matching blood type
  - Location consent enabled
  - Valid coordinates
  - Phone number available

### 4. Custom SMS Messages
- Location-aware messages showing distance
- Includes hospital name, contact number
- Shows urgency and units needed

## 📡 API Endpoints

### 1. Update Donor Location

**Endpoint:** `POST /api/donors/{id}/update_location/`

**Request Body:**
```json
{
    "latitude": 27.7172,
    "longitude": 85.3240,
    "location_consent": true,
    "phone_number": "+9779864165177"  // Optional, only if not already set
}
```

**Response:**
```json
{
    "message": "Location updated successfully",
    "donor": {
        "id": 1,
        "latitude": "27.717200",
        "longitude": "85.324000",
        "location_consent": true,
        ...
    }
}
```

### 2. Create Blood Request (with location)

**Endpoint:** `POST /api/blood-requests/`

**Request Body:**
```json
{
    "hospital_name": "Test Hospital",
    "district": "Kathmandu",
    "city": "Kathmandu",
    "location": "Thamel, Kathmandu",
    "latitude": 27.7172,
    "longitude": 85.3240,
    "blood_type": "O+",
    "urgency": "High",
    "units_needed": 2,
    "contact_number": "+9771234567890"
}
```

**Response includes SMS summary:**
```json
{
    "id": 1,
    "hospital_name": "Test Hospital",
    ...
    "sms_summary": {
        "matched": 5,
        "sent": 5,
        "failed": 0,
        "radius_used": 1000,
        "method": "location_based"
    }
}
```

### 3. User Registration (with phone)

**Endpoint:** `POST /api/users/register/` or `POST /api/users/`

**Request Body:**
```json
{
    "username": "donor123",
    "email": "donor@example.com",
    "password": "password123",
    "password2": "password123",
    "user_type": "base_user",
    "phone_number": "+9779864165177",
    "location": "Kathmandu, Nepal"
}
```

## 🔄 How It Works

### Step 1: User Registration
1. User registers with phone number (optional)
2. Phone number is stored in `User.phone_number`
3. If user is a donor, phone is also stored in `DonorProfile.phone`

### Step 2: Location Enablement
1. User enables location access in app
2. App sends location to: `POST /api/donors/{id}/update_location/`
3. System stores:
   - `latitude` and `longitude`
   - `location_consent = true`
   - `location_verified_at = current_time`

### Step 3: Blood Request Creation
1. Hospital creates blood request with location (latitude/longitude)
2. System searches for donors:
   - Starts with 500m radius
   - Expands if not enough donors found
   - Matches blood type and location

### Step 4: SMS Notification
1. Custom message sent to each matching donor
2. Message includes:
   - Distance from request location
   - Hospital details
   - Contact information
   - Urgency level

## 📊 Location Matching Algorithm

```python
# Starting radius: 500m
# Expansion sequence:
500m → 1000m (1km) → 2000m (2km) → 5000m (5km) → 10000m (10km)

# Matching criteria:
- Blood type matches
- Location consent enabled
- Valid coordinates available
- Phone number available
- Within current radius
```

## 🗄️ Database Changes

### BloodRequest Model
- Added `latitude` (DecimalField, 9,6)
- Added `longitude` (DecimalField, 9,6)

### DonorProfile Model (Already exists)
- `phone` (CharField)
- `latitude` (DecimalField)
- `longitude` (DecimalField)
- `location_consent` (BooleanField)
- `location_verified_at` (DateTimeField)

## 🔧 Utility Functions

### `calculate_distance(lat1, lon1, lat2, lon2)`
- Calculates distance between two coordinates using Haversine formula
- Returns distance in meters

### `find_donors_within_radius(request_lat, request_lon, blood_type, radius_meters, max_radius_meters)`
- Finds donors within specified radius
- Expands radius automatically if needed
- Returns donors list and final radius used

## 📱 Frontend Integration

### 1. Request Location Permission
```javascript
navigator.geolocation.getCurrentPosition(
    (position) => {
        const { latitude, longitude } = position.coords;
        // Send to backend
        updateDonorLocation(userId, latitude, longitude);
    }
);
```

### 2. Update Location
```javascript
async function updateDonorLocation(userId, lat, lon) {
    const response = await fetch(`/api/donors/${userId}/update_location/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            latitude: lat,
            longitude: lon,
            location_consent: true
        })
    });
}
```

### 3. Create Blood Request with Location
```javascript
async function createBloodRequest(data) {
    // Get current location
    const position = await getCurrentPosition();
    
    const request = {
        ...data,
        latitude: position.coords.latitude,
        longitude: position.coords.longitude
    };
    
    const response = await fetch('/api/blood-requests/', {
        method: 'POST',
        body: JSON.stringify(request)
    });
}
```

## 🧪 Testing

### Test Location Update
```bash
curl -X POST http://localhost:8000/api/donors/1/update_location/ \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 27.7172,
    "longitude": 85.3240,
    "location_consent": true
  }'
```

### Test Blood Request with Location
```bash
curl -X POST http://localhost:8000/api/blood-requests/ \
  -H "Content-Type: application/json" \
  -d '{
    "hospital_name": "Test Hospital",
    "district": "Kathmandu",
    "city": "Kathmandu",
    "location": "Thamel",
    "latitude": 27.7172,
    "longitude": 85.3240,
    "blood_type": "O+",
    "urgency": "High",
    "units_needed": 2,
    "contact_number": "+9771234567890"
  }'
```

## 📝 SMS Message Format

### Location-Based Message
```
🩸 URGENT BLOOD REQUEST 🩸

Blood Type: O+
Hospital: Test Hospital
Location: Thamel, Kathmandu
Distance: Within 1.0km from you
Urgency: High
Units Needed: 2

Your blood type matches and you're nearby! Please help save lives. Contact the hospital immediately.

Contact: +9771234567890
Reply STOP to unsubscribe.
```

### District-Based Message (Fallback)
```
🩸 URGENT BLOOD REQUEST 🩸

Blood Type: O+
Hospital: Test Hospital
Location: Thamel, Kathmandu
Urgency: High
Units Needed: 2

Your blood type matches! Please help save lives. Contact the hospital immediately.

Contact: +9771234567890
Reply STOP to unsubscribe.
```

## ⚠️ Important Notes

1. **Location Consent Required**: Donors must enable location consent to be matched
2. **Phone Number Required**: Donors must have a phone number to receive SMS
3. **Coordinates Required**: Blood requests need latitude/longitude for location-based matching
4. **Fallback**: If no coordinates, system falls back to district-based matching
5. **Privacy**: Location data is only used for matching, not stored permanently

## 🚀 Next Steps

1. **Run Migration**: Create and run migration for new fields
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Test Location Update**: Test the location update endpoint

3. **Test Blood Request**: Create a blood request with location and verify SMS sending

4. **Frontend Integration**: Integrate location permission and update in frontend

## 📚 Related Files

- `api/models.py` - BloodRequest and DonorProfile models
- `api/views.py` - Location update and blood request endpoints
- `api/utils.py` - Distance calculation and radius search functions
- `api/sms_service.py` - SMS sending functions
- `users/views.py` - Registration with phone number
