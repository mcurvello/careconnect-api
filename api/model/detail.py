from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from model import Base

class Detail(Base):
    __tablename__ = 'detail'  # Define o nome da tabela no banco de dados como 'detail'

    id = Column(Integer, primary_key=True)  # Chave primária para identificar unicamente cada detalhe
    text = Column(String(4000))  # Coluna para armazenar um texto de até 4000 caracteres
    created_at = Column(DateTime, default=datetime.now())  # Armazena a data/hora de criação do registro

    # Define a relação com a tabela 'symptom' através de uma chave estrangeira
    symptom = Column(Integer, ForeignKey("symptom.pk_symptom"), nullable=False)

    def __init__(self, text: str, created_at: Union[DateTime, None] = None):
        """
        Construtor da classe Detail. Inicializa um novo detalhe.
        
        :param text: O texto que descreve o detalhe.
        :param created_at: (Opcional) A data/hora em que o detalhe foi criado. Se não for fornecido, 
                           usa a data/hora atual.
        """
        self.text = text  # Define o texto do detalhe

        # Se uma data de criação for fornecida, usa essa data, caso contrário, usa a atual
        if created_at:
            self.created_at = created_at

