import streamlit as st
import requests
import os

st.set_page_config(page_title="FAQ Spotify", page_icon="🎧")
st.title("Assistente de Planos Spotify")
st.markdown("Tire suas dúvidas sobre os planos Premium.")

st.markdown(
    """
    <style>
    /* Oculta o menu superior padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    
    /* Oculta o rodapé 'Made with Streamlit' */
    footer {visibility: hidden;}
    
    /* Oculta o botão 'Deploy' no canto superior direito */
    .stAppDeployButton {display: none;}
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.title("⚙️ Painel de Controle")
    st.markdown("Bem-vindo ao assistente inteligente de planos.")
    st.markdown("---")
    
    if st.button("Limpar Histórico"):
        st.session_state.mensagens = [] 
        st.rerun()

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

for msg in st.session_state.mensagens:
    icone = "👤" if msg["role"] == "user" else "🎧"
    with st.chat_message(msg["role"], avatar=icone):
        st.markdown(msg["content"])

pergunta = st.chat_input("Digite sua dúvida aqui...")

if pergunta:
    with st.chat_message("user", avatar="👤"):
        st.markdown(pergunta)
    st.session_state.mensagens.append({"role": "user", "content": pergunta})

    with st.chat_message("assistant", avatar="🎧"):
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
            placeholder.markdown("Erro de conexão. Verifique se o servidor FastAPI (backend) está rodando.")