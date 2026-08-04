import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Work Order Compliance Inspector",
    page_icon="🛠️",
    layout="wide"
)

st.title("🛠️ Autonomous Work Order & Compliance Inspector")
st.markdown("Automated multi-agent auditing of work orders against compliance standards and rate cards.")

# API Key Validation
groq_api_key = os.getenv("GROQ_API_KEY") or st.sidebar.text_input("Enter Groq API Key:", type="password")

if not groq_api_key:
    st.warning("Please provide a Groq API Key in the sidebar or via .env file to proceed.")
    st.stop()

# Initialize LLM
llm = ChatGroq(
    temperature=0.2,
    model_name="groq/llama-3.3-70b-versatile",
    groq_api_key=groq_api_key
)

# Sidebar Inputs
st.sidebar.header("Audit Inputs")
work_order_input = st.sidebar.text_area(
    "Work Order Details:",
    height=200,
    placeholder="Paste daily work order breakdown, labor hours, and equipment used..."
)

rate_card_input = st.sidebar.text_area(
    "Contract Rate Card & Guidelines:",
    height=150,
    placeholder="Paste standard hourly rates, allowed equipment, and safety policies..."
)

if st.sidebar.button("Run Audit Inspection", type="primary"):
    if not work_order_input or not rate_card_input:
        st.error("Please provide both Work Order details and Rate Card guidelines.")
    else:
        with st.spinner("Executing Multi-Agent Compliance Audit..."):
            
            # Agent 1: Rate Card Auditor
            rate_auditor = Agent(
                role="Rate Card Auditor",
                goal="Cross-check billing rates, labor hours, and equipment charges against contract rate cards.",
                backstory="An expert financial auditor specialized in industrial contracts, equipment rentals, and labor rate validation.",
                verbose=True,
                allow_delegation=False,
                llm=llm
            )

            # Agent 2: Compliance Specialist
            compliance_officer = Agent(
                role="Compliance Specialist",
                goal="Identify safety, operational, and scope-of-work compliance violations.",
                backstory="A strict compliance officer with 15+ years of experience in industrial safety and contract scope enforcement.",
                verbose=True,
                allow_delegation=False,
                llm=llm
            )

            # Task 1: Audit Rates
            task_rate_audit = Task(
                description=f"Analyze the following Work Order against the Rate Card:\n\nWORK ORDER:\n{work_order_input}\n\nRATE CARD:\n{rate_card_input}\n\nFlag any overbilling or rate discrepancies.",
                expected_output="A detailed list of billing discrepancies and rate compliance findings.",
                agent=rate_auditor
            )

            # Task 2: Audit Compliance
            task_compliance_audit = Task(
                description=f"Review the Work Order for scope violations, unapproved gear, or safety compliance issues:\n\nWORK ORDER:\n{work_order_input}\n\nGUIDELINES:\n{rate_card_input}",
                expected_output="A breakdown of scope, equipment, and safety compliance findings.",
                agent=compliance_officer
            )

            # Orchestrate Crew
            compliance_crew = Crew(
                agents=[rate_auditor, compliance_officer],
                tasks=[task_rate_audit, task_compliance_audit],
                process=Process.sequential,
                verbose=True
            )

            result = compliance_crew.kickoff()

            st.success("Audit Completed Successfully!")
            st.markdown("### 📋 Audit & Compliance Report")
            st.markdown(result)
