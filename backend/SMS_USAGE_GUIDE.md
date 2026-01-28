# SMS System Usage Guide

## Overview
The SMS system is fully integrated and ready to use. You can send SMS messages directly from the backend using multiple methods.

## Configuration Status
✅ Twilio package installed  
✅ Settings configured  
✅ API endpoints created  
✅ Management command available  

## Methods to Send SMS

### Method 1: Django Management Command (Easiest)

**Send a custom message:**
```bash
python manage.py test_sms +1234567890 --message "Hello, this is a test message"
```

**Send a blood request SMS template:**
```bash
python manage.py test_sms +1234567890 --blood-request --blood-type "O+" --location "Kathmandu" --urgency "High"
```

**Send default test message:**
```bash
python manage.py test_sms +1234567890
```

### Method 2: API Endpoint (REST API)

**Send single SMS:**
```bash
POST http://localhost:8000/api/sms/send/
Content-Type: application/json

{
    "phone_number": "+1234567890",
    "message": "Your custom message here"
}
```

**Send bulk SMS:**
```bash
POST http://localhost:8000/api/sms/send_bulk/
Content-Type: application/json

{
    "phone_numbers": ["+1234567890", "+9876543210"],
    "message": "Your message to all recipients"
}
```

**Check SMS service status:**
```bash
GET http://localhost:8000/api/sms/status/
```

### Method 3: Python Code (Django Shell or Scripts)

```python
from api.sms_service import send_sms, send_bulk_sms

# Send single SMS
result = send_sms("+1234567890", "Your message here")
print(result)

# Send bulk SMS
results = send_bulk_sms(
    ["+1234567890", "+9876543210"],
    "Your message here"
)
print(results)
```

### Method 4: Automatic (Blood Request System)

When you create a blood request through the API, SMS is automatically sent to matching donors:

```bash
POST http://localhost:8000/api/blood-requests/
{
    "hospital_name": "Test Hospital",
    "district": "Kathmandu",
    "city": "Kathmandu",
    "blood_type": "O+",
    "urgency": "High",
    "units_needed": 2
}
```

The system will:
1. Find donors with matching blood type and district
2. Send SMS to each donor automatically
3. Log results in SMSNotificationLog
4. Return summary in response

## API Endpoints

### Send SMS
- **URL:** `/api/sms/send/`
- **Method:** POST
- **Body:**
  ```json
  {
    "phone_number": "+1234567890",
    "message": "Your message"
  }
  ```

### Send Bulk SMS
- **URL:** `/api/sms/send_bulk/`
- **Method:** POST
- **Body:**
  ```json
  {
    "phone_numbers": ["+1234567890", "+9876543210"],
    "message": "Your message"
  }
  ```

### Check Status
- **URL:** `/api/sms/status/`
- **Method:** GET
- **Response:**
  ```json
  {
    "enabled": true,
    "status": "active",
    "message": "SMS service is ready"
  }
  ```

## Phone Number Format

- **Required Format:** E.164 format with country code
- **Examples:**
  - US: `+13238437394`
  - Nepal: `+9779812345678`
  - India: `+919876543210`

## Response Format

### Success Response
```json
{
    "success": true,
    "message": "SMS sent successfully",
    "message_sid": "SM1234567890abcdef",
    "phone_number": "+1234567890"
}
```

### Error Response
```json
{
    "success": false,
    "error": "Error message here",
    "phone_number": "+1234567890"
}
```

## Troubleshooting

### SMS Not Sending

1. **Check Twilio Configuration:**
   - Verify `.env` file has correct credentials
   - Restart Django server after adding credentials

2. **Trial Account Limitations:**
   - Can only send to verified phone numbers
   - Verify numbers in Twilio Console: https://www.twilio.com/console/phone-numbers/verified

3. **Phone Number Format:**
   - Must include country code
   - Must start with `+`
   - No spaces or dashes

4. **Check Logs:**
   - Django console will show error messages
   - Check Twilio console for delivery status

### Common Errors

- **"SMS service not enabled"** → Check `.env` file and restart server
- **"Invalid phone number"** → Use E.164 format (+country code)
- **"Unverified number"** → Verify number in Twilio console (trial accounts)
- **"Insufficient credits"** → Add credits to Twilio account

## Testing

### Quick Test
```bash
# Test with your verified phone number
python manage.py test_sms +13238437394
```

### Test via API (using curl)
```bash
curl -X POST http://localhost:8000/api/sms/send/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+13238437394", "message": "Test message"}'
```

## Integration Points

The SMS system is integrated with:
- ✅ Blood Request creation (automatic SMS to donors)
- ✅ SMS Notification Logging (database tracking)
- ✅ API endpoints (REST API access)
- ✅ Management commands (CLI access)
- ✅ Python functions (programmatic access)

## Next Steps

1. **For Production:**
   - Upgrade Twilio account from trial
   - Set up webhook for delivery status
   - Configure error handling and retries
   - Set up monitoring and alerts

2. **For Development:**
   - Test with verified phone numbers
   - Monitor SMS logs in database
   - Check Twilio console for delivery status
