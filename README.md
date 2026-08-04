# Autonomous Work Order & Compliance Inspector 

An autonomous multi-agent software platform designed to automate the auditing of enterprise work orders against vendor contracts, rate cards, and compliance guidelines.

---

### Problem Statement
In technical, industrial, and field operations (such as energy, construction, and electrical management), manually reviewing daily work orders, equipment rentals, and contractor invoices is extremely time-consuming and prone to human error—leading to costly overbilling and compliance leaks.

### Solution & Architecture
This application deploys a team of specialized AI agents built with **CrewAI** and powered by **Groq (Llama 3.3)** to validate unstructured or tabular work orders:
1. **Rate Card Auditor Agent:** Cross-checks billing lines against contractual rate cards.
2. **Compliance Specialist Agent:** Verifies whether requested equipment and labor items adhere to project safety and operational scope.
3. **Report Generation Agent:** Aggregates findings, flags overbilling discrepancies, and exports formatted compliance logs.

---

### Tech Stack

- **Frameworks & Orchestration:** `CrewAI`, `Pydantic`
- **LLM Engine:** `Groq API` (Llama 3.3 70B)
- **User Interface:** `Streamlit`
- **Database & Storage:** `SQLite`
- **Language:** `Python 3.11+`

---

### Getting Started

#### Prerequisites
- Python 3.11 or higher
- Groq API Key

#### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/bokii85-dotcom/work-order-compliance-inspector.git
   cd work-order-compliance-inspector
   python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
GROQ_API_KEY=your_groq_api_key_here
streamlit run app.py

