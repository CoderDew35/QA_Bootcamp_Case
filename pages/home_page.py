"""
HomePage — page object for https://useinsider.com/

Responsibilities:
- Navigate to the homepage
- Expose locators for key visible sections
"""

from playwright.sync_api import Locator
from playwright.sync_api import Page
from pages.base_page import BasePage
from utils import config


class HomePage(BasePage):

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def navigate(self) -> None:
        self.logger.info("Navigating to homepage: %s", config.BASE_URL)
        self.page.goto(config.BASE_URL, wait_until="domcontentloaded",
                       timeout=config.NAVIGATION_TIMEOUT)
        self.dismiss_cookies()

    # ------------------------------------------------------------------
    # Locators — one property per visible section (no assertions here)
    # ------------------------------------------------------------------

    @property
    def hero_section(self) -> Locator:
        """The above-the-fold hero / banner area."""
        return self.page.locator("#hero-section, .hero-section, [class*='hero']").first

    @property
    def header(self) -> Locator:
        """Top-level site header."""
        return self.page.locator("header, #navigation").first

    @property
    def nav_company_link(self) -> Locator:
        """'Company' nav item used to verify navigation is interactive."""
        return self.page.locator("a[href*='/about'], a:has-text('Company')").first
