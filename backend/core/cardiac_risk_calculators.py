"""
Cardiac Risk Score Calculators
===============================

SETUP INSTRUCTIONS:
-------------------
1. No additional packages needed - uses only Python standard library

2. This module implements 4 major cardiovascular risk calculators:
   - ASCVD Risk Calculator (10-year atherosclerotic cardiovascular disease risk)
   - CHADS2-VASc Score (Stroke risk in atrial fibrillation)
   - HAS-BLED Score (Bleeding risk on anticoagulation)
   - Framingham Risk Score (10-year coronary heart disease risk)

3. Usage:
   from cardiac_risk_calculators import ASCVDCalculator, CHADS2VAScCalculator
   
   ascvd = ASCVDCalculator()
   risk = ascvd.calculate(age=55, gender='male', race='white', 
                          total_chol=200, hdl=45, systolic_bp=140, 
                          on_bp_meds=True, diabetic=False, smoker=True)

HOW IT WORKS:
-------------
Each calculator:
1. Takes patient parameters as input
2. Applies validated clinical algorithms
3. Returns risk score with interpretation
4. Provides recommendations based on risk level
"""

from typing import Dict, Union
import math


class ASCVDCalculator:
    """
    ASCVD (Atherosclerotic Cardiovascular Disease) Risk Calculator
    
    Estimates 10-year risk of heart attack or stroke.
    Based on 2013 ACC/AHA Pooled Cohort Equations.
    
    Valid for patients aged 40-79 without prior ASCVD.
    """
    
    def __init__(self):
        """Initialize the ASCVD calculator with coefficients"""
        
        # Regression coefficients for different populations
        self.coefficients = {
            'white_male': {
                'ln_age': 12.344,
                'ln_total_chol': 11.853,
                'ln_age_x_ln_total_chol': -2.664,
                'ln_hdl': -7.990,
                'ln_age_x_ln_hdl': 1.769,
                'ln_treated_sbp': 1.797,
                'ln_untreated_sbp': 1.764,
                'smoker': 7.837,
                'ln_age_x_smoker': -1.795,
                'diabetes': 0.658,
                'baseline_survival': 0.9144,
                'mean_coefficient': 61.18
            },
            'white_female': {
                'ln_age': -29.799,
                'ln_age_squared': 4.884,
                'ln_total_chol': 13.540,
                'ln_age_x_ln_total_chol': -3.114,
                'ln_hdl': -13.578,
                'ln_age_x_ln_hdl': 3.149,
                'ln_treated_sbp': 2.019,
                'ln_untreated_sbp': 1.957,
                'smoker': 7.574,
                'ln_age_x_smoker': -1.665,
                'diabetes': 0.661,
                'baseline_survival': 0.9665,
                'mean_coefficient': -29.18
            },
            'black_male': {
                'ln_age': 2.469,
                'ln_total_chol': 0.302,
                'ln_hdl': -0.307,
                'ln_treated_sbp': 1.916,
                'ln_untreated_sbp': 1.809,
                'smoker': 0.549,
                'diabetes': 0.645,
                'baseline_survival': 0.8954,
                'mean_coefficient': 19.54
            },
            'black_female': {
                'ln_age': 17.114,
                'ln_total_chol': 0.940,
                'ln_hdl': -18.920,
                'ln_age_x_ln_hdl': 4.475,
                'ln_treated_sbp': 29.291,
                'ln_age_x_ln_treated_sbp': -6.432,
                'ln_untreated_sbp': 27.820,
                'ln_age_x_ln_untreated_sbp': -6.087,
                'smoker': 0.691,
                'diabetes': 0.874,
                'baseline_survival': 0.9533,
                'mean_coefficient': 86.61
            }
        }
    
    def calculate(self, 
                  age: int, 
                  gender: str, 
                  race: str,
                  total_chol: float,
                  hdl: float,
                  systolic_bp: float,
                  on_bp_meds: bool,
                  diabetic: bool,
                  smoker: bool) -> Dict:
        """
        Calculate ASCVD risk score.
        
        Args:
            age: Age in years (40-79)
            gender: 'male' or 'female'
            race: 'white' or 'black' (other races use white equations)
            total_chol: Total cholesterol in mg/dL
            hdl: HDL cholesterol in mg/dL
            systolic_bp: Systolic blood pressure in mmHg
            on_bp_meds: Whether on blood pressure medication
            diabetic: Whether has diabetes
            smoker: Whether current smoker
            
        Returns:
            Dictionary with risk score and interpretation
        """
        
        # Input validation
        if age < 40 or age > 79:
            return {
                'error': 'ASCVD calculator is valid for ages 40-79 only',
                'risk_percent': None
            }
        
        # Determine coefficient set
        key = f"{race.lower()}_{gender.lower()}"
        if key not in self.coefficients:
            key = f"white_{gender.lower()}"  # Default to white equations
        
        coef = self.coefficients[key]
        
        # Calculate natural logarithms
        ln_age = math.log(age)
        ln_total_chol = math.log(total_chol)
        ln_hdl = math.log(hdl)
        ln_sbp = math.log(systolic_bp)
        
        # Calculate individual sum
        ind_sum = 0
        
        # Add age terms
        if 'ln_age' in coef:
            ind_sum += coef['ln_age'] * ln_age
        if 'ln_age_squared' in coef:
            ind_sum += coef['ln_age_squared'] * ln_age * ln_age
        
        # Add cholesterol terms
        if 'ln_total_chol' in coef:
            ind_sum += coef['ln_total_chol'] * ln_total_chol
        if 'ln_age_x_ln_total_chol' in coef:
            ind_sum += coef['ln_age_x_ln_total_chol'] * ln_age * ln_total_chol
        
        # Add HDL terms
        if 'ln_hdl' in coef:
            ind_sum += coef['ln_hdl'] * ln_hdl
        if 'ln_age_x_ln_hdl' in coef:
            ind_sum += coef['ln_age_x_ln_hdl'] * ln_age * ln_hdl
        
        # Add blood pressure terms
        if on_bp_meds:
            if 'ln_treated_sbp' in coef:
                ind_sum += coef['ln_treated_sbp'] * ln_sbp
            if 'ln_age_x_ln_treated_sbp' in coef:
                ind_sum += coef['ln_age_x_ln_treated_sbp'] * ln_age * ln_sbp
        else:
            if 'ln_untreated_sbp' in coef:
                ind_sum += coef['ln_untreated_sbp'] * ln_sbp
            if 'ln_age_x_ln_untreated_sbp' in coef:
                ind_sum += coef['ln_age_x_ln_untreated_sbp'] * ln_age * ln_sbp
        
        # Add smoker terms
        if smoker:
            if 'smoker' in coef:
                ind_sum += coef['smoker']
            if 'ln_age_x_smoker' in coef:
                ind_sum += coef['ln_age_x_smoker'] * ln_age
        
        # Add diabetes term
        if diabetic:
            if 'diabetes' in coef:
                ind_sum += coef['diabetes']
        
        # Calculate 10-year risk
        risk = 1 - math.pow(coef['baseline_survival'], 
                           math.exp(ind_sum - coef['mean_coefficient']))
        risk_percent = risk * 100
        
        # Interpret risk
        interpretation = self._interpret_ascvd_risk(risk_percent)
        
        return {
            'risk_percent': round(risk_percent, 1),
            'risk_category': interpretation['category'],
            'interpretation': interpretation['message'],
            'recommendations': interpretation['recommendations']
        }
    
    def _interpret_ascvd_risk(self, risk_percent: float) -> Dict:
        """Interpret ASCVD risk score and provide recommendations"""
        
        if risk_percent < 5:
            return {
                'category': 'Low Risk',
                'message': 'Low 10-year risk of heart attack or stroke',
                'recommendations': [
                    'Focus on healthy lifestyle habits',
                    'Regular exercise and heart-healthy diet',
                    'Monitor blood pressure and cholesterol annually'
                ]
            }
        elif risk_percent < 7.5:
            return {
                'category': 'Borderline Risk',
                'message': 'Borderline 10-year risk of cardiovascular disease',
                'recommendations': [
                    'Discuss risk factors with your doctor',
                    'Consider lifestyle modifications',
                    'May benefit from statin therapy if risk factors present'
                ]
            }
        elif risk_percent < 20:
            return {
                'category': 'Intermediate Risk',
                'message': 'Intermediate 10-year risk - statin therapy recommended',
                'recommendations': [
                    'Moderate-intensity statin therapy recommended',
                    'Aggressive lifestyle modifications',
                    'Control of blood pressure and diabetes if present',
                    'Consider additional risk assessment (CAC score)'
                ]
            }
        else:
            return {
                'category': 'High Risk',
                'message': 'High 10-year risk - aggressive risk reduction needed',
                'recommendations': [
                    'High-intensity statin therapy recommended',
                    'Tight control of all risk factors',
                    'Consider additional therapies (e.g., PCSK9 inhibitors)',
                    'Regular follow-up with cardiologist'
                ]
            }


