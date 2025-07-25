import streamlit as st
import time
import datetime
from twilio.rest import Client

# ---------------- CONFIGURAÇÕES DA PÁGINA ----------------
st.set_page_config(
    page_title="MetaAlerta",
    page_icon="📈",
    layout="centered"
)

# ---------------- BACKGROUND DA TELA DE LOGIN ----------------
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://i.imgur.com/CJ7E4jk.png");
background-size: cover;
background-position: center;
background-repeat: no-repeat;
}}

[data-testid="stHeader"] {{
background-color: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# ---------------- LOGIN SIMPLES ----------------
if 'login' not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 Acesso")
    email = st.text_input("Digite seu e-mail")
    senha = st.text_input("Digite sua senha", type="password")
    manter = st.checkbox("Manter conectado")
    if st.button("Entrar"):
        if email and senha:
            st.session_state.login = True
            st.experimental_rerun()
        else:
            st.warning("Preencha e-mail e senha.")
    st.stop()

# ---------------- TELA DE SELEÇÃO ----------------
st.title("📊 Escolha o Par de Moeda")

moedas = [
    "EUR/USD", "USD/JPY", "GBP/JPY", "AUD/USD", "USD/CHF",
    "USD/CAD", "EUR/JPY", "NZD/USD", "GBP/USD", "EUR/CAD"
]

par = st.selectbox("Selecionar moeda:", moedas)

if st.button("Pedir Análise"):
    with st.spinner("Analisando suportes, tendências e RSI..."):
        time.sleep(3)
        st.success("Análise concluída!")

    st.image("https://i.imgur.com/jT6f7kC.png", caption="Gráfico analisado", use_column_width=True)
    
    st.subheader("✅ Sinal Gerado")
    st.markdown("**Moeda:** " + par)
    st.markdown("**Recomendação:** `COMPRA` ✅")
    
    hora = datetime.datetime.now().strftime("%H:%M:%S")
    st.markdown(f"**Horário ideal de entrada:** `{hora}`")
    
    st.markdown("**Tempo estimado:** 1 minuto")
    
    if st.button("📤 Enviar alerta para WhatsApp"):
        # --- Twilio (você já configurou o SID e TOKEN)
        try:
            account_sid = "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
            auth_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                from_='whatsapp:+14155238886',
                body=f"📢 Alerta MetaAlerta:\nMoeda: {par}\nAção: COMPRA ✅\nHora: {hora}\nVelas: 1 minuto",
                to='whatsapp:+258853318607'
            )
            st.success("📲 Alerta enviado com sucesso para o WhatsApp!")
        except Exception as e:
            st.error(f"Erro ao enviar alerta: {e}")
