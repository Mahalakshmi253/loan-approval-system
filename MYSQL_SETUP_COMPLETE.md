# 🗄️ COMPLETE MYSQL SETUP & BACKEND CONNECTION GUIDE

## 📋 TABLE OF CONTENTS
1. MySQL Installation
2. Database Setup in MySQL Workbench
3. Python Dependencies
4. Backend Configuration
5. Running the System
6. Testing API with Database

---

## STEP 1: MYSQL INSTALLATION

### Windows
1. Download: https://dev.mysql.com/downloads/mysql/
2. Run installer
3. Configuration: Default settings, Port 3306
4. Configure MySQL as Windows Service (auto-start)

### Mac
```bash
brew install mysql
brew services start mysql-community-server
mysql_secure_installation
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install mysql-server
sudo mysql_secure_installation
sudo systemctl start mysql
```

---

## STEP 2: MYSQL WORKBENCH SETUP

### Install MySQL Workbench
Download: https://dev.mysql.com/downloads/workbench/

### Create Connection
1. Open MySQL Workbench
2. Click "+" to add new connection
3. Configure:
   - **Connection Name:** LoanApprovalDB
   - **Hostname:** 127.0.0.1 (or localhost)
   - **Port:** 3306
   - **Username:** root
   - **Password:** (your MySQL root password)
4. Click "Test Connection"
5. Click "OK"

### Create Database & User

Double-click to connect, then run these SQL commands:

```sql
-- Create database
CREATE DATABASE IF NOT EXISTS loan_approval_system;
USE loan_approval_system;

-- Create user
CREATE USER IF NOT EXISTS 'loan_user'@'localhost' IDENTIFIED BY 'loan_password_123';

-- Grant privileges
GRANT ALL PRIVILEGES ON loan_approval_system.* TO 'loan_user'@'localhost';
FLUSH PRIVILEGES;

-- Verify
SHOW DATABASES;
SELECT user, host FROM mysql.user;
```

---

## STEP 3: INSTALL PYTHON DEPENDENCIES

### Update requirements.txt

Add these packages:

```txt
sqlalchemy==2.0.23
pymysql==1.1.0
mysql-connector-python==8.2.0
alembic==1.12.1
```

### Install Dependencies

```bash
cd "/home/ubuntu/bfs batch8/loan-approval-system"
pip install -r requirements.txt
```

Or install individually:

```bash
pip install sqlalchemy==2.0.23
pip install pymysql==1.1.0
pip install mysql-connector-python==8.2.0
pip install alembic==1.12.1
```

---

## STEP 4: CONFIGURE ENVIRONMENT

### Create/Update .env file

```env
# MySQL Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=loan_user
MYSQL_PASSWORD=loan_password_123
MYSQL_DATABASE=loan_approval_system

# SQLAlchemy Configuration
DATABASE_URL=mysql+pymysql://loan_user:loan_password_123@localhost:3306/loan_approval_system
SQLALCHEMY_ECHO=True
SQLALCHEMY_TRACK_MODIFICATIONS=False

# API Configuration
API_HOST=127.0.0.1
API_PORT=8000

# Streamlit Configuration
STREAMLIT_HOST=127.0.0.1
STREAMLIT_PORT=8501

# LLM Configuration
ANTHROPIC_API_KEY=your_api_key_here
MODEL_NAME=claude-3-5-sonnet-20241022

# Debug Mode
DEBUG_MODE=True
LOG_LEVEL=INFO
```

---

## STEP 5: FILES STRUCTURE (NEW DATABASE FILES)

Your project now has:

```
loan-approval-system/
├── backend/
│   ├── database/                      ← NEW
│   │   ├── __init__.py
│   │   ├── config.py                 ← Database config
│   │   ├── session.py                ← Connection setup
│   │   ├── models.py                 ← SQLAlchemy models
│   │   └── crud.py                   ← Database operations
│   ├── main_with_db.py               ← NEW (updated main)
│   ├── routes/
│   │   ├── loan_routes_with_db.py    ← NEW (with database)
│   │   └── loan_routes.py            ← OLD (keep for reference)
│   └── ...
```

---

## STEP 6: DATABASE MODELS CREATED

The system creates these MySQL tables automatically:

### loan_applications
```
- id (Primary Key)
- applicant_id (Unique)
- age, income, employment_type
- credit_score, loan_amount, tenure_months
- existing_liabilities, location
- application_timestamp
- status (pending, approved, rejected, review)
```

### application_profiles
```
- id (Primary Key)
- application_id (Foreign Key)
- income_stability_score, employment_risk
- credit_history_summary
- completeness_flags (JSON)
- age_risk_factor
- analysis_timestamp
```

### financial_risks
```
- id (Primary Key)
- application_id (Foreign Key)
- debt_to_income_ratio, credit_score_risk_level
- loan_amount_risk
- anomaly_detected, anomaly_reasons (JSON)
- risk_score, reasoning
- analysis_timestamp
```

### loan_decisions
```
- id (Primary Key)
- application_id (Foreign Key)
- classification (approved, rejected, review)
- risk_score, confidence_level
- key_decision_factors (JSON)
- explanation
- decision_timestamp
```

### compliance_records
```
- id (Primary Key)
- application_id (Foreign Key)
- case_id (Unique)
- action_taken
- notification_sent
- audit_trail (JSON)
- created_timestamp
- processing_time_seconds
```

