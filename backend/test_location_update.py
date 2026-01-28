"""
Simple script to test location update API
Run: python test_location_update.py
"""
import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
DONOR_ID = 1  # Change this to your donor ID

def update_donor_location(donor_id, latitude, longitude):
    """
    Update donor location via API
    """
    url = f"{BASE_URL}/api/donors/{donor_id}/update_location/"
    
    data = {
        "latitude": latitude,
        "longitude": longitude,
        "location_consent": True
    }
    
    print(f"\n📍 Updating location for donor ID: {donor_id}")
    print(f"   Latitude: {latitude}")
    print(f"   Longitude: {longitude}")
    print(f"   URL: {url}")
    
    try:
        response = requests.post(url, json=data, timeout=5)
        
        print(f"\n✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Location updated")
            print(f"   Response: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Connection Error!")
        print(f"   Make sure Django server is running:")
        print(f"   python manage.py runserver")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    # Example: Kathmandu coordinates
    update_donor_location(
        donor_id=DONOR_ID,
        latitude=27.7172,
        longitude=85.3240
    )
    
    print("\n" + "="*50)
    print("💡 TIP: Change DONOR_ID in the script to test with different donors")
    print("="*50)
