"""
Tests for `manim_optics.optics_3d` — OpticalElement3D, ThinLens3D, RayBundle3D.
"""

import numpy as np
import pytest

pytest.importorskip("manim", reason="Manim not installed")

from manim_optics import OpticalElement3D, RayBundle3D, ThinLens3D  # noqa: E402

# ---------------------------------------------------------------------------
# OpticalElement3D — abstract base
# ---------------------------------------------------------------------------


class TestOpticalElement3D:
    def test_construction_normalizes_normal(self):
        element = OpticalElement3D(
            position=np.array([0.0, 0.0, 0.0]),
            normal_vector=np.array([0.0, 2.0, 0.0]),  # not normalized
        )
        np.testing.assert_allclose(np.linalg.norm(element.normal), 1.0, atol=1e-10)

    def test_get_optical_plane_position(self):
        element = OpticalElement3D(position=np.array([1.0, 2.0, 3.0]))
        np.testing.assert_allclose(
            element.get_optical_plane_position(), [1.0, 2.0, 3.0]
        )

    def test_get_normal_vector_returns_copy(self):
        element = OpticalElement3D(normal_vector=np.array([1.0, 0.0, 0.0]))
        n = element.get_normal_vector()
        n[0] = 999.0  # try to mutate
        # Internal normal should not be modified
        assert element.normal[0] != pytest.approx(999.0)

    def test_intersect_3d_horizontal_plane(self):
        """Plane at y=2 with normal UP, ray going up from origin."""
        plane = OpticalElement3D(
            position=np.array([0.0, 2.0, 0.0]),
            normal_vector=np.array([0.0, 1.0, 0.0]),
        )
        ray_start = np.array([0.0, 0.0, 0.0])
        ray_dir = np.array([0.0, 1.0, 0.0])
        intersection = plane.intersect_3d(ray_start, ray_dir)
        assert intersection is not None
        np.testing.assert_allclose(intersection, [0.0, 2.0, 0.0], atol=1e-6)

    def test_intersect_3d_parallel_ray_returns_none(self):
        """Ray parallel to plane never intersects."""
        plane = OpticalElement3D(
            position=np.array([0.0, 2.0, 0.0]),
            normal_vector=np.array([0.0, 1.0, 0.0]),
        )
        ray_start = np.array([0.0, 0.0, 0.0])
        ray_dir = np.array([1.0, 0.0, 0.0])  # along x, plane is xz
        result = plane.intersect_3d(ray_start, ray_dir)
        assert result is None

    def test_intersect_3d_behind_ray_start_returns_none(self):
        plane = OpticalElement3D(
            position=np.array([0.0, -2.0, 0.0]),
            normal_vector=np.array([0.0, 1.0, 0.0]),
        )
        ray_start = np.array([0.0, 0.0, 0.0])
        ray_dir = np.array([0.0, 1.0, 0.0])  # going away from plane
        result = plane.intersect_3d(ray_start, ray_dir)
        assert result is None

    def test_propagate_ray_3d_not_implemented_in_base(self):
        plane = OpticalElement3D()
        with pytest.raises(NotImplementedError):
            plane.propagate_ray_3d(
                np.array([0.0, 0.0, 0.0]),
                np.array([0.0, 1.0, 0.0]),
                np.array([0.0, 1.0, 0.0]),
            )


# ---------------------------------------------------------------------------
# ThinLens3D
# ---------------------------------------------------------------------------


