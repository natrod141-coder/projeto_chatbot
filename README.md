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