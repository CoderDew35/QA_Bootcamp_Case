# Insider One — QA Automation Framework

> Production-grade end-to-end test automation for [insiderone.com](https://insiderone.com)  
> Built with **Python · Playwright · Pytest** following DRY, SOLID, and YAGNI principles.

---

## Table of Contents

- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Test Scenarios](#test-scenarios)
- [Getting Started](#getting-started)
- [Running Tests](#running-tests)
- [Configuration](#configuration)
- [Reports & Evidence](#reports--evidence)
- [CI/CD](#cicd)
- [Design Principles](#design-principles)

---

## Architecture

The framework is built on the **Page Object Model (POM)** pattern:

```
Test Functions  →  Page Objects  →  Playwright API  →  Browser
     ↓                  ↓
  Assertions       Actions / Locators
     ↓
  utils/config.py  (single source of truth for all URLs, strings, timeouts)
```

**Key rule:** Page objects never assert. Assertions live exclusively in test functions.

---

## Project Structure

```
qabootcampscase/
│
├── tests/                     # Test modules (one file per scenario)
│   ├── test_homepage.py       # Scenario 1 — Homepage validation
│   ├── test_careers.py        # Scenario 2 — Careers flow + QA filter
│   └── test_apply_flow.py     # Scenario 3 — Apply → Lever redirect
│
├── pages/                     # Page Object Model layer
│   ├── base_page.py           # Abstract base: shared state & cookie dismissal
│   ├── home_page.py           # insiderone.com homepage
│   ├── careers_page.py        # /careers/ — navigation, filter, job list
│   └── jobs_page.py           # lever.co application page
│
├── utils/
│   ├── config.py              # ⭐ Single source of truth (URLs, timeouts, strings)
│   ├── logger.py              # get_logger(name) factory — no print() anywhere
│   └── helpers.py             # Pure utility functions (network wait, assertions)
│
├── fixtures/
│   └── conftest.py            # Pytest fixtures, screenshot-on-failure hook
│
├── conftest.py                # Root re-export so pytest discovers all fixtures
│
├── reports/                   # Generated at runtime (gitignored)
│   ├── report.html            # Self-contained HTML report
│   ├── screenshots/           # Auto-captured on test failure
│   └── traces/                # Playwright trace zips on failure
│
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions — runs on every PR to main
│
├── .env.example               # Environment variable template
├── pyproject.toml             # Dependencies + pytest config
└── uv.lock                    # Locked dependency versions
```

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| [Playwright](https://playwright.dev/python/) | Browser automation |
| [Pytest](https://pytest.org) | Test runner |
| [pytest-playwright](https://pypi.org/project/pytest-playwright/) | Playwright fixtures for pytest |
| [pytest-html](https://pypi.org/project/pytest-html/) | Self-contained HTML reports |
| [pytest-rerunfailures](https://pypi.org/project/pytest-rerunfailures/) | Retry flaky tests |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | `.env` config loading |
| [uv](https://github.com/astral-sh/uv) | Fast Python package manager |

---

## Test Scenarios

### ✅ Scenario 1 — Homepage Validation (`test_homepage.py`)
| Test | Marker | What it checks |
|------|--------|---------------|
| `test_homepage_loads` | `smoke` | Page title contains "Insider" |
| `test_homepage_key_sections_visible` | `smoke` | Header, nav, footer are visible |

### ✅ Scenario 2 — Careers Flow (`test_careers.py`)
| Test | Marker | What it checks |
|------|--------|---------------|
| `test_careers_page_loads` | `smoke` | Careers URL is reachable |
| `test_see_all_teams_button_is_visible` | `smoke` | "See all teams" button present |
| `test_qa_jobs_filter` | `regression` | Filter → QA; each job has correct dept + Istanbul location |

### ✅ Scenario 3 — Apply Flow (`test_apply_flow.py`)
| Test | Marker | What it checks |
|------|--------|---------------|
| `test_apply_redirects_to_lever` | `e2e` | Click Apply → new tab → `lever.co` URL + form visible |

> **Edge case handled:** When 0 QA positions are listed, `test_qa_jobs_filter` fails with a clear descriptive message (not silent). `test_apply_redirects_to_lever` is skipped gracefully with an informative reason.

---

## Getting Started

### Prerequisites
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) — install with `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Installation

```bash
# 1. Clone the repo
git clone <repo-url>
cd qabootcampscase

# 2. Install all dependencies (including dev)
uv sync --all-groups

# 3. Install Chromium browser
uv run playwright install chromium

# 4. Copy env template (optional — defaults work out of the box)
cp .env.example .env
```

---

## Running Tests

```bash
# Run all tests (headed — browser window visible)
uv run pytest -v

# Run only smoke tests (fast, critical path)
uv run pytest -v -m smoke

# Run only regression suite
uv run pytest -v -m regression

# Run only e2e tests
uv run pytest -v -m e2e

# Run headless (no browser window)
uv run pytest -v --headless

# Run with HTML report
uv run pytest -v --html=reports/report.html --self-contained-html

# Run a specific test file
uv run pytest tests/test_careers.py -v

# Run a specific test by name
uv run pytest -v -k "test_qa_jobs_filter"
```

---

## Configuration

All configurable values live in **`utils/config.py`** — never hard-coded in tests or page objects.

| Variable | Default | Description |
|----------|---------|-------------|
| `BASE_URL` | `https://insiderone.com` | Target site root URL |
| `DEFAULT_TIMEOUT` | `60000` ms | Global Playwright element timeout |
| `NAVIGATION_TIMEOUT` | `90000` ms | Page navigation timeout |
| `NETWORK_IDLE_TIMEOUT` | `15000` ms | Post-action network idle wait |
| `QA_DEPARTMENT` | `"Quality Assurance"` | Department filter text |
| `EXPECTED_LOCATION` | `"Istanbul, Turkey"` | Expected job location |

Override any value via `.env`:

```bash
# .env
BASE_URL=https://insiderone.com
HEADLESS=false
SLOW_MO=100
```

---

## Reports & Evidence

After each run, artifacts are saved to `reports/` (gitignored):

| Artifact | Location | Generated |
|----------|----------|-----------|
| HTML report | `reports/report.html` | Every run |
| Failure screenshots | `reports/screenshots/<test_name>.png` | On failure |
| Playwright traces | `reports/traces/<test_name>.zip` | On failure |

Open the HTML report locally:
```bash
open reports/report.html
```

View a Playwright trace:
```bash
uv run playwright show-trace reports/traces/<test_name>.zip
```

---

## CI/CD

**Trigger:** Every pull request to `main`.

**Pipeline steps:**
1. Checkout → Python 3.10 → Install uv
2. `uv sync --all-groups` — install all deps
3. `playwright install --with-deps chromium`
4. `pytest --headless` — run full suite
5. Upload `reports/` as a GitHub Actions artifact (14-day retention)

The report is downloadable from the **Actions** tab after each run.

---

## Design Principles

### DRY — Don't Repeat Yourself
- All URLs, expected strings, and timeouts defined **once** in `utils/config.py`
- Cookie dismissal logic lives **once** in `BasePage` — not duplicated per page
- Screenshot-on-failure hook is **one** `pytest_runtest_makereport` in `conftest.py`

### SOLID
| Principle | Applied |
|-----------|---------|
| **S**ingle Responsibility | Page objects only hold locators + actions. Tests own assertions. |
| **O**pen/Closed | Add a new page = new file inheriting `BasePage`. Zero changes to existing code. |
| **D**ependency Inversion | Tests receive page objects via pytest fixtures — no `new` calls in test code. |

### YAGNI — You Aren't Gonna Need It
- No OpenAI/AI layer (not needed to validate the 3 test scenarios)
- No Allure server (pytest-html generates a fully self-contained report)
- No video recording (traces + screenshots cover failure analysis)
- No parallel execution config (can be added with `pytest-xdist` when scale demands it)

---

## Test Markers Reference

```bash
@pytest.mark.smoke       # Fast, critical-path checks — run on every commit
@pytest.mark.regression  # Full business logic validation
@pytest.mark.e2e         # Cross-page flows, new-tab interactions
```

---

## Author

| | |
|---|---|
| **Name** | Şebnem KÖŞKER |
| **Email** | [sebnemkosker3500@gmail.com](mailto:sebnemkosker3500@gmail.com) |

---

<p align="center">Made with ❤️ for the Insider One QA Bootcamp</p>
