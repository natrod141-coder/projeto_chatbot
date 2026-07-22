from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.backend.rag_engine import processar_pergunta

# instancia da aplicação
app = FastAPI(title="API do Chatbot Spotify FAQ")

class RequisicaoChat(BaseModel):
    pergunta: str

# rota da api
@app.post("/chat")
def chat_endpoint(requisicao: RequisicaoChat):
    
    try:

        resultado = processar_pergunta(requisicao.pergunta)
        
        return resultado
        
    except Exception as erro:
        # em caso de falha, retorna um erro http 500
        raise HTTPException(status_code=500, detail=str(erro))