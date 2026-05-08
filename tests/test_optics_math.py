"""
Pure-math tests — no Manim dependency.

These tests validate the optical formulas directly, independently of
any Manim rendering or display context.
"""

import math

import numpy as np
import pytest


# ---------------------------------------------------------------------------
# Helpers — extract pure functions without triggering `from manim import *`
# ---------------------------------------------------------------------------


def _rotate_vector_2d(vector: np.ndarray, angle: float) -> np.ndarray:
    """Inline copy of base.rotate_vector_2d to avoid importing Manim."""
    cos_a = np.cos(angle)
    sin_a = np.sin(angle)
    x, y = vector[0], vector[1]
    return np.array([x * cos_a - y * sin_a, x * sin_a + y * cos_a, vector[2]])


def _calculate_image_position(object_distance: float, focal_length: float):
    """Inline copy of scene_utils.calculate_image_position."""
    if abs(object_distance) < 1e-6:
        return float("inf"), float("inf"), True
    try:
        image_distance = 1 / (1 / focal_length - 1 / object_distance)
    except ZeroDivisionError:
        return float("inf"), float("inf"), True
    magnification = -image_distance / object_distance
    is_real = image_distance > 0
    return image_distance, magnification, is_real


def _thin_lens_transfer_matrix(focal_length: float) -> np.ndarray:
    """ABCD matrix for a thin lens: [[1, 0], [-1/f, 1]]."""
    return np.array([[1.0, 0.0], [-1.0 / focal_length, 1.0]])


# ---------------------------------------------------------------------------
# rotate_vector_2d
# ---------------------------------------------------------------------------


class TestRotateVector2D:
    def test_zero_rotation(self):
        v = np.array([1.0, 0.0, 0.0])
        result = _rotate_vector_2d(v, 0.0)
        np.testing.assert_allclose(result, v, atol=1e-10)

    def test_90_degrees(self):
        v = np.array([1.0, 0.0, 0.0])
        result = _rotate_vector_2d(v, math.pi / 2)
        np.testing.assert_allclose(result, [0.0, 1.0, 0.0], atol=1e-10)

    def test_180_degrees(self):
        v = np.array([1.0, 0.0, 0.0])
        result = _rotate_vector_2d(v, math.pi)
        np.testing.assert_allclose(result, [-1.0, 0.0, 0.0], atol=1e-10)

    def test_360_degrees_identity(self):
        v = np.array([3.0, 4.0, 0.0])
        result = _rotate_vector_2d(v, 2 * math.pi)
        np.testing.assert_allclose(result, v, atol=1e-10)

    def test_preserves_z(self):
        v = np.array([1.0, 0.0, 7.0])
        result = _rotate_vector_2d(v, math.pi / 4)
        assert result[2] == pytest.approx(7.0)

    def test_preserves_norm(self):
        v = np.array([3.0, 4.0, 0.0])
        result = _rotate_vector_2d(v, 1.23)
        np.testing.assert_allclose(
            np.linalg.norm(result[:2]), np.linalg.norm(v[:2]), atol=1e-10
        )


# ---------------------------------------------------------------------------
# calculate_image_position — thin lens equation  1/f = 1/p + 1/p'
# ---------------------------------------------------------------------------


