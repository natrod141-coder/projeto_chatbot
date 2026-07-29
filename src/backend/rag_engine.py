from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
vector_store = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 8})

llm = ChatOllama(model="llama3", temperature=0, base_url="http://host.docker.internal:11434")

# Prompt Restrito 
system_prompt = (
    "Você é um assistente de suporte do Spotify.\n"
    "Responda à pergunta de forma direta, utilizando APENAS as informações do Contexto abaixo.\n"
    "Se o contexto afirmar que algo é incompatível, exclusivo ou não permitido, informe isso ao usuário claramente.\n\n"
    "Contexto:\n{context}\n\n"
    "Se a informação exata não estiver no Contexto, responda apenas: 'Desculpe, não tenho essa informação.'"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

def formatar_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | formatar_docs, "input": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

def processar_pergunta(pergunta: str) -> dict:
    """
    Executa a busca para extrair fontes e gera a resposta contextualizada.
    """
    # Buscar os documentos brutos para extrair de onde a informação veio
    documentos_recuperados = retriever.invoke(pergunta)
    fontes = list(set([doc.metadata.get("source", "Fonte desconhecida") for doc in documentos_recuperados]))
    
    print("\n\n=== TEXTOS ENCONTRADOS PELO BANCO DE DADOS ===")
    for i, doc in enumerate(documentos_recuperados):
        print(f"\n[Bloco {i+1}]: {doc.page_content}")
    print("==============================================\n\n")

    #Gera a resposta passando a pergunta pelo chain
    texto_resposta = rag_chain.invoke(pergunta)
    
    return {
        "resposta": texto_resposta,
        "fontes": fontes
    }