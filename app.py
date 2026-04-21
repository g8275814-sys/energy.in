import streamlit as st
import pandas as pd
import google.generativeai as genai

# Gemini API setup
genai.configure(api_key="AIzaSyBLenR9qjZma3GJgArzqJdVWRT7QcSlEaw")

model = genai.GenerativeModel("gemini-2.0-flash")

st.title("⚡ AI Energy Usage Dashboard")

# Load data
df = pd.read_csv("data.csv")

# Show data
st.subheader("Energy Data")
st.write(df)

# Graph
st.subheader("Energy Usage Graph")
st.line_chart(df.set_index("day"))

# -------- Anomaly Detection --------
st.subheader("⚠️ Anomaly Detection")

mean_usage = df["usage"].mean()
threshold = mean_usage * 1.3

df["anomaly"] = df["usage"] > threshold

for i in range(len(df)):
    if df["anomaly"][i]:
        st.error(f"High energy usage detected on Day {df['day'][i]} 🚨")

# -------- AI Analysis --------
st.subheader("🤖 AI Energy Analysis")

if st.button("Analyze Energy Usage"):

    data_text = df.to_string()

    prompt = f"""
    Analyze this household energy usage data.

    {data_text}

    Identify abnormal energy usage,
    explain possible reasons,
    and suggest ways to reduce electricity consumption.
    """

    response = model.generate_content(prompt)

    st.write(response.text)