class CHADS2VAScCalculator:
    """
    CHA2DS2-VASc Score Calculator
    
    Estimates stroke risk in patients with atrial fibrillation.
    Used to guide anticoagulation therapy decisions.
    
    Score components:
    - Congestive heart failure (1 point)
    - Hypertension (1 point)
    - Age ≥75 (2 points)
    - Diabetes (1 point)
    - Stroke/TIA/thromboembolism history (2 points)
    - Vascular disease (1 point)
    - Age 65-74 (1 point)
    - Sex category (female, 1 point)
    """
    
    def calculate(self,
                  age: int,
                  gender: str,
                  chf: bool = False,
                  hypertension: bool = False,
                  stroke_tia_history: bool = False,
                  vascular_disease: bool = False,
                  diabetes: bool = False) -> Dict:
        """
        Calculate CHA2DS2-VASc score.
        
        Args:
            age: Age in years
            gender: 'male' or 'female'
            chf: Congestive heart failure
            hypertension: History of hypertension
            stroke_tia_history: Prior stroke or TIA
            vascular_disease: Prior MI, peripheral artery disease, or aortic plaque
            diabetes: Diabetes mellitus
            
        Returns:
            Dictionary with score and recommendations
        """
        
        score = 0
        components = []
        
        # Congestive heart failure
        if chf:
            score += 1
            components.append('CHF (1 point)')
        
        # Hypertension
        if hypertension:
            score += 1
            components.append('Hypertension (1 point)')
        
        # Age scoring
        if age >= 75:
            score += 2
            components.append('Age ≥75 (2 points)')
        elif age >= 65:
            score += 1
            components.append('Age 65-74 (1 point)')
        
        # Diabetes
        if diabetes:
            score += 1
            components.append('Diabetes (1 point)')
        
        # Stroke/TIA history
        if stroke_tia_history:
            score += 2
            components.append('Prior Stroke/TIA (2 points)')
        
        # Vascular disease
        if vascular_disease:
            score += 1
            components.append('Vascular Disease (1 point)')
        
        # Sex (female)
        if gender.lower() == 'female':
            score += 1
            components.append('Female (1 point)')
        
        # Interpret score
        interpretation = self._interpret_chads2vasc(score)
        
        return {
            'score': score,
            'components': components,
            'risk_category': interpretation['category'],
            'annual_stroke_risk': interpretation['stroke_risk'],
            'recommendation': interpretation['recommendation']
        }
    
    def _interpret_chads2vasc(self, score: int) -> Dict:
        """Interpret CHA2DS2-VASc score"""
        
        risk_table = {
            0: {'risk': '0%', 'category': 'Very Low Risk'},
            1: {'risk': '1.3%', 'category': 'Low Risk'},
            2: {'risk': '2.2%', 'category': 'Moderate Risk'},
            3: {'risk': '3.2%', 'category': 'Moderate Risk'},
            4: {'risk': '4.0%', 'category': 'High Risk'},
            5: {'risk': '6.7%', 'category': 'High Risk'},
            6: {'risk': '9.8%', 'category': 'High Risk'},
            7: {'risk': '9.6%', 'category': 'Very High Risk'},
            8: {'risk': '12.5%', 'category': 'Very High Risk'},
            9: {'risk': '15.2%', 'category': 'Very High Risk'}
        }
        
        risk_info = risk_table.get(score, risk_table[9])
        
        if score == 0:
            recommendation = 'No anticoagulation recommended (aspirin may be considered)'
        elif score == 1:
            recommendation = 'Consider anticoagulation based on individual risk/benefit assessment'
        else:
            recommendation = 'Oral anticoagulation recommended (warfarin or DOAC)'
        
        return {
            'category': risk_info['category'],
            'stroke_risk': risk_info['risk'],
            'recommendation': recommendation
        }


