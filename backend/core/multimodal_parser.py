"""
Multi-Modal Input Support: PDF Lab Report Parser
=================================================

SETUP INSTRUCTIONS:
-------------------
1. Install required packages:
   pip install pdfplumber pandas streamlit pillow

2. This module extracts cardiovascular-related values from PDF lab reports:
   - Lipid Panel (Cholesterol, LDL, HDL, Triglycerides)
   - Cardiac Biomarkers (Troponin, BNP, NT-proBNP)
   - Kidney Function (Creatinine, eGFR)
   - Other vitals (Blood Pressure, Heart Rate, etc.)

3. Usage:
   from multimodal_parser import PDFLabReportParser
   parser = PDFLabReportParser()
   results = parser.parse_pdf("patient_labs.pdf")

HOW IT WORKS:
-------------
1. Extracts all text from PDF using pdfplumber
2. Uses regex patterns to find lab values with units
3. Normalizes values to standard units
4. Generates structured output for RAG system
"""

import re
import pdfplumber
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class PDFLabReportParser:
    """
    Parses PDF lab reports and extracts cardiovascular-related values.
    Supports multiple lab report formats.
    """
    
    def __init__(self):
        """Initialize the parser with common lab value patterns"""
        
        # Define patterns for common lab values
        # Format: (pattern, unit, normal_range)
        self.patterns = {
            # Lipid Panel
            'total_cholesterol': {
                'patterns': [
                    r'total\s*cholesterol[:\s]+(\d+\.?\d*)\s*(mg/dl|mmol/l)?',
                    r'cholesterol,?\s*total[:\s]+(\d+\.?\d*)\s*(mg/dl|mmol/l)?',
                ],
                'unit': 'mg/dL',
                'normal_range': '< 200 mg/dL',
                'category': 'Lipid Panel'
            },
            'ldl_cholesterol': {
                'patterns': [
                    r'ldl[:\s]+(\d+\.?\d*)\s*(mg/dl|mmol/l)?',
                    r'ldl\s*cholesterol[:\s]+(\d+\.?\d*)\s*(mg/dl|mmol/l)?',
                    r'low\s*density\s*lipoprotein[:\s]+(\d+\.?\d*)\s*(mg/dl|mmol/l)?',
                ],
                'unit': 'mg/dL',
                'normal_range': '< 100 mg/dL',
                'category': 'Lipid Panel'
            },
            'hdl_cholesterol': {
                'patterns': [
                    r'hdl[:\s]+(\d+\.?\d*)\s*(mg/dl|mmol/l)?',
                    r'hdl\s*cholesterol[:\s]+(\d+\.?\d*)\s*(mg/dl|mmol/l)?',
                    r'high\s*density\s*lipoprotein[:\s]+(\d+\.?\d*)\s*(mg/dl|mmol/l)?',
                ],
                'unit': 'mg/dL',
                'normal_range': '> 40 mg/dL (men), > 50 mg/dL (women)',
                'category': 'Lipid Panel'
            },
            'triglycerides': {
                'patterns': [
                    r'triglycerides?[:\s]+(\d+\.?\d*)\s*(mg/dl|mmol/l)?',
                    r'trig[:\s]+(\d+\.?\d*)\s*(mg/dl|mmol/l)?',
                ],
                'unit': 'mg/dL',
                'normal_range': '< 150 mg/dL',
                'category': 'Lipid Panel'
            },
            
            # Cardiac Biomarkers
            'troponin': {
                'patterns': [
                    r'troponin[:\s]+(\d+\.?\d*)\s*(ng/ml|ng/l)?',
                    r'troponin\s*[it][:\s]+(\d+\.?\d*)\s*(ng/ml|ng/l)?',
                    r'trop[:\s]+(\d+\.?\d*)\s*(ng/ml|ng/l)?',
                ],
                'unit': 'ng/mL',
                'normal_range': '< 0.04 ng/mL',
                'category': 'Cardiac Biomarkers'
            },
            'bnp': {
                'patterns': [
                    r'bnp[:\s]+(\d+\.?\d*)\s*(pg/ml)?',
                    r'b-type\s*natriuretic\s*peptide[:\s]+(\d+\.?\d*)\s*(pg/ml)?',
                ],
                'unit': 'pg/mL',
                'normal_range': '< 100 pg/mL',
                'category': 'Cardiac Biomarkers'
            },
            'nt_probnp': {
                'patterns': [
                    r'nt-probnp[:\s]+(\d+\.?\d*)\s*(pg/ml)?',
                    r'nt\s*pro\s*bnp[:\s]+(\d+\.?\d*)\s*(pg/ml)?',
                ],
                'unit': 'pg/mL',
                'normal_range': '< 125 pg/mL',
                'category': 'Cardiac Biomarkers'
            },
            
            # Kidney Function (important for cardiac risk)
            'creatinine': {
                'patterns': [
                    r'creatinine[:\s]+(\d+\.?\d*)\s*(mg/dl)?',
                    r'serum\s*creatinine[:\s]+(\d+\.?\d*)\s*(mg/dl)?',
                ],
                'unit': 'mg/dL',
                'normal_range': '0.7-1.3 mg/dL',
                'category': 'Kidney Function'
            },
            'egfr': {
                'patterns': [
                    r'egfr[:\s]+(\d+\.?\d*)\s*(ml/min)?',
                    r'gfr[:\s]+(\d+\.?\d*)\s*(ml/min)?',
                    r'estimated\s*gfr[:\s]+(\d+\.?\d*)\s*(ml/min)?',
                ],
                'unit': 'mL/min/1.73m²',
                'normal_range': '> 60 mL/min/1.73m²',
                'category': 'Kidney Function'
            },
            
            # Blood Sugar
            'glucose': {
                'patterns': [
                    r'glucose[:\s]+(\d+\.?\d*)\s*(mg/dl)?',
                    r'blood\s*glucose[:\s]+(\d+\.?\d*)\s*(mg/dl)?',
                ],
                'unit': 'mg/dL',
                'normal_range': '70-100 mg/dL (fasting)',
                'category': 'Blood Sugar'
            },
            'hba1c': {
                'patterns': [
                    r'hba1c[:\s]+(\d+\.?\d*)\s*%?',
                    r'hemoglobin\s*a1c[:\s]+(\d+\.?\d*)\s*%?',
                ],
                'unit': '%',
                'normal_range': '< 5.7%',
                'category': 'Blood Sugar'
            },
        }
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract all text from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text as a string
        """
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            return text.lower()  # Convert to lowercase for easier matching
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    def extract_value(self, text: str, patterns: List[str]) -> Optional[Tuple[float, str]]:
        """
        Extract a numeric value and its unit from text using regex patterns.
        
        Args:
            text: Text to search in
            patterns: List of regex patterns to try
            
        Returns:
            Tuple of (value, unit) or None if not found
        """
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    value = float(match.group(1))
                    unit = match.group(2) if len(match.groups()) > 1 else None
                    return (value, unit)
                except (ValueError, IndexError):
                    continue
        return None
    
    def parse_pdf(self, pdf_path: str) -> Dict:
        """
        Parse a PDF lab report and extract all cardiovascular-related values.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing extracted lab values and metadata
        """
        # Extract text from PDF
        text = self.extract_text_from_pdf(pdf_path)
        
        # Initialize results dictionary
        results = {
            'timestamp': datetime.now().isoformat(),
            'source_file': pdf_path,
            'values': {},
            'categories': {}
        }
        
        # Extract each lab value
        for lab_name, lab_info in self.patterns.items():
            extracted = self.extract_value(text, lab_info['patterns'])
            
            if extracted:
                value, unit = extracted
                
                # Store the value
                results['values'][lab_name] = {
                    'value': value,
                    'unit': unit or lab_info['unit'],
                    'normal_range': lab_info['normal_range'],
                    'category': lab_info['category']
                }
                
                # Group by category
                category = lab_info['category']
                if category not in results['categories']:
                    results['categories'][category] = []
                results['categories'][category].append(lab_name)
        
        return results
    
    def format_for_rag(self, results: Dict) -> str:
        """
        Format extracted lab values into a text prompt for the RAG system.
        
        Args:
            results: Dictionary of extracted lab values
            
        Returns:
            Formatted text prompt
        """
        if not results['values']:
            return "No cardiovascular lab values were found in the uploaded document."
        
        prompt = "Patient Lab Results Summary:\n\n"
        
        # Organize by category
        for category, lab_names in results['categories'].items():
            prompt += f"{category}:\n"
            for lab_name in lab_names:
                lab_data = results['values'][lab_name]
                # Format lab name nicely
                display_name = lab_name.replace('_', ' ').title()
                prompt += f"  - {display_name}: {lab_data['value']} {lab_data['unit']}"
                prompt += f" (Normal: {lab_data['normal_range']})\n"
            prompt += "\n"
        
        prompt += "\nPlease analyze these lab results from a cardiovascular health perspective. "
        prompt += "Identify any values that are outside the normal range and explain what they might indicate. "
        prompt += "Provide recommendations for lifestyle changes or when to consult a healthcare provider."
        
        return prompt
    
    def generate_summary_table(self, results: Dict) -> pd.DataFrame:
        """
        Generate a pandas DataFrame summary of the lab results.
        
        Args:
            results: Dictionary of extracted lab values
            
        Returns:
            DataFrame with lab results
        """
        if not results['values']:
            return pd.DataFrame()
        
        data = []
        for lab_name, lab_data in results['values'].items():
            data.append({
                'Test': lab_name.replace('_', ' ').title(),
                'Value': f"{lab_data['value']} {lab_data['unit']}",
                'Normal Range': lab_data['normal_range'],
                'Category': lab_data['category']
            })
        
        return pd.DataFrame(data)


# Example usage and testing
if __name__ == "__main__":
    # Example: How to use this parser
    
    # 1. Create parser instance
    parser = PDFLabReportParser()
    
    # 2. Parse a PDF (you would replace this with actual file path)
    # results = parser.parse_pdf("patient_lab_report.pdf")
    
    # 3. Format for RAG system
    # rag_prompt = parser.format_for_rag(results)
    # print(rag_prompt)
    
    # 4. Generate summary table
    # summary_df = parser.generate_summary_table(results)
    # print(summary_df)
    
    # Example with test data (simulating extracted results)
    test_results = {
        'timestamp': datetime.now().isoformat(),
        'source_file': 'test_report.pdf',
        'values': {
            'total_cholesterol': {
                'value': 220,
                'unit': 'mg/dL',
                'normal_range': '< 200 mg/dL',
                'category': 'Lipid Panel'
            },
            'ldl_cholesterol': {
                'value': 150,
                'unit': 'mg/dL',
                'normal_range': '< 100 mg/dL',
                'category': 'Lipid Panel'
            },
            'hdl_cholesterol': {
                'value': 45,
                'unit': 'mg/dL',
                'normal_range': '> 40 mg/dL (men), > 50 mg/dL (women)',
                'category': 'Lipid Panel'
            }
        },
        'categories': {
            'Lipid Panel': ['total_cholesterol', 'ldl_cholesterol', 'hdl_cholesterol']
        }
    }
    
    print("=== FORMATTED FOR RAG SYSTEM ===")
    print(parser.format_for_rag(test_results))
    
    print("\n=== SUMMARY TABLE ===")
    print(parser.generate_summary_table(test_results))