"""MCP Server for Notification System - Compliance and Actions."""
import uuid
from datetime import datetime
from typing import Any
from fastmcp import Server


def create_notification_server():
    """Create and return the notification MCP server."""
    server = Server("NotificationSystem")

    @server.call_tool()
    async def send_decision_notification(
        applicant_id: str, decision: str, decision_details: dict
    ) -> dict[str, Any]:
        """
        Send notification of decision to applicant.

        Args:
            applicant_id: Applicant ID
            decision: Decision type (approved/rejected/review)
            decision_details: Details of the decision

        Returns:
            Notification confirmation
        """
        case_id = f"CASE-{str(uuid.uuid4())[:8].upper()}"

        notification_method = "email"
        notification_status = "sent"

        notification_content = f"Loan Application Decision: {decision.upper()}"
        if decision == "approved":
            notification_content += "\nCongratulations! Your loan application has been approved."
        elif decision == "rejected":
            notification_content += "\nUnfortunately, your loan application has been rejected at this time."
        else:
            notification_content += "\nYour application requires additional review. We will contact you soon."

        return {
            "action_taken": f"Notification sent via {notification_method}",
            "notification_sent": True,
            "notification_method": notification_method,
            "notification_status": notification_status,
            "case_id": case_id,
            "applicant_id": applicant_id,
            "notification_content": notification_content,
            "timestamp": datetime.now().isoformat(),
            "summary": f"Decision notification sent to applicant via {notification_method}. Case ID: {case_id}",
        }

    @server.call_tool()
    async def log_decision_audit(
        applicant_id: str, decision: str, decision_factors: dict, risk_score: float
    ) -> dict[str, Any]:
        """
        Log decision for audit trail and compliance.

        Args:
            applicant_id: Applicant ID
            decision: Decision type
            decision_factors: Factors influencing decision
            risk_score: Overall risk score

        Returns:
            Audit log confirmation
        """
        audit_id = str(uuid.uuid4())

        return {
            "audit_id": audit_id,
            "applicant_id": applicant_id,
            "decision_logged": True,
            "log_timestamp": datetime.now().isoformat(),
            "decision_factors_logged": True,
            "regulatory_compliant": True,
            "audit_summary": f"Decision {decision} logged with factors: {', '.join(decision_factors.get('primary_factors', []))}",
        }

    @server.call_tool()
    async def create_case_file(applicant_id: str, application_data: dict) -> dict[str, Any]:
        """
        Create case file for compliance and record keeping.

        Args:
            applicant_id: Applicant ID
            application_data: Complete application data

        Returns:
            Case file creation status
        """
        case_id = f"CASE-{str(uuid.uuid4())[:12].upper()}"

        return {
            "case_id": case_id,
            "applicant_id": applicant_id,
            "case_created": True,
            "creation_timestamp": datetime.now().isoformat(),
            "case_status": "active",
            "retention_period_days": 2555,
            "case_summary": f"Loan application case file created for applicant {applicant_id}",
        }

    @server.call_tool()
    async def get_compliance_status(applicant_id: str) -> dict[str, Any]:
        """
        Get compliance status for applicant.

        Args:
            applicant_id: Applicant ID

        Returns:
            Compliance status
        """
        return {
            "applicant_id": applicant_id,
            "kyc_verified": True,
            "aml_cleared": True,
            "sanctions_checked": True,
            "compliance_status": "compliant",
            "verification_timestamp": datetime.now().isoformat(),
        }

    @server.call_tool()
    async def schedule_followup(
        applicant_id: str, decision: str, reason: str = ""
    ) -> dict[str, Any]:
        """
        Schedule follow-up action based on decision.

        Args:
            applicant_id: Applicant ID
            decision: Decision type
            reason: Reason for follow-up

        Returns:
            Follow-up schedule
        """
        followup_days = 0
        followup_type = None

        if decision == "approved":
            followup_days = 7
            followup_type = "loan_disbursement"
        elif decision == "rejected":
            followup_days = 30
            followup_type = "reapplication_eligibility"
        else:
            followup_days = 3
            followup_type = "additional_documentation"

        followup_date = datetime.now()
        from datetime import timedelta

        followup_date = followup_date + timedelta(days=followup_days)

        return {
            "followup_scheduled": True,
            "followup_type": followup_type,
            "scheduled_date": followup_date.isoformat(),
            "days_until_followup": followup_days,
            "action_description": f"Schedule {followup_type} for applicant",
            "timestamp": datetime.now().isoformat(),
        }

    return server


if __name__ == "__main__":
    import uvicorn

    server = create_notification_server()
    uvicorn.run(server, host="127.0.0.1", port=8004)
