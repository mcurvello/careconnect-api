from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from model.symptom import SeverityLevel, SymptomType, Symptom

from schemas import DetailSchema

class SymptomSchema(BaseModel):
  name: str
  severity: SeverityLevel
  symptom_type: SymptomType  
  occurred_at: Optional[datetime]

class SymptomSearchSchema(BaseModel):
  id: int

class ListSymptomsSchema(BaseModel):
  symptoms: List[SymptomSchema]

def show_symptoms(symptoms: List[Symptom]):
  result = []

  for symptom in symptoms:
    result.append({
      "name": symptom.name,
      "severity": symptom.severity.value,
      "type": symptom.symptom_type.value,
      "date": symptom.created_at.strftime("%d/%m/%Y"),
      "time": symptom.created_at.strftime("%H:%M"),
    })

  return {"symptoms": result}

class SymptomViewSchema(BaseModel):
  id: int
  name: str
  severity: SeverityLevel
  symptom_type: SymptomType
  total_details: int
  details: List[DetailSchema]

class SymptomDelSchema(BaseModel):
  message: str
  name: str

def show_symptom(symptom: Symptom):
  return {
    "id": symptom.id,
    "name": symptom.name,
    "severity": symptom.severity.value,
    "type": symptom.symptom_type.value,
    "total_details": len(symptom.details),
    "details": [{"text": c.text} for c in symptom.details]
  }

class SymptomPatchSchema(BaseModel):
    id: int 
    name: Optional[str] = None
    severity: Optional[SeverityLevel] = None
    symptom_type: Optional[SymptomType] = None

class SymptomPutSchema(BaseModel):
    id: int 
    name: str
    severity: SeverityLevel
    symptom_type: SymptomType


