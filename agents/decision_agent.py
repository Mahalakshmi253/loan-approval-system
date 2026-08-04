"""Decision Agent - Synthesizes all agent outputs for final decision."""
from typing import Any, Dict
from backend.models import (
    LoanDecisionOutput,
    DecisionFactors,
    DecisionType,
    ApplicantProfileOutput,
    FinancialRiskOutput,
)
from utils.logger import setup_logger

logger = setup_logger(__name__)


class LoanDecisionAgent:
    """Agent for synthesizing loan decision from all analysis."""

    def __init__(self):
        """Initialize the decision agent."""
        self.name = "LoanDecisionAgent"

    async def decide(
        self, applicant_profile: ApplicantProfileOutput, financial_risk: FinancialRiskOutput
    ) -> LoanDecisionOutput:
        """
        Make loan decision based on all inputs.

        Args:
            applicant_profile: Applicant profile analysis
            financial_risk: Financial risk analysis

        Returns:
            Loan decision with explanation
        """
        logger.info("Making loan decision...")

        classification = self._determine_classification(applicant_profile, financial_risk)

        confidence = self._calculate_confidence(applicant_profile, financial_risk, classification)

        key_factors = self._identify_key_factors(applicant_profile, financial_risk, classification)

        explanation = self._generate_explanation(
            classification, key_factors, applicant_profile, financial_risk
        )

        logger.info(
            f"Decision made: {classification} with confidence {confidence:.2%}"
        )

        return LoanDecisionOutput(
            classification=classification,
            risk_score=financial_risk.risk_score,
            confidence_level=confidence,
            key_decision_factors=key_factors,
            explanation=explanation,
        )

    def _determine_classification(
        self, applicant: ApplicantProfileOutput, financial: FinancialRiskOutput
    ) -> DecisionType:
        """Determine if loan should be approved, rejected, or reviewed."""

        approval_score = 0.0
        approval_score += applicant.income_stability_score * 0.25
        approval_score += (1 - applicant.employment_risk) * 0.20
        approval_score += (1 - financial.risk_score) * 0.35

        if financial.credit_score_risk_level == "low":
            approval_score += 0.15
        elif financial.credit_score_risk_level == "medium":
            approval_score += 0.05
        elif financial.credit_score_risk_level == "high":
            approval_score -= 0.10

        if financial.debt_to_income_ratio > 0.5:
            approval_score -= 0.20
        elif financial.debt_to_income_ratio > 0.43:
            approval_score -= 0.10

        if financial.anomaly_detected:
            approval_score -= 0.15

        if approval_score > 0.65:
            return DecisionType.APPROVED
        elif approval_score < 0.35:
            return DecisionType.REJECTED
        else:
            return DecisionType.REVIEW

    def _calculate_confidence(
        self,
        applicant: ApplicantProfileOutput,
        financial: FinancialRiskOutput,
        classification: DecisionType,
    ) -> float:
        """Calculate confidence level in the decision."""
        base_confidence = 0.5

        consistency = (
            abs(applicant.income_stability_score - (1 - financial.risk_score)) / 2
        )
        base_confidence += (1 - consistency) * 0.3

        if applicant.employment_risk < 0.3:
            base_confidence += 0.1
        elif applicant.employment_risk > 0.7:
            base_confidence -= 0.1

        if not financial.anomaly_detected:
            base_confidence += 0.1
        else:
            base_confidence -= 0.15

        if financial.credit_score_risk_level == "low":
            base_confidence += 0.1
        elif financial.credit_score_risk_level == "very_high":
            base_confidence -= 0.1

        if classification == DecisionType.APPROVED:
            base_confidence = min(
                max(base_confidence, 0.7), 1.0
            )
        elif classification == DecisionType.REJECTED:
            base_confidence = min(
                max(base_confidence, 0.65), 1.0
            )
        else:
            base_confidence = 0.5

        return min(max(base_confidence, 0), 1)

    def _identify_key_factors(
        self,
        applicant: ApplicantProfileOutput,
        financial: FinancialRiskOutput,
        classification: DecisionType,
    ) -> DecisionFactors:
        """Identify key decision factors."""
        primary = []
        secondary = []
        risk_mitigation = None

        if applicant.income_stability_score > 0.7:
            primary.append("Strong income stability")
        else:
            secondary.append("Moderate income stability")

        if applicant.employment_risk < 0.3:
            primary.append("Low employment risk")
        elif applicant.employment_risk > 0.6:
            primary.append("High employment risk")

        if financial.debt_to_income_ratio < 0.35:
            primary.append("Healthy DTI ratio")
        elif financial.debt_to_income_ratio > 0.50:
            primary.append("High DTI ratio")
            if classification == DecisionType.APPROVED:
                risk_mitigation = "Monitor debt levels closely"

        if financial.credit_score_risk_level == "low":
            primary.append("Excellent credit profile")
        elif financial.credit_score_risk_level == "very_high":
            primary.append("Poor credit history")

        if financial.anomaly_detected:
            secondary.append("Financial anomalies detected")

        if not primary:
            primary = ["Mixed financial profile"]

        return DecisionFactors(
            primary_factors=primary[:3],
            secondary_factors=secondary[:2],
            risk_mitigation=risk_mitigation,
        )

    def _generate_explanation(
        self,
        classification: DecisionType,
        factors: DecisionFactors,
        applicant: ApplicantProfileOutput,
        financial: FinancialRiskOutput,
    ) -> str:
        """Generate explanation for the decision."""
        if classification == DecisionType.APPROVED:
            explanation = (
                f"Application APPROVED. {factors.primary_factors[0] if factors.primary_factors else 'Applicant meets requirements'}. "
                f"Income stability: {applicant.income_stability_score:.1%}. "
                f"Risk score: {financial.risk_score:.1%}."
            )
        elif classification == DecisionType.REJECTED:
            explanation = (
                f"Application REJECTED. Primary concerns: {', '.join(factors.primary_factors[:2])}. "
                f"Risk score: {financial.risk_score:.1%} exceeds acceptable threshold."
            )
        else:
            explanation = (
                f"Application requires MANUAL REVIEW. "
                f"Mixed signals: Income stability {applicant.income_stability_score:.1%}, "
                f"Risk score {financial.risk_score:.1%}. "
                f"Recommend human evaluation."
            )

        return explanation

    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process state in workflow."""
        import asyncio

        applicant_profile = state.get("applicant_profile")
        financial_risk = state.get("financial_risk")
        result = asyncio.run(self.decide(applicant_profile, financial_risk))
        state["decision"] = result
        return state
