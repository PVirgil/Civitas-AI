# civitas_ai_app.py

import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from groq import Groq
import logging

# Setup
logging.basicConfig(level=logging.INFO)
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# Unified AI call

def call_agent(prompt: str, model="llama-3.1-8b-instant") -> str:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are Civitas AI, a secure multi-agent system for private funds managing operations, LPs, legal, ESG, and financial analytics."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Agent logic

def lp_concierge_agent(question: str, fund_context: str) -> str:
    prompt = f"LP asks: {question}\nContext: {fund_context}\nRespond as a professional LP relations assistant."
    return call_agent(prompt)

def fund_accountant_agent(df: pd.DataFrame) -> str:
    prompt = f"Analyze this fund ledger: {df.head(3).to_dict()}\nGenerate capital account summary, IRR, NAV."
    return call_agent(prompt)

def legal_clerk_agent(request_type: str, context: str) -> str:
    prompt = f"Generate a {request_type} legal document for this context: {context}"
    return call_agent(prompt)

def esg_auditor_agent(context: str) -> str:
    prompt = f"Assess this fund's ESG policy and recommend scoring + gaps: {context}"
    return call_agent(prompt)

def performance_analyst_agent(df: pd.DataFrame) -> str:
    prompt = f"Review fund returns: {df.head(3).to_dict()}. Report MOIC, DPI, and risks."
    return call_agent(prompt)

# Streamlit App

def main():
    st.set_page_config("Civitas AI – Private Markets OS", page_icon="🏛", layout="wide")
    st.title("🏛 Civitas AI – Private Markets Intelligence System")
    st.markdown("A unified AI for fund operations, compliance, performance, and investor communications.")

    uploaded_file = st.file_uploader("Upload fund data CSV", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("Data uploaded successfully.")
    else:
        df = pd.DataFrame()

    tabs = st.tabs([
        "💬 LP Concierge",
        "📊 Fund Accounting",
        "📄 Legal Clerk",
        "🌱 ESG Auditor",
        "📈 Performance Analyst"
    ])

    with tabs[0]:
        st.subheader("💬 LP Concierge")
        fund_context = st.text_area("Context (fund summary, history)")
        q = st.text_input("LP question")
        if st.button("Answer LP"):
            if not q or not fund_context:
                st.error("Enter question and context.")
            else:
                response = lp_concierge_agent(q, fund_context)
                st.text_area("Response", response, height=300)

    with tabs[1]:
        st.subheader("📊 Fund Accounting")
        if st.button("Run Accounting"):
            if df.empty:
                st.error("Upload fund data.")
            else:
                output = fund_accountant_agent(df)
                st.text_area("Capital Accounting Summary", output, height=400)

    with tabs[2]:
        st.subheader("📄 Legal Clerk")
        doc_type = st.selectbox("Document Type", ["NDA", "LPA", "Board Resolution", "Fund Memo"])
        context = st.text_area("Context for document")
        if st.button("Generate Document"):
            if not context:
                st.error("Enter context.")
            else:
                doc = legal_clerk_agent(doc_type, context)
                st.text_area("Legal Draft", doc, height=400)

    with tabs[3]:
        st.subheader("🌱 ESG Auditor")
        context = st.text_area("Describe ESG practices or policy")
        if st.button("Audit ESG"):
            if not context:
                st.error("Enter ESG context.")
            else:
                output = esg_auditor_agent(context)
                st.text_area("ESG Audit Output", output, height=400)

    with tabs[4]:
        st.subheader("📈 Performance Analyst")
        if st.button("Analyze Performance"):
            if df.empty:
                st.error("Upload performance data.")
            else:
                result = performance_analyst_agent(df)
                st.text_area("Performance Report", result, height=400)

if __name__ == "__main__":
    main()
