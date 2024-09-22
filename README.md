# Symptom's API

## Descrição
Este projeto é uma API para gerenciamento de sintomas, permitindo adicionar, visualizar, atualizar e remover sintomas e seus detalhes. A API é construída com Flask e utiliza SQLAlchemy para interagir com o banco de dados.

## Instalação

### Pré-requisitos
Certifique-se de ter o Python 3.7 ou superior instalado em seu ambiente.

### Passos para Configuração

1. **Fazer Fork do Repositório**
   - Vá até [este repositório no GitHub](https://github.com/mcurvello/mvp1-backend.git) e faça um fork para sua conta.

2. **Clonar o Repositório**
   - Clone o repositório forkado para seu ambiente local:
     ```bash
     git clone https://github.com/SEU_USUARIO/mvp1-backend.git
     cd mvp1-backend/api
     ```

3. **Criar um Ambiente Virtual**
   - É recomendável criar um ambiente virtual para instalar as dependências:
     ```bash
     python -m venv venv
     source venv/bin/activate  # Para Linux/Mac
     venv\Scripts\activate  # Para Windows
     ```

4. **Instalar Dependências**
   - Instale as dependências necessárias:
     ```bash
     pip install -r requirements.txt
     ```

5. **Executar a API**
   - Para executar a API basta executar::
     ```bash
     flask run --host 0.0.0.0 --port 5001
     ```

## Uso
- A API está disponível em `http://localhost:5001`.
- Acesse a documentação da API em `http://localhost:5001/openapi`.

## Contribuição
Sinta-se à vontade para contribuir! Faça um fork deste repositório, faça suas alterações e envie um pull request.
