"""
Root conftest.py — Fixture wiring layer

Provides core fixtures: env, app_config, browser_instance, page.
Hooks pytest failure callback for automatic screenshot capture.

Every test receives what it declares — no setup code needed in test files.
"""

import pytest
from playwright.sync_api import sync_playwright

from config.config_loader import ConfigLoader
from utils.logger import get_logger
from utils.screenshot_helper import capture_on_failure

logger = get_logger(__name__)


# ── CLI Options ───────────────────────────────────────────────────────────────

def pytest_addoption(parser):
    """Register custom CLI flags."""
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Target environment (dev, uat, prod). Loads config/environments/<env>.yaml"
    )
    parser.addoption(
        "--slowmo",
        action="store",
        default=0,
        type=int,
        help="Slow down each Playwright action by this many ms (demo mode)"
    )


# ── Session-Scope Fixtures ────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def env(request):
    """Returns the environment name passed via --env flag."""
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def app_config(env):
    """
    Loads and returns the environment configuration dict.
    Resolves ${ENV_VAR} references from .env automatically.
    """
    config = ConfigLoader()
    loaded = config.load(env)
    logger.info(f"Framework initialised — environment: {env.upper()}")
    logger.info(f"Base URL: {loaded.get('base_url')}")
    return loaded


@pytest.fixture(scope="session")
def browser_instance(request, app_config):
    """
    Launches a browser once per session.
    Uses system Edge (channel='msedge') for better corporate network compatibility.
    """
    with sync_playwright() as p:
        headed = request.config.getoption("--headed", default=False)
        slowmo = request.config.getoption("--slowmo", default=0)
        headless = not headed if headed else app_config.get("headless", True)

        browser = p.chromium.launch(
            channel="msedge",
            headless=headless,
            slow_mo=slowmo
        )
        logger.info(
            f"Browser launched — Microsoft Edge | "
            f"headless: {headless} | slowmo: {slowmo}ms"
        )
        yield browser
        browser.close()
        logger.info("Browser closed")


# ── Function-Scope Fixtures ───────────────────────────────────────────────────

@pytest.fixture(scope="function")
def page(browser_instance, app_config):
    """
    Fresh browser context + page per test.
    Ensures test isolation — no state leaks between tests.
    """
    context = browser_instance.new_context(
        base_url=app_config.get("base_url"),
        viewport={"width": 1920, "height": 1080}
    )
    page = context.new_page()
    yield page
    context.close()


# ── Failure Hook ──────────────────────────────────────────────────────────────

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Runs after each test phase. Captures screenshot on failure
    and attaches to Allure report automatically.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            capture_on_failure(page, item.name)