class HASBLEDCalculator:
    """
    HAS-BLED Score Calculator
    
    Estimates bleeding risk in patients on anticoagulation.
    
    Score components (1 point each):
    - Hypertension (uncontrolled, >160 mmHg)
    - Abnormal renal/liver function (1 point each)
    - Stroke history
    - Bleeding history or predisposition
    - Labile INR (for warfarin patients)
    - Elderly (age >65)
    - Drugs (antiplatelet agents, NSAIDs) or alcohol (1 point each)
    """
    
    def calculate(self,
                  age: int,
                  hypertension_uncontrolled: bool = False,
                  renal_disease: bool = False,
                  liver_disease: bool = False,
                  stroke_history: bool = False,
                  bleeding_history: bool = False,
                  labile_inr: bool = False,
                  on_antiplatelet_or_nsaid: bool = False,
                  alcohol_abuse: bool = False) -> Dict:
        """
        Calculate HAS-BLED score.
        
        Args:
            age: Age in years
            hypertension_uncontrolled: SBP >160 mmHg
            renal_disease: Chronic dialysis, transplant, or creatinine >2.26 mg/dL
            liver_disease: Cirrhosis or bilirubin >2x normal or AST/ALT >3x normal
            stroke_history: Prior stroke
            bleeding_history: Prior bleeding or predisposition to bleeding
            labile_inr: Unstable/high INRs or <60% time in therapeutic range
            on_antiplatelet_or_nsaid: Concurrent antiplatelet or NSAID use
            alcohol_abuse: ≥8 drinks per week
            
        Returns:
            Dictionary with score and interpretation
        """
        
        score = 0
        components = []
        
        # Hypertension
        if hypertension_uncontrolled:
            score += 1
            components.append('Uncontrolled Hypertension')
        
        # Renal disease
        if renal_disease:
            score += 1
            components.append('Abnormal Renal Function')
        
        # Liver disease
        if liver_disease:
            score += 1
            components.append('Abnormal Liver Function')
        
        # Stroke
        if stroke_history:
            score += 1
            components.append('Stroke History')
        
        # Bleeding
        if bleeding_history:
            score += 1
            components.append('Bleeding History')
        
        # Labile INR
        if labile_inr:
            score += 1
            components.append('Labile INR')
        
        # Elderly
        if age > 65:
            score += 1
            components.append('Age >65')
        
        # Drugs
        if on_antiplatelet_or_nsaid:
            score += 1
            components.append('Antiplatelet/NSAID Use')
        
        # Alcohol
        if alcohol_abuse:
            score += 1
            components.append('Alcohol Abuse')
        
        # Interpret score
        interpretation = self._interpret_hasbled(score)
        
        return {
            'score': score,
            'components': components,
            'risk_category': interpretation['category'],
            'bleeding_risk': interpretation['risk'],
            'recommendation': interpretation['recommendation']
        }
    
    def _interpret_hasbled(self, score: int) -> Dict:
        """Interpret HAS-BLED score"""
        
        if score <= 2:
            return {
                'category': 'Low Risk',
                'risk': f'{score} points - relatively low bleeding risk',
                'recommendation': 'Anticoagulation generally safe. Address modifiable risk factors.'
            }
        else:
            return {
                'category': 'High Risk',
                'risk': f'{score} points - increased bleeding risk',
                'recommendation': 'Caution required with anticoagulation. Closely monitor and address modifiable risk factors. High score should not preclude anticoagulation if clearly indicated.'
            }


