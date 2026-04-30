"""
Single source of truth for all configuration values.

All URLs, timeouts, and expected test strings live here.
Never hard-code these values in page objects or tests (DRY).
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# URLs  (canonical domain is insiderone.com)
# ---------------------------------------------------------------------------
BASE_URL: str = os.getenv("BASE_URL", "https://insiderone.com")
CAREERS_URL: str = f"{BASE_URL}/careers/"
CAREERS_OPEN_ROLES_URL: str = f"{BASE_URL}/careers/#open-roles"

# Accept both domains in URL assertions (CDN may serve either)
CAREERS_URL_FRAGMENTS: tuple[str, ...] = (
    "insiderone.com/careers",
    "useinsider.com/careers",
)

# ---------------------------------------------------------------------------
# Browser / timing
# ---------------------------------------------------------------------------
DEFAULT_TIMEOUT: int = 60_000          # ms — global Playwright timeout
NAVIGATION_TIMEOUT: int = 90_000       # ms — page navigations can be slow on CI
NETWORK_IDLE_TIMEOUT: int = 15_000     # ms — wait for network after interactions

# headless=false by default so you can watch tests run locally;
# set HEADLESS=true in CI via the env var.
HEADLESS: bool = os.getenv("HEADLESS", "false").lower() == "true"
SLOW_MO: int = int(os.getenv("SLOW_MO", "0"))

# ---------------------------------------------------------------------------
# Expected content — change here, nowhere else
# ---------------------------------------------------------------------------
EXPECTED_HOME_TITLE_FRAGMENT: str = "Insider"
EXPECTED_CAREERS_HEADING: str = "Find your calling"

# Careers filter
QA_DEPARTMENT: str = "Quality Assurance"
EXPECTED_LOCATION: str = "Istanbul, Turkey"

# Apply flow
EXPECTED_APPLY_URL_FRAGMENT: str = "lever.co"
