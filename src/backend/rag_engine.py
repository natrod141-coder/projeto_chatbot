from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. Conexão com o Banco de Dados Vetorial
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# 2. Configuração do Modelo Local
llm = ChatOllama(model="llama3")

# 3. Prompt Restrito
system_prompt = (
    "Você é um assistente de suporte especializado nos planos do Spotify. "
    "Responda à pergunta do usuário utilizando APENAS o contexto fornecido abaixo. "
    "Se a resposta não estiver no contexto, diga: 'Desculpe, não tenho essa informação'. "
    "Não invente informações em hipótese alguma.\n\n"
    "Contexto:\n{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

# Função auxiliar para extrair apenas o texto dos blocos encontrados
def formatar_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# 4. Cadeia Moderna RAG (LCEL)
# O símbolo "|" atua como um "cano" (pipe), passando a informação de uma etapa para a outra
rag_chain = (
    {"context": retriever | formatar_docs, "input": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser() # Garante que a saída seja um texto limpo
)

def processar_pergunta(pergunta: str) -> dict:
    """
    Executa a busca para extrair fontes e gera a resposta contextualizada.
    """
    # Passo A: Buscamos os documentos brutos para extrair de onde a informação veio
    documentos_recuperados = retriever.invoke(pergunta)
    fontes = list(set([doc.metadata.get("source", "Fonte desconhecida") for doc in documentos_recuperados]))
    
    # Passo B: Geramos a resposta passando a pergunta pelo "cano" (chain)
    texto_resposta = rag_chain.invoke(pergunta)
    
    return {
        "resposta": texto_resposta,
        "fontes": fontes
    }