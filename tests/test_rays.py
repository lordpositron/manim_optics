"""
Tests for `manim_optics.rays` — DynamicRay, RayBundle, helpers.

Note: DynamicRay's `_update_ray_path` calls `self.become(temp_ray)` which
moves the rendered geometry into submobjects, leaving the parent's `points`
empty. Functions like `find_ray_intersection` therefore only work in a live
Scene context (where the renderer aggregates points). The tests below avoid
that path by stubbing rays with explicit `get_points()` data.
"""

import numpy as np
import pytest

pytest.importorskip("manim", reason="Manim not installed")

from manim import RIGHT  # noqa: E402

from manim_optics import (  # noqa: E402
    ConvergingLens,
    DynamicRay,
    PrincipalRays,
    RayBundle,
    create_diverging_bundle,
    create_parallel_bundle,
    find_ray_intersection,
)

# ---------------------------------------------------------------------------
# DynamicRay — construction
# ---------------------------------------------------------------------------


class TestDynamicRayConstruction:
    def test_static_start_and_direction(self):
        """Ray with static start/direction should construct without error."""
        ray = DynamicRay(
            start_point=np.array([-3.0, 0.0, 0.0]),
            direction=np.array([1.0, 0.0, 0.0]),
            optical_elements=[],
        )
        assert ray.optical_elements == []
        assert ray.max_segments == 10  # default

    def test_callable_direction_stored(self):
        ray = DynamicRay(
            start_point=np.array([-3.0, 0.0, 0.0]),
            direction=lambda: np.array([1.0, 0.5, 0.0]),
            optical_elements=[],
        )
        assert callable(ray.direction_source)

    def test_optical_elements_list_stored(self):
        lens = ConvergingLens(focal_length=2.0)
        ray = DynamicRay(
            start_point=np.array([-3.0, 0.5, 0.0]),
            direction=np.array([1.0, 0.0, 0.0]),
            optical_elements=[lens],
        )
        assert lens in ray.optical_elements

    def test_add_optical_element(self):
        lens = ConvergingLens(focal_length=2.0)
        ray = DynamicRay(
            start_point=np.array([-3.0, 0.0, 0.0]),
            direction=np.array([1.0, 0.0, 0.0]),
            optical_elements=[],
        )
        ray.add_optical_element(lens)
        assert lens in ray.optical_elements

    def test_remove_optical_element(self):
        lens = ConvergingLens(focal_length=2.0)
        ray = DynamicRay(
            start_point=np.array([-3.0, 0.0, 0.0]),
            direction=np.array([1.0, 0.0, 0.0]),
            optical_elements=[lens],
        )
        ray.remove_optical_element(lens)
        assert lens not in ray.optical_elements

    def test_set_optical_elements_replaces_list(self):
        lens1 = ConvergingLens(focal_length=2.0)
        lens2 = ConvergingLens(focal_length=3.0)
        ray = DynamicRay(
            start_point=np.array([-3.0, 0.0, 0.0]),
            direction=np.array([1.0, 0.0, 0.0]),
            optical_elements=[lens1],
        )
        ray.set_optical_elements([lens2])
        assert ray.optical_elements == [lens2]


# ---------------------------------------------------------------------------
# RayBundle
# ---------------------------------------------------------------------------


class TestRayBundle:
    def test_parallel_bundle_via_helper(self):
        bundle = create_parallel_bundle(
            num_rays=5, spacing=0.5, start_x=-5.0, optical_elements=[]
        )
        assert len(bundle.rays) == 5

    def test_diverging_bundle_via_helper(self):
        bundle = create_diverging_bundle(
            source_point=np.array([-3.0, 0.0, 0.0]),
            angle_range_deg=(-30, 30),
            num_rays=4,
            optical_elements=[],
        )
        assert len(bundle.rays) == 4

    def test_bundle_with_explicit_directions(self):
        bundle = RayBundle(
            start_points=np.array([0.0, 0.0, 0.0]),
            direction_angle_deg=[0.0, 30.0, 60.0],
            optical_elements=[],
        )
        assert len(bundle.rays) == 3

    def test_bundle_with_per_ray_starts(self):
        bundle = RayBundle(
            start_points=[
                np.array([-2.0, 1.0, 0.0]),
                np.array([-2.0, 0.0, 0.0]),
                np.array([-2.0, -1.0, 0.0]),
            ],
            direction_vector=RIGHT,
            optical_elements=[],
        )
        assert len(bundle.rays) == 3


# ---------------------------------------------------------------------------
# find_ray_intersection (using stub rays with explicit points)
# ---------------------------------------------------------------------------


class _RayStub:
    """Minimal ray-shaped object exposing only `get_points()` for the helper."""

    def __init__(self, points: np.ndarray):
        self._points = np.asarray(points)

    def get_points(self) -> np.ndarray:
        return self._points


class TestFindRayIntersection:
    def test_two_crossing_rays(self):
        """Two segments crossing at the origin should intersect there."""
        # Ray 1: from (-2, 1) to (2, -1) — passes through origin
        ray1 = _RayStub(np.array([[-2.0, 1.0, 0.0], [2.0, -1.0, 0.0]]))
        # Ray 2: from (-2, -1) to (2, 1) — passes through origin
        ray2 = _RayStub(np.array([[-2.0, -1.0, 0.0], [2.0, 1.0, 0.0]]))
        intersection = find_ray_intersection(ray1, ray2)
        assert intersection is not None
        assert intersection[0] == pytest.approx(0.0, abs=1e-6)
        assert intersection[1] == pytest.approx(0.0, abs=1e-6)

    def test_parallel_segments_return_none(self):
        ray1 = _RayStub(np.array([[-2.0, 0.5, 0.0], [2.0, 0.5, 0.0]]))
        ray2 = _RayStub(np.array([[-2.0, -0.5, 0.0], [2.0, -0.5, 0.0]]))
        assert find_ray_intersection(ray1, ray2) is None

    def test_too_few_points_returns_none(self):
        ray1 = _RayStub(np.zeros((0, 3)))
        ray2 = _RayStub(np.array([[-2.0, 0.0, 0.0], [2.0, 0.0, 0.0]]))
        assert find_ray_intersection(ray1, ray2) is None


# ---------------------------------------------------------------------------
# PrincipalRays
# ---------------------------------------------------------------------------


class TestPrincipalRays:
    def test_three_rays_created(self):
        lens = ConvergingLens(focal_length=2.0)
        principals = PrincipalRays(object_point=np.array([-3.0, 1.0, 0.0]), lens=lens)
        assert isinstance(principals.parallel_ray, DynamicRay)
        assert isinstance(principals.center_ray, DynamicRay)
        assert isinstance(principals.focal_ray, DynamicRay)

    def test_lens_reference_stored(self):
        lens = ConvergingLens(focal_length=2.0)
        principals = PrincipalRays(object_point=np.array([-3.0, 1.0, 0.0]), lens=lens)
        assert principals.lens is lens
