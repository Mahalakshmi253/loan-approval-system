"""Database configuration."""
import os
from dotenv import load_dotenv

load_dotenv()

# MySQL Configuration
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER = os.getenv("MYSQL_USER", "loan_user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "loan_password_123")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "loan_approval_system")

# SQLAlchemy Configuration
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)

# Echo SQL statements
SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "False") == "True"

# Connection pooling
SQLALCHEMY_POOL_SIZE = 10
SQLALCHEMY_MAX_OVERFLOW = 20
SQLALCHEMY_POOL_RECYCLE = 3600
SQLALCHEMY_POOL_PRE_PING = True
