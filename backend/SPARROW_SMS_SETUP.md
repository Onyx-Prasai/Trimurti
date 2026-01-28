# Sparrow SMS Setup Guide (Recommended for Nepal)

## Why Sparrow SMS?

Since Twilio API is not accessible from your network (connection timeout), **Sparrow SMS** is the perfect solution for Nepal:

✅ **Better Connectivity** - Works reliably in Nepal  
✅ **No Network Restrictions** - No firewall/VPN issues  
✅ **Local Provider** - Optimized for Nepal Telecom, Ncell, etc.  
✅ **Cost Effective** - Better pricing for Nepal  
✅ **Easy Setup** - Simple API integration  

## Quick Setup Steps

### Step 1: Create Sparrow SMS Account

1. Go to: **https://web.sparrowsms.com**
2. Click "Sign Up" or "Register"
3. Fill in your details and verify your email
4. Complete the registration process

### Step 2: Get Your API Credentials

1. Log in to your Sparrow SMS dashboard
2. Go to **API Settings** or **Developer** section
3. You'll find:
   - **Token**: Your API token (keep this secret!)
   - **From**: Your sender ID (can be your registered number or a text ID like "BLOODHUB")

### Step 3: Add Credentials to .env File

Add these lines to your `.env` file in the backend directory:

```env
# Sparrow SMS Configuration (Nepal)
SPARROW_TOKEN=your_token_here
SPARROW_FROM=your_sender_id_here
```

**Example:**
```env
SPARROW_TOKEN=abc123xyz789
SPARROW_FROM=BLOODHUB
```

### Step 4: Restart Django Server

After adding credentials, restart your Django server:

```powershell
python manage.py runserver
```

### Step 5: Test SMS

```powershell
python manage.py test_sms +9779864165177 --message "Test from Blood Hub"
```

## Phone Number Format

For Sparrow SMS:
- **With country code**: `+9779864165177` ✅
- **Without country code**: `9864165177` ✅
- Both formats work!

## How It Works

The SMS system now supports **dual providers**:

1. **Sparrow SMS** (Primary for Nepal) - Tries first
2. **Twilio** (Fallback) - Used if Sparrow fails or not configured

The system automatically:
- Tries Sparrow SMS first
- Falls back to Twilio if Sparrow fails
- Works seamlessly with your existing code

## API Endpoints

All existing API endpoints work the same:

```bash
POST /api/sms/send/
{
    "phone_number": "+9779864165177",
    "message": "Your message"
}
```

## Pricing

- Check Sparrow SMS dashboard for current pricing
- Usually very affordable for Nepal
- Pay-as-you-go or prepaid credits

## Support

- **Sparrow SMS Docs**: https://docs.sparrowsms.com
- **API Documentation**: https://docs.sparrowsms.com/sms/documentation/
- **Support**: Contact Sparrow SMS support through dashboard

## Troubleshooting

### SMS Not Sending?

1. **Check credentials**: Verify token and sender ID in `.env`
2. **Check balance**: Ensure you have credits in Sparrow SMS account
3. **Check logs**: Django console will show error messages
4. **Verify sender ID**: Make sure your sender ID is approved

### Common Errors

- **"Invalid token"** → Check your SPARROW_TOKEN in .env
- **"Invalid sender"** → Check your SPARROW_FROM (must be approved)
- **"Insufficient credits"** → Add credits to your Sparrow SMS account

## Next Steps

1. ✅ Sign up at https://web.sparrowsms.com
2. ✅ Get your token and sender ID
3. ✅ Add to `.env` file
4. ✅ Restart Django server
5. ✅ Test with: `python manage.py test_sms +9779864165177`

Your SMS system will now work perfectly in Nepal! 🎉
