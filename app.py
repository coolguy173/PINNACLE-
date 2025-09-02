# app.py
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Pinnacle - Investment Advisor", layout="wide")
st.title("🏔️ Pinnacle - Smart Investment Advisor")

# --- User Inputs ---
salary = st.number_input("Enter your monthly salary (₹):", min_value=0)
invest_percent = st.slider("Percentage of salary to invest:", 0, 100, 10)
risk = st.radio("Choose your risk appetite:", ["Low", "Medium", "High"])
horizon = st.selectbox("Investment horizon (years):", [1,3,5,10])

investment_amount = salary * (invest_percent / 100)

# --- Portfolio Allocation with clickable links ---
def allocate_with_links(risk_level, amount):
    links = {
        "Bonds": "https://www.investopedia.com/terms/b/bond.asp",
        "Index Funds": "https://www.investopedia.com/terms/i/indexfund.asp",
        "Gold": "https://www.investopedia.com/articles/basics/06/investgold.asp",
        "Stocks": "https://www.investopedia.com/terms/s/stock.asp",
        "Crypto": "https://www.investopedia.com/terms/c/cryptocurrency.asp"
    }
    
    if risk_level == "Low":
        portfolio = {"Bonds": amount*0.7, "Index Funds": amount*0.2, "Gold": amount*0.1}
    elif risk_level == "Medium":
        portfolio = {"Index Funds": amount*0.5, "Bonds": amount*0.3, "Stocks": amount*0.2}
    else:
        portfolio = {"Stocks": amount*0.7, "Index Funds": amount*0.2, "Crypto": amount*0.1}
    
    portfolio_links = {k: (v, links[k]) for k,v in portfolio.items()}
    return portfolio_links

portfolio = allocate_with_links(risk, investment_amount)

# --- Display Allocation with clickable links ---
st.subheader("📊 Portfolio Allocation")
for asset, (amt, url) in portfolio.items():
    st.markdown(f"- **{asset}**: ₹{amt:.2f} [Learn More]({url})")

# --- Pie Chart ---
fig1 = go.Figure(data=[go.Pie(labels=list(portfolio.keys()), 
                              values=[amt for amt, _ in portfolio.values()], hole=0.3)])
fig1.update_layout(title="Investment Allocation")
st.plotly_chart(fig1, use_container_width=True)

# --- Projected Returns ---
st.subheader("💰 Projected Returns")
expected_returns = {"Low": 0.05, "Medium": 0.08, "High": 0.12}

future_values = []
for year in range(1, horizon+1):
    fv = investment_amount * ((1 + expected_returns[risk]) ** year)
    future_values.append(fv)

st.line_chart(data=future_values, width=0, height=300, use_container_width=True)
st.write(f"If you invest ₹{investment_amount:.2f} today, it could grow to ₹{future_values[-1]:.2f} in {horizon} years.")

# --- Year-wise Table ---
st.subheader("📋 Year-wise Projection")
st.table({f"Year {i+1}": f"₹{future_values[i]:.2f}" for i in range(horizon)})

# --- Emergency Fund ---
st.subheader("🛡️ Emergency Fund Check")
emergency_fund = salary * 3
if investment_amount > emergency_fund:
    st.warning(f"You're investing more than 3 months of your salary. Make sure you have an emergency fund!")
else:
    st.success("Good! Your investment amount is safe compared to your emergency fund.")

# --- Footer ---
st.markdown("---")
st.markdown("Made by Jayawanth | Pinnacle Investment Advisor")