class FraminghamRiskCalculator:
    """
    Framingham Risk Score Calculator
    
    Estimates 10-year risk of coronary heart disease.
    Older but still widely used risk calculator.
    """
    
    def calculate(self,
                  age: int,
                  gender: str,
                  total_chol: float,
                  hdl: float,
                  systolic_bp: float,
                  on_bp_meds: bool,
                  smoker: bool,
                  diabetic: bool) -> Dict:
        """
        Calculate Framingham risk score.
        
        Args:
            age: Age in years (30-74)
            gender: 'male' or 'female'
            total_chol: Total cholesterol mg/dL
            hdl: HDL cholesterol mg/dL
            systolic_bp: Systolic blood pressure mmHg
            on_bp_meds: On blood pressure medication
            smoker: Current smoker
            diabetic: Has diabetes
            
        Returns:
            Dictionary with risk score and interpretation
        """
        
        points = 0
        
        if gender.lower() == 'male':
            # Age points (men)
            if age < 35:
                points += -9
            elif age < 40:
                points += -4
            elif age < 45:
                points += 0
            elif age < 50:
                points += 3
            elif age < 55:
                points += 6
            elif age < 60:
                points += 8
            elif age < 65:
                points += 10
            elif age < 70:
                points += 11
            else:
                points += 12
            
            # Total cholesterol points (men)
            if total_chol < 160:
                points += 0
            elif total_chol < 200:
                points += 4
            elif total_chol < 240:
                points += 7
            elif total_chol < 280:
                points += 9
            else:
                points += 11
            
        else:  # Female
            # Age points (women)
            if age < 35:
                points += -7
            elif age < 40:
                points += -3
            elif age < 45:
                points += 0
            elif age < 50:
                points += 3
            elif age < 55:
                points += 6
            elif age < 60:
                points += 8
            elif age < 65:
                points += 10
            elif age < 70:
                points += 12
            else:
                points += 14
            
            # Total cholesterol points (women)
            if total_chol < 160:
                points += 0
            elif total_chol < 200:
                points += 4
            elif total_chol < 240:
                points += 8
            elif total_chol < 280:
                points += 11
            else:
                points += 13
        
        # HDL points (same for both)
        if hdl >= 60:
            points += -1
        elif hdl >= 50:
            points += 0
        elif hdl >= 40:
            points += 1
        else:
            points += 2
        
        # Blood pressure points
        if systolic_bp < 120:
            points += 0 if not on_bp_meds else 0
        elif systolic_bp < 130:
            points += 0 if not on_bp_meds else 1
        elif systolic_bp < 140:
            points += 1 if not on_bp_meds else 2
        elif systolic_bp < 160:
            points += 1 if not on_bp_meds else 2
        else:
            points += 2 if not on_bp_meds else 3
        
        # Diabetes
        if diabetic:
            points += 2
        
        # Smoking
        if smoker:
            points += 2
        
        # Calculate risk percentage
        risk_percent = self._points_to_risk(points, gender)
        
        return {
            'points': points,
            'risk_percent': risk_percent,
            'risk_category': self._categorize_framingham_risk(risk_percent),
            'interpretation': f'{risk_percent}% 10-year risk of coronary heart disease'
        }
    
    def _points_to_risk(self, points: int, gender: str) -> float:
        """Convert Framingham points to risk percentage"""
        
        if gender.lower() == 'male':
            risk_map = {
                -3: 1, -2: 1, -1: 1, 0: 1, 1: 1, 2: 2, 3: 2, 4: 2,
                5: 3, 6: 4, 7: 5, 8: 6, 9: 8, 10: 10, 11: 12, 12: 16,
                13: 20, 14: 25, 15: 30, 16: 30
            }
        else:
            risk_map = {
                -2: 1, -1: 1, 0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 2,
                6: 2, 7: 3, 8: 4, 9: 5, 10: 6, 11: 8, 12: 10, 13: 12,
                14: 16, 15: 20, 16: 25, 17: 30
            }
        
        return risk_map.get(points, 30 if points > 16 else 1)
    
    def _categorize_framingham_risk(self, risk_percent: float) -> str:
        """Categorize Framingham risk"""
        
        if risk_percent < 10:
            return 'Low Risk'
        elif risk_percent < 20:
            return 'Moderate Risk'
        else:
            return 'High Risk'


