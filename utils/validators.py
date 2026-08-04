"""Validation utilities for loan application data."""
from typing import Optional, Dict, Any
from pydantic import BaseModel, field_validator, ValidationError


class LoanValidator:
    """Validator for loan application data."""

    @staticmethod
    def validate_credit_score(score: int) -> bool:
        """Validate credit score range."""
        return 300 <= score <= 850

    @staticmethod
    def validate_age(age: int) -> bool:
        """Validate applicant age."""
        return 18 <= age <= 80

    @staticmethod
    def validate_income(income: float) -> bool:
        """Validate income."""
        return income > 0

    @staticmethod
    def validate_loan_amount(amount: float) -> bool:
        """Validate loan amount."""
        return 1000 <= amount <= 5000000

    @staticmethod
    def validate_tenure(months: int) -> bool:
        """Validate loan tenure in months."""
        return 6 <= months <= 360

    @staticmethod
    def validate_liabilities(liabilities: float) -> bool:
        """Validate existing liabilities."""
        return liabilities >= 0

    @staticmethod
    def calculate_dti_ratio(income: float, monthly_liabilities: float, monthly_payment: float) -> float:
        """Calculate debt-to-income ratio."""
        monthly_income = income / 12
        total_monthly_debt = monthly_liabilities + monthly_payment
        if monthly_income <= 0:
            return 1.0
        return total_monthly_debt / monthly_income

    @staticmethod
    def estimate_monthly_payment(loan_amount: float, tenure_months: int, annual_rate: float = 0.07) -> float:
        """Estimate monthly payment using standard formula."""
        if tenure_months <= 0:
            return 0
        monthly_rate = annual_rate / 12
        if monthly_rate == 0:
            return loan_amount / tenure_months
        payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** tenure_months) / (
            (1 + monthly_rate) ** tenure_months - 1
        )
        return payment