---

## STEP 7: RUNNING THE SYSTEM

### Option A: With Database (Recommended)

**Terminal 1 - Backend with MySQL:**
```bash
cd "/home/ubuntu/bfs batch8/loan-approval-system"
python -m backend.main_with_db
```

**Terminal 2 - Frontend:**
```bash
cd "/home/ubuntu/bfs batch8/loan-approval-system"
streamlit run frontend/streamlit_app.py
```

### Option B: Original (Without Database)

**Terminal 1:**
```bash
python -m backend.main
```

**Terminal 2:**
```bash
streamlit run frontend/streamlit_app.py
```

---

## STEP 8: API ENDPOINTS WITH DATABASE

### Submit Application (Saves to Database)
```bash
curl -X POST http://localhost:8000/api/loan-application \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "APP-001",
    "age": 35,
    "income": 75000,
    "employment_type": "employed",
    "credit_score": 720,
    "loan_amount": 250000,
    "tenure_months": 180,
    "existing_liabilities": 500,
    "location": "USA"
  }'
```

### Get Application
```bash
curl http://localhost:8000/api/applications/APP-001
```

### Get All Applications
```bash
curl http://localhost:8000/api/applications
curl http://localhost:8000/api/applications?status=approved
curl http://localhost:8000/api/applications?skip=0&limit=10
```

### Get Decision Only
```bash
curl http://localhost:8000/api/applications/APP-001/decision
```

### Get Statistics
```bash
curl http://localhost:8000/api/statistics
```

### Check Database Connection
```bash
curl http://localhost:8000/database/status
```

### Health Check
```bash
curl http://localhost:8000/api/health
```

---

## STEP 9: VERIFY SETUP

### Check MySQL Connection
```bash
mysql -u loan_user -p -h localhost loan_approval_system
```

### View Tables in MySQL Workbench
1. Connect to LoanApprovalDB
2. Expand "loan_approval_system" database
3. See tables created automatically

### Submit Test Application & Check Database
```bash
# 1. Submit via curl
curl -X POST http://localhost:8000/api/loan-application \
  -H "Content-Type: application/json" \
  -d '{"applicant_id":"TEST-001","age":35,...}'

# 2. Check in MySQL Workbench
USE loan_approval_system;
SELECT * FROM loan_applications;
SELECT * FROM application_profiles;
SELECT * FROM financial_risks;
SELECT * FROM loan_decisions;
SELECT * FROM compliance_records;
```

---

## STEP 10: TROUBLESHOOTING

### "Connection refused"
```
Error: Can't connect to MySQL server on 'localhost'
Solution:
- Start MySQL: sudo systemctl start mysql (Linux)
- Check MySQL Workbench connection
- Verify credentials in .env
```

### "Access denied for user"
```
Error: Access denied for user 'loan_user'@'localhost'
Solution:
- Check password in .env matches MySQL
- Run FLUSH PRIVILEGES in MySQL Workbench
- Re-create user if needed
```

### "No database named"
```
Error: Unknown database 'loan_approval_system'
Solution:
- Run CREATE DATABASE command in MySQL Workbench
- Verify DATABASE_URL in .env is correct
```

### "Pymysql not installed"
```
Error: No module named 'pymysql'
Solution:
pip install pymysql==1.1.0
```

### Tables not created automatically
```
Solution:
- Verify database connection works
- Check logs for errors
- Manually verify: python -c "from backend.database import create_all_tables; create_all_tables()"
```

---

## STEP 11: USEFUL MYSQL COMMANDS

```sql
-- Check tables exist
USE loan_approval_system;
SHOW TABLES;

-- View table structure
DESCRIBE loan_applications;

-- Count records
SELECT COUNT(*) FROM loan_applications;

-- View all applications
SELECT * FROM loan_applications;

-- View specific application
SELECT * FROM loan_applications WHERE applicant_id = 'APP-001';

-- View approval statistics
SELECT 
  status,
  COUNT(*) as count,
  ROUND(COUNT(*)*100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM loan_applications
GROUP BY status;

-- Delete test data
DELETE FROM loan_applications WHERE applicant_id LIKE 'TEST-%';

-- Clear all tables (CAREFUL!)
DELETE FROM compliance_records;
DELETE FROM loan_decisions;
DELETE FROM financial_risks;
DELETE FROM application_profiles;
DELETE FROM loan_applications;
```

---

## QUICK START CHECKLIST

- [ ] MySQL server installed and running
- [ ] MySQL Workbench installed
- [ ] Database `loan_approval_system` created
- [ ] User `loan_user` created with password
- [ ] `.env` file configured with MySQL credentials
- [ ] Python dependencies installed
- [ ] Backend runs on port 8000
- [ ] Frontend runs on port 8501
- [ ] Test application submits and saves to database
- [ ] Can view data in MySQL Workbench

---

## SUMMARY

Your Loan Approval System now:

✅ Uses MySQL for persistent storage  
✅ Saves all application data and decisions  
✅ Can retrieve historical data  
✅ Provides statistics and analytics  
✅ Full audit trail in compliance_records  
✅ Professional-grade database backend  

**Access:** http://localhost:8501

**API Docs:** http://localhost:8000/docs

**Database:** MySQL via Workbench

---

**🎉 Setup Complete! Your system is production-ready with MySQL integration.**
