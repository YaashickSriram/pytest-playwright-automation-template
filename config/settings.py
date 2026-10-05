"""
settings.py — Global paths and constants.

Establishes all filesystem paths relative to the project root.
No hardcoded absolute paths anywhere else in the framework.
"""

from pathlib import Path

# ── Core Paths ────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).parent.parent.resolve()

CONFIG_DIR       = PROJECT_ROOT / "config"
ENVIRONMENTS_DIR = CONFIG_DIR / "environments"

TESTS_DIR     = PROJECT_ROOT / "tests"
PAGES_DIR     = PROJECT_ROOT / "pages"
WORKFLOWS_DIR = PROJECT_ROOT / "workflows"
SERVICES_DIR  = PROJECT_ROOT / "services"
DATA_DIR      = PROJECT_ROOT / "data"
UTILS_DIR     = PROJECT_ROOT / "utils"

FIXTURES_DIR = DATA_DIR / "fixtures"

# ── Report Paths ──────────────────────────────────────────────────────────────

REPORTS_DIR         = PROJECT_ROOT / "reports"
ALLURE_RESULTS_DIR  = REPORTS_DIR / "allure-results"
ALLURE_REPORT_DIR   = REPORTS_DIR / "allure-report"
SCREENSHOTS_DIR     = REPORTS_DIR / "screenshots"
EXECUTION_LOG       = REPORTS_DIR / "execution.log"

# ── Environment Files ─────────────────────────────────────────────────────────

ENV_FILE = PROJECT_ROOT / ".env"

# ── Defaults ──────────────────────────────────────────────────────────────────

DEFAULT_TIMEOUT_MS = 10000
DEFAULT_RETRY_COUNT = 1

# Ensure runtime directories exist
for d in [REPORTS_DIR, ALLURE_RESULTS_DIR, SCREENSHOTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)
