import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Bitget SMC Paper Trader",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Bitget SMC Paper Trader")
st.caption("Smart Money Concepts — Paper Trading Simulator")

st.warning(
    "Mode simulasi saja. Tidak ada order sungguhan "
    "dan tidak memerlukan API key."
)

if "balance" not in st.session_state:
    st.session_state.balance = 10000.0

if "trades" not in st.session_state:
    st.session_state.trades = []

st.metric(
    "Saldo Simulasi",
    f"${st.session_state.balance:,.2f}"
)

st.subheader("Buat Trade Simulasi")

col1, col2 = st.columns(2)

with col1:
    symbol = st.selectbox(
        "Pasangan",
        ["BTC/USDT", "ETH/USDT", "SOL/USDT"]
    )

    direction = st.selectbox(
        "Arah",
        ["LONG", "SHORT"]
    )

with col2:
    entry = st.number_input(
        "Harga Entry",
        min_value=0.0,
        value=100.0
    )

    exit_price = st.number_input(
        "Harga Exit",
        min_value=0.0,
        value=101.0
    )

amount = st.number_input(
    "Ukuran Posisi (USDT)",
    min_value=1.0,
    max_value=10000.0,
    value=100.0
)

if st.button("Catat Trade Simulasi"):
    if entry <= 0 or exit_price <= 0:
        st.error("Harga harus lebih besar dari nol.")
    elif amount > st.session_state.balance:
        st.error("Saldo simulasi tidak mencukupi.")
    else:
        change = (exit_price - entry) / entry

        if direction == "SHORT":
            change = -change

        pnl = amount * change
        st.session_state.balance += pnl

        st.session_state.trades.append({
            "Pair": symbol,
            "Arah": direction,
            "Entry": entry,
            "Exit": exit_price,
            "Ukuran": amount,
            "P/L (USDT)": round(pnl, 2)
        })

        st.success(f"Trade simulasi dicatat. P/L: ${pnl:.2f}")

st.subheader("Riwayat Trade")

if st.session_state.trades:
    st.dataframe(
        pd.DataFrame(st.session_state.trades),
        use_container_width=True
    )
else:
    st.info("Belum ada trade simulasi.")
