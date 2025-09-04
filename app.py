import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

# -------------------------
# App Title and Welcome
# -------------------------
st.set_page_config(page_title="Most Powerful Trading App", layout="wide")

st.title("🚀 Welcome to the Most Powerful Trading App")
st.markdown("### This is a **Premium Tool** for Smart Traders 🔥")

# -------------------------
# Payment Section
# -------------------------
st.info("🔑 To access this app, you need a **Monthly Premium Subscription**")
st.write("💵 Subscription Fee: **2000 PKR / Month**")
st.write("📲 Send payment to EasyPaisa Account: **03198322695**")

# Payment Confirmation
payment_done = st.checkbox("✅ I have sent the payment (2000 PKR) to the above EasyPaisa number")

if not payment_done:
    st.warning("⚠️ Please complete payment to unlock the app features.")
    st.stop()

# -------------------------
# Main App (After Payment)
# -------------------------
st.success("✅ Payment confirmed! You now have full access to the trading tool.")

# -------------------------
# Live Market Data
# -------------------------
st.subheader("📊 Live Market Heatmap (Sample Data)")

url = "https://api.binance.com/api/v3/ticker/24hr"
response = requests.get(url).json()
df = pd.DataFrame(response)

# Select important columns
df = df[["symbol", "lastPrice", "priceChangePercent", "volume"]]

# Convert numeric columns
df["lastPrice"] = pd.to_numeric(df["lastPrice"], errors="coerce")
df["priceChangePercent"] = pd.to_numeric(df["priceChangePercent"], errors="coerce")
df["volume"] = pd.to_numeric(df["volume"], errors="coerce")

# Show top 20 coins
st.dataframe(df.head(20))

# -------------------------
# Whale Activity Detector
# -------------------------
st.subheader("🐋 Whale Activity Detector (Top 10 by Volume)")
top_volume = df.sort_values(by="volume", ascending=False).head(10)
st.table(top_volume)

# -------------------------
# Best Gainers & Losers
# -------------------------
st.subheader("📈 Top 5 Gainers")
gainers = df.sort_values(by="priceChangePercent", ascending=False).head(5)
st.table(gainers)

# Bar chart for gainers
fig, ax = plt.subplots()
ax.bar(gainers["symbol"], gainers["priceChangePercent"], color="green")
ax.set_title("Top 5 Gainers (%)")
ax.set_ylabel("Price Change %")
st.pyplot(fig)

st.subheader("📉 Top 5 Losers")
losers = df.sort_values(by="priceChangePercent", ascending=True).head(5)
st.table(losers)

# Bar chart for losers
fig, ax = plt.subplots()
ax.bar(losers["symbol"], losers["priceChangePercent"], color="red")
ax.set_title("Top 5 Losers (%)")
ax.set_ylabel("Price Change %")
st.pyplot(fig)

# -------------------------
# Search Bar
# -------------------------
st.subheader("🔍 Search Any Coin")
coin = st.text_input("Enter coin symbol (e.g. BTCUSDT):")

if coin:
    result = df[df["symbol"] == coin.upper()]
    if not result.empty:
        st.write(result)

        # Chart for searched coin
        price = float(result["lastPrice"].values[0])
        change = float(result["priceChangePercent"].values[0])

        fig, ax = plt.subplots()
        ax.bar([coin.upper()], [change], color="blue")
        ax.set_title(f"{coin.upper()} Price Change %")
        st.pyplot(fig)

    else:
        st.error("❌ Coin not found! Please check symbol again.")
