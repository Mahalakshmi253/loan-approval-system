# 🏦 Multi-Agent Agentic AI Loan Approval System

A comprehensive, production-ready loan approval system using Agentic AI with multiple specialized agents working in orchestration to analyze loan applications and provide explainable, consistent decisions.

## 🎯 Project Overview

This system demonstrates a sophisticated multi-agent architecture for automating loan application analysis. It evaluates applicant details, credit history, risk indicators, and regulatory rules through independent agents that collaborate via LangGraph orchestration, resulting in transparent and auditable loan decisions.

### Business Objectives
✅ Automate loan application analysis using Agentic AI  
✅ Improve decision speed and consistency  
✅ Provide explainable, auditable decisions  
✅ Adopt scalable, loosely coupled microservices architecture  

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│         Presentation Layer (Streamlit UI)                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│      Microservice Layer (FastAPI)                            │
│      - Request validation                                    │
│      - Response formatting                                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│  Orchestration Layer (LangGraph)                             │
│  - Workflow coordination                                     │
│  - State management                                          │
│  - Error handling & retry logic                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              Agent Layer                                     │
│  ┌──────────────┬──────────────┬──────────────┬────────────┐ │
│  │  Applicant   │  Financial   │    Loan      │ Compliance │ │
│  │   Profile    │     Risk     │   Decision   │   Agent    │ │
│  │   Agent      │    Agent     │    Agent     │            │ │
│  └──────────────┴──────────────┴──────────────┴────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│       MCP Servers (Model Context Protocol)                   │
│  ┌──────────────┬──────────────┬──────────────┬────────────┐ │
│  │  Applicant   │   Risk       │  Decision    │Notification│ │
│  │     DB       │   Rules      │  Synthesis   │   System   │ │
│  └──────────────┴──────────────┴──────────────┴────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Project Structure

```
loan-approval-system/
├── frontend/
│   ├── streamlit_app.py          # Streamlit UI application
│   └── __init__.py
├── backend/
│   ├── main.py                    # FastAPI application entry
│   ├── routes/
│   │   ├── loan_routes.py        # API endpoints
│   │   └── __init__.py
│   ├── models/
│   │   ├── loan_models.py        # Pydantic data models
│   │   └── __init__.py
│   └── __init__.py
├── agents/
│   ├── orchestrator.py            # LangGraph orchestration engine
│   ├── applicant_agent.py         # Applicant profile analysis
│   ├── financial_risk_agent.py    # Financial risk analysis
│   ├── decision_agent.py          # Decision synthesis
│   ├── compliance_agent.py        # Compliance & notifications
│   └── __init__.py
├── mcp_servers/
│   ├── applicant_db_server.py    # Applicant DB MCP server
│   ├── risk_rules_server.py      # Risk rules MCP server
│   ├── decision_synthesis_server.py  # Decision MCP server
│   ├── notification_server.py    # Notification MCP server
│   └── __init__.py
├── config/
│   ├── settings.py                # Configuration management
│   └── __init__.py
├── utils/
│   ├── logger.py                  # Logging utilities
│   ├── validators.py              # Data validation utilities
│   └── __init__.py
├── tests/                          # Test suite
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── README.md                      # This file
└── run.sh                         # Startup script
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager
- Anthropic API key (for Claude LLM)

### Installation

1. **Clone or navigate to the project:**
```bash
cd /home/ubuntu/bfs\ batch8/loan-approval-system
```

2. **Create virtual environment (optional but recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Running the System

#### Option 1: Run Everything

```bash
# Terminal 1 - Start FastAPI Backend
python -m backend.main

# Terminal 2 - Start Streamlit UI
streamlit run frontend/streamlit_app.py

