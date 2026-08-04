"""CRUD operations for database."""
import json
from datetime import datetime
from sqlalchemy.orm import Session
from .models import (
    LoanApplicationDB,
    ApplicationProfile,
    FinancialRisk,
    LoanDecision,
    ComplianceRecord,
)


class LoanApplicationCRUD:
    """CRUD operations for loan applications."""

    @staticmethod
    def create_application(db: Session, applicant_id: str, age: int, income: float,
                          employment_type: str, credit_score: int, loan_amount: float,
                          tenure_months: int, existing_liabilities: float, location: str) -> LoanApplicationDB:
        """Create new loan application record."""
        db_application = LoanApplicationDB(
            applicant_id=applicant_id,
            age=age,
            income=income,
            employment_type=employment_type,
            credit_score=credit_score,
            loan_amount=loan_amount,
            tenure_months=tenure_months,
            existing_liabilities=existing_liabilities,
            location=location,
            status="pending"
        )
        db.add(db_application)
        db.commit()
        db.refresh(db_application)
        return db_application

    @staticmethod
    def get_application_by_id(db: Session, application_id: int) -> LoanApplicationDB:
        """Get application by ID."""
        return db.query(LoanApplicationDB).filter(
            LoanApplicationDB.id == application_id
        ).first()

    @staticmethod
    def get_application_by_applicant_id(db: Session, applicant_id: str) -> LoanApplicationDB:
        """Get application by applicant ID."""
        return db.query(LoanApplicationDB).filter(
            LoanApplicationDB.applicant_id == applicant_id
        ).first()

    @staticmethod
    def update_application_status(db: Session, application_id: int, status: str) -> LoanApplicationDB:
        """Update application status."""
        db_application = LoanApplicationCRUD.get_application_by_id(db, application_id)
        if db_application:
            db_application.status = status
            db.commit()
            db.refresh(db_application)
        return db_application

    @staticmethod
    def get_all_applications(db: Session, skip: int = 0, limit: int = 100):
        """Get all applications with pagination."""
        return db.query(LoanApplicationDB).offset(skip).limit(limit).all()

    @staticmethod
    def get_applications_by_status(db: Session, status: str):
        """Get applications filtered by status."""
        return db.query(LoanApplicationDB).filter(
            LoanApplicationDB.status == status
        ).all()


class ApplicationProfileCRUD:
    """CRUD operations for application profiles."""

    @staticmethod
    def create_profile(db: Session, application_id: int, income_stability_score: float,
                      employment_risk: float, credit_history_summary: str,
                      completeness_flags: list, age_risk_factor: float) -> ApplicationProfile:
        """Create application profile record."""
        db_profile = ApplicationProfile(
            application_id=application_id,
            income_stability_score=income_stability_score,
            employment_risk=employment_risk,
            credit_history_summary=credit_history_summary,
            completeness_flags=json.dumps(completeness_flags),
            age_risk_factor=age_risk_factor
        )
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return db_profile

    @staticmethod
    def get_profile_by_application(db: Session, application_id: int) -> ApplicationProfile:
        """Get profile by application ID."""
        return db.query(ApplicationProfile).filter(
            ApplicationProfile.application_id == application_id
        ).first()


class FinancialRiskCRUD:
    """CRUD operations for financial risk."""

    @staticmethod
    def create_risk(db: Session, application_id: int, debt_to_income_ratio: float,
                   credit_score_risk_level: str, loan_amount_risk: str,
                   anomaly_detected: bool, anomaly_reasons: list, risk_score: float,
                   reasoning: str) -> FinancialRisk:
        """Create financial risk record."""
        db_risk = FinancialRisk(
            application_id=application_id,
            debt_to_income_ratio=debt_to_income_ratio,
            credit_score_risk_level=credit_score_risk_level,
            loan_amount_risk=loan_amount_risk,
            anomaly_detected=anomaly_detected,
            anomaly_reasons=json.dumps(anomaly_reasons),
            risk_score=risk_score,
            reasoning=reasoning
        )
        db.add(db_risk)
        db.commit()
        db.refresh(db_risk)
        return db_risk

    @staticmethod
    def get_risk_by_application(db: Session, application_id: int) -> FinancialRisk:
        """Get risk by application ID."""
        return db.query(FinancialRisk).filter(
            FinancialRisk.application_id == application_id
        ).first()


class LoanDecisionCRUD:
    """CRUD operations for loan decisions."""

    @staticmethod
    def create_decision(db: Session, application_id: int, classification: str,
                       risk_score: float, confidence_level: float,
                       key_decision_factors: dict, explanation: str) -> LoanDecision:
        """Create loan decision record."""
        db_decision = LoanDecision(
            application_id=application_id,
            classification=classification,
            risk_score=risk_score,
            confidence_level=confidence_level,
            key_decision_factors=json.dumps(key_decision_factors),
            explanation=explanation
        )
        db.add(db_decision)
        db.commit()
        db.refresh(db_decision)
        return db_decision

    @staticmethod
    def get_decision_by_application(db: Session, application_id: int) -> LoanDecision:
        """Get decision by application ID."""
        return db.query(LoanDecision).filter(
            LoanDecision.application_id == application_id
        ).first()


class ComplianceRecordCRUD:
    """CRUD operations for compliance records."""

    @staticmethod
    def create_compliance(db: Session, application_id: int, case_id: str,
                         action_taken: str, notification_sent: bool,
                         audit_trail: list, processing_time_seconds: float) -> ComplianceRecord:
        """Create compliance record."""
        db_compliance = ComplianceRecord(
            application_id=application_id,
            case_id=case_id,
            action_taken=action_taken,
            notification_sent=notification_sent,
            audit_trail=json.dumps(audit_trail),
            processing_time_seconds=processing_time_seconds
        )
        db.add(db_compliance)
        db.commit()
        db.refresh(db_compliance)
        return db_compliance

    @staticmethod
    def get_compliance_by_case_id(db: Session, case_id: str) -> ComplianceRecord:
        """Get compliance record by case ID."""
        return db.query(ComplianceRecord).filter(
            ComplianceRecord.case_id == case_id
        ).first()

    @staticmethod
    def get_compliance_by_application(db: Session, application_id: int) -> ComplianceRecord:
        """Get compliance record by application ID."""
        return db.query(ComplianceRecord).filter(
            ComplianceRecord.application_id == application_id
        ).first()
