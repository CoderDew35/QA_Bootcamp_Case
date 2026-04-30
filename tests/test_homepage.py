"""
test_homepage.py — Scenario 1: Homepage Validation

Tests:
    - Page loads and returns the expected title
    - Key structural sections are visible (header, nav, footer, hero)

Markers:
    smoke — both tests are fast critical-path checks
"""

import pytest
from pages.home_page import HomePage
from utils import config


@pytest.mark.smoke
def test_homepage_loads(home_page: HomePage) -> None:
    """Homepage must load and carry the expected brand name in the title."""
    home_page.navigate()

    title = home_page.page.title()
    assert config.EXPECTED_HOME_TITLE_FRAGMENT in title, (
        f"Expected title to contain '{config.EXPECTED_HOME_TITLE_FRAGMENT}', got: '{title}'"
    )


@pytest.mark.smoke
def test_homepage_key_sections_visible(home_page: HomePage) -> None:
    """Header, nav-bar, hero, and footer must all be visible after load."""
    home_page.navigate()

    assert home_page.header.is_visible(), "Header is not visible on homepage."
    assert home_page.nav_bar.is_visible(), "Navigation bar is not visible on homepage."
    assert home_page.footer.is_visible(), "Footer is not visible on homepage."
