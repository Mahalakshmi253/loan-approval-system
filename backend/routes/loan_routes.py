"""FastAPI routes for loan applications."""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from datetime import datetime
from backend.models import LoanApplication, LoanDecisionResponse, ProcessingStatus
from agents.orchestrator import LoanApprovalOrchestrator
from utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter(prefix="/api", tags=["loans"])

orchestrator = LoanApprovalOrchestrator()
processing_jobs = {}


@router.post("/loan-application", response_model=LoanDecisionResponse)
async def submit_loan_application(application: LoanApplication) -> LoanDecisionResponse:
    """
    Submit and process a loan application.

    Args:
        application: Loan application data

    Returns:
        Complete loan decision response
    """
    logger.info(f"Received loan application from {application.applicant_id}")

    validation = await orchestrator.validate_application(application)
    if not validation["valid"]:
        logger.error(f"Validation failed: {validation['issues']}")
        raise HTTPException(status_code=400, detail=f"Validation failed: {validation['issues']}")

    try:
        response = await orchestrator.process_application(application)
        logger.info(f"Application processed successfully: {response.applicant_id}")
        return response
    except Exception as e:
        logger.error(f"Error processing application: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing application: {str(e)}")


@router.post("/loan-application/async")
async def submit_loan_application_async(
    application: LoanApplication, background_tasks: BackgroundTasks
) -> dict:
    """
    Submit loan application asynchronously.

    Args:
        application: Loan application data
        background_tasks: FastAPI background tasks

    Returns:
        Processing job ID
    """
    import uuid

    job_id = str(uuid.uuid4())
    processing_jobs[job_id] = {
        "status": "processing",
        "applicant_id": application.applicant_id,
        "started_at": datetime.now().isoformat(),
    }

    async def process_async():
        try:
            result = await orchestrator.process_application(application)
            processing_jobs[job_id] = {
                "status": "completed",
                "applicant_id": application.applicant_id,
                "result": result.dict(),
                "completed_at": datetime.now().isoformat(),
            }
        except Exception as e:
            processing_jobs[job_id] = {
                "status": "failed",
                "applicant_id": application.applicant_id,
                "error": str(e),
                "failed_at": datetime.now().isoformat(),
            }

    background_tasks.add_task(process_async)

    return {"job_id": job_id, "status": "processing"}


@router.get("/loan-application/{job_id}/status")
async def get_application_status(job_id: str) -> ProcessingStatus:
    """
    Get status of a loan application.

    Args:
        job_id: Job ID

    Returns:
        Processing status
    """
    if job_id not in processing_jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = processing_jobs[job_id]
    status = job.get("status", "unknown")

    return ProcessingStatus(
        status=status,
        current_step="Loan Decision" if status == "completed" else status,
        progress_percentage=100 if status == "completed" else 50 if status == "processing" else 0,
        message=f"Application {status}",
    )


@router.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "orchestrator": orchestrator.get_workflow_status(),
    }


@router.get("/workflow/status")
async def get_workflow_status() -> dict:
    """Get workflow status."""
    return orchestrator.get_workflow_status()


@router.get("/applications/{applicant_id}/history")
async def get_application_history(applicant_id: str) -> dict:
    """
    Get application history for applicant.

    Args:
        applicant_id: Applicant ID

    Returns:
        Application history
    """
    logger.info(f"Fetching history for {applicant_id}")

    return {
        "applicant_id": applicant_id,
        "applications": [
            {
                "case_id": "CASE-ABC123",
                "decision": "approved",
                "applied_date": datetime.now().isoformat(),
            }
        ],
    }


@router.post("/workflow/retry")
async def retry_application(application: LoanApplication) -> LoanDecisionResponse:
    """
    Retry a failed loan application with error handling.

    Args:
        application: Loan application data

    Returns:
        Decision response after retry
    """
    logger.info(f"Retrying application {application.applicant_id}")

    try:
        response = await orchestrator.retry_workflow(application, max_retries=3)
        return response
    except Exception as e:
        logger.error(f"Retry failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Retry failed after multiple attempts: {str(e)}"
        )
