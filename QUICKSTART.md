# 🚀 Quick Start Guide

Get the Loan Approval System running in 5 minutes!

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Terminal/Command prompt

## Step 1: Navigate to Project
```bash
cd "/home/ubuntu/bfs batch8/loan-approval-system"
```

## Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- FastAPI, Uvicorn
- Streamlit
- Pydantic
- And all other required packages

## Step 3: Configure Environment
```bash
cp .env.example .env
```

**Optional:** Edit `.env` to customize settings (API ports, thresholds, etc.)

## Step 4: Start the System

### Option A: Automated (Recommended)
```bash
chmod +x run.sh
./run.sh
```

This automatically:
- Starts FastAPI backend on port 8000
- Starts Streamlit UI on port 8501
- Handles cleanup on exit

### Option B: Manual

**Terminal 1 - Start Backend API:**
```bash
python -m backend.main
```
Expected output:
```
INFO:     Loan Approval System starting up...
INFO:     Model: claude-3-5-sonnet-20241022
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Terminal 2 - Start Frontend UI:**
```bash
streamlit run frontend/streamlit_app.py
```
Expected output:
```
  You can now view your Streamlit app in your browser.
  Local URL: http://127.0.0.1:8501
```

## Step 5: Access the System

### Web UI
Open browser to: **http://localhost:8501**

### API Documentation
Open browser to: **http://localhost:8000/docs**

## Step 6: Submit a Test Application

### Via UI (Easiest)
1. Click **"📝 Apply"** tab
2. Fill in the form:
   - Applicant ID: `APP-TEST-001`
   - Age: `35`
   - Annual Income: `75000`
   - Employment Type: `employed`
   - Credit Score: `720`
   - Loan Amount: `250000`
   - Tenure: `180` months
3. Click **"🚀 Submit Application"**
4. View decision in real-time!

### Via API (Using curl)
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

## Step 7: View Results

The response includes:
- ✅ **Decision**: APPROVED / REJECTED / REVIEW
- 📊 **Risk Score**: Overall risk assessment
- 💯 **Confidence**: Decision confidence level
- 📋 **Factors**: Key decision factors
- 🔍 **Explanation**: Why this decision was made
- 📜 **Audit Trail**: Complete processing log
- 🎫 **Case ID**: Unique case identifier

## Test Scenarios

### Scenario 1: Application That Gets APPROVED
```json
{
  "applicant_id": "TEST-APPROVED",
  "age": 40,
  "income": 120000,
  "employment_type": "employed",
  "credit_score": 780,
  "loan_amount": 200000,
  "tenure_months": 180,
  "existing_liabilities": 300
}
```
**Expected**: ✅ APPROVED (Strong profile)

### Scenario 2: Application That Gets REJECTED
```json
{
  "applicant_id": "TEST-REJECTED",
  "age": 25,
  "income": 25000,
  "employment_type": "unemployed",
  "credit_score": 450,
  "loan_amount": 500000,
  "tenure_months": 360,
  "existing_liabilities": 2000
}
```
**Expected**: ❌ REJECTED (High risk)

### Scenario 3: Application That Requires REVIEW
```json
{
  "applicant_id": "TEST-REVIEW",
  "age": 45,
  "income": 65000,
  "employment_type": "self_employed",
  "credit_score": 650,
  "loan_amount": 180000,
  "tenure_months": 240,
  "existing_liabilities": 800
}
```
**Expected**: ⚠️ REVIEW (Mixed signals)

## Running Tests

Run the full test suite:
```bash
python tests/test_system.py
```

Output shows:
- ✅ Test 1: APPROVED application
- ❌ Test 2: REJECTED application  
- ⚠️ Test 3: REVIEW application
- 🔍 Test 4: Individual agent outputs
- 🔐 Test 5: Validation checks

## Troubleshooting

### "Connection refused"
**Problem**: Can't connect to http://localhost:8000  
**Solution**: Make sure FastAPI is running in Terminal 1

### "Streamlit not found"
**Problem**: Streamlit command not found  
**Solution**: Run `pip install streamlit` first

### "Port already in use"
**Problem**: Port 8000 or 8501 is taken  
**Solution**: Edit `.env` to use different ports, or:
```bash
# Kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Kill process using port 8501
lsof -ti:8501 | xargs kill -9
```

### "ModuleNotFoundError"
**Problem**: Python can't find required modules  
**Solution**: 
```bash
# Make sure you installed requirements
pip install -r requirements.txt

# Make sure you're in the right directory
pwd  # Should show: .../loan-approval-system
```

## Directory Layout
```
loan-approval-system/
├── frontend/
│   └── streamlit_app.py         ← UI
├── backend/
│   ├── main.py                  ← API server
│   ├── routes/
│   │   └── loan_routes.py       ← Endpoints
│   └── models/
│       └── loan_models.py       ← Data models
├── agents/
│   ├── orchestrator.py          ← Workflow coordinator
│   ├── applicant_agent.py       ← Agent 1
│   ├── financial_risk_agent.py  ← Agent 2
│   ├── decision_agent.py        ← Agent 3
│   └── compliance_agent.py      ← Agent 4
├── mcp_servers/
│   ├── applicant_db_server.py   ← MCP Server 1
│   ├── risk_rules_server.py     ← MCP Server 2
│   ├── decision_synthesis_server.py  ← MCP Server 3
│   └── notification_server.py   ← MCP Server 4
├── tests/
│   └── test_system.py           ← Integration tests
├── requirements.txt             ← Dependencies
├── .env.example                 ← Config template
├── README.md                    ← Full documentation
├── ARCHITECTURE.md              ← Technical details
└── run.sh                       ← Startup script
```

## What Happens Next?

1. **UI loads** with 4 tabs
2. **Fill out application form** in "Apply" tab
3. **Click Submit** to process
4. **System processes** through 4 agents
5. **Decision appears** with full explanation
6. **View details** in expandable sections
7. **See audit trail** of all steps

## Key Files to Understand

| File | Purpose |
|------|---------|
| `agents/orchestrator.py` | Main workflow logic |
| `agents/*_agent.py` | Individual agent implementations |
| `backend/main.py` | FastAPI entry point |
| `backend/routes/loan_routes.py` | API endpoints |
| `frontend/streamlit_app.py` | UI implementation |

## Next Steps

1. ✅ Get system running
2. ✅ Submit test applications
3. ✅ Review decisions and audit trails
4. 📖 Read `README.md` for full documentation
5. 🏗️ Read `ARCHITECTURE.md` for technical details
6. 🧪 Run `python tests/test_system.py` for tests
7. 🎓 Study agent implementations in `agents/` directory

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python tests/test_system.py

# Start backend only
python -m backend.main

# Start UI only
streamlit run frontend/streamlit_app.py

# Check API health
curl http://localhost:8000/api/health

# View API documentation
open http://localhost:8000/docs
```

## Learning Outcomes

By exploring this system, you'll understand:

✅ Multi-agent architecture design  
✅ Orchestration patterns with state management  
✅ MCP (Model Context Protocol) communication  
✅ FastAPI REST API development  
✅ Streamlit UI development  
✅ Async/await in Python  
✅ Pydantic data validation  
✅ Error handling strategies  
✅ Explainable AI implementation  
✅ Audit trail design  

---

**🎉 You're all set! Start with `./run.sh` or the manual steps above.**

**Questions?** Check README.md or ARCHITECTURE.md for detailed information.
