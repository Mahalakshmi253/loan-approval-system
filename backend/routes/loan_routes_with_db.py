"""FastAPI routes for loan applications with MySQL database integration."""
import json
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from datetime import datetime
from sqlalchemy.orm import Session
from backend.models import LoanApplication, LoanDecisionResponse, ProcessingStatus
from backend.database import get_db
from backend.database.crud import (
    LoanApplicationCRUD,
    ApplicationProfileCRUD,
    FinancialRiskCRUD,
    LoanDecisionCRUD,
    ComplianceRecordCRUD,
)
from agents.orchestrator import LoanApprovalOrchestrator
from utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter(prefix="/api", tags=["loans"])

orchestrator = LoanApprovalOrchestrator()
processing_jobs = {}


@router.post("/loan-application", response_model=LoanDecisionResponse)
async def submit_loan_application(
    application: LoanApplication,
    db: Session = Depends(get_db)
) -> LoanDecisionResponse:
    """
    Submit and process a loan application.
    Saves to MySQL database and returns complete decision.

    Args:
        application: Loan application data
        db: Database session

    Returns:
        Complete loan decision response
    """
    logger.info(f"Received loan application from {application.applicant_id}")

    # Validate application
    validation = await orchestrator.validate_application(application)
    if not validation["valid"]:
        logger.error(f"Validation failed: {validation['issues']}")
        raise HTTPException(status_code=400, detail=f"Validation failed: {validation['issues']}")

    try:
        # 1. Save application to database
        db_application = LoanApplicationCRUD.create_application(
            db=db,
            applicant_id=application.applicant_id,
            age=application.age,
            income=application.income,
            employment_type=application.employment_type.value,
            credit_score=application.credit_score,
            loan_amount=application.loan_amount,
            tenure_months=application.tenure_months,
            existing_liabilities=application.existing_liabilities,
            location=application.location
        )
        logger.info(f"Application saved to DB with ID: {db_application.id}")

        # 2. Process application through orchestrator
        response = await orchestrator.process_application(application)
        logger.info(f"Application processed: {response.applicant_id}")

        # 3. Save applicant profile to database
        ApplicationProfileCRUD.create_profile(
            db=db,
            application_id=db_application.id,
            income_stability_score=response.applicant_profile.income_stability_score,
            employment_risk=response.applicant_profile.employment_risk,
            credit_history_summary=response.applicant_profile.credit_history_summary,
            completeness_flags=response.applicant_profile.completeness_flags,
            age_risk_factor=response.applicant_profile.age_risk_factor
        )
        logger.info(f"Applicant profile saved to DB")

        # 4. Save financial risk to database
        FinancialRiskCRUD.create_risk(
            db=db,
            application_id=db_application.id,
            debt_to_income_ratio=response.financial_risk.debt_to_income_ratio,
            credit_score_risk_level=response.financial_risk.credit_score_risk_level,
            loan_amount_risk=response.financial_risk.loan_amount_risk,
            anomaly_detected=response.financial_risk.anomaly_detected,
            anomaly_reasons=[],
            risk_score=response.financial_risk.risk_score,
            reasoning=response.financial_risk.reasoning
        )
        logger.info(f"Financial risk saved to DB")

        # 5. Save decision to database
        LoanDecisionCRUD.create_decision(
            db=db,
            application_id=db_application.id,
            classification=response.decision.classification.value,
            risk_score=response.decision.risk_score,
            confidence_level=response.decision.confidence_level,
            key_decision_factors=response.decision.key_decision_factors.dict(),
            explanation=response.decision.explanation
        )
        logger.info(f"Decision saved to DB")

        # 6. Save compliance record to database
        ComplianceRecordCRUD.create_compliance(
            db=db,
            application_id=db_application.id,
            case_id=response.compliance.case_id,
            action_taken=response.compliance.action_taken,
            notification_sent=response.compliance.notification_sent,
            audit_trail=response.audit_trail,
            processing_time_seconds=response.processing_time_seconds
        )
        logger.info(f"Compliance record saved to DB: {response.compliance.case_id}")

        # 7. Update application status
        LoanApplicationCRUD.update_application_status(
            db=db,
            application_id=db_application.id,
            status=response.decision.classification.value
        )
        logger.info(f"Application status updated to: {response.decision.classification.value}")

        return response

    except Exception as e:
        logger.error(f"Error processing application: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing application: {str(e)}")


