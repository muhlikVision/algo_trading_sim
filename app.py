import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Trading Agent", page_icon="📈", layout="wide")
st.title("🤖 AI Algorithmic Trading Backtester")
st.markdown("Powered by **Live Yahoo Finance Data**, **Retrieval-Augmented Generation (RAG)**, and **NVIDIA Llama 3**.")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Simulation Parameters")
ticker = st.sidebar.text_input("Stock Ticker", value="AAPL").upper()
# --- REPLACED CSV INPUT WITH A DYNAMIC SLIDER ---
days_back = st.sidebar.slider("Days of History (Live Data)", min_value=7, max_value=90, value=30)

# The URL of your FastAPI Docker container
#API_URL = "http://127.0.0.1:8000/api/v1/simulate"
API_URL = "https://algo-trading-engine-xxxx.onrender.com/api/v1/simulate"

if st.sidebar.button("🚀 Run Live AI Backtest", type="primary"):
    with st.spinner(f"Agent is fetching live market data and analyzing {ticker}..."):
        try:
            # 1. Ping the FastAPI backend with the new payload
            payload = {"ticker": ticker, "days_back": days_back}
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                result_data = response.json()["data"]
                
                # --- METRICS DASHBOARD ---
                st.subheader("📊 Backtest Results")
                col1, col2, col3 = st.columns(3)
                col1.metric("Final Portfolio Value", f"${result_data.get('final_value', 100000):,.2f}")
                col2.metric("Total ROI", f"{result_data.get('roi', 0):.2f}%")
                col3.metric("Trades Executed", len([x for x in result_data.get('history', []) if x['action'] in ['BUY', 'SELL']]))

                # --- INTERACTIVE CHART ---
                history = result_data.get('history', [])
                if history:
                    df = pd.DataFrame(history)
                    
                    # Create the base price line
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=df['date'], y=df['price'], mode='lines', name=f'{ticker} Price', line=dict(color='blue')))
                    
                    # Overlay BUY signals (Green triangles)
                    buys = df[df['action'] == 'BUY']
                    if not buys.empty:
                        fig.add_trace(go.Scatter(x=buys['date'], y=buys['price'], mode='markers', name='BUY', 
                                                 marker=dict(symbol='triangle-up', color='green', size=15)))
                    
                    # Overlay SELL signals (Red triangles)
                    sells = df[df['action'] == 'SELL']
                    if not sells.empty:
                        fig.add_trace(go.Scatter(x=sells['date'], y=sells['price'], mode='markers', name='SELL', 
                                                 marker=dict(symbol='triangle-down', color='red', size=15)))

                    fig.update_layout(title="Agent Trading Behavior", xaxis_title="Date", yaxis_title="Price ($)", template="plotly_dark")
                    st.plotly_chart(fig, use_container_width=True)

                # --- LOGS & REASONING ---
                st.subheader("🧠 Agent Reasoning Logs")
                for day in history:
                    with st.expander(f"{day['date']} | Action: {day['action']} | Price: ${day['price']:.2f}"):
                        st.write(day.get('reasoning', 'No reasoning provided.'))

            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("🚨 Could not connect to the API. Is your Docker container running on port 8000?")