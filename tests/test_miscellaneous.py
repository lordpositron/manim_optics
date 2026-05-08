"""
Tests for `manim_optics.miscellaneous` — Graticule classes for measurements.
"""

import numpy as np
import pytest

pytest.importorskip("manim", reason="Manim not installed")

from manim import RIGHT, UP  # noqa: E402

from manim_optics import (  # noqa: E402
    CrossGraticule,
    Graticule,
    GridGraticule,
    LinearGraticule,
)


# ---------------------------------------------------------------------------
# Graticule (base)
# ---------------------------------------------------------------------------


class TestGraticule:
    def test_construction_default(self):
        g = Graticule()
        assert g.length == pytest.approx(10.0)
        assert g.unit_length == pytest.approx(1.0)

    def test_custom_parameters_stored(self):
        g = Graticule(length=5.0, unit_length=0.5, primary_interval=2)
        assert g.length == pytest.approx(5.0)
        assert g.unit_length == pytest.approx(0.5)
        assert g.primary_interval == 2

    def test_show_main_line_default_false(self):
        g = Graticule()
        assert g.show_main_line is False


# ---------------------------------------------------------------------------
# LinearGraticule
# ---------------------------------------------------------------------------


class TestLinearGraticule:
    def test_construction_horizontal(self):
        g = LinearGraticule(direction=RIGHT, length=4.0)
        np.testing.assert_allclose(g.direction, RIGHT)
        # Has perpendicular vector
        assert hasattr(g, "perpendicular")

    def test_construction_vertical(self):
        g = LinearGraticule(direction=UP, length=4.0)
        np.testing.assert_allclose(g.direction, UP)

    def test_normalizes_direction(self):
        g = LinearGraticule(direction=np.array([3.0, 0.0, 0.0]))  # not normalized
        assert np.linalg.norm(g.direction) == pytest.approx(1.0, abs=1e-10)

    def test_axis_line_when_show_main_line(self):
        g = LinearGraticule(show_main_line=True)
        assert g.axis_line is not None

    def test_no_axis_line_when_hidden(self):
        g = LinearGraticule(show_main_line=False)
        assert g.axis_line is None

    def test_has_ticks(self):
        g = LinearGraticule(length=10.0, unit_length=1.0)
        # Ticks group should not be empty for a length-10 graticule
        assert len(g.ticks) > 0


# ---------------------------------------------------------------------------
# CrossGraticule
# ---------------------------------------------------------------------------


class TestCrossGraticule:
    def test_construction_default(self):
        g = CrossGraticule()
        assert g.x_length == pytest.approx(g.length)
        assert g.y_length == pytest.approx(g.length)

    def test_custom_axis_lengths(self):
        g = CrossGraticule(x_length=5.0, y_length=3.0)
        assert g.x_length == pytest.approx(5.0)
        assert g.y_length == pytest.approx(3.0)

    def test_two_axes_present(self):
        g = CrossGraticule()
        assert isinstance(g.x_axis, LinearGraticule)
        assert isinstance(g.y_axis, LinearGraticule)


# ---------------------------------------------------------------------------
# GridGraticule
# ---------------------------------------------------------------------------


class TestGridGraticule:
    def test_construction_default(self):
        g = GridGraticule()
        # Default uses base length for both width and height
        assert hasattr(g, "length")

    def test_construction_explicit_dimensions(self):
        g = GridGraticule(width=8.0, height=6.0)
        # Should not raise; dimensions stored
        assert g is not None
