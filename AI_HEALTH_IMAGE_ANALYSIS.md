# AI Health Image Analysis Feature

## Overview

The AI Health feature now includes blood report image analysis capability. Users can upload blood report images (JPG, PNG, GIF, WebP), and the AI will analyze them to:

1. **Identify Health Issues** - Detect and explain health problems visible in the report
2. **Recommend Foods to Eat** - Suggest specific Nepalese foods that address the identified health issues
3. **Foods to Avoid** - List foods that should be avoided based on the blood report findings
4. **Lifestyle Tips** - Provide exercise and lifestyle recommendations
5. **Wellness Advice** - Additional preventive health measures

## Features

### Two Analysis Modes

#### 1. Text Report Analysis (Existing)
- Paste medical report text
- Select report type (Blood Test, Hemoglobin, Iron Levels, etc.)
- Get AI analysis with dietary recommendations

#### 2. Blood Report Image Analysis (New)
- Upload blood report images (up to 5MB)
- Real-time image preview
- AI-powered vision analysis using Google Gemini
- Structured analysis output with health insights and food recommendations

## Setup Instructions

### Backend Setup

#### 1. Install Google Generative AI Package

```bash
pip install google-generativeai
```

Or add it to `requirements.txt`:
```
google-generativeai>=0.8.6
```

#### 2. Configure Google API Key

Set the `GOOGLE_API_KEY` environment variable:

```bash
# Windows PowerShell
$env:GOOGLE_API_KEY = "your-google-api-key-here"

# Windows CMD
set GOOGLE_API_KEY=your-google-api-key-here

# Linux/Mac
export GOOGLE_API_KEY=your-google-api-key-here
```

The key is automatically loaded in `settings.py`:
```python
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
```

#### 3. Get Your Google API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the generated key
4. Set it in your environment variables

### Frontend Setup

No additional package installation needed. The feature uses React hooks and existing dependencies.

## API Endpoints

### 1. Chat Endpoint
- **URL**: `/api/ai-health/chat/`
- **Method**: `POST`
- **Body**: `{ "message": "your question" }`
- **Response**: `{ "response": "AI answer" }`

### 2. Text Report Analysis Endpoint
- **URL**: `/api/ai-health/analyze_report/`
- **Method**: `POST`
- **Body**: 
  ```json
  {
    "report_text": "blood test values here",
    "report_type": "blood_test"
  }
  ```
- **Response**: `{ "analysis": "detailed analysis" }`

### 3. Image Analysis Endpoint (New)
- **URL**: `/api/ai-health/analyze_image/`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Body**: Form data with `image` file
- **Accepted Formats**: JPEG, PNG, GIF, WebP
- **Max Size**: 5MB
- **Response**: 
  ```json
  {
    "analysis": "detailed analysis with health issues, foods to eat/avoid, etc.",
    "status": "success"
  }
  ```

## UI Components

### AIHealth.jsx Page

The page now includes:

1. **Left Column (Chat Interface)**
   - Chat with AI health assistant
   - Real-time message display
   - Send messages with Enter key or button

2. **Right Column (Report Analysis Panel)**
   - Tabbed interface with two options:
     - **Text Report Tab**: Paste medical report text
     - **Blood Report Image Tab**: Upload blood report images
   - Image preview with ability to change/remove
   - Loading states and error handling

### Key UI Features

- **Tab Navigation**: Easy switching between text and image analysis modes
- **Image Preview**: Shows selected image before analysis
- **File Validation**: 
  - Accepts only image files
  - Validates file size (max 5MB)
  - Shows helpful error messages
- **Loading States**: Visual feedback during analysis
- **Responsive Design**: Works on desktop and mobile

## Image Analysis Workflow

```
1. User selects image
   ↓
2. Image preview is displayed
   ↓
3. User clicks "Analyze Image" button
   ↓
4. Frontend sends to /ai-health/analyze_image/ endpoint
   ↓
5. Backend converts image to base64
   ↓
6. Google Gemini Vision API analyzes image
   ↓
7. Structured analysis is returned:
   - Health Issues Identified
   - Foods to Eat (Nepalese options)
   - Foods to Avoid
   - Lifestyle Tips
   - Wellness Advice
   ↓
8. Results displayed in chat interface
```

## File Changes

### Backend Changes

1. **`backend/api/views.py`**
   - Added imports: `base64`, `BytesIO`
   - Added `_get_gemini_client()` method to AIHealthViewSet
   - Added `analyze_image()` action to handle image uploads

2. **`backend/bloodhub/settings.py`**
   - Added `GOOGLE_API_KEY` configuration

### Frontend Changes

1. **`frontend/src/pages/AIHealth.jsx`**
   - Added image analysis UI with tabbed interface
   - Added state management: `selectedImage`, `imagePreview`, `analyzingImage`
   - Added handlers: `handleImageSelect()`, `handleAnalyzeImage()`, `clearImageSelection()`
   - Updated initial greeting message

