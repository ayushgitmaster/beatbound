"""Heart Health Knowledge Base."""
# Common heart-related symptoms and their descriptions
HEART_SYMPTOMS = {
    "chest_pain": {"name": "Chest Pain or Discomfort", "description": "Pain, pressure, squeezing, or fullness in the center or left side of the chest. May last several minutes or come and go.", "severity": "high", "advice": "Seek immediate medical attention, especially if severe, lasting more than a few minutes, or accompanied by other symptoms.", "emergency": True},
    "shortness_of_breath": {"name": "Shortness of Breath", "description": "Difficulty breathing or feeling like you can't get enough air, especially when lying down or with minimal exertion.", "severity": "high", "advice": "Seek immediate medical attention if sudden or severe, especially if accompanied by chest pain.", "emergency": True},
    "heart_palpitations": {"name": "Heart Palpitations", "description": "Feeling like your heart is racing, pounding, fluttering, or skipping beats.", "severity": "medium", "advice": "Contact your doctor if palpitations are frequent, severe, or accompanied by chest pain, shortness of breath, or dizziness.", "emergency": False},
    "fatigue": {"name": "Unusual Fatigue", "description": "Extreme tiredness or unexplained weakness, especially during activities that were previously easy.", "severity": "medium", "advice": "Consult with your doctor, especially if fatigue is persistent or worsening.", "emergency": False},
    "swelling": {"name": "Swelling in Legs, Ankles, or Feet", "description": "Fluid buildup causing swelling in the lower extremities, which may be a sign of heart failure.", "severity": "medium", "advice": "Contact your doctor, especially if swelling is sudden or worsening.", "emergency": False},
    "dizziness": {"name": "Dizziness or Lightheadedness", "description": "Feeling faint, lightheaded, or like you might pass out.", "severity": "medium", "advice": "Sit or lie down immediately. If symptoms persist or recur, contact your doctor.", "emergency": False},
    "syncope": {"name": "Fainting (Syncope)", "description": "Temporary loss of consciousness due to insufficient blood flow to the brain.", "severity": "high", "advice": "Seek immediate medical attention, as this could indicate a serious heart problem.", "emergency": True},
    "nausea": {"name": "Nausea or Vomiting", "description": "Feeling sick to your stomach or vomiting, which can sometimes accompany heart problems, especially in women.", "severity": "medium", "advice": "If accompanied by chest pain or other heart symptoms, seek immediate medical attention.", "emergency": False},
    "cold_sweat": {"name": "Cold Sweat", "description": "Sudden, unexplained cold sweating, often accompanying chest pain during a heart attack.", "severity": "high", "advice": "Seek immediate medical attention, especially if accompanied by chest pain or shortness of breath.", "emergency": True},
    "jaw_pain": {"name": "Jaw, Neck, or Back Pain", "description": "Pain or discomfort in the jaw, neck, or back, particularly during physical activity or stress. Can be a symptom of heart attack, especially in women.", "severity": "high", "advice": "Seek immediate medical attention if pain is sudden, severe, or accompanied by other heart attack symptoms.", "emergency": True},
}
HEART_CONDITIONS = {
    "coronary_artery_disease": {"name": "Coronary Artery Disease (CAD)", "description": "Narrowing or blockage of the coronary arteries that supply blood to the heart muscle.", "common_symptoms": ["chest_pain", "shortness_of_breath", "fatigue"], "risk_factors": ["high blood pressure", "high cholesterol", "smoking", "diabetes", "obesity", "family history"], "prevention": "Healthy diet, regular exercise, not smoking, managing blood pressure and cholesterol."},
    "heart_attack": {"name": "Heart Attack (Myocardial Infarction)", "description": "Occurs when blood flow to part of the heart is blocked, causing damage to heart muscle.", "common_symptoms": ["chest_pain", "shortness_of_breath", "cold_sweat", "nausea", "jaw_pain"], "risk_factors": ["coronary artery disease", "high blood pressure", "high cholesterol", "smoking", "diabetes", "family history"], "emergency_action": "Call emergency services (911) immediately. If prescribed, take aspirin."},
    "heart_failure": {"name": "Heart Failure", "description": "Condition where the heart can't pump blood effectively to meet the body's needs.", "common_symptoms": ["shortness_of_breath", "fatigue", "swelling"], "risk_factors": ["coronary artery disease", "heart attack", "high blood pressure", "diabetes", "valve disease"], "management": "Medications, lifestyle changes, device therapy in some cases."},
    "arrhythmia": {"name": "Arrhythmia", "description": "Abnormal heart rhythm - too fast, too slow, or irregular.", "common_symptoms": ["heart_palpitations", "dizziness", "syncope", "fatigue"], "types": ["atrial fibrillation", "bradycardia", "tachycardia", "heart block"], "management": "Medications, cardioversion, ablation, pacemakers or implantable defibrillators in some cases."},
    "valve_disease": {"name": "Heart Valve Disease", "description": "Problems with one or more heart valves that affect blood flow through the heart.", "common_symptoms": ["shortness_of_breath", "fatigue", "heart_palpitations", "swelling"], "types": ["stenosis (narrowing)", "regurgitation (leaking)", "prolapse (bulging)"], "management": "Monitoring, medications, valve repair or replacement surgery when necessary."},
}
HEART_HEALTH_ADVICE = {
    "diet": {"title": "Heart-Healthy Diet", "recommendations": ["Eat plenty of fruits, vegetables, and whole grains", "Choose lean proteins like fish, poultry, beans, and nuts", "Limit saturated and trans fats, sodium, and added sugars", "Consider Mediterranean or DASH diet approaches", "Stay hydrated with water rather than sugary drinks"]},
    "exercise": {"title": "Physical Activity", "recommendations": ["Aim for at least 150 minutes of moderate-intensity exercise per week", "Include both aerobic exercise and strength training", "Start slowly and gradually increase intensity if you've been inactive", "Find activities you enjoy to help maintain consistency", "Even short periods of activity throughout the day are beneficial"]},
    "lifestyle": {"title": "Healthy Lifestyle Habits", "recommendations": ["Don't smoke or use tobacco products", "Limit alcohol consumption", "Manage stress through techniques like meditation, deep breathing, or yoga", "Get 7-9 hours of quality sleep each night", "Maintain a healthy weight"]},
    "monitoring": {"title": "Regular Health Monitoring", "recommendations": ["Schedule regular check-ups with your healthcare provider", "Know your numbers: blood pressure, cholesterol, blood sugar", "Take medications as prescribed", "Learn to recognize warning signs of heart problems", "Consider home monitoring for blood pressure if recommended by your doctor"]},
}
EMERGENCY_GUIDANCE = {
    "heart_attack": {"title": "Heart Attack Emergency Actions", "steps": ["Call emergency services (911) immediately", "Chew and swallow an aspirin if not allergic and if advised by emergency services", "Rest in a comfortable position, typically sitting upright", "Loosen tight clothing", "If unconscious and not breathing normally, begin CPR if trained"]},
    "when_to_call": {"title": "When to Seek Emergency Help", "situations": ["Chest pain or discomfort lasting more than a few minutes or that goes away and comes back", "Severe shortness of breath", "Fainting, sudden dizziness, or weakness", "Pain or discomfort in the jaw, neck, back, one or both arms, or stomach", "Cold sweat along with chest discomfort", "Sudden confusion or trouble speaking"]},
}
RISK_FACTORS = {
    "non_modifiable": {"title": "Non-Modifiable Risk Factors", "factors": ["Age (risk increases with age)", "Gender (men generally at higher risk, though risk for women increases after menopause)", "Family history of heart disease", "Ethnicity (some groups have higher risk)"]},
    "modifiable": {"title": "Modifiable Risk Factors", "factors": ["High blood pressure", "High cholesterol", "Smoking", "Diabetes", "Obesity", "Physical inactivity", "Unhealthy diet", "Excessive alcohol consumption", "Stress", "Poor sleep habits"]},
}
def get_symptom_info(symptom_key): return HEART_SYMPTOMS.get(symptom_key, None)
def get_condition_info(condition_key): return HEART_CONDITIONS.get(condition_key, None)
def get_health_advice(topic_key): return HEART_HEALTH_ADVICE.get(topic_key, None)
def get_emergency_guidance(situation_key): return EMERGENCY_GUIDANCE.get(situation_key, None)
def is_emergency(symptoms_list):
    for symptom in symptoms_list:
        if symptom in HEART_SYMPTOMS and HEART_SYMPTOMS[symptom].get("emergency", False):
            return True
    return False
