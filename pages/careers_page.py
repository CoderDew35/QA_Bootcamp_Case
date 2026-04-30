"""
CareersPage — page object for https://insiderone.com/careers/

Responsibilities:
- Navigate to the careers page and the open-roles anchor
- Expose actions: see-all-teams, department filter
- Return raw job item locators — no assertions, no data extraction
"""

from playwright.sync_api import Locator, Page
from pages.base_page import BasePage
from utils import config
from utils.helpers import wait_for_network_idle


class CareersPage(BasePage):

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def navigate(self) -> None:
        self.logger.info("Navigating to careers page: %s", config.CAREERS_URL)
        self.page.goto(config.CAREERS_URL, wait_until="domcontentloaded",
                       timeout=config.NAVIGATION_TIMEOUT)
        wait_for_network_idle(self.page)
        self.dismiss_cookies()

    def go_to_open_roles(self) -> None:
        """Navigate directly to the #open-roles section."""
        self.logger.info("Going to open roles anchor.")
        self.page.goto(config.CAREERS_OPEN_ROLES_URL, wait_until="domcontentloaded",
                       timeout=config.NAVIGATION_TIMEOUT)
        wait_for_network_idle(self.page)
        self.dismiss_cookies()

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def click_see_all_teams(self) -> None:
        """Click the 'See all teams' button and wait for all team cards to render."""
        self.logger.info("Clicking 'See all teams'.")
        btn = self.page.locator("a:has-text('See all teams'), span:has-text('See all teams')")
        btn.first.scroll_into_view_if_needed()
        # Count visible cards before clicking so we can assert more appeared
        before_count = self.page.locator("[class*='career-position'], .career-position, section h3, h3").count()
        btn.first.click()
        # Wait for at least one new element to become visible; use a broad but
        # safe selector — the 'See Less' link only appears after expansion
        try:
            self.page.wait_for_selector(
                "a:has-text('See Less'), a:has-text('Quality Assurance')",
                timeout=config.DEFAULT_TIMEOUT,
            )
        except Exception:
            self.logger.warning("Expansion confirmation selector not found — continuing anyway.")

    def filter_by_department(self, department: str) -> None:
        """
        Click the Open Positions link inside the matching department card.

        The careers page shows team cards; each has a heading and a link
        to open positions. We locate the team card by its heading text,
        then click its 'Open Positions' / 'N Open Positions' link.

        Args:
            department: Department card heading text (e.g. 'Quality Assurance').
        """
        self.logger.info("Filtering jobs by department: '%s'", department)

        # Find the section/card whose h3 heading exactly matches the department,
        # then click the first link inside it (the 'Open Positions' link)
        section = self.page.locator(
            f"h3:has-text('{department}'), h4:has-text('{department}'), "
            f"[class*='career'] :has-text('{department}')"
        ).first
        section.scroll_into_view_if_needed()

        # Navigate up to the card container and click its anchor
        card_link = section.locator("..").locator("a").first
        if not card_link.is_visible(timeout=3_000):
            # Fallback: find the link nearest to the heading by going up two levels
            card_link = section.locator("..").locator("..").locator("a").first

        card_link.click()
        wait_for_network_idle(self.page)

    # ------------------------------------------------------------------
    # Locators / data access
    # ------------------------------------------------------------------

    @property
    def page_heading(self) -> Locator:
        return self.page.locator("h1, h2").first

    @property
    def see_all_teams_button(self) -> Locator:
        return self.page.locator("a:has-text('See all teams'), span:has-text('See all teams')").first

    def get_job_items(self) -> list[Locator]:
        """
        Return all visible job listing items after a filter has been applied.

        Returns an empty list when no positions are open — callers decide
        whether this is an error (see helpers.assert_jobs_list_not_empty).
        """
        items = self.page.locator(".position-list-item")
        count = items.count()
        self.logger.info("Found %d job item(s) in current view.", count)
        return [items.nth(i) for i in range(count)]

    def get_first_apply_button(self) -> Locator:
        """Return the 'Apply Now' button on the first visible job card."""
        return self.page.locator(".position-list-item a:has-text('Apply Now')").first
