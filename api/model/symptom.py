from sqlalchemy import Column, String, Integer, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from typing import Literal, Union

from model import Base, Detail

# Definindo os enums para os níveis de gravidade e tipo de sintoma

class SeverityLevel(PyEnum):
    """
    Níveis de gravidade dos sintomas: leve, moderada ou severa
    """
    LEVE = "leve"
    MODERADA = "moderada"
    SEVERA = "severa"

class SymptomType(PyEnum):
    """
   Tipos de sintomas: agudo, crônico ou recorrente
    """
    AGUDO = "agudo"
    CRONICO = "crônico"
    RECORRENTE = "recorrente"

# Definição da classe Symptom, que representa um sintoma no banco de dados
class Symptom(Base):
    __tablename__ = 'symptom'  # Define o nome da tabela no banco de dados como 'symptom'

    # Definindo as colunas da tabela
    id = Column("pk_symptom", Integer, primary_key=True)  # Chave primária
    name = Column(String(140))  # Nome do sintoma, limitado a 140 caracteres
    severity = Column(Enum(SeverityLevel))  # Nível de gravidade do sintoma
    symptom_type = Column(Enum(SymptomType))  # Tipo de sintoma (agudo, crônico, recorrente)
    created_at = Column(DateTime, default=datetime.now())  # Data de criação do registro
    updated_at = Column(DateTime, onupdate=datetime.now)  # Data de última atualização do registro

    # Relacionamento com a tabela Detail (um sintoma pode ter vários detalhes associados)
    details = relationship("Detail")

    def __init__(self, name: str, severity: SeverityLevel, symptom_type: SymptomType, created_at: Union[DateTime, None] = None):
        """
        Construtor da classe Symptom. Inicializa um novo sintoma.
        
        :param name: Nome do sintoma
        :param created_at: (Opcional) Data de criação do sintoma. Se não fornecida, 
                           a data/hora atual será utilizada.
        """
        self.name = name  # Define o nome do sintoma
        self.severity = severity
        self.symptom_type = symptom_type

        # Se uma data de criação for fornecida, utiliza essa data, caso contrário, usa a atual
        if created_at:
            self.created_at = created_at

    def add_detail(self, detail: Detail):
        """
        Método para adicionar um detalhe ao sintoma.
        
        :param detail: Objeto Detail que descreve mais informações sobre o sintoma.
        """
        self.details.append(detail)  # Adiciona o detalhe à lista de detalhes relacionados ao sintoma
