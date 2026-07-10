from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.backend.rag_engine import processar_pergunta

# 1. Instância da Aplicação
app = FastAPI(title="API do Chatbot Spotify FAQ")

# 2. Validação de Dados (Schema)
# O Pydantic garante que a nossa API só aceite requisições no formato correto
class RequisicaoChat(BaseModel):
    pergunta: str

# 3. Definição do Endpoint (Rota)
@app.post("/chat")
def chat_endpoint(requisicao: RequisicaoChat):
    """
    Recebe a pergunta, repassa para o motor RAG e retorna a resposta gerada.
    """
    try:
        # Chama a função que abstrai toda a complexidade do LangChain
        resultado = processar_pergunta(requisicao.pergunta)
        
        # Retorna o dicionário contendo {"resposta": "...", "fontes": [...] }
        return resultado
        
    except Exception as erro:
        # Em caso de falha (ex: Ollama desligado), retorna um erro HTTP 500
        raise HTTPException(status_code=500, detail=str(erro))