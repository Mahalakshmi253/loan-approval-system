"""SQLAlchemy database models for loan approval system."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from .session import Base


class LoanApplicationDB(Base):
    """Loan application database model."""
    __tablename__ = "loan_applications"

    id = Column(Integer, primary_key=True, index=True)
    applicant_id = Column(String(100), unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    income = Column(Float, nullable=False)
    employment_type = Column(String(50), nullable=False)
    credit_score = Column(Integer, nullable=False)
    loan_amount = Column(Float, nullable=False)
    tenure_months = Column(Integer, nullable=False)
    existing_liabilities = Column(Float, default=0)
    location = Column(String(100), default="USA")
    application_timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    status = Column(String(20), default="pending")  # pending, approved, rejected, review

    # Relationships
    profile = relationship("ApplicationProfile", uselist=False, back_populates="application")
    financial_risk = relationship("FinancialRisk", uselist=False, back_populates="application")
    decision = relationship("LoanDecision", uselist=False, back_populates="application")
    compliance = relationship("ComplianceRecord", uselist=False, back_populates="application")

    def __repr__(self):
        return f"<LoanApplication(applicant_id={self.applicant_id}, status={self.status})>"


class ApplicationProfile(Base):
    """Applicant profile analysis results."""
    __tablename__ = "application_profiles"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("loan_applications.id"), nullable=False)
    income_stability_score = Column(Float, nullable=False)
    employment_risk = Column(Float, nullable=False)
    credit_history_summary = Column(String(255), nullable=False)
    completeness_flags = Column(Text)  # JSON string
    age_risk_factor = Column(Float, nullable=False)
    analysis_timestamp = Column(DateTime, default=datetime.utcnow)

    application = relationship("LoanApplicationDB", back_populates="profile")

    def __repr__(self):
        return f"<ApplicationProfile(income_stability={self.income_stability_score})>"


class FinancialRisk(Base):
    """Financial risk analysis results."""
    __tablename__ = "financial_risks"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("loan_applications.id"), nullable=False)
    debt_to_income_ratio = Column(Float, nullable=False)
    credit_score_risk_level = Column(String(50), nullable=False)
    loan_amount_risk = Column(String(50), nullable=False)
    anomaly_detected = Column(Boolean, default=False)
    anomaly_reasons = Column(Text)  # JSON string
    risk_score = Column(Float, nullable=False)
    reasoning = Column(Text, nullable=False)
    analysis_timestamp = Column(DateTime, default=datetime.utcnow)

    application = relationship("LoanApplicationDB", back_populates="financial_risk")

    def __repr__(self):
        return f"<FinancialRisk(dti={self.debt_to_income_ratio}, risk={self.risk_score})>"


class LoanDecision(Base):
    """Loan decision results."""
    __tablename__ = "loan_decisions"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("loan_applications.id"), nullable=False)
    classification = Column(String(20), nullable=False)  # approved, rejected, review
    risk_score = Column(Float, nullable=False)
    confidence_level = Column(Float, nullable=False)
    key_decision_factors = Column(Text, nullable=False)  # JSON string
    explanation = Column(Text, nullable=False)
    decision_timestamp = Column(DateTime, default=datetime.utcnow)

    application = relationship("LoanApplicationDB", back_populates="decision")

    def __repr__(self):
        return f"<LoanDecision(classification={self.classification}, confidence={self.confidence_level})>"


class ComplianceRecord(Base):
    """Compliance and audit record."""
    __tablename__ = "compliance_records"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("loan_applications.id"), nullable=False)
    case_id = Column(String(100), unique=True, index=True, nullable=False)
    action_taken = Column(String(255), nullable=False)
    notification_sent = Column(Boolean, default=False)
    audit_trail = Column(Text)  # JSON string
    created_timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    processing_time_seconds = Column(Float)

    application = relationship("LoanApplicationDB", back_populates="compliance")

    def __repr__(self):
        return f"<ComplianceRecord(case_id={self.case_id})>"
