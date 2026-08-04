"""MCP Server for Risk Rules Database - Financial Risk Analysis."""
from datetime import datetime
from typing import Any
from fastmcp import Server


def create_risk_rules_server():
    """Create and return the risk rules MCP server."""
    server = Server("RiskRulesDB")

    @server.call_tool()
    async def analyze_financial_risk(
        credit_score: int,
        loan_amount: float,
        tenure_months: int,
        existing_liabilities: float,
        income: float,
    ) -> dict[str, Any]:
        """
        Analyze financial risk metrics.

        Args:
            credit_score: Credit score
            loan_amount: Requested loan amount
            tenure_months: Loan tenure in months
            existing_liabilities: Current debt obligations
            income: Annual income

        Returns:
            Risk analysis metrics
        """
        monthly_income = income / 12
        if monthly_income <= 0:
            monthly_income = 1

        monthly_payment = (loan_amount * 0.07 / 12 * (1 + 0.07 / 12) ** tenure_months) / (
            (1 + 0.07 / 12) ** tenure_months - 1
        )
        total_monthly_debt = existing_liabilities + monthly_payment
        dti_ratio = total_monthly_debt / monthly_income

        credit_risk = "low"
        if credit_score < 500:
            credit_risk = "very_high"
        elif credit_score < 600:
            credit_risk = "high"
        elif credit_score < 700:
            credit_risk = "medium"

        loan_amount_risk = "low"
        if loan_amount > income * 5:
            loan_amount_risk = "high"
        elif loan_amount > income * 3:
            loan_amount_risk = "medium"

        anomaly_detected = False
        anomaly_reasons = []
        if dti_ratio > 0.5:
            anomaly_detected = True
            anomaly_reasons.append("DTI exceeds 50%")
        if credit_score < 550 and loan_amount > income * 2:
            anomaly_detected = True
            anomaly_reasons.append("Low credit score with high loan amount")

        risk_score = 0.0
        risk_score += (1 - credit_score / 850) * 0.4
        risk_score += min(dti_ratio, 1.0) * 0.3
        risk_score += min(loan_amount / (income * 5), 1.0) * 0.3

        return {
            "debt_to_income_ratio": round(dti_ratio, 4),
            "credit_score_risk_level": credit_risk,
            "loan_amount_risk": loan_amount_risk,
            "anomaly_detected": anomaly_detected,
            "anomaly_reasons": anomaly_reasons,
            "risk_score": round(risk_score, 4),
            "reasoning": f"DTI: {dti_ratio:.2f}, Credit Risk: {credit_risk}, Loan Risk: {loan_amount_risk}",
            "timestamp": datetime.now().isoformat(),
        }

    @server.call_tool()
    async def calculate_dti_ratio(
        monthly_income: float, monthly_liabilities: float, monthly_payment: float
    ) -> dict[str, Any]:
        """
        Calculate debt-to-income ratio.

        Args:
            monthly_income: Monthly income
            monthly_liabilities: Current monthly liabilities
            monthly_payment: Proposed monthly payment

        Returns:
            DTI calculation
        """
        total_monthly_debt = monthly_liabilities + monthly_payment
        if monthly_income <= 0:
            dti = 1.0
        else:
            dti = total_monthly_debt / monthly_income

        return {
            "monthly_income": monthly_income,
            "total_monthly_debt": total_monthly_debt,
            "dti_ratio": round(dti, 4),
            "dti_acceptable": dti <= 0.43,
            "timestamp": datetime.now().isoformat(),
        }

    @server.call_tool()
    async def check_business_rules(
        credit_score: int, dti_ratio: float, loan_amount: float, income: float
    ) -> dict[str, Any]:
        """
        Check against business rules.

        Args:
            credit_score: Credit score
            dti_ratio: Debt-to-income ratio
            loan_amount: Loan amount
            income: Annual income

        Returns:
            Business rule violations
        """
        violations = []

        if credit_score < 600:
            violations.append("Credit score below minimum threshold")
        if dti_ratio > 0.43:
            violations.append("DTI ratio exceeds maximum allowed")
        if loan_amount > income * 5:
            violations.append("Loan amount exceeds 5x annual income")

        return {
            "violations_found": len(violations) > 0,
            "violation_count": len(violations),
            "violations": violations,
            "timestamp": datetime.now().isoformat(),
        }

    return server


if __name__ == "__main__":
    import uvicorn

    server = create_risk_rules_server()
    uvicorn.run(server, host="127.0.0.1", port=8002)