class TestThinLens3D:
    def test_construction(self):
        lens = ThinLens3D(focal_length=3.0, aperture_radius=1.5)
        assert lens.focal_length == pytest.approx(3.0)
        assert lens.aperture_radius == pytest.approx(1.5)

    def test_default_display_mode(self):
        lens = ThinLens3D()
        assert lens.display_mode == "simple"

    def test_intersect_3d_central_ray(self):
        """Ray along the lens normal hits the center of the lens."""
        lens = ThinLens3D(
            focal_length=3.0,
            position=np.array([0.0, 0.0, 0.0]),
            normal_vector=np.array([0.0, 1.0, 0.0]),  # lens in xz plane
        )
        ray_start = np.array([0.0, -2.0, 0.0])
        ray_dir = np.array([0.0, 1.0, 0.0])
        intersection = lens.intersect_3d(ray_start, ray_dir)
        assert intersection is not None
        np.testing.assert_allclose(intersection, [0.0, 0.0, 0.0], atol=1e-6)

    def test_propagate_central_ray_undeflected(self):
        """A ray hitting the lens center along the normal exits unchanged."""
        lens = ThinLens3D(
            focal_length=3.0,
            aperture_radius=2.0,
            position=np.array([0.0, 0.0, 0.0]),
            normal_vector=np.array([0.0, 1.0, 0.0]),
        )
        ray_start = np.array([0.0, -2.0, 0.0])
        ray_dir = np.array([0.0, 1.0, 0.0])
        intersection = np.array([0.0, 0.0, 0.0])
        new_dir, continues = lens.propagate_ray_3d(ray_start, ray_dir, intersection)
        assert continues is True
        np.testing.assert_allclose(new_dir, [0.0, 1.0, 0.0], atol=1e-6)

    def test_propagate_off_axis_ray_deflected(self):
        """A parallel ray off-axis must be deflected toward the focus."""
        lens = ThinLens3D(
            focal_length=3.0,
            aperture_radius=2.0,
            position=np.array([0.0, 0.0, 0.0]),
            normal_vector=np.array([0.0, 1.0, 0.0]),
        )
        # Parallel ray hitting at offset
        ray_start = np.array([1.0, -2.0, 0.0])
        ray_dir = np.array([0.0, 1.0, 0.0])
        intersection = np.array([1.0, 0.0, 0.0])
        new_dir, continues = lens.propagate_ray_3d(ray_start, ray_dir, intersection)
        assert continues is True
        # The deflected ray should converge: x-component negative
        assert new_dir[0] < 0

    def test_ray_outside_aperture_blocked(self):
        """A ray hitting beyond aperture_radius is blocked."""
        lens = ThinLens3D(
            focal_length=3.0,
            aperture_radius=1.0,
            position=np.array([0.0, 0.0, 0.0]),
            normal_vector=np.array([0.0, 1.0, 0.0]),
        )
        ray_start = np.array([2.0, -2.0, 0.0])  # 2.0 > aperture 1.0
        ray_dir = np.array([0.0, 1.0, 0.0])
        intersection = np.array([2.0, 0.0, 0.0])
        new_dir, continues = lens.propagate_ray_3d(ray_start, ray_dir, intersection)
        assert continues is False
        assert new_dir is None

    def test_propagate_returns_normalized_direction(self):
        lens = ThinLens3D(focal_length=3.0, aperture_radius=2.0)
        ray_start = np.array([0.5, -2.0, 0.0])
        ray_dir = np.array([0.0, 1.0, 0.0])
        intersection = np.array([0.5, 0.0, 0.0])
        new_dir, _ = lens.propagate_ray_3d(ray_start, ray_dir, intersection)
        assert np.linalg.norm(new_dir) == pytest.approx(1.0, abs=1e-6)


# ---------------------------------------------------------------------------
# RayBundle3D
# ---------------------------------------------------------------------------


class TestRayBundle3D:
    def test_construction_empty_elements(self):
        bundle = RayBundle3D(
            start_points=[np.array([0.0, 0.0, 0.0])],
            direction_vector=np.array([0.0, 1.0, 0.0]),
            optical_elements=[],
        )
        assert len(bundle.start_points) == 1

    def test_normalizes_direction(self):
        bundle = RayBundle3D(
            start_points=[np.array([0.0, 0.0, 0.0])],
            direction_vector=np.array([0.0, 2.0, 0.0]),  # not normalized
            optical_elements=[],
        )
        assert np.linalg.norm(bundle.direction) == pytest.approx(1.0, abs=1e-10)

    def test_traces_through_lens(self):
        lens = ThinLens3D(
            focal_length=3.0,
            aperture_radius=2.0,
            position=np.array([0.0, 0.0, 0.0]),
            normal_vector=np.array([0.0, 1.0, 0.0]),
        )
        bundle = RayBundle3D(
            start_points=[
                np.array([0.5, -3.0, 0.0]),
                np.array([-0.5, -3.0, 0.0]),
            ],
            direction_vector=np.array([0.0, 1.0, 0.0]),
            optical_elements=[lens],
        )
        # Should produce visible 3D segments
        assert len(bundle.submobjects) > 0
