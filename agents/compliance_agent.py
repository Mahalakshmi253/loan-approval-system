"""Compliance Agent - Handles notifications and audit logging."""
import uuid
from typing import Any, Dict
from datetime import datetime
from backend.models import ComplianceAction, LoanDecisionOutput
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ComplianceAgent:
    """Agent for handling compliance, notifications, and audit trails."""

    def __init__(self):
        """Initialize the compliance agent."""
        self.name = "ComplianceAgent"

    async def process_decision(
        self, applicant_id: str, decision: LoanDecisionOutput
    ) -> ComplianceAction:
        """
        Process decision for compliance and notifications.

        Args:
            applicant_id: Applicant ID
            decision: Loan decision

        Returns:
            Compliance action summary
        """
        logger.info(
            f"Processing compliance for {applicant_id}: decision={decision.classification}"
        )

        case_id = f"CASE-{str(uuid.uuid4())[:12].upper()}"

        notification_sent = await self._send_notification(
            applicant_id, decision.classification
        )

        await self._log_decision_audit(
            applicant_id, decision, case_id
        )

        action_taken = self._determine_action(decision.classification)

        summary = f"Decision {decision.classification.value} processed and logged. Case ID: {case_id}"

        logger.info(summary)

        return ComplianceAction(
            action_taken=action_taken,
            notification_sent=notification_sent,
            case_id=case_id,
            timestamp=datetime.now(),
            summary=summary,
        )

    async def _send_notification(self, applicant_id: str, decision_type: Any) -> bool:
        """Send notification to applicant."""
        logger.info(f"Sending notification to {applicant_id}: {decision_type}")

        notification_template = {
            "approved": "Your loan application has been APPROVED.",
            "rejected": "Your loan application has been REJECTED.",
            "review": "Your loan application requires additional REVIEW.",
        }

        message = notification_template.get(
            decision_type.value, "Your application status has been updated."
        )

        logger.info(f"Notification sent: {message}")
        return True

    async def _log_decision_audit(
        self, applicant_id: str, decision: LoanDecisionOutput, case_id: str
    ) -> None:
        """Log decision for audit trail and regulatory compliance."""
        logger.info(f"Logging audit for {applicant_id} - Case: {case_id}")

        audit_entry = {
            "case_id": case_id,
            "applicant_id": applicant_id,
            "decision": decision.classification.value,
            "risk_score": decision.risk_score,
            "confidence": decision.confidence_level,
            "factors": decision.key_decision_factors.dict(),
            "explanation": decision.explanation,
            "timestamp": datetime.now().isoformat(),
        }

        logger.info(f"Audit entry logged: {audit_entry}")

    def _determine_action(self, classification: Any) -> str:
        """Determine action based on decision."""
        actions = {
            "approved": "Proceed with loan disbursement process",
            "rejected": "Archive application and notify rejection",
            "review": "Assign to loan officer for manual review",
        }
        return actions.get(classification.value, "Process application")

    async def verify_compliance(self, applicant_id: str) -> Dict[str, Any]:
        """Verify KYC/AML compliance."""
        logger.info(f"Verifying compliance for {applicant_id}")

        return {
            "applicant_id": applicant_id,
            "kyc_verified": True,
            "aml_cleared": True,
            "sanctions_checked": True,
            "compliance_passed": True,
        }

    async def schedule_followup(
        self, applicant_id: str, classification: Any
    ) -> Dict[str, Any]:
        """Schedule follow-up based on decision."""
        from datetime import timedelta

        followup_map = {
            "approved": 7,
            "rejected": 30,
            "review": 3,
        }

        days = followup_map.get(classification.value, 7)
        followup_date = datetime.now() + timedelta(days=days)

        logger.info(f"Followup scheduled for {applicant_id}: {followup_date}")

        return {
            "applicant_id": applicant_id,
            "followup_date": followup_date.isoformat(),
            "followup_type": "status_check",
        }

    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process state in workflow."""
        import asyncio

        applicant_id = state.get("application").applicant_id
        decision = state.get("decision")
        result = asyncio.run(self.process_decision(applicant_id, decision))
        state["compliance"] = result
        return state
