"""
Prediction model for future blood needs based on historical and current hospital requests.
"""
from django.db.models import Count
from .models import HospitalReq
from collections import Counter

def predict_blood_needs():
    """
    Predicts future blood needs for top hospitals in key cities based on historical data.
    The model identifies high-demand hospitals and predicts the most-needed blood type.
    Urgency is determined by current, unfulfilled requests.
    """
    predictions = []
    
    # Use the entire HospitalReq table as our dynamic dataset
    all_requests = HospitalReq.objects.all().values('hospital_name', 'city', 'blood_type_needed', 'fulfilled')

    if not all_requests:
        return []

    cities = ['Kathmandu', 'Bhaktapur', 'Lalitpur']
    
    for city in cities:
        # Filter requests for the current city
        city_requests = [req for req in all_requests if req['city'] == city]
        
        if not city_requests:
            continue

        # Find the 2 hospitals with the most requests in this city
        hospital_counts = Counter(req['hospital_name'] for req in city_requests)
        top_hospitals = hospital_counts.most_common(2)

        for hospital_name, _ in top_hospitals:
            # Filter requests for the current hospital
            hospital_requests = [req for req in city_requests if req['hospital_name'] == hospital_name]
            
            # Find the most requested blood type for this hospital from historical data
            blood_type_counts = Counter(req['blood_type_needed'] for req in hospital_requests)
            predicted_blood_type = blood_type_counts.most_common(1)[0][0] if blood_type_counts else 'N/A'

            # Determine urgency based on current, unfulfilled requests for the predicted blood type
            current_active_requests = [
                req for req in hospital_requests 
                if req['blood_type_needed'] == predicted_blood_type and not req['fulfilled']
            ]
            
            urgency = 'Low'
            if len(current_active_requests) > 0:
                urgency = 'High'
            elif any(not req['fulfilled'] for req in hospital_requests):
                # If there are other active requests, urgency is medium
                urgency = 'Medium'

            predictions.append({
                'city': city,
                'hospital_name': hospital_name,
                'predicted_blood_type': predicted_blood_type,
                'urgency': urgency,
                'last_updated': 'now' # Placeholder, as this is a real-time prediction
            })
            
    return predictions

