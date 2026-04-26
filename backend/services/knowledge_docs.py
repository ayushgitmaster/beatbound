"""
Cardiac knowledge documents used to seed the ChromaDB vector store.
These cover key clinical guidelines, risk factor education, and emergency protocols.
"""
from langchain_core.documents import Document


def get_cardiac_documents() -> list[Document]:
    docs = [
        Document(
            page_content=(
                "Chest pain assessment: Typical angina has three features — (1) substernal chest "
                "discomfort, (2) provoked by exertion or emotional stress, (3) relieved by rest or "
                "nitrates in <5 minutes. Atypical presentations are more common in women, diabetics, "
                "and the elderly. STEMI is identified by ≥1 mm ST elevation in ≥2 contiguous limb "
                "leads or ≥2 mm in precordial leads. Immediate reperfusion therapy (PCI within 90 min) "
                "is the standard of care for STEMI. Troponin levels rise 3–6 h after onset and peak "
                "at 24 h; high-sensitivity troponin allows earlier 0/2h or 0/3h rule-out algorithms."
            ),
            metadata={"source": "AHA STEMI Guidelines 2023", "doc_type": "clinical", "page": 1},
        ),
        Document(
            page_content=(
                "ACC/AHA 2019 Primary Prevention Guidelines: Statin therapy is recommended for "
                "adults aged 40–75 with LDL-C ≥70 mg/dL who have diabetes, or LDL-C ≥190 mg/dL. "
                "For primary prevention in 40-75 year olds, calculate 10-year ASCVD risk using the "
                "Pooled Cohort Equations. High-intensity statins (atorvastatin 40–80 mg, rosuvastatin "
                "20–40 mg) reduce LDL by ≥50%. Moderate intensity reduces LDL by 30–50%. Lifestyle "
                "counselling (diet, exercise, avoid smoking) is recommended for everyone. Aspirin for "
                "primary prevention is NOT routinely recommended due to increased bleeding risk."
            ),
            metadata={"source": "ACC/AHA Primary Prevention Guidelines 2019", "doc_type": "clinical", "page": 3},
        ),
        Document(
            page_content=(
                "Heart failure classification and management: NYHA class I–IV based on symptoms. "
                "HFrEF (EF<40%) is treated with ACE inhibitors/ARBs/ARNi (sacubitril-valsartan), "
                "beta-blockers (carvedilol, metoprolol succinate, bisoprolol), MRAs (spironolactone), "
                "and SGLT2 inhibitors (dapagliflozin, empagliflozin). BNP >400 pg/mL or NT-proBNP "
                ">1800 pg/mL supports diagnosis. Diuretics (furosemide) relieve congestion. "
                "Device therapy: ICD for EF<35% despite 3 months GDMT, CRT for EF<35% with LBBB "
                "and QRS ≥150 ms. Hospitalization triggers: dyspnea at rest, orthopnea, weight gain >2 kg in 3 days."
            ),
            metadata={"source": "ACC/AHA HF Guidelines 2022", "doc_type": "clinical", "page": 5},
        ),
        Document(
            page_content=(
                "Atrial fibrillation management: Rate control targets HR <80 bpm at rest (beta-blockers, "
                "diltiazem, digoxin). Rhythm control with antiarrhythmics (flecainide, propafenone for "
                "paroxysmal AF without structural heart disease; amiodarone, dofetilide for HF). "
                "Anticoagulation using CHA2DS2-VASc score: score ≥2 (men) or ≥3 (women) → DOAC "
                "(apixaban, rivaroxaban, dabigatran, edoxaban) preferred over warfarin. Assess bleeding "
                "risk with HAS-BLED score. Catheter ablation (pulmonary vein isolation) can maintain "
                "sinus rhythm; consider in symptomatic paroxysmal AF refractory to antiarrhythmics."
            ),
            metadata={"source": "ESC AF Guidelines 2023", "doc_type": "clinical", "page": 2},
        ),
        Document(
            page_content=(
                "Cardiovascular risk factors and lifestyle modification: "
                "Hypertension target <130/80 mmHg per ACC/AHA 2017 guidelines. Lifestyle: "
                "DASH diet, sodium <2.3 g/day, weight loss, aerobic exercise 150 min/week moderate "
                "or 75 min vigorous. Diabetes HbA1c target <7% (individualize 7–8% for elderly). "
                "Smoking cessation reduces CV risk by 50% within 1 year. LDL targets: very high risk "
                "<55 mg/dL, high risk <70 mg/dL, moderate risk <100 mg/dL. Obesity (BMI>30) increases "
                "risk; target 5–10% weight loss improves metabolic parameters. Mediterranean diet reduces "
                "MACE by ~30% (PREDIMED trial)."
            ),
            metadata={"source": "ESC CVD Prevention Guidelines 2021", "doc_type": "clinical", "page": 7},
        ),
        Document(
            page_content=(
                "ASCVD risk calculation using Pooled Cohort Equations (2013 ACC/AHA): "
                "Variables: age, sex, race, total cholesterol, HDL cholesterol, systolic BP, "
                "BP treatment status, diabetes, smoking status. Valid for ages 40–79. "
                "10-year ASCVD risk categories: Low <5%, Borderline 5–7.5%, Intermediate 7.5–20%, "
                "High ≥20%. For high risk: initiate high-intensity statin. For intermediate risk: "
                "discuss statin therapy (risk-enhancing factors: LDL ≥160, hs-CRP ≥2, CAC score ≥100). "
                "For borderline risk with risk-enhancing factors: moderate-intensity statin. "
                "For low risk: lifestyle modification."
            ),
            metadata={"source": "ACC/AHA PCE Guidelines 2013", "doc_type": "clinical", "page": 9},
        ),
        Document(
            page_content=(
                "Emergency cardiac protocols — heart attack recognition and action: "
                "Call emergency services (911) immediately for: crushing chest pain, pain radiating to "
                "jaw/left arm/back, sudden shortness of breath, cold sweat + nausea, sudden sense of doom. "
                "While waiting: chew aspirin 325 mg (not swallow) if not allergic, loosen tight clothing, "
                "remain calm, do NOT drive yourself to hospital. Bystander CPR if unconscious: 30 chest "
                "compressions (2 inches deep, 100–120/min) then 2 rescue breaths. Use AED if available. "
                "Golden hour principle: door-to-balloon time <90 minutes for STEMI."
            ),
            metadata={"source": "AHA Emergency Cardiac Care 2023", "doc_type": "emergency", "page": 1},
        ),
        Document(
            page_content=(
                "Cholesterol management and dyslipidemia: Fasting lipid panel interpretation — "
                "Desirable: Total chol <200 mg/dL, LDL <100 mg/dL (optimal), HDL>60 protective, "
                "TG <150 mg/dL. Borderline high: total 200–239, LDL 130–159, TG 150–199. "
                "High: total ≥240, LDL ≥160, TG 200–499. Very high TG ≥500: pancreatitis risk. "
                "Non-HDL cholesterol = Total − HDL (target <130 mg/dL for primary prevention, <100 for high risk). "
                "Drug therapy: statins first-line; ezetimibe adds 15–25% LDL reduction; PCSK9 inhibitors "
                "(evolocumab, alirocumab) reduce LDL by 50–60% with minimal side effects; omega-3 FA "
                "reduces TG 20–30%."
            ),
            metadata={"source": "ACC/AHA Cholesterol Guidelines 2018", "doc_type": "clinical", "page": 4},
        ),
        Document(
            page_content=(
                "Cardiac biomarkers interpretation: High-sensitivity troponin I/T (hs-cTn): Levels "
                "above 99th percentile URL indicate myocardial injury. Serial measurements at 0/1h or "
                "0/2h recommended. Rise and/or fall pattern with clinical symptoms = NSTEMI. "
                "BNP >100 pg/mL or NT-proBNP >300 pg/mL suggests heart failure, though CKD and "
                "obesity affect levels. CK-MB: less specific, useful for reinfarction detection. "
                "D-dimer: elevated in PE/DVT but non-specific (elevated in infections, pregnancy, malignancy). "
                "LDH: nonspecific marker of tissue damage. hs-CRP >3 mg/L = high CV risk even when "
                "LDL is normal."
            ),
            metadata={"source": "ESC Biomarker Guidelines 2023", "doc_type": "clinical", "page": 6},
        ),
        Document(
            page_content=(
                "Hypertensive emergencies: Hypertensive urgency (BP ≥180/120 without organ damage) "
                "vs hypertensive emergency (with organ damage — aortic dissection, hypertensive "
                "encephalopathy, pulmonary oedema, STEMI, acute kidney injury, eclampsia). "
                "Emergency management: IV labetalol, nicardipine, or clevidipine. Target: reduce MAP "
                "by ≤25% in first hour, then 160/100 over next 2–6 hours (not to normal acutely; "
                "risk of ischemia). Aortic dissection exception: target SBP 100–120 immediately "
                "with IV esmolol + nicardipine. Eclampsia: IV magnesium sulphate + antihypertensives."
            ),
            metadata={"source": "AHA Hypertension Crisis Statement 2023", "doc_type": "clinical", "page": 8},
        ),
        Document(
            page_content=(
                "Coronary artery disease (CAD) diagnosis and management: "
                "Stable CAD workup: resting ECG, exercise stress testing (sensitivity 68%, specificity 77%), "
                "stress echo or nuclear imaging for intermediate risk. CT coronary angiography for low-intermediate "
                "risk (high NPV). Invasive coronary angiography gold standard. FFR ≤0.80 = haemodynamically "
                "significant lesion → revascularisation. SYNTAX score guides PCI vs CABG: SYNTAX >22 "
                "multivessel disease → CABG preferred (SYNTAX trial). Medical therapy: aspirin 75–100 mg/day, "
                "statin, beta-blocker post-MI, ACEi/ARB for EF<40% or diabetes."
            ),
            metadata={"source": "ESC Chronic Coronary Syndromes Guidelines 2019", "doc_type": "clinical", "page": 10},
        ),
        Document(
            page_content=(
                "Diabetes and cardiovascular disease: Cardiovascular disease is the leading cause of "
                "death in type 2 diabetes. SGLT2 inhibitors (empagliflozin, dapagliflozin, canagliflozin) "
                "reduce MACE, hospitalisation for HF, and CKD progression. GLP-1 RAs (liraglutide, "
                "semaglutide, dulaglutide) reduce MACE in patients with established CVD or high risk. "
                "Target HbA1c 7% for most; 8% for elderly or frail. BP target <130/80. Statin therapy "
                "recommended for all diabetics aged 40-75. Weight loss (5-10%) improves glycaemic control "
                "and reduces CV risk. Screen for autonomic neuropathy (affects resting HR and BP response)."
            ),
            metadata={"source": "ADA/ACC Diabetes CVD Guidance 2023", "doc_type": "clinical", "page": 11},
        ),
    ]
    return docs
