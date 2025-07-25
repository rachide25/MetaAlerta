import streamlit as st
from datetime import datetime
from twilio.rest import Client

# === Sessão de Estado ===
if "logado" not in st.session_state:
    st.session_state.logado = False
if "alerta_gerado" not in st.session_state:
    st.session_state.alerta_gerado = False
if "sinal" not in st.session_state:
    st.session_state.sinal = ""
if "par" not in st.session_state:
    st.session_state.par = ""
if "hora_entrada" not in st.session_state:
    st.session_state.hora_entrada = ""
if "tempo" not in st.session_state:
    st.session_state.tempo = ""

# === Função para fundo com imagem personalizada ===
def set_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded = image_file.read().encode("base64").decode()
    css = f"""
    <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# === Aplicar o fundo ===
# set_background("imagem_fundo_sem_fundo.jpg")  # substitua pelo caminho da sua imagem

# === Título ===
st.title("🔐 MetaAlerta - Login")

# === Tela de Login ===
if not st.session_state.logado:
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if (email == "admin" and senha == "rachide@123") or (email == "rachidecarlosbilar908@gmail.com" and senha == "rachide@123"):
            st.session_state.logado = True
        else:
            st.warning("Credenciais incorretas. Tente novamente.")
    st.stop()

# === Segunda tela - Análise Técnica ===
st.success("Você está ligado na MetaAlerta 🔔")

moedas = ["EUR/USD", "USD/JPY", "GBP/USD", "BTC/USD"]
selecionados = st.multiselect("Selecione os pares de moedas:", moedas)

tempos = ["1 minuto", "5 minutos", "15 minutos"]
tempo = st.selectbox("Tempo de vela:", tempos)

if st.button("✅ Iniciar Análise"):
    if len(selecionados) == 0:
        st.error("Por favor, selecione pelo menos um par.")
    else:
        st.success(f"Iniciando análise para: {', '.join(selecionados)}")

        # Simulação do alerta
        sinal = "🟢 COMPRA"
        par = selecionados[0]
        hora_entrada = datetime.now().strftime('%H:%M:%S')

        # Salvar no estado
        st.session_state.alerta_gerado = True
        st.session_state.sinal = sinal
        st.session_state.par = par
        st.session_state.hora_entrada = hora_entrada
        st.session_state.tempo = tempo

# === Mostrar alerta se foi gerado ===
if st.session_state.alerta_gerado:
    st.header("🚨 Alerta de Entrada Detectado")
    sinal = st.session_state.sinal
    par = st.session_state.par
    hora_entrada = st.session_state.hora_entrada
    tempo = st.session_state.tempo

    if sinal == "🟢 COMPRA":
        st.markdown(f"<h2 style='color:limegreen;'>{sinal}</h2>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h2 style='color:red;'>{sinal}</h2>", unsafe_allow_html=True)

    st.write(f"**Par de moedas:** {par}")
    st.write(f"**Hora de entrada:** {hora_entrada}")
    st.write(f"**Tempo de vela:** {tempo}")

    # === Envio WhatsApp ===
    st.markdown("---")
    st.subheader("📩 Enviar este alerta via WhatsApp?")

    enviar_wh = st.checkbox("Ativar envio WhatsApp")
    num_destino = st.text_input("Número destino (+25885xxxxxxx)")
    sid = st.text_input("ACxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    token = st.text_input("xxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    twilio_number = "whatsapp:+14155238886"

    mensagem = f"{sinal} em {par} às {hora_entrada} (vela de {tempo})"

    if st.button("📤 Enviar alerta"):
        if enviar_wh and all([sid, token, num_destino]):
            try:
                client = Client(sid, token)
                client.messages.create(
                    body=mensagem,
                    from_=twilio_number,
                    to=num_destino
                )
                st.success("Mensagem enviada com sucesso! ✅")
            except Exception as e:
                st.error(f"Erro ao enviar mensagem: {e}")
        else:
            st.warning("Preencha todos os campos e ative o envio.")

# === Botão de sair ===
if st.button("Sair"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()
