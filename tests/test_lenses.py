"""
Tests for `manim_optics.lenses` — ThinLens, ConvergingLens, DivergingLens.
"""

import numpy as np
import pytest

pytest.importorskip("manim", reason="Manim not installed")

from manim_optics import ConvergingLens, DivergingLens, ThinLens  # noqa: E402


# ---------------------------------------------------------------------------
# Construction & validation
# ---------------------------------------------------------------------------


class TestLensConstruction:
    def test_thinlens_default_focal(self):
        lens = ThinLens()
        assert lens.focal_length == pytest.approx(2.0)

    def test_thinlens_custom_height(self):
        lens = ThinLens(focal_length=2.0, height=5.0)
        assert lens.lens_height == pytest.approx(5.0)

    def test_converging_default_positive(self):
        lens = ConvergingLens()
        assert lens.focal_length > 0

    def test_diverging_default_negative(self):
        lens = DivergingLens()
        assert lens.focal_length < 0

    @pytest.mark.parametrize("bad_focal", [-1.0, -2.5, 0.0])
    def test_converging_rejects_nonpositive_focal(self, bad_focal):
        with pytest.raises(ValueError):
            ConvergingLens(focal_length=bad_focal)

    @pytest.mark.parametrize("bad_focal", [1.0, 2.5, 0.0])
    def test_diverging_rejects_nonnegative_focal(self, bad_focal):
        with pytest.raises(ValueError):
            DivergingLens(focal_length=bad_focal)


# ---------------------------------------------------------------------------
# Transfer matrix
# ---------------------------------------------------------------------------


class TestTransferMatrix:
    @pytest.mark.parametrize("f", [1.0, 2.5, 10.0, -1.5, -3.0])
    def test_determinant_unit(self, f):
        if f > 0:
            lens = ConvergingLens(focal_length=f)
        else:
            lens = DivergingLens(focal_length=f)
        M = lens.get_transfer_matrix()
        assert np.linalg.det(M) == pytest.approx(1.0, abs=1e-10)

    def test_matrix_changes_with_tracker(self):
        """Transfer matrix should reflect tracker value, not constructor value."""
        lens = ConvergingLens(focal_length=2.0)
        M_initial = lens.get_transfer_matrix()
        lens.set_focal_length(4.0)
        M_after = lens.get_transfer_matrix()
        assert M_initial[1, 0] != pytest.approx(M_after[1, 0])
        assert M_after[1, 0] == pytest.approx(-1.0 / 4.0)


# ---------------------------------------------------------------------------
# Focal length API
# ---------------------------------------------------------------------------


class TestFocalLengthAPI:
    def test_set_focal_length_returns_self(self):
        lens = ConvergingLens(focal_length=2.0)
        result = lens.set_focal_length(3.0)
        assert result is lens

    def test_set_focal_length_updates_attribute_and_tracker(self):
        lens = ConvergingLens(focal_length=2.0)
        lens.set_focal_length(5.0)
        assert lens.focal_length == pytest.approx(5.0)
        assert lens.focal_length_tracker.get_value() == pytest.approx(5.0)

    def test_animate_focal_length_returns_callable_animation(self):
        """The returned object must be playable by Scene (Animation or _AnimationBuilder)."""
        lens = ConvergingLens(focal_length=2.0)
        anim = lens.animate_focal_length(4.0, run_time=1.0)
        # Manim's `.animate.set_value(...)` returns an _AnimationBuilder which Scene.play() accepts.
        assert anim is not None
        assert hasattr(anim, "build") or hasattr(anim, "begin")


# ---------------------------------------------------------------------------
# Ray intersection
# ---------------------------------------------------------------------------


