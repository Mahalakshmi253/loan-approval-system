"""Pydantic models for loan application data."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from enum import Enum


class EmploymentType(str, Enum):
    """Employment type enumeration."""

    EMPLOYED = "employed"
    SELF_EMPLOYED = "self_employed"
    UNEMPLOYED = "unemployed"
    RETIRED = "retired"


class DecisionType(str, Enum):
    """Loan decision enumeration."""

    APPROVED = "approved"
    REJECTED = "rejected"
    REVIEW = "review"


class LoanApplication(BaseModel):
    """Input loan application data."""

    applicant_id: str = Field(..., min_length=1)
    age: int = Field(..., ge=18, le=80)
    income: float = Field(..., gt=0)
    employment_type: EmploymentType
    credit_score: int = Field(..., ge=300, le=850)
    loan_amount: float = Field(..., gt=0, le=5000000)
    tenure_months: int = Field(..., ge=6, le=360)
    existing_liabilities: float = Field(default=0, ge=0)
    location: str = Field(default="USA")
    application_timestamp: Optional[datetime] = None

    @field_validator("application_timestamp", mode="before")
    @classmethod
    def set_timestamp(cls, v):
        """Set timestamp if not provided."""
        return v or datetime.now()


class ApplicantProfileOutput(BaseModel):
    """Output from applicant profile agent."""

    income_stability_score: float = Field(..., ge=0, le=1)
    employment_risk: float = Field(..., ge=0, le=1)
    credit_history_summary: str
    completeness_flags: List[str]
    age_risk_factor: float = Field(..., ge=0, le=1)


class FinancialRiskOutput(BaseModel):
    """Output from financial risk agent."""

    debt_to_income_ratio: float = Field(..., ge=0)
    credit_score_risk_level: str
    loan_amount_risk: str
    anomaly_detected: bool
    risk_score: float = Field(..., ge=0, le=1)
    reasoning: str


class DecisionFactors(BaseModel):
    """Key factors in the decision."""

    primary_factors: List[str]
    secondary_factors: List[str]
    risk_mitigation: Optional[str] = None


class LoanDecisionOutput(BaseModel):
    """Output from loan decision agent."""

    classification: DecisionType
    risk_score: float = Field(..., ge=0, le=1)
    confidence_level: float = Field(..., ge=0, le=1)
    key_decision_factors: DecisionFactors
    explanation: str


class ComplianceAction(BaseModel):
    """Compliance and action output."""

    action_taken: str
    notification_sent: bool
    case_id: str
    timestamp: datetime
    summary: str


class LoanDecisionResponse(BaseModel):
    """Complete loan decision response."""

    applicant_id: str
    decision: LoanDecisionOutput
    applicant_profile: ApplicantProfileOutput
    financial_risk: FinancialRiskOutput
    compliance: ComplianceAction
    processing_time_seconds: float
    audit_trail: List[str]


class ProcessingStatus(BaseModel):
    """Status of loan application processing."""

    status: str
    current_step: str
    progress_percentage: int
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)
