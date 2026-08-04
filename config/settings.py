"""Configuration settings for the loan approval system."""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # API Configuration
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000
    API_WORKERS: int = 1

    # Streamlit Configuration
    STREAMLIT_HOST: str = "127.0.0.1"
    STREAMLIT_PORT: int = 8501

    # LLM Configuration
    ANTHROPIC_API_KEY: str = ""
    MODEL_NAME: str = "claude-3-5-sonnet-20241022"

    # MCP Server Configuration
    APPLICANT_DB_PORT: int = 8001
    RISK_RULES_PORT: int = 8002
    DECISION_SYNTHESIS_PORT: int = 8003
    NOTIFICATION_SYSTEM_PORT: int = 8004

    # MySQL Configuration
    DATABASE_URL: str = "mysql+pymysql://loan_user:loan_password_123@localhost:3306/loan_approval_system"
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "loan_user"
    MYSQL_PASSWORD: str = "loan_password_123"
    MYSQL_DATABASE: str = "loan_approval_system"

    # SQLAlchemy Configuration
    SQLALCHEMY_ECHO: bool = True
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = None

    # Decision Thresholds
    CREDIT_SCORE_THRESHOLD: int = 600
    DTI_RATIO_THRESHOLD: float = 0.43
    INCOME_STABILITY_MIN: float = 0.7

    # Feature Flags
    ENABLE_PARALLEL_AGENTS: bool = False
    DEBUG_MODE: bool = False

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
