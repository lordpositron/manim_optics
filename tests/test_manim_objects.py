"""
Tests for Manim-backed optical objects.

These tests require Manim (and its system dependencies: Cairo, LaTeX, etc.)
to be installed. They are skipped automatically in environments where Manim
is unavailable (e.g. minimal CI images).

Run locally with:
    pip install -e ".[dev]"
    pytest tests/test_manim_objects.py -v
"""

import numpy as np
import pytest

manim = pytest.importorskip("manim", reason="Manim not installed")


from manim_optics import (  # noqa: E402
    ConvergingLens,
    DivergingLens,
    ThinLens,
    PlaneMirror,
    rotate_vector_2d,
    calculate_image_position,
)


# ---------------------------------------------------------------------------
# rotate_vector_2d — import from package (manim-backed module)
# ---------------------------------------------------------------------------


class TestRotateVector2DFromPackage:
    def test_matches_manual_rotation(self):
        import math

        v = np.array([1.0, 0.0, 0.0])
        result = rotate_vector_2d(v, math.pi / 2)
        np.testing.assert_allclose(result, [0.0, 1.0, 0.0], atol=1e-10)


# ---------------------------------------------------------------------------
# calculate_image_position — import from package
# ---------------------------------------------------------------------------


class TestCalculateImagePositionFromPackage:
    def test_object_at_2f(self):
        image_dist, mag, is_real = calculate_image_position(4.0, 2.0)
        assert image_dist == pytest.approx(4.0)
        assert mag == pytest.approx(-1.0)
        assert is_real is True


# ---------------------------------------------------------------------------
# ConvergingLens
# ---------------------------------------------------------------------------


class TestConvergingLens:
    def test_instantiation(self):
        lens = ConvergingLens(focal_length=2.0)
        assert lens.focal_length == pytest.approx(2.0)

    def test_negative_focal_length_raises(self):
        with pytest.raises(ValueError, match="positive"):
            ConvergingLens(focal_length=-1.0)

    def test_zero_focal_length_raises(self):
        with pytest.raises(ValueError):
            ConvergingLens(focal_length=0.0)

    def test_transfer_matrix_shape(self):
        lens = ConvergingLens(focal_length=2.0)
        M = lens.get_transfer_matrix()
        assert M.shape == (2, 2)

    def test_transfer_matrix_determinant(self):
        lens = ConvergingLens(focal_length=3.0)
        M = lens.get_transfer_matrix()
        assert np.linalg.det(M) == pytest.approx(1.0, abs=1e-10)

    def test_set_focal_length(self):
        lens = ConvergingLens(focal_length=2.0)
        lens.set_focal_length(5.0)
        assert lens.focal_length == pytest.approx(5.0)
        assert lens.focal_length_tracker.get_value() == pytest.approx(5.0)

    def test_is_not_mirror(self):
        lens = ConvergingLens(focal_length=2.0)
        assert lens.is_mirror() is False


# ---------------------------------------------------------------------------
# DivergingLens
# ---------------------------------------------------------------------------


class TestDivergingLens:
    def test_instantiation(self):
        lens = DivergingLens(focal_length=-2.0)
        assert lens.focal_length == pytest.approx(-2.0)

    def test_positive_focal_length_raises(self):
        with pytest.raises(ValueError, match="negative"):
            DivergingLens(focal_length=1.0)

    def test_transfer_matrix_diverges_rays(self):
        """C = -1/f > 0 for a diverging lens (f < 0)."""
        lens = DivergingLens(focal_length=-2.0)
        M = lens.get_transfer_matrix()
        assert M[1, 0] > 0  # C = -1/f > 0 when f < 0

    def test_transfer_matrix_determinant(self):
        lens = DivergingLens(focal_length=-3.0)
        M = lens.get_transfer_matrix()
        assert np.linalg.det(M) == pytest.approx(1.0, abs=1e-10)


# ---------------------------------------------------------------------------
# PlaneMirror
# ---------------------------------------------------------------------------


class TestPlaneMirror:
    def test_is_mirror(self):
        mirror = PlaneMirror()
        assert mirror.is_mirror() is True

    def test_transfer_matrix(self):
        mirror = PlaneMirror()
        M = mirror.get_transfer_matrix()
        expected = np.array([[1.0, 0.0], [0.0, -1.0]])
        np.testing.assert_allclose(M, expected, atol=1e-10)

    def test_reflection_horizontal_ray(self):
        """A horizontal ray hitting a vertical mirror reflects back horizontally."""
        mirror = PlaneMirror()
        ray_dir = np.array([1.0, 0.0, 0.0])
        intersection = np.array([0.0, 0.0, 0.0])
        new_dir, continues = mirror.propagate_ray(
            np.array([-1.0, 0.0, 0.0]), ray_dir, intersection
        )
        assert continues is True
        # Reflected direction should be [-1, 0, 0]
        np.testing.assert_allclose(np.abs(new_dir[0]), 1.0, atol=1e-6)
        np.testing.assert_allclose(new_dir[1], 0.0, atol=1e-6)

    def test_refractive_index_inversion(self):
        """Mirror models path reversal as n_after = -n_before."""
        mirror = PlaneMirror(refractive_index=1.5)
        assert mirror.n_before == pytest.approx(1.5)
        assert mirror.n_after == pytest.approx(-1.5)
