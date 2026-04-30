"""
JobsPage — page object for the Lever application page.

After clicking 'Apply Now' the browser may open a new tab/window pointing
to lever.co. This page object handles the new context, not the careers page.

Responsibilities:
- Wait for the Lever page to fully load
- Expose the application form locator for assertion in tests
"""

from playwright.sync_api import Locator, Page
from pages.base_page import BasePage


class JobsPage(BasePage):

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def wait_for_load(self) -> None:
        """Wait for the Lever application page to reach a usable state."""
        self.logger.info("Waiting for Lever job page to load.")
        self.page.wait_for_load_state("domcontentloaded")

    # ------------------------------------------------------------------
    # Locators
    # ------------------------------------------------------------------

    @property
    def apply_form(self) -> Locator:
        """The main application form on the Lever page."""
        return self.page.locator("form#application-form, form[data-qa='application-form'], form")

    @property
    def page_title_heading(self) -> Locator:
        return self.page.locator("h1, h2").first
