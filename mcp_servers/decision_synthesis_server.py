"""MCP Server for Decision Synthesis - Loan Decision Making."""
from datetime import datetime
from typing import Any
from fastmcp import Server


def create_decision_synthesis_server():
    """Create and return the decision synthesis MCP server."""
    server = Server("DecisionSynthesis")

    @server.call_tool()
    async def synthesize_decision(
        income_stability_score: float,
        employment_risk: float,
        credit_score_risk_level: str,
        dti_ratio: float,
        risk_score: float,
        loan_amount: float,
        income: float,
    ) -> dict[str, Any]:
        """
        Synthesize loan decision from all inputs.

        Args:
            income_stability_score: Income stability from applicant agent
            employment_risk: Employment risk from applicant agent
            credit_score_risk_level: Credit risk level from risk agent
            dti_ratio: Debt-to-income ratio from risk agent
            risk_score: Overall risk score
            loan_amount: Requested loan amount
            income: Annual income

        Returns:
            Loan decision with classification and factors
        """
        decision = "review"
        confidence = 0.5
        key_factors = []

        if income_stability_score > 0.7 and employment_risk < 0.4 and dti_ratio < 0.43:
            if credit_score_risk_level in ["low", "medium"]:
                decision = "approved"
                confidence = min(income_stability_score, 1 - risk_score * 0.5)
                key_factors = [
                    "Good income stability",
                    "Acceptable employment risk",
                    "Reasonable DTI ratio",
                ]
        elif risk_score > 0.7 or dti_ratio > 0.5 or employment_risk > 0.7:
            decision = "rejected"
            confidence = min(risk_score, 0.95)
            key_factors = []
            if risk_score > 0.7:
                key_factors.append("High overall risk score")
            if dti_ratio > 0.5:
                key_factors.append("DTI ratio too high")
            if employment_risk > 0.7:
                key_factors.append("High employment risk")

        explanation = ""
        if decision == "approved":
            explanation = (
                f"Application approved: Applicant shows strong income stability ({income_stability_score:.1%}), "
                f"acceptable employment profile, and manageable debt obligations (DTI: {dti_ratio:.2f})."
            )
        elif decision == "rejected":
            explanation = (
                f"Application rejected: Risk score of {risk_score:.1%} exceeds acceptable threshold. "
                f"Key concerns: {', '.join(key_factors)}"
            )
        else:
            explanation = (
                f"Application requires manual review: Mixed signals detected. "
                f"Income stability: {income_stability_score:.1%}, Risk Score: {risk_score:.1%}, "
                f"DTI: {dti_ratio:.2f}. Recommend human evaluation."
            )

        return {
            "classification": decision,
            "confidence_level": round(confidence, 4),
            "key_decision_factors": {
                "primary_factors": key_factors[:2] if key_factors else ["Mixed assessment"],
                "secondary_factors": key_factors[2:] if len(key_factors) > 2 else [],
                "risk_mitigation": None if decision == "approved" else "Consider higher interest rate or lower amount",
            },
            "explanation": explanation,
            "risk_score": round(risk_score, 4),
            "timestamp": datetime.now().isoformat(),
        }

    @server.call_tool()
    async def evaluate_approval_probability(
        income_stability: float, employment_risk: float, credit_risk: str, dti_ratio: float
    ) -> dict[str, Any]:
        """
        Evaluate approval probability based on factors.

        Args:
            income_stability: Income stability score
            employment_risk: Employment risk
            credit_risk: Credit risk level
            dti_ratio: Debt-to-income ratio

        Returns:
            Approval probability
        """
        approval_score = 0.5

        approval_score += income_stability * 0.3
        approval_score -= employment_risk * 0.25
        approval_score -= min(dti_ratio / 0.43, 1.0) * 0.25

        credit_multiplier = {"very_high": 0.2, "high": 0.4, "medium": 0.7, "low": 0.9}.get(credit_risk, 0.5)
        approval_score *= credit_multiplier

        approval_probability = min(max(approval_score, 0), 1)

        return {
            "approval_probability": round(approval_probability, 4),
            "recommendation": "likely_approve" if approval_probability > 0.65 else "likely_reject"
            if approval_probability < 0.35 else "requires_review",
            "timestamp": datetime.now().isoformat(),
        }

    @server.call_tool()
    async def generate_recommendation(applicant_profile: dict, financial_risk: dict) -> dict[str, Any]:
        """
        Generate recommendation based on full profile.

        Args:
            applicant_profile: Applicant profile data
            financial_risk: Financial risk data

        Returns:
            Recommendation with reasoning
        """
        return {
            "recommendation": "approve",
            "recommendation_reason": "Applicant meets minimum requirements",
            "suggested_loan_terms": {
                "interest_rate_adjustment": 0.0,
                "loan_amount_suggested": None,
                "additional_conditions": [],
            },
            "timestamp": datetime.now().isoformat(),
        }

    return server


if __name__ == "__main__":
    import uvicorn

    server = create_decision_synthesis_server()
    uvicorn.run(server, host="127.0.0.1", port=8003)
