from typing import Dict, List, Any, Optional
from langchain_core.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableSequence
from pydantic import BaseModel, Field
from . import heart_knowledge as hk


class SymptomAssessment(BaseModel):
    identified_symptoms: List[str] = Field(description="List of potential heart-related symptoms identified from user input")
    emergency_level: str = Field(description="Emergency level: 'high', 'medium', or 'low'")
    reasoning: str = Field(description="Reasoning behind the assessment")
    recommended_actions: List[str] = Field(description="List of recommended actions based on symptoms")


class HeartHealthAdvice(BaseModel):
    topic: str = Field(description="Main topic of the advice")
    key_points: List[str] = Field(description="Key points of advice")
    explanation: str = Field(description="Detailed explanation of the advice")
    references: Optional[List[str]] = Field(default=None, description="Optional references")


class SymptomAssessmentChain:
    def __init__(self, llm: BaseChatModel):
        self.llm = llm
        self.parser = PydanticOutputParser(pydantic_object=SymptomAssessment)
        template = """
You are a heart health assistant. Analyze the user's symptoms and provide an assessment.
User Input: {user_input}
{format_instructions}
Guidelines: Only identify mentioned symptoms; when in doubt recommend medical attention; for chest pain/shortness of breath recommend immediate care. Do not diagnose.
Response:
"""
        self.prompt = PromptTemplate(template=template, input_variables=["user_input"], partial_variables={"format_instructions": self.parser.get_format_instructions()})
        self.chain = self.prompt | self.llm | self.parser

    def run(self, user_input: str) -> Dict[str, Any]:
        try:
            parsed_result = self.chain.invoke({"user_input": user_input})
            emergency_symptoms = []
            for symptom_key, symptom_info in hk.HEART_SYMPTOMS.items():
                symptom_name = symptom_info["name"].lower()
                for identified in parsed_result.identified_symptoms:
                    if symptom_name in identified.lower() and symptom_info.get("emergency", False):
                        emergency_symptoms.append(symptom_info["name"])
            if emergency_symptoms and parsed_result.emergency_level != "high":
                parsed_result.emergency_level = "high"
                parsed_result.reasoning += f"\n\nEmergency level upgraded to HIGH due to: {', '.join(emergency_symptoms)}"
            return parsed_result.dict()
        except Exception as e:
            return {"identified_symptoms": ["Unable to parse symptoms"], "emergency_level": "medium", "reasoning": str(e), "recommended_actions": ["Consult a healthcare provider."]}


class HeartHealthAdviceChain:
    def __init__(self, llm: BaseChatModel):
        self.llm = llm
        self.parser = PydanticOutputParser(pydantic_object=HeartHealthAdvice)
        template = """
You are a heart health assistant. Provide evidence-based advice on heart health.
User Query: {user_query}
{format_instructions}
Guidelines: Specific actionable advice; heart health only; suggest consulting providers when appropriate.
Response:
"""
        self.prompt = PromptTemplate(template=template, input_variables=["user_query"], partial_variables={"format_instructions": self.parser.get_format_instructions()})
        self.chain = self.prompt | self.llm | self.parser

    def run(self, user_query: str) -> Dict[str, Any]:
        try:
            parsed_result = self.chain.invoke({"user_query": user_query})
            topic_lower = parsed_result.topic.lower()
            for key in ("diet", "exercise", "lifestyle"):
                if key in topic_lower and key in hk.HEART_HEALTH_ADVICE:
                    parsed_result.key_points.extend(hk.HEART_HEALTH_ADVICE[key]["recommendations"])
            return parsed_result.dict()
        except Exception as e:
            return {"topic": "General Heart Health", "key_points": ["Healthy diet", "Regular exercise", "Avoid smoking", "Manage stress", "Regular check-ups"], "explanation": str(e), "references": ["AHA Guidelines"]}
