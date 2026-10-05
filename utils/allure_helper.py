"""
allure_helper.py — Allure reporting utilities.

Provides @step decorator and attachment helpers.
Every workflow/page method decorated with @step appears as a
collapsible, named step in the Allure report.
"""

import functools
import allure

from utils.logger import get_logger

logger = get_logger(__name__)


def step(title: str):
    """
    Decorator that wraps a method as a named Allure step.
    The title appears exactly as given in the report.

    Example:
        @step("Enter email address")
        def enter_email(self, email): ...
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"STEP → {title}")
            with allure.step(title):
                return func(*args, **kwargs)
        return wrapper
    return decorator


def attach_text(name: str, content: str) -> None:
    """Attach a plain text block to the current Allure step."""
    allure.attach(
        body=str(content),
        name=name,
        attachment_type=allure.attachment_type.TEXT
    )


def attach_json(name: str, content: str) -> None:
    """Attach a JSON string to the current Allure step."""
    allure.attach(
        body=str(content),
        name=name,
        attachment_type=allure.attachment_type.JSON
    )


def attach_screenshot(name: str, image_bytes: bytes) -> None:
    """Attach a PNG screenshot to the current Allure step."""
    allure.attach(
        body=image_bytes,
        name=name,
        attachment_type=allure.attachment_type.PNG
    )


def set_test_metadata(
    feature: str = None,
    story: str = None,
    severity: str = None,
    description: str = None
) -> None:
    """
    Attach rich metadata to the current test.
    Call this inside a test if you prefer runtime assignment
    over decorator-based @allure.feature annotations.
    """
    if feature:
        allure.dynamic.feature(feature)
    if story:
        allure.dynamic.story(story)
    if severity:
        allure.dynamic.severity(severity)
    if description:
        allure.dynamic.description(description)