# The UI will be available at http://localhost:8501
```

#### Option 2: Using the provided script

```bash
chmod +x run.sh
./run.sh
```

## 👥 Agents Overview

### 1. **Applicant Profile Agent**
Analyzes applicant demographics and employment history.

**Responsibilities:**
- Calculate income stability score
- Assess employment risk
- Evaluate credit history
- Identify completeness flags

**Input:**
- Age, income, employment type, credit score

**Output:**
```json
{
  "income_stability_score": 0.75,
  "employment_risk": 0.3,
  "credit_history_summary": "Good credit history",
  "completeness_flags": ["Below average income"],
  "age_risk_factor": 0.15
}
```

### 2. **Financial Risk Agent**
Analyzes credit metrics and loan parameters.

**Responsibilities:**
- Calculate debt-to-income ratio
- Assess credit score risk
- Evaluate loan amount risk
- Detect financial anomalies

**Input:**
- Credit score, loan amount, tenure, liabilities, income

**Output:**
```json
{
  "debt_to_income_ratio": 0.35,
  "credit_score_risk_level": "medium",
  "loan_amount_risk": "low",
  "anomaly_detected": false,
  "risk_score": 0.32,
  "reasoning": "DTI: 0.35, Credit Risk: medium, Loan Risk: low"
}
```

### 3. **Loan Decision Agent**
Synthesizes all analysis into final decision.

**Responsibilities:**
- Determine approval/rejection/review classification
- Calculate decision confidence
- Identify key decision factors
- Generate explanation

**Input:**
- Applicant profile, financial risk analysis

**Output:**
```json
{
  "classification": "approved",
  "risk_score": 0.32,
  "confidence_level": 0.85,
  "key_decision_factors": {
    "primary_factors": ["Good income stability", "Low employment risk"],
    "secondary_factors": [],
    "risk_mitigation": null
  },
  "explanation": "Application approved: Applicant shows strong income stability..."
}
```

### 4. **Compliance Agent**
Handles notifications, audit logging, and regulatory compliance.

**Responsibilities:**
- Send decision notifications
- Log audit trail
- Create case files
- Schedule follow-up actions

**Output:**
```json
{
  "action_taken": "Notification sent via email",
  "notification_sent": true,
  "case_id": "CASE-ABC123XYZ",
  "timestamp": "2024-01-15T10:30:45",
  "summary": "Decision notification sent to applicant via email"
}
```

## 🔄 Workflow Process

The orchestrator manages a sequential workflow:

```
1. START
   ↓
2. Applicant Profile Agent
   - Input: Loan application data
   - Output: Income stability, employment risk, credit history
   ↓
3. Financial Risk Agent
   - Input: Loan application data + applicant profile
   - Output: DTI ratio, credit risk, anomalies, risk score
   ↓
4. Loan Decision Agent
   - Input: Applicant profile + financial risk
   - Output: Decision (Approve/Reject/Review) with confidence
   ↓
5. Compliance Agent
   - Input: Decision results
   - Output: Case ID, notifications, audit trail
   ↓
6. END - Return complete decision response
```

## 🔌 MCP Servers

Each agent communicates with specialized MCP servers for data and decision-making:

### ApplicantDB Server (Port 8001)
- `analyze_applicant_profile()` - Generate profile scores
- `get_credit_history()` - Fetch credit data
- `get_employment_verification()` - Verify employment

### RiskRulesDB Server (Port 8002)
- `analyze_financial_risk()` - Calculate risk metrics
- `calculate_dti_ratio()` - Compute DTI
- `check_business_rules()` - Validate against rules

### DecisionSynthesis Server (Port 8003)
- `synthesize_decision()` - Make final decision
- `evaluate_approval_probability()` - Estimate approval odds
- `generate_recommendation()` - Provide loan terms

### NotificationSystem Server (Port 8004)
- `send_decision_notification()` - Notify applicant
- `log_decision_audit()` - Audit trail logging
- `create_case_file()` - Create compliance record
- `get_compliance_status()` - Verify KYC/AML
- `schedule_followup()` - Schedule actions

## 📊 API Endpoints

### Submit Loan Application
```bash
POST /api/loan-application
Content-Type: application/json

{
  "applicant_id": "APP-20240115100001",
  "age": 35,
  "income": 75000,
  "employment_type": "employed",
  "credit_score": 720,
  "loan_amount": 250000,
  "tenure_months": 180,
  "existing_liabilities": 500,
  "location": "USA"
}
```

**Response:**
```json
{
  "applicant_id": "APP-20240115100001",
  "decision": {...},
  "applicant_profile": {...},
  "financial_risk": {...},
  "compliance": {...},
  "processing_time_seconds": 2.34,
  "audit_trail": [...]
}
```

### Check Health
```bash
GET /api/health
```

### Get Workflow Status
```bash
GET /api/workflow/status
```

### Submit Async (Non-blocking)
```bash
POST /api/loan-application/async
# Returns job_id for status polling
```

### Check Status
```bash
GET /api/loan-application/{job_id}/status
```

## 🧪 Testing

### Test with Sample Data

Run the included test script:

```bash
python tests/test_system.py
```

Or manually test via API:

```bash
curl -X POST http://localhost:8000/api/loan-application \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "TEST-001",
    "age": 35,
    "income": 75000,
    "employment_type": "employed",
    "credit_score": 720,
    "loan_amount": 250000,
    "tenure_months": 180,
    "existing_liabilities": 500
  }'