class TestLensIntersect:
    def test_horizontal_ray_hits_lens_at_origin(self):
        lens = ConvergingLens(focal_length=2.0, height=3.0)
        ray_start = np.array([-3.0, 0.5, 0.0])
        ray_dir = np.array([1.0, 0.0, 0.0])
        point, hit = lens.intersect(ray_start, ray_dir)
        assert hit is True
        assert point[0] == pytest.approx(0.0, abs=1e-6)
        assert point[1] == pytest.approx(0.5, abs=1e-6)

    def test_ray_parallel_to_lens_misses(self):
        lens = ConvergingLens(focal_length=2.0, height=3.0)
        ray_start = np.array([-3.0, 0.0, 0.0])
        ray_dir = np.array([0.0, 1.0, 0.0])
        point, hit = lens.intersect(ray_start, ray_dir)
        assert hit is False
        assert point is None

    def test_ray_above_lens_height_misses(self):
        lens = ConvergingLens(focal_length=2.0, height=3.0)
        # height=3 → half-height 1.5; ray at y=2.0 misses
        ray_start = np.array([-3.0, 2.0, 0.0])
        ray_dir = np.array([1.0, 0.0, 0.0])
        point, hit = lens.intersect(ray_start, ray_dir)
        assert hit is False

    def test_ray_behind_lens_misses(self):
        """Ray going away from the lens (t<0) should not register an intersection."""
        lens = ConvergingLens(focal_length=2.0, height=3.0)
        ray_start = np.array([3.0, 0.0, 0.0])
        ray_dir = np.array([1.0, 0.0, 0.0])  # moving away
        point, hit = lens.intersect(ray_start, ray_dir)
        assert hit is False


# ---------------------------------------------------------------------------
# Ray propagation (paraxial refraction)
# ---------------------------------------------------------------------------


class TestLensPropagate:
    def test_axial_ray_undeflected(self):
        """A ray on the optical axis (y=0, θ=0) exits unchanged."""
        lens = ConvergingLens(focal_length=2.0)
        ray_dir = np.array([1.0, 0.0, 0.0])
        intersection = np.array([0.0, 0.0, 0.0])
        new_dir, continues = lens.propagate_ray(
            np.array([-3.0, 0.0, 0.0]), ray_dir, intersection
        )
        assert continues is True
        np.testing.assert_allclose(new_dir, [1.0, 0.0, 0.0], atol=1e-6)

    def test_parallel_ray_converges_to_focal(self):
        """Parallel ray at height y exits with slope -y/f → crosses axis at f."""
        f = 2.0
        y = 1.0
        lens = ConvergingLens(focal_length=f)
        ray_dir = np.array([1.0, 0.0, 0.0])
        intersection = np.array([0.0, y, 0.0])
        new_dir, continues = lens.propagate_ray(
            np.array([-3.0, y, 0.0]), ray_dir, intersection
        )
        assert continues is True
        # Slope of new direction (paraxial: dy/dx) ≈ -y/f
        slope = new_dir[1] / new_dir[0]
        assert slope == pytest.approx(-y / f, rel=1e-3)

    def test_diverging_lens_diverges_parallel_ray(self):
        f = -2.0
        y = 1.0
        lens = DivergingLens(focal_length=f)
        ray_dir = np.array([1.0, 0.0, 0.0])
        intersection = np.array([0.0, y, 0.0])
        new_dir, _ = lens.propagate_ray(np.array([-3.0, y, 0.0]), ray_dir, intersection)
        slope = new_dir[1] / new_dir[0]
        # f<0 → slope = -y/f > 0 (ray climbs away from axis)
        assert slope > 0

    def test_propagate_returns_normalized_direction(self):
        lens = ConvergingLens(focal_length=2.0)
        ray_dir = np.array([1.0, 0.0, 0.0])
        intersection = np.array([0.0, 0.5, 0.0])
        new_dir, _ = lens.propagate_ray(
            np.array([-3.0, 0.5, 0.0]), ray_dir, intersection
        )
        assert np.linalg.norm(new_dir) == pytest.approx(1.0, abs=1e-6)


# ---------------------------------------------------------------------------
# Optical-plane geometry
# ---------------------------------------------------------------------------


class TestOpticalPlane:
    def test_optical_plane_at_origin_by_default(self):
        from manim import ORIGIN

        lens = ConvergingLens(focal_length=2.0)
        np.testing.assert_allclose(lens.get_optical_plane_position(), ORIGIN, atol=1e-6)

    def test_is_not_mirror(self):
        lens = ConvergingLens(focal_length=2.0)
        assert lens.is_mirror() is False
