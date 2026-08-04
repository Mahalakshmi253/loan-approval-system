"""Financial Risk Agent - Analyzes credit metrics and loan parameters."""
from typing import Any, Dict
from backend.models import FinancialRiskOutput, LoanApplication
from utils.logger import setup_logger
from utils.validators import LoanValidator

logger = setup_logger(__name__)


class FinancialRiskAgent:
    """Agent for analyzing financial risk metrics."""

    def __init__(self):
        """Initialize the financial risk agent."""
        self.name = "FinancialRiskAgent"
        self.validator = LoanValidator()

    async def analyze(self, application: LoanApplication) -> FinancialRiskOutput:
        """
        Analyze financial risk.

        Args:
            application: Loan application data

        Returns:
            Financial risk analysis output
        """
        logger.info(f"Analyzing financial risk for {application.applicant_id}")

        monthly_payment = self.validator.estimate_monthly_payment(
            application.loan_amount, application.tenure_months
        )

        dti_ratio = self.validator.calculate_dti_ratio(
            application.income, application.existing_liabilities, monthly_payment
        )

        credit_risk_level = self._assess_credit_risk(application.credit_score)

        loan_amount_risk = self._assess_loan_amount_risk(
            application.loan_amount, application.income
        )

        anomaly_detected, anomaly_reason = self._detect_anomalies(
            application, dti_ratio, monthly_payment
        )

        risk_score = self._calculate_risk_score(
            application.credit_score, dti_ratio, application.loan_amount, application.income
        )

        reasoning = self._generate_reasoning(
            dti_ratio, credit_risk_level, loan_amount_risk, anomaly_detected
        )

        logger.info(
            f"Financial risk analysis complete: risk_score={risk_score:.3f}, "
            f"dti={dti_ratio:.3f}, anomaly={anomaly_detected}"
        )

        return FinancialRiskOutput(
            debt_to_income_ratio=dti_ratio,
            credit_score_risk_level=credit_risk_level,
            loan_amount_risk=loan_amount_risk,
            anomaly_detected=anomaly_detected,
            risk_score=risk_score,
            reasoning=reasoning,
        )

    def _assess_credit_risk(self, credit_score: int) -> str:
        """Assess credit risk based on score."""
        if credit_score >= 750:
            return "low"
        elif credit_score >= 700:
            return "low"
        elif credit_score >= 650:
            return "medium"
        elif credit_score >= 600:
            return "high"
        else:
            return "very_high"

    def _assess_loan_amount_risk(self, loan_amount: float, income: float) -> str:
        """Assess loan amount risk relative to income."""
        loan_to_income = loan_amount / income if income > 0 else 10

        if loan_to_income <= 3:
            return "low"
        elif loan_to_income <= 5:
            return "medium"
        else:
            return "high"

    def _detect_anomalies(
        self, application: LoanApplication, dti_ratio: float, monthly_payment: float
    ) -> tuple:
        """Detect financial anomalies."""
        anomalies = []

        if dti_ratio > 0.5:
            anomalies.append("DTI ratio exceeds 50%")

        if application.loan_amount > application.income * 5:
            anomalies.append("Loan amount exceeds 5x annual income")

        if (
            application.credit_score < 600
            and application.loan_amount > application.income * 2
        ):
            anomalies.append("Low credit score with high loan amount")

        if application.existing_liabilities > application.income * 2:
            anomalies.append("Existing liabilities exceed 2x annual income")

        return len(anomalies) > 0, " | ".join(anomalies)

    def _calculate_risk_score(
        self, credit_score: int, dti_ratio: float, loan_amount: float, income: float
    ) -> float:
        """Calculate overall risk score (0-1, higher = riskier)."""
        risk = 0.0

        credit_factor = max(0, (850 - credit_score) / 550)
        risk += min(credit_factor, 1.0) * 0.4

        dti_factor = min(dti_ratio / 0.43, 1.0)
        risk += dti_factor * 0.35

        loan_factor = min(loan_amount / (income * 5), 1.0)
        risk += loan_factor * 0.25

        return min(max(risk, 0), 1)

    def _generate_reasoning(
        self, dti_ratio: float, credit_risk: str, loan_risk: str, anomaly: bool
    ) -> str:
        """Generate reasoning for risk assessment."""
        parts = [
            f"DTI: {dti_ratio:.2f}",
            f"Credit Risk: {credit_risk}",
            f"Loan Risk: {loan_risk}",
        ]

        if anomaly:
            parts.append("Anomalies detected")

        return " | ".join(parts)

    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process state in workflow."""
        import asyncio

        application = state.get("application")
        result = asyncio.run(self.analyze(application))
        state["financial_risk"] = result
        return state
