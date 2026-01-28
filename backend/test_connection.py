"""
Simple script to test Twilio API connection
Run: python test_connection.py
"""
import socket
import sys

print("🔍 Testing Twilio API Connection...\n")

# Test 1: Internet connectivity
print("1. Testing Internet Connection...")
try:
    socket.create_connection(("8.8.8.8", 53), timeout=3)
    print("   ✅ Internet: OK")
except OSError:
    print("   ❌ Internet: FAILED - No internet connection")
    sys.exit(1)

# Test 2: DNS resolution
print("\n2. Testing DNS Resolution...")
try:
    ip = socket.gethostbyname('api.twilio.com')
    print(f"   ✅ DNS: OK (api.twilio.com -> {ip})")
except socket.gaierror:
    print("   ❌ DNS: FAILED - Cannot resolve api.twilio.com")
    sys.exit(1)

# Test 3: HTTPS connection
print("\n3. Testing HTTPS Connection...")
try:
    import urllib.request
    response = urllib.request.urlopen('https://api.twilio.com', timeout=10)
    print(f"   ✅ HTTPS: OK (Status: {response.getcode()})")
except Exception as e:
    print(f"   ❌ HTTPS: FAILED")
    print(f"   Error: {str(e)}")
    print("\n⚠️  Troubleshooting:")
    print("   - Check firewall settings")
    print("   - Disable VPN if enabled")
    print("   - Try different network")
    print("   - Some ISPs block international APIs")
    sys.exit(1)

print("\n✅ All connection tests passed!")
print("   Your network can reach Twilio API.")
