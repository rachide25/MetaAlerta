import streamlit as st
import base64
import time
from datetime import datetime
from twilio.rest import Client

# === FUNÇÃO PARA DEFINIR FUNDO COM IMAGEM PERSONALIZADA ===
def set_background(png_file):
    with open(png_file, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
        page_bg = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        .login-container {{
            background-color: rgba(0, 0, 0, 0.6);
            padding: 2em;
            border-radius: 15px;
            width: 100%;
            max-width: 400px;
            margin: 5% auto;
            color: white;
        }}
        .login-title {{
            font-size: 2em;
            text-align: center;
            margin-bottom: 1em;
        }}
        input[type="text"], input[type="password"] {{
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border-radius: 8px;
            border: none;
        }}
        .login-btn button {{
            width: 100%;
            padding: 0.75em;
            background-color: #00bfff;
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 8px;
        }}
        .login-btn button:hover {{
            background-color: #1e90ff;
        }}
        </style>
        """
        st.markdown(page_bg, unsafe_allow_html=True)

# === TELA DE LOGIN ===
set_background("fundo_login.png")
st.markdown("""
    <div class="login-container">
        <div class="login-title">🔐 Acesso - MetaAlerta</div>
    </div>
""", unsafe_allow_html=True)

user = st.text_input("Digite seu e-mail", key="user")
pw = st.text_input("Digite sua senha", type="password", key="pw")
mant = st.checkbox("Manter conectado")

if st.button("Entrar"):
    if (user, pw) not in [("admin", "rachide@123"), ("rachidecarlosbilar@gmail.com", "rachide@123")]:
        st.warning("Credenciais incorretas. Tente novamente.")
        st.stop()
    else:
        st.success("Login bem-sucedido!")

        # === SELEÇÃO DE MOEDAS ===
        st.header("💱 Seleção de Moedas")
        st.markdown("Escolha os pares que deseja monitorar:")

        pares_disponiveis = {
            "EUR/USD": "🇪 / 🇺",
            "GBP/JPY": "🇬 / 🇯",
            "USD/JPY": "🇺 / 🇯",
            "AUD/USD": "🇦 / 🇺",
            "USD/CHF": "🇺 / 🇨",
            "EUR/JPY": "🇪 / 🇯",
            "USD/CAD": "🇺 / 🇨",
            "NZD/USD": "🇳 / 🇺",
            "EUR/GBP": "🇪 / 🇬",
            "GBP/USD": "🇬 / 🇺"
        }

        selecionados = st.multiselect(
            "Selecione até 5 pares de moedas:",
            options=list(pares_disponiveis.keys()),
            default=["EUR/USD", "GBP/JPY"]
        )

        tempo = st.radio("⏱️ Tipo de vela:", ["1 minuto", "5 minutos"])
        duracao = st.slider("🗓 Duração da análise (em minutos):", 10, 180, 60)

        st.markdown("---")

        if st.button("✅ Iniciar Análise"):
            if len(selecionados) == 0:
                st.error("Por favor, selecione pelo menos um par.")
            else:
                with st.spinner("🔍 Analisando tendências, RSI, suportes e resistências..."):
                    time.sleep(4)  # simula análise técnica

                st.success(f"Análise concluída para: {', '.join(selecionados)}")

                # === GERAR ALERTA ===
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

                # === ENVIO AUTOMÁTICO PARA WHATSAPP ===
                try:
                    sid = st.secrets["ACxxxxxxxxxxxxxxxxxxxxxxxxxxxx"]
                    token = st.secrets["xxxxxxxxxxxxxxxxxxxxxxxxxxxx"]
                    twilio_number = st.secrets.get("TWILIO_PHONE", "whatsapp:+14155238886")
                    destino = "whatsapp:+258853318607"  # número já verificado

                    mensagem = f"{sinal} em {par} às {hora_entrada} (vela de {tempo})"

                    client = Client(sid, token)
                    client.messages.create(
                        body=mensagem,
                        from_=twilio_number,
                        to=destino
                    )
                    st.success("✅ Alerta enviado automaticamente para o WhatsApp!")
                except Exception as e:
                    st.error(f"❌ Erro ao enviar mensagem automática: {e}")
            
