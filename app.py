import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import ta
from PIL import Image

# --- Configuração da Página ---
st.set_page_config(page_title="MetaAlerta", layout="wide")

# --- Fundo da Tela de Login ---
def add_bg():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("fundo_login.png");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- Dados de usuários fictícios ---
usuarios = {
    "admin": "rachide@123",
    "rachidecarlosbilar@gmail.com": "rachide@123"
}

# --- Sessão de autenticação ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    add_bg()
    st.markdown("<h1 style='text-align: center; color: white;'>MetaAlerta</h1>", unsafe_allow_html=True)
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if email in usuarios and usuarios[email] == senha:
            st.session_state.autenticado = True
            st.experimental_rerun()
        else:
            st.error("Credenciais incorretas. Tente novamente.")
    st.stop()

# --- Tela principal após login ---
st.title("📈 MetaAlerta – Análise Técnica ao Vivo")

col1, col2 = st.columns(2)
with col1:
    moeda = st.selectbox("Selecione o par de moedas", ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "BTC-USD", "ETH-USD"])
with col2:
    tempo = st.selectbox("Tempo da vela", ["1m", "5m", "15m", "1h", "1d"])

if st.button("🔍 Analisar"):
    st.info("Buscando dados e analisando...")

    intervalo = {
        "1m": "1m",
        "5m": "5m",
        "15m": "15m",
        "1h": "60m",
        "1d": "1d"
    }[tempo]

    df = yf.download(tickers=moeda, period="2d", interval=intervalo)

    if df.empty:
        st.error("Erro ao obter dados. Tente novamente.")
        st.stop()

    df['RSI'] = ta.momentum.RSIIndicator(df['Close']).rsi()
    df['EMA20'] = ta.trend.EMAIndicator(df['Close'], window=20).ema_indicator()
    df['EMA50'] = ta.trend.EMAIndicator(df['Close'], window=50).ema_indicator()

    macd = ta.trend.MACD(df['Close'])
    df['MACD'] = macd.macd()
    df['MACD_signal'] = macd.macd_signal()

    suporte = df['Close'].rolling(window=20).min().iloc[-1]
    resistencia = df['Close'].rolling(window=20).max().iloc[-1]

    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close'],
        name='Candlestick'
    ))
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], line=dict(color='blue', width=1), name="EMA20"))
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA50'], line=dict(color='orange', width=1), name="EMA50"))
    fig.add_hline(y=suporte, line_dash="dot", line_color="green", annotation_text="Suporte", annotation_position="bottom left")
    fig.add_hline(y=resistencia, line_dash="dot", line_color="red", annotation_text="Resistência", annotation_position="top left")

    fig.update_layout(height=500, width=1000, xaxis_rangeslider_visible=False)

    st.plotly_chart(fig)

    st.subheader("📊 Indicadores Técnicos")
    col1, col2, col3 = st.columns(3)
    col1.metric("RSI", f"{df['RSI'].iloc[-1]:.2f}")
    col2.metric("MACD", f"{df['MACD'].iloc[-1]:.4f}")
    col3.metric("Sinal MACD", f"{df['MACD_signal'].iloc[-1]:.4f}")

    if df['RSI'].iloc[-1] < 30:
        st.success("Tendência: 🟢 COMPRA (RSI < 30)")
    elif df['RSI'].iloc[-1] > 70:
        st.error("Tendência: 🔴 VENDA (RSI > 70)")
    else:
        st.warning("Tendência: 🔄 Lateral (RSI entre 30 e 70)")

    st.caption(f"Suporte: {suporte:.4f} | Resistência: {resistencia:.4f}")

st.markdown("---")
if st.button("Sair"):
    st.session_state.autenticado = False
    st.experimental_rerun()
