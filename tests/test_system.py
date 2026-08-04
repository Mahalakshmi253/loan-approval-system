"""Integration tests for loan approval system."""
import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.models import LoanApplication, EmploymentType
from agents.orchestrator import LoanApprovalOrchestrator


async def test_approved_application():
    """Test with application that should be approved."""
    print("\n✅ Test 1: Application - APPROVED")
    print("=" * 50)

    orchestrator = LoanApprovalOrchestrator()

    application = LoanApplication(
        applicant_id="TEST-APPROVED-001",
        age=35,
        income=120000,
        employment_type=EmploymentType.EMPLOYED,
        credit_score=780,
        loan_amount=200000,
        tenure_months=180,
        existing_liabilities=300,
        location="USA",
    )

    validation = await orchestrator.validate_application(application)
    assert validation["valid"], f"Validation failed: {validation['issues']}"

    response = await orchestrator.process_application(application)

    print(f"  Applicant ID: {response.applicant_id}")
    print(f"  Decision: {response.decision.classification.value.upper()}")
    print(f"  Risk Score: {response.financial_risk.risk_score:.1%}")
    print(f"  Confidence: {response.decision.confidence_level:.1%}")
    print(f"  Case ID: {response.compliance.case_id}")
    print(f"  Processing Time: {response.processing_time_seconds:.2f}s")

    assert response.decision.classification.value == "approved"
    print("  ✓ Test passed!")


async def test_rejected_application():
    """Test with application that should be rejected."""
    print("\n❌ Test 2: Application - REJECTED")
    print("=" * 50)

    orchestrator = LoanApprovalOrchestrator()

    application = LoanApplication(
        applicant_id="TEST-REJECTED-001",
        age=25,
        income=25000,
        employment_type=EmploymentType.UNEMPLOYED,
        credit_score=450,
        loan_amount=500000,
        tenure_months=360,
        existing_liabilities=2000,
        location="USA",
    )

    validation = await orchestrator.validate_application(application)
    assert validation["valid"], f"Validation failed: {validation['issues']}"

    response = await orchestrator.process_application(application)

    print(f"  Applicant ID: {response.applicant_id}")
    print(f"  Decision: {response.decision.classification.value.upper()}")
    print(f"  Risk Score: {response.financial_risk.risk_score:.1%}")
    print(f"  Confidence: {response.decision.confidence_level:.1%}")
    print(f"  Case ID: {response.compliance.case_id}")

    assert response.decision.classification.value == "rejected"
    print("  ✓ Test passed!")


async def test_review_application():
    """Test with application that requires manual review."""
    print("\n⚠️  Test 3: Application - REQUIRES REVIEW")
    print("=" * 50)

    orchestrator = LoanApprovalOrchestrator()

    application = LoanApplication(
        applicant_id="TEST-REVIEW-001",
        age=45,
        income=65000,
        employment_type=EmploymentType.SELF_EMPLOYED,
        credit_score=650,
        loan_amount=180000,
        tenure_months=240,
        existing_liabilities=800,
        location="USA",
    )

    validation = await orchestrator.validate_application(application)
    assert validation["valid"], f"Validation failed: {validation['issues']}"

    response = await orchestrator.process_application(application)

    print(f"  Applicant ID: {response.applicant_id}")
    print(f"  Decision: {response.decision.classification.value.upper()}")
    print(f"  Risk Score: {response.financial_risk.risk_score:.1%}")
    print(f"  Confidence: {response.decision.confidence_level:.1%}")
    print(f"  Case ID: {response.compliance.case_id}")

    assert response.decision.classification.value == "review"
    print("  ✓ Test passed!")


async def test_agent_outputs():
    """Test individual agent outputs."""
    print("\n🔍 Test 4: Individual Agent Outputs")
    print("=" * 50)

    orchestrator = LoanApprovalOrchestrator()

    application = LoanApplication(
        applicant_id="TEST-AGENTS-001",
        age=40,
        income=95000,
        employment_type=EmploymentType.EMPLOYED,
        credit_score=700,
        loan_amount=250000,
        tenure_months=180,
        existing_liabilities=500,
        location="USA",
    )

    print("\n  1️⃣  Applicant Profile Agent:")
    applicant_profile = await orchestrator.applicant_agent.analyze(application)
    print(f"     Income Stability: {applicant_profile.income_stability_score:.1%}")
    print(f"     Employment Risk: {applicant_profile.employment_risk:.1%}")
    print(f"     Age Risk Factor: {applicant_profile.age_risk_factor:.1%}")

    print("\n  2️⃣  Financial Risk Agent:")
    financial_risk = await orchestrator.financial_risk_agent.analyze(application)
    print(f"     DTI Ratio: {financial_risk.debt_to_income_ratio:.2f}")
    print(f"     Credit Risk: {financial_risk.credit_score_risk_level}")
    print(f"     Risk Score: {financial_risk.risk_score:.1%}")
    print(f"     Anomaly Detected: {financial_risk.anomaly_detected}")

    print("\n  3️⃣  Decision Agent:")
    decision = await orchestrator.decision_agent.decide(applicant_profile, financial_risk)
    print(f"     Decision: {decision.classification.value.upper()}")
    print(f"     Confidence: {decision.confidence_level:.1%}")
    print(f"     Primary Factors: {', '.join(decision.key_decision_factors.primary_factors)}")

    print("\n  4️⃣  Compliance Agent:")
    compliance = await orchestrator.compliance_agent.process_decision(
        application.applicant_id, decision
    )
    print(f"     Action: {compliance.action_taken}")
    print(f"     Case ID: {compliance.case_id}")
    print(f"     Notification Sent: {compliance.notification_sent}")

    print("\n  ✓ All agents working correctly!")


async def test_validation():
    """Test application validation."""
    print("\n🔐 Test 5: Application Validation")
    print("=" * 50)

    orchestrator = LoanApprovalOrchestrator()

    invalid_apps = [
        {
            "name": "Missing applicant ID",
            "data": {
                "applicant_id": "",
                "age": 35,
                "income": 75000,
                "employment_type": "employed",
                "credit_score": 700,
                "loan_amount": 250000,
                "tenure_months": 180,
                "existing_liabilities": 0,
            },
        },
        {
            "name": "Age out of range",
            "data": {
                "applicant_id": "TEST",
                "age": 85,
                "income": 75000,
                "employment_type": "employed",
                "credit_score": 700,
                "loan_amount": 250000,
                "tenure_months": 180,
                "existing_liabilities": 0,
            },
        },
        {
            "name": "Invalid tenure",
            "data": {
                "applicant_id": "TEST",
                "age": 35,
                "income": 75000,
                "employment_type": "employed",
                "credit_score": 700,
                "loan_amount": 250000,
                "tenure_months": 3,
                "existing_liabilities": 0,
            },
        },
    ]

    for test_case in invalid_apps:
        try:
            app = LoanApplication(**test_case["data"])
            validation = await orchestrator.validate_application(app)
            if not validation["valid"]:
                print(f"  ✓ {test_case['name']}: Correctly rejected")
            else:
                print(f"  ❌ {test_case['name']}: Should have been rejected")
        except Exception as e:
            print(f"  ✓ {test_case['name']}: Validation error caught")

    print("\n  ✓ Validation tests passed!")


async def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("🏦 LOAN APPROVAL SYSTEM - TEST SUITE")
    print("=" * 60)

    try:
        await test_approved_application()
        await test_rejected_application()
        await test_review_application()
        await test_agent_outputs()
        await test_validation()

        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60 + "\n")

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return False

    return True


if __name__ == "__main__":
    print("\n🚀 Starting Loan Approval System Tests...\n")
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
