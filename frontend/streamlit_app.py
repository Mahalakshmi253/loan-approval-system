"""Streamlit frontend for loan approval system."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import requests
import json
from datetime import datetime
from backend.models import LoanApplication, EmploymentType, DecisionType

st.set_page_config(
    page_title="Loan Approval System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_BASE_URL = "http://127.0.0.1:8000"

st.title("🏦 Loan Approval System")
st.markdown("### Multi-Agent AI for Automated Loan Application Analysis")

tab1, tab2, tab3, tab4 = st.tabs(
    ["📝 Apply", "📊 Status", "📈 Analytics", "ℹ️ About"]
)

with tab1:
    st.header("Loan Application Form")

    col1, col2 = st.columns(2)

    with col1:
        applicant_id = st.text_input(
            "Applicant ID",
            value="APP-" + datetime.now().strftime("%Y%m%d%H%M%S"),
        )
        age = st.number_input("Age", min_value=18, max_value=80, value=35)
        income = st.number_input("Annual Income ($)", min_value=1000, value=75000)
        employment_type = st.selectbox(
            "Employment Type",
            [e.value for e in EmploymentType],
        )

    with col2:
        credit_score = st.number_input(
            "Credit Score",
            min_value=300,
            max_value=850,
            value=700,
        )
        loan_amount = st.number_input("Loan Amount ($)", min_value=1000, value=250000)
        tenure_months = st.number_input(
            "Loan Tenure (months)",
            min_value=6,
            max_value=360,
            value=180,
        )
        existing_liabilities = st.number_input(
            "Existing Monthly Liabilities ($)",
            min_value=0,
            value=0,
        )

    location = st.text_input("Location", value="USA")

    st.markdown("---")

    if st.button("🚀 Submit Application", use_container_width=True):
        with st.spinner("Processing your application..."):
            try:
                application_data = {
                    "applicant_id": applicant_id,
                    "age": age,
                    "income": income,
                    "employment_type": employment_type,
                    "credit_score": credit_score,
                    "loan_amount": loan_amount,
                    "tenure_months": tenure_months,
                    "existing_liabilities": existing_liabilities,
                    "location": location,
                }

                response = requests.post(
                    f"{API_BASE_URL}/api/loan-application",
                    json=application_data,
                    timeout=30,
                )

                if response.status_code == 200:
                    decision = response.json()

                    st.success("✅ Application processed successfully!")

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        decision_val = decision["decision"]["classification"]
                        if decision_val == "approved":
                            st.metric("Decision", "✅ APPROVED", delta="Positive")
                        elif decision_val == "rejected":
                            st.metric("Decision", "❌ REJECTED", delta="Negative")
                        else:
                            st.metric("Decision", "⚠️ REVIEW", delta="Pending")

                    with col2:
                        st.metric(
                            "Risk Score",
                            f"{decision['financial_risk']['risk_score']:.1%}",
                        )

                    with col3:
                        st.metric(
                            "Confidence",
                            f"{decision['decision']['confidence_level']:.1%}",
                        )

                    st.markdown("---")

                    with st.expander("📋 Decision Details", expanded=True):
                        st.markdown("### Explanation")
                        st.write(decision["decision"]["explanation"])

                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("### Primary Factors")
                            for factor in decision["decision"]["key_decision_factors"][
                                "primary_factors"
                            ]:
                                st.write(f"• {factor}")

                        with col2:
                            st.markdown("### Secondary Factors")
                            factors = decision["decision"]["key_decision_factors"].get(
                                "secondary_factors", []
                            )
                            if factors:
                                for factor in factors:
                                    st.write(f"• {factor}")
                            else:
                                st.write("None")

                    with st.expander("👤 Applicant Profile Analysis"):
                        profile = decision["applicant_profile"]
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric(
                                "Income Stability",
                                f"{profile['income_stability_score']:.1%}",
                            )
                            st.metric(
                                "Employment Risk",
                                f"{profile['employment_risk']:.1%}",
                            )

                        with col2:
                            st.metric("Age Risk Factor", f"{profile['age_risk_factor']:.1%}")
                            st.write(f"**Credit History:** {profile['credit_history_summary']}")

                    with st.expander("💰 Financial Risk Analysis"):
                        risk = decision["financial_risk"]
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("DTI Ratio", f"{risk['debt_to_income_ratio']:.2f}")
                            st.metric(
                                "Credit Risk Level",
                                risk["credit_score_risk_level"].upper(),
                            )

                        with col2:
                            st.metric("Loan Amount Risk", risk["loan_amount_risk"].upper())
                            st.metric(
                                "Anomaly Detected",
                                "🔴 Yes" if risk["anomaly_detected"] else "🟢 No",
                            )

                    with st.expander("🎫 Case Information"):
                        st.write(f"**Case ID:** {decision['compliance']['case_id']}")
                        st.write(
                            f"**Processing Time:** {decision['processing_time_seconds']:.2f}s"
                        )
                        st.write(
                            f"**Timestamp:** {decision['compliance']['timestamp']}"
                        )

                    with st.expander("📜 Audit Trail"):
                        for entry in decision["audit_trail"]:
                            st.write(entry)

                else:
                    st.error(f"❌ Error: {response.json()['detail']}")

            except requests.exceptions.ConnectionError:
                st.error(
                    "❌ Cannot connect to API. Make sure the backend is running on port 8000."
                )
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

with tab2:
    st.header("Application Status")

    job_id = st.text_input("Enter Job ID to check status")

    if st.button("Check Status"):
        try:
            response = requests.get(
                f"{API_BASE_URL}/api/loan-application/{job_id}/status",
                timeout=10,
            )
            if response.status_code == 200:
                status = response.json()
                st.json(status)
            else:
                st.error("Job not found")
        except Exception as e:
            st.error(f"Error: {str(e)}")

with tab3:
    st.header("System Analytics")

    try:
        response = requests.get(f"{API_BASE_URL}/api/health", timeout=10)
        if response.status_code == 200:
            health = response.json()

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("System Status", "🟢 Healthy")
            with col2:
                st.metric("Timestamp", health["timestamp"][:10])
            with col3:
                st.metric("Agents Active", "4")

            st.subheader("Workflow Agents")
            agents = health["orchestrator"]["agents"]
            for agent in agents:
                st.write(f"✓ {agent}")

    except Exception as e:
        st.error(f"Error fetching health data: {str(e)}")

with tab4:
    st.header("About This System")

    st.markdown("""
    ## Loan Approval System - Multi-Agent Architecture

    This system uses Agentic AI to automate loan application analysis and approval decisions.

    ### 🏗️ Architecture
    - **Presentation Layer:** Streamlit UI
    - **Microservice Layer:** FastAPI REST API
    - **Orchestration Layer:** LangGraph-based workflow
    - **Agent Layer:** 4 domain-specific agents
    - **Communication:** MCP Protocol servers

    ### 👥 Agents

    1. **Applicant Profile Agent**
       - Analyzes applicant demographics and employment
       - Outputs: Income stability, employment risk, credit history

    2. **Financial Risk Agent**
       - Analyzes credit metrics and loan parameters
       - Outputs: DTI ratio, risk levels, anomalies

    3. **Loan Decision Agent**
       - Synthesizes all analysis into final decision
       - Outputs: Approve/Reject/Review with confidence

    4. **Compliance Agent**
       - Handles notifications and audit logging
       - Outputs: Case ID, audit trail, compliance status

    ### 📊 Input Parameters
    - Applicant Profile: Age, Income, Employment Type
    - Credit Metrics: Credit Score
    - Loan Details: Amount, Tenure, Existing Liabilities
    - Location & Timestamp

    ### 🎯 Output Decision
    - **APPROVED:** Applicant meets criteria
    - **REJECTED:** High risk identified
    - **REVIEW:** Requires manual evaluation

    ### 🔒 Features
    - Explainable AI decisions
    - Full audit trail
    - Regulatory compliance
    - Error handling & retry logic
    - Real-time processing

    ### 📚 Technology Stack
    - Python 3.x
    - FastAPI, Streamlit
    - LangGraph, LangChain
    - Anthropic Claude LLM
    - MCP Protocol
    """)
