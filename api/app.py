from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from flask_cors import CORS

from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Symptom, Detail
from schemas import *

info = Info(title="CareConnect API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
symptom_tag = Tag(name="Sintomas", description="Adição, visualização e remoção de sintomas à base")
detail_tag = Tag(name="Detalhes", description="Adição de um detalhamento à um sintoma cadastrado na base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/symptom', tags=[symptom_tag], responses={"200": SymptomViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_symptom(form: SymptomSchema):
    """Adiciona um novo sintoma à base de dados

    Retorna uma representação dos sintomas e respectivos detalhes.
    """
    symptom = Symptom(
        name=form.name,
        severity=form.severity,
        symptom_type=form.symptom_type
        )
    if form.occurred_at:
        symptom.created_at = form.occurred_at

    try:
        session = Session()
        session.add(symptom)
        session.commit()
        return show_symptom(symptom), 200

    except IntegrityError as e:
        error_msg = "Sintoma não foi salvo na base :/"
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        return {"mesage": error_msg}, 400
    
    finally:
        session.close() 

@app.get('/symptoms', tags=[symptom_tag], responses={"200": ListSymptomsSchema, "404": ErrorSchema})
def get_symptoms():
    """Faz a busca por todos os sintomas cadastrados

    Retorna uma representação da listagem de sintomas.
    """
    session = Session()
    symptoms = session.query(Symptom).order_by(Symptom.created_at).all()

    if not symptoms:
        return {"symptoms": []}, 200
    else:
        return show_symptoms(symptoms), 200
    
@app.get('/symptom', tags=[symptom_tag],
         responses={"200": SymptomViewSchema, "404": ErrorSchema})
def get_symptom(query: SymptomSearchSchema):
    """Faz a busca por um sintoma a partir do id do sintoma

    Retorna uma representação dos sintomas e respectivos detalhes.
    """
    symptom_id = query.id
    session = Session()
    symptom = session.query(Symptom).filter(Symptom.id == symptom_id).first()

    if not symptom:
        error_msg = "Sintoma não encontrado na base :/"
        return {"message": error_msg}, 404
    else:
        return show_symptom(symptom), 200
    
@app.delete('/symptom', tags=[symptom_tag], responses={"200": SymptomDelSchema, "404": ErrorSchema})
def del_symptom(query: SymptomSearchSchema):
    """Deleta um sintoma a partir do nome de sintoma informado

    Retorna uma mensagem de confirmação da remoção.
    """
    symptom_id = query.id
    session = Session()
    symptom = session.query(Symptom).filter(Symptom.id == symptom_id).first()
    count = session.query(Symptom).filter(Symptom.id == symptom_id).delete()
    session.commit()
    session.close()

    if count:
        return {"message": "Sintoma removido", "id": symptom.name}
    else: 
        error_msg = "Sintoma não encontrado na base :/"
        return {"message": error_msg}, 404
    
@app.post('/detail', tags=[detail_tag], responses={"200": SymptomSearchSchema, "404": ErrorSchema})
def add_detail(form: DetailSchema):
    """Adiciona de um novo detalhe à um sintoma cadastrado na base identificado pelo id

    Retorna uma representação dos sintomas e detalhes associados.
    """
    symptom_id = form.symptom_id
    session = Session()
    symptom = session.query(Symptom).filter(Symptom.id == symptom_id).first()

    if not symptom:
        error_msg = "Sintoma não encontrado na base :/"
        return {"message": error_msg}, 404
    
    text = form.text
    detail = Detail(text)

    symptom.add_detail(detail)
    session.commit()

    return show_symptom(symptom), 200

@app.put('/symptom', tags=[symptom_tag], responses={"200": SymptomViewSchema, "404": ErrorSchema})
def update_symptom(form: SymptomPutSchema):
    """Atualiza um sintoma existente na base de dados"""
    session = Session()
    symptom = session.query(Symptom).filter(Symptom.id == form.id).first()

    if not symptom:
        error_msg = "Sintoma não encontrado na base :/"
        return {"message": error_msg}, 404

    symptom.name = form.name
    symptom.severity = form.severity
    symptom.symptom_type = form.symptom_type

    session.commit()
    return show_symptom(symptom), 200

@app.patch('/symptom', tags=[symptom_tag], responses={"200": SymptomViewSchema, "404": ErrorSchema})
def partial_update_symptom(form: SymptomPatchSchema):
    """Atualiza parcialmente um sintoma existente na base de dados"""
    session = Session()
    symptom = session.query(Symptom).filter(Symptom.id == form.id).first()

    if not symptom:
        error_msg = "Sintoma não encontrado na base :/"
        return {"message": error_msg}, 404

    if form.name:
        symptom.name = form.name
    if form.severity:
        symptom.severity = form.severity
    if form.symptom_type:
        symptom.symptom_type = form.symptom_type

    session.commit()
    return show_symptom(symptom), 200
