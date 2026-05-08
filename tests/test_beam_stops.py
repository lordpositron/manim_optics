"""
Tests for `manim_optics.beam_stops` — BeamStop, LineBeamStop, CircularAperture, ArcBeamStop.
"""

import numpy as np
import pytest

pytest.importorskip("manim", reason="Manim not installed")

from manim_optics import (  # noqa: E402
    ArcBeamStop,
    BeamStop,
    CircularAperture,
    LineBeamStop,
)


# ---------------------------------------------------------------------------
# BeamStop (abstract)
# ---------------------------------------------------------------------------


class TestBeamStopAbstract:
    def test_cannot_instantiate_abstract(self):
        with pytest.raises(TypeError):
            BeamStop()


# ---------------------------------------------------------------------------
# LineBeamStop
# ---------------------------------------------------------------------------


class TestLineBeamStop:
    def test_construction(self):
        stop = LineBeamStop(height=4.0)
        assert stop.stop_height == pytest.approx(4.0)

    def test_is_not_mirror(self):
        stop = LineBeamStop()
        assert stop.is_mirror() is False

    def test_propagate_terminates_ray(self):
        """BeamStop returns (None, False) — ray is absorbed."""
        stop = LineBeamStop()
        new_dir, continues = stop.propagate_ray(
            np.array([-1.0, 0.0, 0.0]),
            np.array([1.0, 0.0, 0.0]),
            np.array([0.0, 0.0, 0.0]),
        )
        assert new_dir is None
        assert continues is False

    def test_intersect_within_height(self):
        stop = LineBeamStop(height=2.0)
        ray_start = np.array([-1.0, 0.5, 0.0])
        ray_dir = np.array([1.0, 0.0, 0.0])
        point, hit = stop.intersect(ray_start, ray_dir)
        assert hit is True
        assert point[0] == pytest.approx(0.0, abs=1e-6)

    def test_intersect_outside_height_misses(self):
        stop = LineBeamStop(height=2.0)
        ray_start = np.array([-1.0, 1.5, 0.0])  # above top (1.0)
        ray_dir = np.array([1.0, 0.0, 0.0])
        _, hit = stop.intersect(ray_start, ray_dir)
        assert hit is False

    def test_transfer_matrix_identity(self):
        stop = LineBeamStop()
        M = stop.get_transfer_matrix()
        np.testing.assert_allclose(M, np.eye(2), atol=1e-10)


# ---------------------------------------------------------------------------
# CircularAperture
# ---------------------------------------------------------------------------


class TestCircularAperture:
    def test_construction_default_total_length(self):
        ap = CircularAperture(radius=0.5)
        assert ap.aperture_radius == pytest.approx(0.5)
        assert ap.total_length == pytest.approx(4.0)  # 8 * radius

    def test_construction_explicit_total_length(self):
        ap = CircularAperture(radius=0.5, total_length=3.0)
        assert ap.total_length == pytest.approx(3.0)

    def test_ray_through_center_passes(self):
        """Ray hitting within radius is NOT blocked (passes through aperture)."""
        ap = CircularAperture(radius=0.5)
        ray_start = np.array([-1.0, 0.2, 0.0])  # within 0.5 radius
        ray_dir = np.array([1.0, 0.0, 0.0])
        point, hit = ap.intersect(ray_start, ray_dir)
        # hit=False means ray passes through the opening
        assert hit is False

    def test_ray_in_blocking_region_is_stopped(self):
        """Ray hitting between aperture radius and total_length/2 is blocked."""
        ap = CircularAperture(radius=0.5, total_length=4.0)
        # blocking region: 0.5 < |y| < 2.0
        ray_start = np.array([-1.0, 1.0, 0.0])
        ray_dir = np.array([1.0, 0.0, 0.0])
        point, hit = ap.intersect(ray_start, ray_dir)
        assert hit is True

    def test_ray_outside_total_length_passes(self):
        """Ray missing the entire stop returns False."""
        ap = CircularAperture(radius=0.5, total_length=4.0)
        ray_start = np.array([-1.0, 3.0, 0.0])  # above total_length/2
        ray_dir = np.array([1.0, 0.0, 0.0])
        _, hit = ap.intersect(ray_start, ray_dir)
        assert hit is False

    def test_set_radius_updates_tracker(self):
        ap = CircularAperture(radius=0.5)
        ap.set_radius(0.8)
        assert ap.aperture_radius == pytest.approx(0.8)
        assert ap.radius_tracker.get_value() == pytest.approx(0.8)

    def test_set_radius_returns_self(self):
        ap = CircularAperture(radius=0.5)
        assert ap.set_radius(0.3) is ap

    def test_animate_radius_returns_playable(self):
        """Returned object must be playable by Scene.play (Animation or _AnimationBuilder)."""
        ap = CircularAperture(radius=0.5)
        anim = ap.animate_radius(0.8, run_time=1.0)
        assert anim is not None
        assert hasattr(anim, "build") or hasattr(anim, "begin")

    def test_get_top_coordinates(self):
        ap = CircularAperture(radius=0.5, total_length=4.0)
        top = ap.get_top_coordinates()
        assert top[1] == pytest.approx(2.0)  # total_length/2

    def test_get_bottom_coordinates(self):
        ap = CircularAperture(radius=0.5, total_length=4.0)
        bottom = ap.get_bottom_coordinates()
        assert bottom[1] == pytest.approx(-2.0)


# ---------------------------------------------------------------------------
# ArcBeamStop
# ---------------------------------------------------------------------------


class TestArcBeamStop:
    def test_construction(self):
        arc = ArcBeamStop(radius=2.0)
        assert arc.arc_radius == pytest.approx(2.0)

    def test_is_not_mirror(self):
        arc = ArcBeamStop()
        assert arc.is_mirror() is False

    def test_propagate_terminates_ray(self):
        arc = ArcBeamStop()
        new_dir, continues = arc.propagate_ray(
            np.array([-1.0, 0.0, 0.0]),
            np.array([1.0, 0.0, 0.0]),
            np.array([0.0, 0.0, 0.0]),
        )
        assert new_dir is None
        assert continues is False

    def test_curvature_center_is_3d_point(self):
        arc = ArcBeamStop(radius=2.0)
        center = arc.get_curvature_center()
        assert center.shape == (3,)

    def test_ray_far_from_arc_misses(self):
        """Ray with closest approach > arc_radius misses the arc."""
        arc = ArcBeamStop(radius=1.0, arc_angle=np.pi / 2)
        # Ray going away from arc
        ray_start = np.array([10.0, 10.0, 0.0])
        ray_dir = np.array([1.0, 0.0, 0.0])
        _, hit = arc.intersect(ray_start, ray_dir)
        assert hit is False

    def test_debug_info_contains_keys(self):
        arc = ArcBeamStop(radius=2.0)
        info = arc.get_debug_info(np.array([-1.0, 0.0, 0.0]), np.array([1.0, 0.0, 0.0]))
        for key in ["curvature_center", "arc_radius", "distance_to_ray"]:
            assert key in info
