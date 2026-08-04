"""LangGraph-based orchestration engine for loan approval workflow."""
from typing import Any, Dict, List, Optional
from datetime import datetime
from backend.models import LoanApplication, LoanDecisionResponse
from agents.applicant_agent import ApplicantProfileAgent
from agents.financial_risk_agent import FinancialRiskAgent
from agents.decision_agent import LoanDecisionAgent
from agents.compliance_agent import ComplianceAgent
from utils.logger import setup_logger

logger = setup_logger(__name__)


class LoanApprovalOrchestrator:
    """LangGraph-based orchestration for loan approval workflow."""

    def __init__(self):
        """Initialize orchestrator with all agents."""
        self.applicant_agent = ApplicantProfileAgent()
        self.financial_risk_agent = FinancialRiskAgent()
        self.decision_agent = LoanDecisionAgent()
        self.compliance_agent = ComplianceAgent()
        self.audit_trail: List[str] = []

    async def process_application(
        self, application: LoanApplication
    ) -> LoanDecisionResponse:
        """
        Process loan application through orchestrated workflow.

        Workflow DAG:
        1. Applicant Profile Agent → analyze demographics
        2. Financial Risk Agent → analyze financials
        3. Loan Decision Agent → synthesize decision
        4. Compliance Agent → handle notifications & logging

        Args:
            application: Loan application data

        Returns:
            Complete decision response with audit trail
        """
        start_time = datetime.now()
        self.audit_trail = []

        logger.info(f"Starting loan approval workflow for {application.applicant_id}")
        self._log_audit("Workflow started")

        try:
            self._log_audit("Step 1: Analyzing applicant profile")
            applicant_profile = await self.applicant_agent.analyze(application)
            logger.info(f"Applicant profile: {applicant_profile}")

            self._log_audit("Step 2: Analyzing financial risk")
            financial_risk = await self.financial_risk_agent.analyze(application)
            logger.info(f"Financial risk: {financial_risk}")

            self._log_audit("Step 3: Making loan decision")
            decision = await self.decision_agent.decide(applicant_profile, financial_risk)
            logger.info(f"Decision: {decision.classification}")

            self._log_audit(f"Step 4: Processing compliance (Decision: {decision.classification})")
            compliance = await self.compliance_agent.process_decision(
                application.applicant_id, decision
            )
            logger.info(f"Compliance processed: {compliance.case_id}")

            processing_time = (datetime.now() - start_time).total_seconds()
            self._log_audit(f"Workflow completed in {processing_time:.2f} seconds")

            response = LoanDecisionResponse(
                applicant_id=application.applicant_id,
                decision=decision,
                applicant_profile=applicant_profile,
                financial_risk=financial_risk,
                compliance=compliance,
                processing_time_seconds=processing_time,
                audit_trail=self.audit_trail,
            )

            return response

        except Exception as e:
            logger.error(f"Error in workflow: {str(e)}")
            self._log_audit(f"Error: {str(e)}")
            raise

    def _log_audit(self, message: str) -> None:
        """Add message to audit trail."""
        timestamp = datetime.now().isoformat()
        audit_entry = f"[{timestamp}] {message}"
        self.audit_trail.append(audit_entry)
        logger.info(f"Audit: {audit_entry}")

    async def validate_application(self, application: LoanApplication) -> Dict[str, Any]:
        """
        Validate application before processing.

        Args:
            application: Loan application data

        Returns:
            Validation result
        """
        logger.info(f"Validating application: {application.applicant_id}")

        issues = []

        if not application.applicant_id:
            issues.append("Missing applicant ID")

        if application.age < 18 or application.age > 80:
            issues.append("Age out of acceptable range")

        if application.income <= 0:
            issues.append("Invalid income")

        if application.loan_amount <= 0:
            issues.append("Invalid loan amount")

        if application.tenure_months < 6:
            issues.append("Tenure too short (minimum 6 months)")

        is_valid = len(issues) == 0

        return {
            "valid": is_valid,
            "issues": issues,
            "timestamp": datetime.now().isoformat(),
        }

    def get_workflow_status(self) -> Dict[str, Any]:
        """Get current workflow status."""
        return {
            "status": "ready",
            "agents": [
                self.applicant_agent.name,
                self.financial_risk_agent.name,
                self.decision_agent.name,
                self.compliance_agent.name,
            ],
            "audit_trail_length": len(self.audit_trail),
            "timestamp": datetime.now().isoformat(),
        }

    async def retry_workflow(
        self, application: LoanApplication, max_retries: int = 2
    ) -> LoanDecisionResponse:
        """
        Retry workflow with error handling.

        Args:
            application: Loan application
            max_retries: Maximum retry attempts

        Returns:
            Decision response
        """
        for attempt in range(max_retries):
            try:
                logger.info(f"Workflow attempt {attempt + 1}/{max_retries}")
                return await self.process_application(application)
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    logger.error(f"All {max_retries} attempts failed")
                    raise
                continue

    def reset_audit_trail(self) -> None:
        """Reset audit trail for new application."""
        self.audit_trail = []
        logger.info("Audit trail reset")