```

## 📈 Key Features

✅ **Multi-Agent Architecture**
- Independent agents with clear responsibilities
- LangGraph orchestration for coordination
- Modular and extensible design

✅ **Explainable AI**
- Clear decision reasoning
- Key factor identification
- Confidence levels
- Audit trails

✅ **Robust Error Handling**
- Retry logic with configurable attempts
- Validation at multiple layers
- Comprehensive error messages

✅ **Scalability**
- Async processing support
- Background job handling
- MCP-based communication

✅ **Compliance & Security**
- Full audit trail logging
- Case ID generation
- Compliance status tracking
- KYC/AML verification

✅ **Real-time UI**
- Streamlit-based dashboard
- Live decision updates
- Detailed analytics
- Application history

## ⚙️ Configuration

Edit `config/settings.py` or `.env` to customize:

```env
# Decision Thresholds
CREDIT_SCORE_THRESHOLD=600
DTI_RATIO_THRESHOLD=0.43
INCOME_STABILITY_MIN=0.7

# Feature Flags
ENABLE_PARALLEL_AGENTS=false
DEBUG_MODE=true

# Ports
API_PORT=8000
STREAMLIT_PORT=8501
```

## 📚 Decision Logic

### Approval Score Calculation

```
approval_score = 0.0
+ income_stability_score × 0.25
+ (1 - employment_risk) × 0.20
+ (1 - financial_risk_score) × 0.35
+ credit_factor × 0.15
- dti_penalty
- anomaly_penalty

if approval_score > 0.65  → APPROVED
if approval_score < 0.35  → REJECTED
else                      → REVIEW
```

### Risk Score Formula

```
risk_score = 0.0
+ (1 - credit_score/850) × 0.40
+ min(dti_ratio, 1.0) × 0.35
+ min(loan_amount/(income×5), 1.0) × 0.25
```

## 🔐 Security Considerations

- Input validation on all endpoints
- Error handling without exposing sensitive data
- Audit trail for compliance
- API key protection via environment variables
- CORS configuration for deployment

## 🚦 Monitoring & Debugging

Enable debug logging:

```python
# In config/settings.py
DEBUG_MODE = True
LOG_LEVEL = "DEBUG"
```

View audit trail in decision response:

```json
"audit_trail": [
  "[2024-01-15T10:30:45.123456] Workflow started",
  "[2024-01-15T10:30:45.234567] Step 1: Analyzing applicant profile",
  "[2024-01-15T10:30:45.345678] Step 2: Analyzing financial risk",
  ...
]
```

## 📖 Code Walkthrough

### Adding a New Agent

1. Create `agents/new_agent.py`:
```python
class NewAgent:
    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # Process logic
        return state
```

2. Integrate into orchestrator in `agents/orchestrator.py`:
```python
result = await self.new_agent.process(state)
state["new_agent_output"] = result
```

3. Update workflow workflow in Streamlit if needed

### Modifying Decision Logic

Edit decision thresholds in `agents/decision_agent.py`:

```python
def _determine_classification(self, ...):
    if approval_score > 0.65:  # Adjust threshold
        return DecisionType.APPROVED
```

## 🤝 Live Code Walkthrough

During evaluation, demonstrate:

1. **Full workflow execution** - Submit application and show all agent outputs
2. **Decision modification** - Change approval threshold in code and re-test
3. **Audit trail** - Show full decision reasoning
4. **Error handling** - Test with invalid data
5. **Agent independence** - Show individual agent calculations

## 📝 Evaluation Criteria

✅ Understanding of Agentic AI architecture  
✅ Correct orchestration using LangGraph  
✅ Clear agent responsibilities and MCP usage  
✅ Ability to modify code live  
✅ Explainable AI outputs with full audit trail  

## 🐛 Troubleshooting

### Connection Error
```
Error: Cannot connect to API on port 8000
Solution: Ensure FastAPI is running: python -m backend.main
```

### API Key Error
```
Error: ANTHROPIC_API_KEY not set
Solution: Add API key to .env file
```

### Port Already in Use
```
Error: Address already in use
Solution: Change port in config/settings.py or kill process on port
```

## 📞 Support & Contact

For questions or issues:
1. Check audit trail for debugging
2. Review error messages in logs
3. Verify configuration in `.env`
4. Test endpoints with curl before using UI

## 📄 License

This project is provided as-is for evaluation purposes.

---

**Built with ❤️ using Python, FastAPI, Streamlit, LangGraph, and Anthropic Claude**
