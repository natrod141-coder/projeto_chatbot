from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def configurar_banco_de_dados():
    print("1. Carregando documento de FAQ...")
    loader = TextLoader("data/faq_spotify.md", encoding="utf-8")
    documentos = loader.load()

    print("2. Dividindo o texto em pedaços menores (chunks)...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    textos_divididos = text_splitter.split_documents(documentos)

    print("3. Configurando o modelo de embeddings local...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

    print("4. Criando e salvando o banco de dados vetorial...")
    Chroma.from_documents(
        documents=textos_divididos,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    
    print("Processo concluído! Banco de dados populado com sucesso.")

if __name__ == "__main__":
    configurar_banco_de_dados()