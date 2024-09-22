from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

from model.base import Base
from model.detail import Detail
from model.symptom import Symptom

db_path = "database/"

# Verifica se o diretório do banco de dados existe, se não, cria
if not os.path.exists(db_path):
  os.makedirs(db_path)

# URL de conexão para o banco de dados SQLite
db_url = 'sqlite:///%s/db.sqlite3' % db_path

# Cria o mecanismo de conexão com o banco de dados
engine = create_engine(db_url, echo=False)

# Cria sessão para interagir com o banco de dados
Session = sessionmaker(bind=engine)

# Verifica se o banco de dados já existe, se não, cria um novo
if not database_exists(engine.url):
  create_database(engine.url)

# Cria todas as tabelas no banco de dados de acordo com os modelos definidos
Base.metadata.create_all(engine)