@router.get("/applications/{applicant_id}")
async def get_application(
    applicant_id: str,
    db: Session = Depends(get_db)
):
    """
    Get application and all related data from database.

    Args:
        applicant_id: Applicant ID
        db: Database session

    Returns:
        Complete application record with all analysis
    """
    logger.info(f"Retrieving application for {applicant_id}")

    db_application = LoanApplicationCRUD.get_application_by_applicant_id(db, applicant_id)
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")

    profile = ApplicationProfileCRUD.get_profile_by_application(db, db_application.id)
    risk = FinancialRiskCRUD.get_risk_by_application(db, db_application.id)
    decision = LoanDecisionCRUD.get_decision_by_application(db, db_application.id)
    compliance = ComplianceRecordCRUD.get_compliance_by_application(db, db_application.id)

    return {
        "application": {
            "id": db_application.id,
            "applicant_id": db_application.applicant_id,
            "age": db_application.age,
            "income": db_application.income,
            "employment_type": db_application.employment_type,
            "credit_score": db_application.credit_score,
            "loan_amount": db_application.loan_amount,
            "tenure_months": db_application.tenure_months,
            "existing_liabilities": db_application.existing_liabilities,
            "location": db_application.location,
            "status": db_application.status,
            "timestamp": db_application.application_timestamp
        },
        "profile": {
            "income_stability": profile.income_stability_score,
            "employment_risk": profile.employment_risk,
            "credit_history": profile.credit_history_summary
        } if profile else None,
        "risk": {
            "dti_ratio": risk.debt_to_income_ratio,
            "credit_risk": risk.credit_score_risk_level,
            "risk_score": risk.risk_score
        } if risk else None,
        "decision": {
            "classification": decision.classification,
            "confidence": decision.confidence_level,
            "explanation": decision.explanation
        } if decision else None,
        "compliance": {
            "case_id": compliance.case_id,
            "status": compliance.notification_sent
        } if compliance else None
    }


@router.get("/applications")
async def get_all_applications(
    skip: int = 0,
    limit: int = 10,
    status: str = None,
    db: Session = Depends(get_db)
):
    """
    Get all applications with pagination and optional filtering.

    Args:
        skip: Number of records to skip
        limit: Number of records to return
        status: Filter by status (approved, rejected, review, pending)
        db: Database session

    Returns:
        List of applications
    """
    logger.info(f"Retrieving applications: skip={skip}, limit={limit}, status={status}")

    if status:
        applications = LoanApplicationCRUD.get_applications_by_status(db, status)
    else:
        applications = LoanApplicationCRUD.get_all_applications(db, skip, limit)

    return {
        "total": len(applications),
        "applications": [
            {
                "id": app.id,
                "applicant_id": app.applicant_id,
                "status": app.status,
                "income": app.income,
                "loan_amount": app.loan_amount,
                "timestamp": app.application_timestamp
            }
            for app in applications
        ]
    }


@router.get("/applications/{applicant_id}/decision")
async def get_application_decision(
    applicant_id: str,
    db: Session = Depends(get_db)
):
    """
    Get only the decision for an application.

    Args:
        applicant_id: Applicant ID
        db: Database session

    Returns:
        Decision details
    """
    logger.info(f"Retrieving decision for {applicant_id}")

    db_application = LoanApplicationCRUD.get_application_by_applicant_id(db, applicant_id)
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")

    decision = LoanDecisionCRUD.get_decision_by_application(db, db_application.id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")

    return {
        "applicant_id": applicant_id,
        "case_id": db_application.id,
        "classification": decision.classification,
        "risk_score": decision.risk_score,
        "confidence_level": decision.confidence_level,
        "explanation": decision.explanation,
        "factors": json.loads(decision.key_decision_factors),
        "timestamp": decision.decision_timestamp
    }


@router.get("/statistics")
async def get_statistics(db: Session = Depends(get_db)):
    """
    Get system statistics from database.

    Args:
        db: Database session

    Returns:
        Statistics about applications
    """
    approved = len(LoanApplicationCRUD.get_applications_by_status(db, "approved"))
    rejected = len(LoanApplicationCRUD.get_applications_by_status(db, "rejected"))
    review = len(LoanApplicationCRUD.get_applications_by_status(db, "review"))
    pending = len(LoanApplicationCRUD.get_applications_by_status(db, "pending"))

    total = approved + rejected + review + pending

    return {
        "total_applications": total,
        "approved": approved,
        "rejected": rejected,
        "requires_review": review,
        "pending": pending,
        "approval_rate": round((approved / total * 100) if total > 0 else 0, 2)
    }


@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint with database connection test.

    Args:
        db: Database session

    Returns:
        Health status
    """
    try:
        # Test database connection
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        db_status = "disconnected"

    return {
        "status": "healthy" if db_status == "connected" else "unhealthy",
        "timestamp": datetime.now().isoformat(),
        "database": db_status,
        "orchestrator": orchestrator.get_workflow_status()
    }
