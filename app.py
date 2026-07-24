
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------
# Page Config
# -----------------------
st.set_page_config(
    page_title="MediPulse Analytics",
    page_icon="🏥",
    layout="wide"
)

# -----------------------
# Load Data
# -----------------------
df = pd.read_csv("medical_billing.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.to_period("M").astype(str)

# -----------------------
# Sidebar
# -----------------------
st.sidebar.title("🏥 MediPulse")

providers = ["All"] + sorted(df["Provider"].unique().tolist())
insurances = ["All"] + sorted(df["Insurance"].unique().tolist())

selected_provider = st.sidebar.selectbox("Provider", providers)
selected_insurance = st.sidebar.selectbox("Insurance", insurances)

filtered = df.copy()

if selected_provider != "All":
    filtered = filtered[filtered["Provider"] == selected_provider]

if selected_insurance != "All":
    filtered = filtered[filtered["Insurance"] == selected_insurance]

# -----------------------
# KPIs
# -----------------------
revenue = filtered["Paid"].sum()
charges = filtered["Charge"].sum()
claims = len(filtered)
collection = (revenue / charges * 100) if charges else 0
denial = (len(filtered[filtered["Status"] == "Denied"]) / claims * 100) if claims else 0
avg_ar = filtered["Days AR"].mean()

st.title("🏥 MediPulse Medical Billing Dashboard")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Revenue", f"${revenue:,.0f}")
c2.metric("Charges", f"${charges:,.0f}")
c3.metric("Collection %", f"{collection:.1f}%")
c4.metric("Denial %", f"{denial:.1f}%")
c5.metric("Avg AR", f"{avg_ar:.1f} Days")

st.divider()

# -----------------------
# Revenue Trend
# -----------------------
left, right = st.columns(2)

with left:
    monthly = filtered.groupby("Month")["Paid"].sum().reset_index()

    fig = px.line(
        monthly,
        x="Month",
        y="Paid",
        markers=True,
        title="Monthly Revenue"
    )

    fig.update_layout(height=420)

    st.plotly_chart(fig, use_container_width=True)

with right:

    fig = px.pie(
        filtered,
        names="Status",
        hole=0.65,
        title="Claim Status"
    )

    fig.update_layout(height=420)

    st.plotly_chart(fig, use_container_width=True)

# -----------------------
# Provider / Insurance
# -----------------------
left, right = st.columns(2)

with left:

    provider = (
        filtered
        .groupby("Provider")["Paid"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        provider,
        x="Provider",
        y="Paid",
        title="Revenue by Provider",
        text_auto=True
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    insurance = (
        filtered
        .groupby("Insurance")["Paid"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        insurance,
        x="Insurance",
        y="Paid",
        title="Revenue by Insurance",
        text_auto=True
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------
# Denials
# -----------------------
st.subheader("Top Denial Reasons")

denials = filtered[filtered["Status"] == "Denied"]

if len(denials):

    fig = px.histogram(
        denials,
        x="Denial Reason",
        title="Denial Analysis",
        text_auto=True
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.success("No denied claims for the selected filters.")

# -----------------------
# Executive Summary
# -----------------------
st.subheader("Executive Summary")

best_provider = (
    filtered.groupby("Provider")["Paid"]
    .sum()
    .idxmax()
)

best_insurance = (
    filtered.groupby("Insurance")["Paid"]
    .sum()
    .idxmax()
)

st.info(f"""
### 📈 Performance Overview

• Revenue Collected: **${revenue:,.0f}**

• Collection Rate: **{collection:.1f}%**

• Denial Rate: **{denial:.1f}%**

• Average AR: **{avg_ar:.1f} Days**

• Highest Revenue Provider: **{best_provider}**

• Highest Paying Insurance: **{best_insurance}**

### Recommendation

Focus on reducing denied claims and improving collections from slower-paying insurers.
""")
