"""
screenshot_helper.py — Auto-capture on test failure.

Wired to pytest_runtest_makereport hook in root conftest.py.
No test needs to call this directly — it fires automatically on failure.
"""

from datetime import datetime
from pathlib import Path

from config.settings import SCREENSHOTS_DIR
from utils.allure_helper import attach_screenshot
from utils.logger import get_logger

logger = get_logger(__name__)


def capture_screenshot(page, name: str) -> Path:
    """
    Captures a full-page screenshot and saves to disk.
    Also attaches the screenshot to the active Allure step.

    Args:
        page: Playwright Page instance
        name: Base name for the screenshot file

    Returns:
        Absolute path to the saved screenshot
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    filepath = SCREENSHOTS_DIR / filename

    try:
        image_bytes = page.screenshot(full_page=True)
        filepath.write_bytes(image_bytes)
        attach_screenshot(name=filename, image_bytes=image_bytes)
        logger.info(f"Screenshot captured: {filename}")
        return filepath
    except Exception as e:
        logger.error(f"Screenshot capture failed: {e}")
        return None


def capture_on_failure(page, test_name: str) -> None:
    """
    Called by the pytest failure hook.
    Prefixes screenshot name with FAILED_ for easy identification.
    """
    logger.error(f"Test failed: {test_name} — capturing failure screenshot")
    capture_screenshot(page, f"FAILED_{test_name}")
