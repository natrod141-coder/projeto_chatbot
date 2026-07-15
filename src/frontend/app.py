import streamlit as st
import requests
import os

st.set_page_config(page_title="FAQ Spotify", page_icon="🎧")
st.title("Assistente de Planos Spotify")
st.markdown("Tire suas dúvidas sobre os planos Premium.")


# o Streamlit recarrega a página a cada clique, usei o session_state para não perder o histórico.
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

pergunta = st.chat_input("Digite sua dúvida aqui...")

if pergunta:
    with st.chat_message("user"):
        st.markdown(pergunta)
    st.session_state.mensagens.append({"role": "user", "content": pergunta})

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("Consultando a base de dados...")
        
        try:
            url_da_api = os.environ.get("API_URL", "http://127.0.0.1:8000")
            
            resposta_api = requests.post(
                f"{url_da_api}/chat",
                json={"pergunta": pergunta}
            )
            
            # se retornar sucesso (200)
            if resposta_api.status_code == 200:
                dados = resposta_api.json()
                texto_resposta = dados.get("resposta", "Resposta não encontrada.")
                fontes = dados.get("fontes", [])
                
                resposta_formatada = f"{texto_resposta}\n\n**Fontes:** {', '.join(fontes)}"
                
                placeholder.markdown(resposta_formatada)
                
                st.session_state.mensagens.append({"role": "assistant", "content": resposta_formatada})
            else:
                placeholder.markdown("Desculpe, ocorreu um erro no processamento do servidor.")
                
        except requests.exceptions.ConnectionError:
            # captura o erro caso a API FastAPI esteja desligada
            placeholder.markdown("Erro de conexão. Verifique se o servidor FastAPI (backend) está rodando.")