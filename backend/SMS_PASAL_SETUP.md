# SMS Pasal Setup Guide (Alternative to Sparrow SMS)

## Why SMS Pasal?

- ✅ **Free Trial Available** - Test before committing
- ✅ **Developer Friendly** - Easy REST API
- ✅ **High Speed** - 99.9% uptime
- ✅ **Nepali Unicode** - Full language support
- ✅ **Local Support** - Nepal-based company
- ✅ **No Hidden Fees** - Transparent pricing

## Quick Setup

### Step 1: Sign Up

1. Go to: **https://smspasal.com**
2. Click "Sign Up" or "Register"
3. Fill in your details
4. Verify your email/phone
5. **Get free trial credits**

### Step 2: Get API Credentials

1. Log in to SMS Pasal dashboard
2. Go to **API Settings** or **Developer** section
3. You'll find:
   - **Token**: Your API token
   - **From/Sender ID**: Your approved sender ID

### Step 3: Add to .env

Add these lines to your `.env` file:

```env
# SMS Pasal Configuration
SMS_PASAL_TOKEN=your_token_here
SMS_PASAL_FROM=your_sender_id_here
```

### Step 4: Restart & Test

```powershell
python manage.py runserver
python manage.py test_sms +9779864165177
```

## How It Works

The system will:
1. Try **Sparrow SMS** first (if configured)
2. Try **SMS Pasal** if Sparrow fails (if configured)
3. Fall back to **Twilio** if both fail

## API Endpoint

**Note**: SMS Pasal API endpoint may vary. Check their documentation:
- Contact SMS Pasal support for exact API endpoint
- Update the endpoint in `sms_service.py` if needed

## Pricing

- **Free Trial**: Available for testing
- **Production**: Check SMS Pasal website for current rates
- Usually competitive pricing for Nepal

## Support

- **Website**: https://smspasal.com
- **Contact**: Check website for support contact
- **API Docs**: Contact them for API documentation

## Troubleshooting

### SMS Not Sending?

1. Verify token and sender ID in `.env`
2. Check API endpoint in code (may need update)
3. Contact SMS Pasal for exact API format
4. Check account balance/credits

### Need Help?

Contact SMS Pasal support for:
- API endpoint details
- API format/parameters
- Account setup help

## Alternative: Use Sparrow SMS

If SMS Pasal doesn't work, try **Sparrow SMS** instead:
- See `SPARROW_SMS_SETUP.md` for instructions
- Already fully integrated in code
