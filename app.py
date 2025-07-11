
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Deposit Pricing Demo", layout="wide")

st.title("Simon-Kucher | Deposit Pricing Demo Tool")
st.markdown("This is a demo application for showcasing portfolio insights, competitor pricing, elasticity curves, and optimization simulation.")

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
    st.dataframe(latest_balances)

    st.metric(label="Total Balance", value=f"${latest_balances['Balance'].sum():,.0f}")
    st.metric(label="Number of Products", value=f"{latest_balances['Product'].nunique()}")

elif choice == "Portfolio Analysis":
    st.header("Balance Trends by Product")
    pivot = balances.pivot(index="Date", columns="Product", values="Balance")
    pivot.index = pd.to_datetime(pivot.index)
    st.line_chart(pivot)

elif choice == "Competitor Rates":
    st.header("Bank vs Competitor Rates")
    st.dataframe(competitors)

elif choice == "Elasticity":
    st.header("Elasticity Curves (Simulated)")
    st.dataframe(elasticity)

elif choice == "Optimization":
    st.header("Optimized Rate Scenarios")
    st.dataframe(optimization)

    st.bar_chart(optimization.set_index("Product")[["Current Rate", "Optimized Rate"]])

elif choice == "Constraints":
    st.header("Pricing Constraints")
    st.dataframe(constraints)
