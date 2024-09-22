from pydantic import BaseModel

class DetailSchema(BaseModel):
  symptom_id: int  # ID do sintoma associado, obrigatório
  text: str  # Texto do detalhe, obrigatório