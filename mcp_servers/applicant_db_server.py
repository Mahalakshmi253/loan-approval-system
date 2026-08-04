"""MCP Server for Applicant Database - Profile Analysis."""
import asyncio
from datetime import datetime
from typing import Any
from fastmcp import Server
from pydantic import BaseModel


class ApplicantProfileRequest(BaseModel):
    """Request for applicant profile analysis."""

    applicant_id: str
    age: int
    income: float
    employment_type: str
    credit_score: int


class ApplicantProfileResponse(BaseModel):
    """Response from applicant profile analysis."""

    income_stability_score: float
    employment_risk: float
    credit_history_summary: str
    completeness_flags: list
    age_risk_factor: float


def create_applicant_db_server():
    """Create and return the applicant DB MCP server."""
    server = Server("ApplicantDB")

    @server.call_tool()
    async def analyze_applicant_profile(
        applicant_id: str,
        age: int,
        income: float,
        employment_type: str,
        credit_score: int,
    ) -> dict[str, Any]:
        """
        Analyze applicant profile and generate scores.

        Args:
            applicant_id: Unique applicant identifier
            age: Applicant age
            income: Annual income
            employment_type: Type of employment (employed, self_employed, etc.)
            credit_score: Credit score (300-850)

        Returns:
            Profile analysis with scores and flags
        """
        completeness_flags = []

        income_stability = 0.8
        if income < 25000:
            income_stability = 0.4
            completeness_flags.append("Low income threshold")
        elif income < 50000:
            income_stability = 0.6
        elif income > 200000:
            income_stability = 0.95

        employment_risk = 0.3
        if employment_type == "self_employed":
            employment_risk = 0.5
            completeness_flags.append("Self-employed - higher risk")
        elif employment_type == "unemployed":
            employment_risk = 0.9
            completeness_flags.append("Currently unemployed")
        elif employment_type == "retired":
            employment_risk = 0.6
            completeness_flags.append("Retired - income verification required")

        age_risk = 0.2
        if age < 25:
            age_risk = 0.4
            completeness_flags.append("Young applicant - limited credit history")
        elif age > 65:
            age_risk = 0.5
            completeness_flags.append("Senior applicant - retirement risk")

        credit_history = "Good credit profile"
        if credit_score < 500:
            credit_history = "Poor credit history - significant risk"
        elif credit_score < 600:
            credit_history = "Fair credit history - moderate risk"
        elif credit_score > 750:
            credit_history = "Excellent credit history"

        return {
            "income_stability_score": income_stability,
            "employment_risk": employment_risk,
            "credit_history_summary": credit_history,
            "completeness_flags": completeness_flags,
            "age_risk_factor": age_risk,
            "timestamp": datetime.now().isoformat(),
        }

    @server.call_tool()
    async def get_credit_history(applicant_id: str) -> dict[str, Any]:
        """
        Fetch credit history for applicant.

        Args:
            applicant_id: Applicant ID

        Returns:
            Credit history summary
        """
        return {
            "applicant_id": applicant_id,
            "credit_inquiries": 3,
            "accounts_open": 5,
            "accounts_closed": 2,
            "average_account_age": 7.5,
            "recent_delinquencies": False,
        }

    @server.call_tool()
    async def get_employment_verification(applicant_id: str, employment_type: str) -> dict[str, Any]:
        """
        Verify employment status.

        Args:
            applicant_id: Applicant ID
            employment_type: Type of employment

        Returns:
            Employment verification status
        """
        return {
            "applicant_id": applicant_id,
            "employment_verified": True,
            "verification_date": datetime.now().isoformat(),
            "employment_type": employment_type,
            "employment_duration_months": 36,
        }

    return server


if __name__ == "__main__":
    import uvicorn

    server = create_applicant_db_server()
    uvicorn.run(server, host="127.0.0.1", port=8001)
