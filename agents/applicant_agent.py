"""Applicant Profile Agent - Analyzes applicant demographics and employment."""
from typing import Any, Dict
from backend.models import ApplicantProfileOutput, LoanApplication
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ApplicantProfileAgent:
    """Agent for analyzing applicant profile and generating scores."""

    def __init__(self):
        """Initialize the applicant profile agent."""
        self.name = "ApplicantProfileAgent"

    async def analyze(self, application: LoanApplication) -> ApplicantProfileOutput:
        """
        Analyze applicant profile.

        Args:
            application: Loan application data

        Returns:
            Applicant profile analysis output
        """
        logger.info(f"Analyzing applicant profile for {application.applicant_id}")

        income_stability = self._calculate_income_stability(application.income, application.age)

        employment_risk = self._calculate_employment_risk(
            application.employment_type, application.age
        )

        age_risk = self._calculate_age_risk(application.age)

        credit_history = self._get_credit_history_summary(application.credit_score)

        completeness_flags = self._check_completeness(application)

        logger.info(
            f"Profile analysis complete: stability={income_stability:.2f}, "
            f"employment_risk={employment_risk:.2f}"
        )

        return ApplicantProfileOutput(
            income_stability_score=income_stability,
            employment_risk=employment_risk,
            credit_history_summary=credit_history,
            completeness_flags=completeness_flags,
            age_risk_factor=age_risk,
        )

    def _calculate_income_stability(self, income: float, age: int) -> float:
        """Calculate income stability score."""
        stability = 0.5
        if income >= 100000:
            stability = 0.85
        elif income >= 75000:
            stability = 0.75
        elif income >= 50000:
            stability = 0.65
        elif income >= 25000:
            stability = 0.55

        if 30 <= age <= 50:
            stability += 0.1
        elif age < 25 or age > 65:
            stability -= 0.1

        return min(max(stability, 0), 1)

    def _calculate_employment_risk(self, employment_type: str, age: int) -> float:
        """Calculate employment risk factor."""
        risk_map = {
            "employed": 0.2,
            "self_employed": 0.5,
            "unemployed": 0.95,
            "retired": 0.6,
        }
        risk = risk_map.get(employment_type, 0.5)

        if employment_type == "retired" and age > 70:
            risk += 0.1

        return min(max(risk, 0), 1)

    def _calculate_age_risk(self, age: int) -> float:
        """Calculate age-related risk factor."""
        if 25 <= age <= 55:
            return 0.1
        elif age < 25:
            return 0.4
        elif age > 70:
            return 0.5
        else:
            return 0.2

    def _get_credit_history_summary(self, credit_score: int) -> str:
        """Get credit history summary based on score."""
        if credit_score >= 750:
            return "Excellent credit history"
        elif credit_score >= 700:
            return "Good credit history"
        elif credit_score >= 650:
            return "Fair credit history - some concerns"
        elif credit_score >= 600:
            return "Poor credit history - significant risk"
        else:
            return "Very poor credit history - high risk"

    def _check_completeness(self, application: LoanApplication) -> list:
        """Check application completeness."""
        flags = []

        if application.age < 25:
            flags.append("Young applicant - limited history")
        if application.income < 30000:
            flags.append("Below average income")
        if application.employment_type == "self_employed":
            flags.append("Self-employed - needs verification")
        if application.credit_score < 600:
            flags.append("Low credit score")

        return flags if flags else ["Application meets standard criteria"]

    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process state in workflow."""
        import asyncio

        application = state.get("application")
        result = asyncio.run(self.analyze(application))
        state["applicant_profile"] = result
        return state
