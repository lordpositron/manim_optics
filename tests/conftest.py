"""
pytest configuration — shared fixtures and Manim availability check.
"""

import pytest


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "manim: mark test as requiring a live Manim environment",
    )


@pytest.fixture
def manim_available():
    """Skip test if Manim cannot be imported (e.g. headless CI without Cairo)."""
    pytest.importorskip(
        "manim", reason="Manim not installed — skipping Manim-dependent test"
    )