# Example usage
if __name__ == "__main__":
    print("=== CARDIOVASCULAR RISK CALCULATORS ===\n")
    
    # Example 1: ASCVD Calculator
    print("1. ASCVD Risk Score Example")
    print("-" * 50)
    ascvd = ASCVDCalculator()
    result = ascvd.calculate(
        age=55,
        gender='male',
        race='white',
        total_chol=220,
        hdl=45,
        systolic_bp=140,
        on_bp_meds=True,
        diabetic=False,
        smoker=True
    )
    print(f"10-Year ASCVD Risk: {result['risk_percent']}%")
    print(f"Category: {result['risk_category']}")
    print(f"Interpretation: {result['interpretation']}")
    print("\nRecommendations:")
    for rec in result['recommendations']:
        print(f"  • {rec}")
    
    # Example 2: CHA2DS2-VASc Calculator
    print("\n\n2. CHA2DS2-VASc Score Example (Atrial Fibrillation)")
    print("-" * 50)
    chads = CHADS2VAScCalculator()
    result = chads.calculate(
        age=72,
        gender='female',
        chf=True,
        hypertension=True,
        stroke_tia_history=False,
        vascular_disease=False,
        diabetes=True
    )
    print(f"CHA2DS2-VASc Score: {result['score']}")
    print(f"Risk Category: {result['risk_category']}")
    print(f"Annual Stroke Risk: {result['annual_stroke_risk']}")
    print(f"Recommendation: {result['recommendation']}")
    print("\nScore Components:")
    for comp in result['components']:
        print(f"  • {comp}")
    
    # Example 3: HAS-BLED Calculator
    print("\n\n3. HAS-BLED Score Example (Bleeding Risk)")
    print("-" * 50)
    hasbled = HASBLEDCalculator()
    result = hasbled.calculate(
        age=70,
        hypertension_uncontrolled=False,
        renal_disease=True,
        liver_disease=False,
        stroke_history=False,
        bleeding_history=False,
        labile_inr=True,
        on_antiplatelet_or_nsaid=True,
        alcohol_abuse=False
    )
    print(f"HAS-BLED Score: {result['score']}")
    print(f"Risk Category: {result['risk_category']}")
    print(f"Bleeding Risk: {result['bleeding_risk']}")
    print(f"Recommendation: {result['recommendation']}")
    print("\nRisk Factors:")
    for comp in result['components']:
        print(f"  • {comp}")
    
    # Example 4: Framingham Risk Score
    print("\n\n4. Framingham Risk Score Example")
    print("-" * 50)
    fram = FraminghamRiskCalculator()
    result = fram.calculate(
        age=50,
        gender='male',
        total_chol=200,
        hdl=40,
        systolic_bp=130,
        on_bp_meds=False,
        smoker=True,
        diabetic=False
    )
    print(f"Framingham Points: {result['points']}")
    print(f"10-Year CHD Risk: {result['risk_percent']}%")
    print(f"Risk Category: {result['risk_category']}")
    print(f"Interpretation: {result['interpretation']}")