class TestCalculateImagePosition:
    def test_object_at_2f_real_inverted(self):
        """Object at 2f → image at 2f, magnification -1."""
        f = 2.0
        p = 4.0  # 2f
        image_dist, mag, is_real = _calculate_image_position(p, f)
        assert image_dist == pytest.approx(4.0, rel=1e-6)
        assert mag == pytest.approx(-1.0, rel=1e-6)
        assert is_real is True

    def test_object_at_3f(self):
        """Object at 3f → image at 3f/2."""
        f = 2.0
        p = 6.0  # 3f
        image_dist, mag, is_real = _calculate_image_position(p, f)
        # 1/p' = 1/f - 1/p = 0.5 - 1/6 = 1/3  → p' = 3
        assert image_dist == pytest.approx(3.0, rel=1e-6)
        assert is_real is True

    def test_diverging_lens_virtual_image(self):
        """Diverging lens always produces a virtual image."""
        f = -2.0
        p = 3.0
        image_dist, mag, is_real = _calculate_image_position(p, f)
        assert is_real is False
        assert image_dist < 0

    def test_object_at_focal_point_returns_infinity(self):
        """Object at focal point → image at infinity."""
        f = 2.0
        p = f
        image_dist, mag, is_real = _calculate_image_position(p, f)
        assert math.isinf(image_dist)

    def test_zero_object_distance_returns_infinity(self):
        image_dist, mag, is_real = _calculate_image_position(0.0, 2.0)
        assert math.isinf(image_dist)

    def test_magnification_sign_inverted_for_real_image(self):
        """Real images beyond 2f are inverted (negative magnification)."""
        _, mag, is_real = _calculate_image_position(3.0, 2.0)
        assert is_real is True
        assert mag < 0

    def test_virtual_image_magnification_positive(self):
        """Virtual images (object inside f) are upright (positive magnification)."""
        f = 2.0
        p = 1.0  # inside focal point
        _, mag, is_real = _calculate_image_position(p, f)
        assert is_real is False
        assert mag > 0


# ---------------------------------------------------------------------------
# ABCD transfer matrix — thin lens
# ---------------------------------------------------------------------------


class TestThinLensTransferMatrix:
    def test_converging_matrix_shape(self):
        M = _thin_lens_transfer_matrix(2.0)
        assert M.shape == (2, 2)

    def test_converging_matrix_values(self):
        f = 2.0
        M = _thin_lens_transfer_matrix(f)
        expected = np.array([[1.0, 0.0], [-0.5, 1.0]])
        np.testing.assert_allclose(M, expected, atol=1e-10)

    def test_diverging_matrix_values(self):
        f = -3.0
        M = _thin_lens_transfer_matrix(f)
        expected = np.array([[1.0, 0.0], [1 / 3, 1.0]])
        np.testing.assert_allclose(M, expected, atol=1e-10)

    def test_unit_determinant(self):
        """ABCD matrix must have det = 1 (symplectic property)."""
        for f in [1.0, 2.0, -1.5, -3.0]:
            M = _thin_lens_transfer_matrix(f)
            assert np.linalg.det(M) == pytest.approx(1.0, abs=1e-10)

    def test_on_axis_ray_undeflected(self):
        """A ray on the axis (y=0) with no tilt exits unchanged."""
        M = _thin_lens_transfer_matrix(2.0)
        state_in = np.array([0.0, 0.0])
        state_out = M @ state_in
        np.testing.assert_allclose(state_out, [0.0, 0.0], atol=1e-10)

    def test_parallel_ray_focused_at_f(self):
        """A parallel ray (θ=0) at height y exits with angle -y/f, converging to f."""
        f = 2.0
        y = 1.0
        M = _thin_lens_transfer_matrix(f)
        state_in = np.array([y, 0.0])
        state_out = M @ state_in
        assert state_out[0] == pytest.approx(y)  # height unchanged
        assert state_out[1] == pytest.approx(-y / f)  # deflects toward axis


# ---------------------------------------------------------------------------
# Thin lens equation consistency check
# ---------------------------------------------------------------------------


class TestLensEquationConsistency:
    @pytest.mark.parametrize(
        "f,p",
        [
            (2.0, 3.0),
            (2.0, 4.0),
            (2.0, 10.0),
            (-2.0, 3.0),
            (5.0, 7.0),
        ],
    )
    def test_reciprocal_identity(self, f, p):
        """Verify 1/f = 1/p + 1/p' holds for each result."""
        image_dist, _, _ = _calculate_image_position(p, f)
        if not math.isinf(image_dist):
            reconstructed_f = 1 / (1 / p + 1 / image_dist)
            assert reconstructed_f == pytest.approx(f, rel=1e-6)
