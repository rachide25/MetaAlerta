import streamlit as st 
import base64 
from datetime import datetime 
from twilio.rest import Client

=== FUNÇÃO PARA DEFINIR FUNDO COM IMAGEM PERSONALIZADA ===

def set_background(png_file): with open(png_file, "rb") as f: data = f.read() encoded = base64.b64encode(data).decode() page_bg = f""" <style> .stApp {{ background-image: url("data:image/png;base64,{encoded}"); background-size: cover; background-position: center; background-repeat: no-repeat; }} </style> """ st.markdown(page_bg, unsafe_allow_html=True)

set_background("fundo_login.png")  # Sua imagem de fundo

=== ESTILO COM CORES PERSONALIZADAS ===

st.markdown(""" <style> .stTextInput > div > div > input { background-color: #1f2937; color: white; border: 1px solid #10b981; }

.stButton button {
    background-color: #10b981;
    color: white;
    font-weight: bold;
    border-radius: 10px;
}

.stAlert {
    background-color: #4b5563;
    color: white;
}
</style>

""", unsafe_allow_html=True)

=== LOGIN SIMPLES ===

st.title("🔐 Login - MetaAlerta") user = st.text_input("Usuário") pw = st.text_input("Senha", type="password")

if user != "admin" or pw != "senha123": st.warning("Faça login para continuar.") st.stop()

st.success("Login bem-sucedido!")

=== SELEÇÃO DE MOEDAS ===

st.header("💱 Seleção de Moedas") st.markdown("Escolha os pares que deseja monitorar:")

pares_disponiveis = { "EUR/USD": "🇪🇺 / 🇺🇸", "GBP/JPY": "🇬🇧 / 🇯🇵", "USD/JPY": "🇺🇸 / 🇯🇵", "AUD/USD": "🇦🇺 / 🇺🇸", "USD/CHF": "🇺🇸 / 🇨🇭", "EUR/JPY": "🇪🇺 / 🇯🇵", "USD/CAD": "🇺🇸 / 🇨🇦", "NZD/USD": "🇳🇿 / 🇺🇸", "EUR/GBP": "🇪🇺 / 🇬🇧", "GBP/USD": "🇬🇧 / 🇺🇸" }

selecionados = st.multiselect( "Selecione até 5 pares de moedas:", options=list(pares_disponiveis.keys()), default=["EUR/USD", "GBP/JPY"] )

tempo = st.radio("⏱️ Tipo de vela:", ["1 minuto", "5 minutos"]) duracao = st.slider("📅 Duração da análise (em minutos):", 10, 180, 60)

st.markdown("---")

if st.button("✅ Iniciar Análise"): if len(selecionados) == 0: st.error("Por favor, selecione pelo menos um par.") else: st.success(f"Iniciando análise para: {', '.join(selecionados)}")

# === ALERTA GERADO ===
    sinal = "🟢 COMPRA"
    par = selecionados[0]
    hora_entrada = datetime.now().strftime('%H:%M:%S')

    st.header("🚨 Alerta de Entrada Detectado")
    if sinal == "🟢 COMPRA":
        st.markdown(f"<h2 style='color:limegreen;'>{sinal}</h2>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h2 style='color:red;'>{sinal}</h2>", unsafe_allow_html=True)

    st.write(f"**Par de moedas:** {par}")
    st.write(f"**Hora de entrada:** {hora_entrada}")
    st.write(f"**Tempo de vela:** {tempo}")

    # === ENVIO WHATSAPP ===
    st.markdown("---")
    st.subheader("📩 Enviar este alerta via WhatsApp?")

    enviar_wh = st.checkbox("Ativar envio WhatsApp")
    num_destino = st.text_input("Número destino (+25885xxxxxxx)")
    sid = st.secrets.get("ACxxxxxxxxxxxxxxxxxxxxxxxxxxxx", "")
    token = st.secrets.get("xxxxxxxxxxxxxxxxxxxxxxxxxxxx", "")
    twilio_number = st.secrets.get("TWILIO_PHONE", "whatsapp:+14155238886")

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
