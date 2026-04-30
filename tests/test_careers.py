"""
test_careers.py — Scenario 2: Careers Flow

Tests:
    - Careers page loads correctly
    - 'See all teams' button is present and clickable
    - QA department filter works; every visible job meets location/dept criteria

Edge case:
    When 0 QA positions are currently open, test_qa_jobs_filter is marked
    xfail (expected failure) with an informative reason, instead of silently
    passing with an empty loop. This surfaces the data-gap clearly in reports
    while not blocking CI on a zero-jobs state.
"""

import pytest
from pages.careers_page import CareersPage
from utils import config
from utils.helpers import assert_jobs_list_not_empty, normalize_whitespace


@pytest.mark.smoke
def test_careers_page_loads(careers_page: CareersPage) -> None:
    """Careers page must load and the main URL must be reachable (either domain)."""
    careers_page.navigate()

    current_url = careers_page.page.url
    assert any(fragment in current_url for fragment in config.CAREERS_URL_FRAGMENTS), (
        f"Expected URL to contain one of {config.CAREERS_URL_FRAGMENTS}, got: '{current_url}'"
    )


@pytest.mark.smoke
def test_see_all_teams_button_is_visible(careers_page: CareersPage) -> None:
    """'See all teams' button must be present on the open-roles section."""
    careers_page.go_to_open_roles()

    assert careers_page.see_all_teams_button.is_visible(), (
        "'See all teams' button is not visible on the careers open-roles section."
    )


@pytest.mark.regression
def test_qa_jobs_filter(careers_page: CareersPage) -> None:
    """
    After filtering by Quality Assurance, every listed job must:
      - Mention 'Quality Assurance' in its text content
      - Show location 'Istanbul, Turkey'

    Edge case: if 0 positions exist, the assertion in assert_jobs_list_not_empty
    fails explicitly with a descriptive message rather than passing silently.
    """
    careers_page.go_to_open_roles()
    careers_page.click_see_all_teams()
    careers_page.filter_by_department(config.QA_DEPARTMENT)

    jobs = careers_page.get_job_items()

    # --- Edge case guard ---
    assert_jobs_list_not_empty(jobs, config.QA_DEPARTMENT)

    for job in jobs:
        text = normalize_whitespace(job.inner_text())
        assert config.QA_DEPARTMENT in text, (
            f"Job item does not contain '{config.QA_DEPARTMENT}'.\nFull text: {text}"
        )
        assert config.EXPECTED_LOCATION in text, (
            f"Job item does not contain location '{config.EXPECTED_LOCATION}'.\nFull text: {text}"
        )
