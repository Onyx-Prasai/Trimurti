# BloodHub Nepal - Hospital Integration Guide

## 🏥 Welcome to BloodHub Nepal

This guide will help your hospital integrate with BloodHub Nepal's real-time blood inventory management system.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Getting Your API Key](#getting-your-api-key)
3. [Integration Methods](#integration-methods)
4. [API Reference](#api-reference)
5. [Code Examples](#code-examples)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)
8. [Support](#support)

---

## 🎯 Overview

### What is bloodhub Nepal?

bloodhub Nepal is a national platform that provides real-time blood inventory visibility across hospitals and blood banks in Nepal. By integrating with our system, your hospital helps:

- ✅ Save lives through better blood availability information
- ✅ Reduce blood wastage
- ✅ Enable faster emergency response
- ✅ Facilitate better resource sharing

### Data Privacy Commitment

**BloodHub Nepal ONLY collects:**
- ✅ Total blood units available (aggregated data)
- ✅ Blood group (A+, B-, etc.)
- ✅ Hospital name and location
- ✅ Timestamp of stock changes

**We NEVER collect:**
- ❌ Donor personal information
- ❌ Patient details
- ❌ Medical records
- ❌ Staff information

This ensures full compliance with Nepal's National Blood Policy.

---

## 🔑 Getting Your API Key

### Step 1: Registration

Contact BloodHub Nepal to register your hospital:

**Email**: onboarding@bloodhub.nepal.gov  
**Phone**: +977-1-XXXXXXX  
**Office Hours**: Sunday-Friday, 10 AM - 5 PM

Provide:
- Hospital name
- City/location
- Contact person details
- Estimated monthly blood transactions

### Step 2: Receive API Key

After verification, you'll receive:
- **Hospital Code**: Unique identifier (e.g., `TU-HOSPITAL`)
- **API Key**: Secret authentication key (64 characters)

**⚠️ IMPORTANT**: Keep your API key secure! Never share it publicly or commit it to version control.

### Step 3: Test Connection

```bash
curl -X POST https://bloodhub.nepal.gov/api/v1/ingest/transaction/ \
  -H "X-API-Key: YOUR_API_KEY_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "blood_group": "O+",
    "units_change": 1,
    "timestamp": "2026-01-27T10:00:00Z",
    "notes": "Test transaction"
  }'
```

If successful, you'll receive a `202 Accepted` response.

---

## 🔌 Integration Methods

### Method 1: Direct API Calls (Recommended)

Best for custom hospital management systems.

**When to use:**
- You have a custom-built system
- You have developer resources
- You want full control

**Pros:**
- Most flexible
- Real-time updates
- Custom error handling

**Cons:**
- Requires development effort
- Need to maintain code

### Method 2: Pre-Built Plugins

Coming soon for popular hospital management software:
- HMS Pro
- MediSoft Nepal
- Hospital ERP

**When to use:**
- You use supported software
- Limited developer resources
- Want quick setup

### Method 3: Manual Web Interface

For hospitals without automation.

**When to use:**
- No technical resources
- Low transaction volume
- Temporary solution

**Access**: https://bloodhub.nepal.gov/hospital/portal

---

## 📚 API Reference

### Base URL

```
Production: https://bloodhub.nepal.gov/api/v1/
Development: http://localhost:8000/api/v1/
```

### Authentication

All requests must include the API key in the header:

```
X-API-Key: your-64-character-api-key
```

### Endpoints

#### 1. Ingest Transaction (POST)

**Endpoint**: `/ingest/transaction/`

**Purpose**: Report blood stock changes

**Request Headers**:
```
X-API-Key: your-api-key
Content-Type: application/json
```

**Request Body**:
```json
{
  "blood_group": "O+",           // Required: A+, A-, B+, B-, AB+, AB-, O+, O-
  "units_change": 5,              // Required: Positive for donations, negative for usage
  "timestamp": "2026-01-27T14:30:00Z",  // Required: ISO 8601 format
  "source_reference": "DON-2026-001234", // Optional: Your internal reference
  "notes": "Blood donation camp"  // Optional: Additional notes
}
```

**Response** (202 Accepted):
```json
{
  "message": "Transaction ingested",
  "transaction": {
    "id": "uuid-here",
    "hospital": {
      "code": "TU-HOSPITAL",
      "name": "Tribhuvan University Teaching Hospital"
    },
    "blood_group": "O+",
    "units_change": 5,
    "timestamp": "2026-01-27T14:30:00Z",
    "ingested_at": "2026-01-27T14:30:05Z"
  },
  "stock": {
    "blood_group": "O+",
    "units_available": 45,
    "updated_at": "2026-01-27T14:30:05Z"
  }
}
```

**Error Responses**:

```json
// 401 Unauthorized
{
  "detail": "Valid X-API-Key header is required."
}

// 400 Bad Request
{
  "blood_group": ["This field is required."],
  "units_change": ["A valid integer is required."]
}

// 429 Too Many Requests
{
  "detail": "Request was throttled. Expected available in 60 seconds."
}
```

#### 2. Query Current Stock (GET)

**Endpoint**: `/public/blood-stock/`

**Purpose**: View your hospital's current stock (public endpoint)

**Query Parameters**:
- `city`: Filter by city (optional)
- `blood_group`: Filter by blood group (optional)
- `min_units`: Minimum units required (optional)

**Example**:
```bash
GET /api/v1/public/blood-stock/?city=Kathmandu&blood_group=O+
```

**Response**:
```json
{
  "results": [
    {
      "hospital": {
        "code": "TU-HOSPITAL",
        "name": "Tribhuvan University Teaching Hospital",
        "city": "Kathmandu"
      },
      "stock": {
        "O+": {"units": 45, "updated_at": "2026-01-27T14:30:05Z"},
        "A+": {"units": 32, "updated_at": "2026-01-27T12:15:00Z"}
      },
      "last_updated": "2026-01-27T14:30:05Z"
    }
  ],
  "total_hospitals": 1,
  "timestamp": "2026-01-27T15:00:00Z"
}
```

---

## 💻 Code Examples

### Python

#### Simple Integration

```python
import requests
from datetime import datetime

API_URL = "https://bloodhub.nepal.gov/api/v1/ingest/transaction/"
API_KEY = "your-api-key-here"  # Store securely!

def report_blood_donation(blood_group, units):
    """Report a blood donation to bloodhub Nepal."""
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    data = {
        "blood_group": blood_group,
        "units_change": units,  # Positive for donations
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "notes": "Blood donation"
    }
    
    response = requests.post(API_URL, json=data, headers=headers)
    
    if response.status_code == 202:
        print(f"✅ Successfully reported {units} units of {blood_group}")
        return response.json()
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.json())
        return None

# Example usage
report_blood_donation("O+", 3)
```

#### Advanced Integration with Error Handling

```python
import requests
import time
from datetime import datetime
from typing import Optional, Dict

class BloodHubClient:
    """Client for BloodHub Nepal API."""
    
    def __init__(self, api_key: str, base_url: str = "https://bloodhub.nepal.gov/api/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        })
    
    def report_transaction(
        self,
        blood_group: str,
        units_change: int,
        source_reference: Optional[str] = None,
        notes: Optional[str] = None,
        retry_count: int = 3
    ) -> Dict:
        """
        Report a blood stock transaction.
        
        Args:
            blood_group: Blood group (A+, A-, B+, B-, AB+, AB-, O+, O-)
            units_change: Positive for donations, negative for usage
            source_reference: Your internal reference ID
            notes: Additional notes
            retry_count: Number of retries on failure
        
        Returns:
            Response JSON if successful
        
        Raises:
            Exception: If all retries fail
        """
        data = {
            "blood_group": blood_group,
            "units_change": units_change,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        if source_reference:
            data["source_reference"] = source_reference
        if notes:
            data["notes"] = notes
        
        for attempt in range(retry_count):
            try:
                response = self.session.post(
                    f"{self.base_url}/ingest/transaction/",
                    json=data,
                    timeout=30
                )
                
                if response.status_code == 202:
                    return response.json()
                elif response.status_code == 429:
                    # Rate limited, wait and retry
                    wait_time = 60 * (attempt + 1)
                    print(f"Rate limited. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    response.raise_for_status()
                    
            except requests.exceptions.RequestException as e:
                if attempt == retry_count - 1:
                    raise Exception(f"Failed after {retry_count} attempts: {e}")
                time.sleep(5 * (attempt + 1))
        
        raise Exception("Max retries exceeded")
    
    def get_current_stock(self) -> Dict:
        """Get current blood stock for all blood groups."""
        response = self.session.get(f"{self.base_url}/public/blood-stock/")
        response.raise_for_status()
        return response.json()


# Example usage
client = BloodHubClient(api_key="your-api-key")

# Report donation
result = client.report_transaction(
    blood_group="O+",
    units_change=5,
    source_reference="DON-2026-001234",
    notes="Blood donation camp at City Hospital"
)

print(f"Current stock: {result['stock']['units_available']} units")
```

### JavaScript/Node.js

```javascript
const axios = require('axios');

const API_URL = 'https://bloodhub.nepal.gov/api/v1/ingest/transaction/';
const API_KEY = process.env.bloodhub_API_KEY;  // Use environment variable

async function reportBloodTransaction(bloodGroup, unitsChange, notes = '') {
    try {
        const response = await axios.post(API_URL, {
            blood_group: bloodGroup,
            units_change: unitsChange,
            timestamp: new Date().toISOString(),
            notes: notes
        }, {
            headers: {
                'X-API-Key': API_KEY,
                'Content-Type': 'application/json'
            },
            timeout: 30000
        });
        
        console.log('✅ Transaction reported successfully');
        console.log(`Current stock: ${response.data.stock.units_available} units`);
        return response.data;
        
    } catch (error) {
        if (error.response) {
            console.error('❌ API Error:', error.response.status);
            console.error(error.response.data);
        } else {
            console.error('❌ Network Error:', error.message);
        }
        throw error;
    }
}

// Example: Report 3 units of O+ donated
reportBloodTransaction('O+', 3, 'Regular donation');

// Example: Report 2 units of A+ used
reportBloodTransaction('A+', -2, 'Emergency transfusion');
```

### PHP

```php
<?php

define('API_URL', 'https://bloodhub.nepal.gov/api/v1/ingest/transaction/');
define('API_KEY', 'your-api-key-here');  // Store in config file

function reportBloodTransaction($bloodGroup, $unitsChange, $notes = '') {
    $data = [
        'blood_group' => $bloodGroup,
        'units_change' => $unitsChange,
        'timestamp' => gmdate('Y-m-d\TH:i:s\Z'),
        'notes' => $notes
    ];
    
    $ch = curl_init(API_URL);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'X-API-Key: ' . API_KEY,
        'Content-Type: application/json'
    ]);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 30);
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($httpCode === 202) {
        $result = json_decode($response, true);
        echo "✅ Successfully reported {$unitsChange} units of {$bloodGroup}\n";
        echo "Current stock: {$result['stock']['units_available']} units\n";
        return $result;
    } else {
        echo "❌ Error: HTTP {$httpCode}\n";
        echo $response . "\n";
        return null;
    }
}

// Example usage
reportBloodTransaction('O+', 5, 'Blood donation camp');
```

---

## 🧪 Testing

### Test Environment

Use our sandbox environment for testing:

```
Base URL: https://sandbox.bloodhub.nepal.gov/api/v1/
Test API Key: test-api-key-request-from-support
```

### Test Scenarios

#### 1. Report Donation
```json
POST /ingest/transaction/
{
  "blood_group": "O+",
  "units_change": 5,
  "timestamp": "2026-01-27T10:00:00Z",
  "notes": "Test donation"
}
```

#### 2. Report Usage
```json
POST /ingest/transaction/
{
  "blood_group": "O+",
  "units_change": -2,
  "timestamp": "2026-01-27T11:00:00Z",
  "notes": "Test usage"
}
```

#### 3. Invalid Blood Group (Should Fail)
```json
POST /ingest/transaction/
{
  "blood_group": "Z+",  // Invalid
  "units_change": 5,
  "timestamp": "2026-01-27T10:00:00Z"
}
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. 401 Unauthorized

**Problem**: `Valid X-API-Key header is required`

**Solutions**:
- Check API key is correct (no extra spaces)
- Ensure header name is exactly `X-API-Key`
- Verify key hasn't been revoked

#### 2. 400 Bad Request

**Problem**: `blood_group: This field is required`

**Solutions**:
- Check all required fields are present
- Verify blood_group is one of: A+, A-, B+, B-, AB+, AB-, O+, O-
- Ensure timestamp is in ISO 8601 format
- Check units_change is an integer

#### 3. 429 Too Many Requests

**Problem**: `Request was throttled`

**Solutions**:
- Implement exponential backoff
- Rate limit: 100 requests per minute
- Queue transactions and batch them

#### 4. Network Timeout

**Problem**: No response after 30 seconds

**Solutions**:
- Check internet connection
- Verify firewall allows HTTPS to bloodhub.nepal.gov
- Implement retry logic with backoff

### Debug Mode

Enable debug logging:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

This will show full request/response details.

---

## 📞 Support

### Technical Support

**Email**: support@bloodhub.nepal.gov  
**Phone**: +977-1-XXXXXXX  
**Hours**: Sunday-Friday, 10 AM - 5 PM NST

### Emergency Support (24/7)

For critical issues affecting blood availability:
**Hotline**: +977-XXX-XXXXXX

### Documentation

- **API Docs**: https://docs.bloodhub.nepal.gov
- **Video Tutorials**: https://youtube.com/bloodhubnepal
- **FAQ**: https://bloodhub.nepal.gov/faq

### Community

- **Forum**: https://community.bloodhub.nepal.gov
- **Slack Channel**: bloodhub-nepal.slack.com

---

## 📄 Compliance & Legal

### Data Privacy

bloodhub Nepal complies with:
- Nepal National Blood Policy
- Personal Data Protection Guidelines
- Medical Data Privacy Standards

### Terms of Service

By using the API, you agree to:
- Report accurate, timely data
- Protect your API key
- Use data only for blood availability purposes
- Comply with Nepal health regulations

### SLA (Service Level Agreement)

- **Uptime**: 99.9% guaranteed
- **Response Time**: < 200ms average
- **Support Response**: < 4 hours during business hours

---

## ✅ Integration Checklist

Before going live:

- [ ] API key received and stored securely
- [ ] Test transactions successful in sandbox
- [ ] Error handling implemented
- [ ] Retry logic in place
- [ ] Logging configured
- [ ] Team trained on system
- [ ] Emergency contact numbers saved
- [ ] Data backup plan in place
- [ ] Monitoring dashboard set up

---

**Document Version**: 1.0  
**Last Updated**: January 27, 2026  
**Contact**: support@bloodhub.nepal.gov
