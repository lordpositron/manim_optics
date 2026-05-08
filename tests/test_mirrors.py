"""
Tests for `manim_optics.mirrors` — Mirror, PlaneMirror, SphericalMirror.
"""

import numpy as np
import pytest

pytest.importorskip("manim", reason="Manim not installed")

from manim import LEFT, RIGHT  # noqa: E402

from manim_optics import Mirror, PlaneMirror, SphericalMirror  # noqa: E402

# ---------------------------------------------------------------------------
# PlaneMirror
# ---------------------------------------------------------------------------


class TestPlaneMirror:
    def test_is_mirror(self):
        mirror = PlaneMirror()
        assert mirror.is_mirror() is True

    def test_refractive_index_inversion(self):
        """Mirror models path reversal as n_after = -n_before."""
        mirror = PlaneMirror(refractive_index=1.5)
        assert mirror.n_before == pytest.approx(1.5)
        assert mirror.n_after == pytest.approx(-1.5)

    def test_transfer_matrix(self):
        mirror = PlaneMirror()
        M = mirror.get_transfer_matrix()
        np.testing.assert_allclose(M, np.array([[1.0, 0.0], [0.0, -1.0]]), atol=1e-10)

    def test_get_normal_at_returns_left(self):
        mirror = PlaneMirror()
        np.testing.assert_allclose(
            mirror.get_normal_at(np.array([0.0, 0.0, 0.0])), LEFT
        )

    def test_intersect_horizontal_ray(self):
        mirror = PlaneMirror(height=3.0)
        ray_start = np.array([-2.0, 0.5, 0.0])
        ray_dir = np.array([1.0, 0.0, 0.0])
        point, hit = mirror.intersect(ray_start, ray_dir)
        assert hit is True
        assert point[0] == pytest.approx(0.0, abs=1e-6)

    def test_intersect_outside_height(self):
        mirror = PlaneMirror(height=2.0)
        # Ray above mirror top (1.0)
        ray_start = np.array([-2.0, 1.5, 0.0])
        ray_dir = np.array([1.0, 0.0, 0.0])
        _, hit = mirror.intersect(ray_start, ray_dir)
        assert hit is False

    def test_normal_incidence_reflects_back(self):
        """A horizontal ray reflects to a horizontal ray going the other way."""
        mirror = PlaneMirror()
        ray_dir = np.array([1.0, 0.0, 0.0])
        intersection = np.array([0.0, 0.0, 0.0])
        new_dir, continues = mirror.propagate_ray(
            np.array([-1.0, 0.0, 0.0]), ray_dir, intersection
        )
        assert continues is True
        # Reflected ray has flipped x-component
        np.testing.assert_allclose(new_dir, [-1.0, 0.0, 0.0], atol=1e-6)

    def test_oblique_reflection_law(self):
        """Angle of incidence = angle of reflection."""
        mirror = PlaneMirror()
        # Ray coming in at 45° from upper-left
        ray_dir = np.array([1.0, -1.0, 0.0]) / np.sqrt(2)
        new_dir, _ = mirror.propagate_ray(
            np.array([-1.0, 1.0, 0.0]), ray_dir, np.array([0.0, 0.0, 0.0])
        )
        # Reflected ray: x-component flipped, y-component preserved
        expected = np.array([-1.0, -1.0, 0.0]) / np.sqrt(2)
        np.testing.assert_allclose(new_dir, expected, atol=1e-6)

    def test_propagated_direction_normalized(self):
        mirror = PlaneMirror()
        ray_dir = np.array([2.0, -1.0, 0.0])  # not normalized
        ray_dir = ray_dir / np.linalg.norm(ray_dir)
        new_dir, _ = mirror.propagate_ray(
            np.array([-2.0, 1.0, 0.0]), ray_dir, np.array([0.0, 0.0, 0.0])
        )
        assert np.linalg.norm(new_dir) == pytest.approx(1.0, abs=1e-6)


# ---------------------------------------------------------------------------
# SphericalMirror
# ---------------------------------------------------------------------------


class TestSphericalMirror:
    def test_is_mirror(self):
        mirror = SphericalMirror(radius_of_curvature=4.0)
        assert mirror.is_mirror() is True

    def test_default_construction(self):
        mirror = SphericalMirror()
        assert mirror.radius_of_curvature == pytest.approx(4.0)

    def test_transfer_matrix_concave(self):
        """Concave (R > 0): M = [[1, 0], [-2/R, 1]]."""
        mirror = SphericalMirror(radius_of_curvature=4.0)
        M = mirror.get_transfer_matrix()
        np.testing.assert_allclose(M, np.array([[1.0, 0.0], [-0.5, 1.0]]), atol=1e-10)

    def test_transfer_matrix_convex(self):
        """Convex (R < 0): C = -2/R > 0."""
        mirror = SphericalMirror(radius_of_curvature=-4.0)
        M = mirror.get_transfer_matrix()
        assert M[1, 0] > 0

    @pytest.mark.parametrize("radius", [2.0, 4.0, 10.0, -3.0, -8.0])
    def test_transfer_matrix_unit_determinant(self, radius):
        mirror = SphericalMirror(radius_of_curvature=radius)
        M = mirror.get_transfer_matrix()
        assert np.linalg.det(M) == pytest.approx(1.0, abs=1e-10)

    def test_get_normal_left_side(self):
        mirror = SphericalMirror(radius_of_curvature=4.0, side="left")
        np.testing.assert_allclose(
            mirror.get_normal_at(np.array([0.0, 0.0, 0.0])), LEFT
        )

    def test_get_normal_right_side(self):
        mirror = SphericalMirror(radius_of_curvature=4.0, side="right")
        np.testing.assert_allclose(
            mirror.get_normal_at(np.array([0.0, 0.0, 0.0])), RIGHT
        )

    def test_intersect_horizontal_ray(self):
        mirror = SphericalMirror(radius_of_curvature=4.0, height=3.0)
        ray_start = np.array([-2.0, 0.5, 0.0])
        ray_dir = np.array([1.0, 0.0, 0.0])
        point, hit = mirror.intersect(ray_start, ray_dir)
        assert hit is True
        assert point[0] == pytest.approx(0.0, abs=1e-6)
        assert point[1] == pytest.approx(0.5, abs=1e-6)


# ---------------------------------------------------------------------------
# Mirror (abstract base) — cannot be instantiated directly
# ---------------------------------------------------------------------------


class TestMirrorAbstract:
    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            Mirror()
