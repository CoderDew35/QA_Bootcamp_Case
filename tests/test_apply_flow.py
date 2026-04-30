"""
test_apply_flow.py — Scenario 3: Apply Flow

Tests:
    - Clicking 'Apply Now' on a QA job opens the Lever application page
    - The Lever URL fragment is present
    - An application form is visible on the redirected page

Dependency: requires at least one QA job to exist. The test is skipped
(pytest.mark.skipif style via dynamic skip) when the jobs list is empty,
with a clear reason that distinguishes a data gap from a real bug.
"""

import pytest
from playwright.sync_api import expect
from pages.careers_page import CareersPage
from pages.jobs_page import JobsPage
from utils import config
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.e2e
def test_apply_redirects_to_lever(careers_page: CareersPage) -> None:
    """
    Clicking 'Apply Now' must redirect to a lever.co URL and show a form.

    Skip gracefully when no QA positions are currently listed so CI stays
    green while clearly surfacing the skip reason in the report.
    """
    careers_page.go_to_open_roles()
    careers_page.click_see_all_teams()
    careers_page.filter_by_department(config.QA_DEPARTMENT)

    jobs = careers_page.get_job_items()

    if not jobs:
        pytest.skip(
            f"Skipping apply flow test: no open '{config.QA_DEPARTMENT}' positions found. "
            "Re-run when positions are available."
        )

    # Hover to reveal the Apply Now button (some sites show it on hover)
    jobs[0].hover()

    apply_btn = careers_page.get_first_apply_button()

    # Lever opens in a new tab — capture that new page
    with careers_page.page.context.expect_page() as new_page_info:
        apply_btn.click()

    lever_page = new_page_info.value
    lever_page.wait_for_load_state("domcontentloaded")

    # --- Assertions (test's responsibility, not the page object's) ---
    current_url = lever_page.url
    assert config.EXPECTED_APPLY_URL_FRAGMENT in current_url, (
        f"Expected URL to contain '{config.EXPECTED_APPLY_URL_FRAGMENT}', got: '{current_url}'"
    )

    jobs_page = JobsPage(lever_page)
    jobs_page.wait_for_load()

    assert jobs_page.apply_form.is_visible(), (
        f"Application form is not visible on the Lever page: {current_url}"
    )

    logger.info("Apply flow verified successfully. Lever URL: %s", current_url)
