"""
Root conftest.py — re-exports everything from fixtures/conftest.py.

pytest discovers conftest.py files bottom-up from the test file location.
Having this at the root ensures fixtures are available to all test modules.
"""

from fixtures.conftest import (  # noqa: F401  (re-export for pytest discovery)
    ensure_report_dirs,
    context_with_tracing,
    home_page,
    careers_page,
    jobs_page,
    pytest_runtest_makereport,
)
