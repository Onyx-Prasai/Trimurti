"""
Prediction model for future blood needs based on historical and current hospital requests.
"""
from django.db.models import Count
from .models import HospitalReq
from collections import Counter

def predict_blood_needs():
    """
    Predicts future blood needs for top hospitals in key districts based on historical data.
    The model identifies high-demand hospitals and predicts the most-needed blood type.
    Urgency is determined by current, unfulfilled requests.
    """
    predictions = []
    
    # Use the entire HospitalReq table as our dynamic dataset
    all_requests = HospitalReq.objects.all().values('hospital_name', 'district', 'blood_type_needed', 'blood_product_needed', 'fulfilled')

    if not all_requests:
        return []

    # Get all unique districts from the data
    all_districts = list(set(req['district'] for req in all_requests))
    
    # Focus on top districts by hospital count (top 10)
    district_counts = Counter(req['district'] for req in all_requests)
    top_districts = [district for district, _ in district_counts.most_common(10)]
    
    for district in top_districts:
        # Filter requests for the current district
        district_requests = [req for req in all_requests if req['district'] == district]
        
        if not district_requests:
            continue

        # Find the 2 hospitals with the most requests in this district
        hospital_counts = Counter(req['hospital_name'] for req in district_requests)
        top_hospitals = hospital_counts.most_common(2)

        for hospital_name, _ in top_hospitals:
            # Filter requests for the current hospital
            hospital_requests = [req for req in district_requests if req['hospital_name'] == hospital_name]
            
            # Find the most requested blood type for this hospital from historical data
            blood_type_counts = Counter(req['blood_type_needed'] for req in hospital_requests)
            predicted_blood_type = blood_type_counts.most_common(1)[0][0] if blood_type_counts else 'N/A'
            
            # Find the most requested blood product type for this hospital
            blood_product_counts = Counter(req['blood_product_needed'] for req in hospital_requests)
            predicted_blood_product = blood_product_counts.most_common(1)[0][0] if blood_product_counts else 'whole_blood'

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
                'district': district,
                'hospital_name': hospital_name,
                'predicted_blood_type': predicted_blood_type,
                'predicted_blood_product': predicted_blood_product,
                'urgency': urgency,
                'last_updated': 'now' # Placeholder, as this is a real-time prediction
            })
            
    return predictions

