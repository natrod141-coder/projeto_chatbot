# FAQ Chatbot - Spotify Premium

Este é um chatbot construído com arquitetura RAG (Retrieval-Augmented Generation) para responder a dúvidas sobre os planos do Spotify de forma segura, utilizando modelos Open Source rodando 100% localmente, sem dependência de APIs pagas.

## Arquitetura e Stack Tecnológica
- **Backend:** Python + FastAPI
- **Frontend:** Streamlit
- **LLM Local:** Ollama (Modelo: Llama 3)
- **Banco Vetorial:** ChromaDB
- **Framework IA:** LangChain
- **Orquestração:** Docker & Docker Compose

## Como executar o projeto (Via Docker)

Certifique-se de ter o [Docker Desktop](https://www.docker.com/) instalado na sua máquina.

1. Clone este repositório.
2. Abra o terminal na raiz do projeto.
3. Execute o comando de orquestração:
   ```bash
   docker-compose up --build

### Como executar o projeto (Localmente sem Docker)

> **⚠️ IMPORTANTE - Configuração da IA:** Ao executar o projeto nativamente, o sistema não utiliza a ponte de rede do Docker. Antes de iniciar os servidores, abra o arquivo `rag_engine.py` e altere o parâmetro `base_url` do modelo de `http://host.docker.internal:11434` para o endereço local: `http://localhost:11434`.

Certifique-se de ter o Python e o Ollama instalados na sua máquina, além de ter feito o download do modelo Llama 3 localmente (`ollama run llama3`).

1. Clone este repositório.
2. Abra o terminal na raiz do projeto.
3. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
4. Instale as bibliotecas necessárias: 
   ```bash 
   pip install -r requirements.txt
5. Inicie o servidor do Backend (FastAPI):
   ```bash
   uvicorn src.backend.main:app --reload
6. Abra um novo terminal na raiz do projeto, ative o ambiente virtual novamente e inicie a interface do Frontend (Streamlit):
   ```bash
   streamlit run src/frontend/app.py


  
