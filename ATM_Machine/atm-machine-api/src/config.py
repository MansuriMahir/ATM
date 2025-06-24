import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database configuration (ALWAYS use SQLAlchemy URL format)
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'atm.db')}"

# API configuration
API_TITLE = "ATM Machine API"
API_DESCRIPTION = "API for ATM Machine operations"
API_VERSION = "1.0.0"

# Security configuration
ADMIN_USERNAME = "Admin"
ADMIN_PIN = "0000"