2. **`frontend/src/utils/api.js`**
   - Added `analyzeBloodReportImage()` function for image uploads

## Error Handling

The feature includes comprehensive error handling:

1. **File Validation Errors**
   - Non-image file selected: "Please select an image file"
   - File too large: "Image size must be less than 5MB"
   - Invalid type: "Invalid file type. Allowed: image/jpeg, image/png..."

2. **API Errors**
   - Network errors: User-friendly error messages in chat
   - Invalid API key: Specific error about Google API configuration
   - Processing errors: Generic error with suggestion to try again

3. **Visual Feedback**
   - Disabled button during analysis
   - Loading spinner
   - Error messages displayed in chat interface

## Nepalese Dietary Recommendations

The AI is configured to recommend authentic Nepalese foods when analyzing blood reports:

### Iron-Rich Foods
- Spinach (पालक - palak)
- Lentils (दालharu)
- Red meat (रात को मासु)
- Fortified grains
- Dates (खेजुर)

### Calcium-Rich Foods
- Milk (दुध)
- Yogurt (दही)
- Sesame seeds (तिलको बिउ)
- Leafy greens

### Protein Sources
- Chickpeas (छोलेको दाल)
- Beans
- Fish (माछा)
- Eggs (अण्डा)
- Nuts (मेबलिङ)

## Testing the Feature

### Manual Testing Steps

1. Navigate to AI Health page
2. Click on "Blood Report Image" tab
3. Upload a blood report image (JPG/PNG)
4. Verify image preview displays correctly
5. Click "Analyze Image" button
6. Wait for analysis to complete
7. Verify analysis appears in chat with:
   - Health issues identified
   - Recommended foods
   - Foods to avoid
   - Lifestyle tips

### Test Cases

```
✓ Image upload with valid file
✓ Image preview display
✓ Analysis with health issues
✓ Food recommendations
✓ Error handling for large files
✓ Error handling for invalid file types
✓ API error handling
✓ Tab switching functionality
✓ Image removal/change
✓ Responsive design on mobile
```

## Production Deployment

### Before Deploying

1. **Ensure Google API Key is set**
   ```bash
   echo $GOOGLE_API_KEY  # Verify it's set
   ```

2. **Install google-generativeai package**
   ```bash
   pip install -r requirements.txt
   ```

3. **Test the feature locally**
   - Upload a test blood report image
   - Verify analysis works correctly

4. **Check file upload limits**
   - Server max upload size should be ≥ 5MB
   - Django settings should allow it

### Environment Variables (Production)

```bash
# .env file or server environment
GOOGLE_API_KEY=your-production-api-key
MISTRAL_API_KEY=your-production-api-key
```

## Troubleshooting

### Issue: "Invalid API Key" Error

**Solution**: 
- Verify Google API key is set correctly
- Check key has Generative AI API enabled in Google Cloud Console
- Ensure the key is not restricted to specific APIs

### Issue: Image Upload Fails

**Solution**:
- Check file size (must be < 5MB)
- Verify file is actual image format (not corrupted)
- Check browser console for detailed error messages

### Issue: Analysis Takes Too Long

**Solution**:
- Network latency with Google API
- Image resolution too high
- Check internet connection
- Large/complex blood reports may take longer

### Issue: Analysis Content is Incomplete

**Solution**:
- Try with clearer/higher resolution image
- Ensure blood report values are clearly visible
- Try text mode instead if image is unclear

## Future Enhancements

Potential improvements for future versions:

1. **Multiple Language Support**
   - Hindi translation of analysis
   - Nepali language responses

2. **Report History**
   - Save analyzed reports
   - Track health trends over time
   - Comparison between reports

3. **Advanced Features**
   - Export analysis as PDF
   - Share results with doctors
   - Prescription parsing

4. **Integration**
   - Connect with hospitals for direct uploads
   - Integration with wearable health devices
   - SMS delivery of recommendations

## Security Notes

1. **Image Data Privacy**
   - Images are sent to Google Gemini API
   - Follow Google's privacy policy
   - No local storage of images
   - Temporary processing only

2. **API Key Security**
   - Never commit API key to version control
   - Use environment variables only
   - Rotate keys periodically
   - Monitor usage in Google Cloud Console

3. **File Upload Security**
   - File size validation (5MB limit)
   - File type validation (image only)
   - No executable files allowed
   - Temporary storage only during processing

## Support

For issues or questions:

1. Check error messages in browser console (F12)
2. Verify Google API key configuration
3. Test with different blood report images
4. Check network connectivity
5. Review logs in backend console

## Additional Resources

- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Google Cloud Console](https://console.cloud.google.com/)
