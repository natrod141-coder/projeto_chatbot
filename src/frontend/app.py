import streamlit as st
import requests

# 1. Configuração da Página
st.set_page_config(page_title="FAQ Spotify", page_icon="🎧")
st.title("Assistente de Planos Spotify")
st.markdown("Tire suas dúvidas sobre os planos Premium.")

# 2. Gerenciamento de Estado (Memória da Interface)
# O Streamlit recarrega a página a cada clique. Usamos o session_state para não perder o histórico.
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# Renderiza o histórico de mensagens na tela
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 3. Captura da Entrada do Usuário
pergunta = st.chat_input("Digite sua dúvida aqui...")

if pergunta:
    # Exibe a pergunta do usuário na tela e salva no histórico
    with st.chat_message("user"):
        st.markdown(pergunta)
    st.session_state.mensagens.append({"role": "user", "content": pergunta})

    # 4. Comunicação com a API (Backend)
    with st.chat_message("assistant"):
        # Cria um espaço vazio para mostrar uma mensagem de carregamento
        placeholder = st.empty()
        placeholder.markdown("Consultando a base de dados...")
        
        try:
            # Envia um POST HTTP para a rota da nossa API FastAPI
            resposta_api = requests.post(
                "http://127.0.0.1:8000/chat",
                json={"pergunta": pergunta}
            )
            
            # Se a API retornar sucesso (200)
            if resposta_api.status_code == 200:
                dados = resposta_api.json()
                texto_resposta = dados.get("resposta", "Resposta não encontrada.")
                fontes = dados.get("fontes", [])
                
                # Formata a resposta final incluindo as fontes consultadas
                resposta_formatada = f"{texto_resposta}\n\n**Fontes:** {', '.join(fontes)}"
                
                # Atualiza o espaço vazio com a resposta real
                placeholder.markdown(resposta_formatada)
                
                # Salva a resposta do assistente no histórico
                st.session_state.mensagens.append({"role": "assistant", "content": resposta_formatada})
            else:
                placeholder.markdown("Desculpe, ocorreu um erro no processamento do servidor.")
                
        except requests.exceptions.ConnectionError:
            # Captura o erro caso a API FastAPI esteja desligada
            placeholder.markdown("Erro de conexão. Verifique se o servidor FastAPI (backend) está rodando.")