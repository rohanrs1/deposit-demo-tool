
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# Load logo and display at the top
logo = Image.open("data/simon-kucher-logo.png")
st.image(logo, width=200)

st.title("Simon-Kucher | Deposit Pricing Tool")
st.subheader("Client Demo • July 2025")
st.markdown("---")

# Sidebar navigation
menu = ["Dashboard", "Portfolio Analysis", "Competitor Rates", "Elasticity", "Optimization", "Constraints"]
choice = st.sidebar.selectbox("Select Module", menu)

# Load data
@st.cache_data
def load_data():
    balances = pd.read_csv("data/balances.csv")
    competitors = pd.read_csv("data/competitor_rates.csv")
    elasticity = pd.read_csv("data/elasticity_curves.csv")
    optimization = pd.read_csv("data/optimization_scenarios.csv")
    constraints = pd.read_csv("data/constraints.csv")
    return balances, competitors, elasticity, optimization, constraints

balances, competitors, elasticity, optimization, constraints = load_data()

if choice == "Dashboard":
    st.header("Portfolio Summary")
    latest_balances = balances.groupby("Product").last().reset_index()
    col1, col2 = st.columns(2)
    col1.metric("Total Balance", f"${latest_balances['Balance'].sum():,.0f}")
    col2.metric("Number of Products", f"{latest_balances['Product'].nunique()}")

    st.dataframe(latest_balances)

elif choice == "Portfolio Analysis":
    st.header("Balance Trends by Product")
    pivot = balances.pivot(index="Date", columns="Product", values="Balance")
    pivot.index = pd.to_datetime(pivot.index)

    fig = px.line(pivot, x=pivot.index, y=pivot.columns,
                  labels={"value": "Balance", "Date": "Date"},
                  title="Portfolio Balance Over Time")
    st.plotly_chart(fig, use_container_width=True)

elif choice == "Competitor Rates":
    st.header("Bank vs Competitor Rates")
    st.dataframe(competitors)

    fig = px.bar(competitors, x="Bank", y="Rate (%)", color="Product",
                 title="Competitor Rates by Product", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

elif choice == "Elasticity":
    st.header("Elasticity Curves (Simulated)")
    st.dataframe(elasticity)

elif choice == "Optimization":
    st.header("Optimized Rate Scenarios")
    st.dataframe(optimization)

    fig = px.bar(optimization, x="Product", y=["Current Rate", "Optimized Rate"],
                 title="Rate Comparison", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

elif choice == "Constraints":
    st.header("Pricing Constraints")
    st.dataframe(constraints)
