# Blood Report Image Analysis - Quick Setup Guide

## What's New

Your AI Health feature can now analyze blood report images! Users can upload blood reports as images and get:
- ✅ Health issues identified
- ✅ Specific foods to eat (Nepalese options)
- ✅ Foods to avoid
- ✅ Lifestyle recommendations

## Quick Start (5 minutes)

### Step 1: Install Package
```bash
cd backend
pip install google-generativeai
```

### Step 2: Get Google API Key
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key

### Step 3: Set Environment Variable
```bash
# PowerShell (Windows)
$env:GOOGLE_API_KEY = "your-api-key-here"

# CMD (Windows)
set GOOGLE_API_KEY=your-api-key-here

# Linux/Mac
export GOOGLE_API_KEY=your-api-key-here
```

### Step 4: Restart Backend
```bash
cd backend
python manage.py runserver
```

### Step 5: Test It!
1. Go to AI Health page
2. Click "Blood Report Image" tab
3. Upload a blood report image
4. Click "Analyze Image"
5. See the magic happen! ✨

## What Changed

### Backend
- `backend/api/views.py` - Added image analysis endpoint
- `backend/bloodhub/settings.py` - Added Google API key config

### Frontend
- `frontend/src/pages/AIHealth.jsx` - Added image upload UI with tabs
- `frontend/src/utils/api.js` - Added image upload API function

## Key Features

### Image Analysis
- **Max Size**: 5MB
- **Formats**: JPG, PNG, GIF, WebP
- **Processing**: Real-time with Google Gemini Vision
- **Output**: Structured analysis with health insights

### UI Improvements
- Tabbed interface (Text Report | Blood Report Image)
- Image preview before analysis
- Error handling with helpful messages
- Loading states
- Responsive on all devices

## File Validation

Automatic validation ensures:
```javascript
✓ File is actually an image
✓ File size < 5MB
✓ Format is supported (JPG, PNG, GIF, WebP)
```

## Error Handling

The feature includes proper error handling:
- Invalid file type? → Shows helpful message
- File too large? → Shows size limit
- API key missing? → Clear setup instructions
- Network error? → Friendly error in chat

## Testing Your Setup

Run this to verify Google API is working:

```python
# In Django shell
python manage.py shell

# Test Google API connection
import google.generativeai as genai
genai.configure(api_key="your-key")
model = genai.GenerativeModel('gemini-2.0-flash')
response = model.generate_content("test")
print(response.text)
```

## Production Checklist

- [ ] Google API key set in production environment
- [ ] `google-generativeai` installed on production server
- [ ] Max file upload size configured (at least 5MB)
- [ ] Tested with sample blood report image
- [ ] Error handling verified
- [ ] Environment variable securely stored

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| "Invalid API Key" | Verify key in Google Cloud Console |
| Image won't upload | Check file size < 5MB and is valid image |
| Analysis timeout | Check internet connection, try again |
| No package found | Run `pip install google-generativeai` |

## File Structure

```
backend/
├── api/
│   ├── views.py              ← Updated with analyze_image()
│   └── urls.py               ← Already configured
└── bloodhub/
    └── settings.py           ← Added GOOGLE_API_KEY

frontend/
├── src/
│   ├── pages/
│   │   └── AIHealth.jsx       ← Updated with image UI
│   └── utils/
│       └── api.js            ← Added analyzeBloodReportImage()
└── ...

Documentation/
├── AI_HEALTH_IMAGE_ANALYSIS.md  ← Comprehensive guide
└── This file                     ← Quick setup
```

## API Endpoint

```
POST /api/ai-health/analyze_image/
Content-Type: multipart/form-data

Body:
  image: <file>

Response:
{
  "analysis": "Health issues identified: ...\n\nFoods to eat: ...\n\nFoods to avoid: ...",
  "status": "success"
}
```

## Next Steps

1. ✅ Complete the setup above
2. ✅ Test with a real blood report image
3. ✅ Share with users
4. 📖 Read full docs in `AI_HEALTH_IMAGE_ANALYSIS.md` for details

## Support

- 📖 Full documentation: `AI_HEALTH_IMAGE_ANALYSIS.md`
- 🐛 Issues? Check browser console (F12) for error details
- 🔑 API key issues? Visit Google Cloud Console

---

**That's it! Your AI Health feature is now ready to analyze blood report images!** 🎉
