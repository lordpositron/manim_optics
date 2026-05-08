"""
Tests for composite optical systems — `manim_optics.centered_system` and `manim_optics.eye`.
"""

import numpy as np
import pytest

pytest.importorskip("manim", reason="Manim not installed")

from manim_optics import (  # noqa: E402
    ArcBeamStop,
    CenteredSystem,
    CircularAperture,
    ConvergingLens,
    Eye,
)

# ---------------------------------------------------------------------------
# CenteredSystem
# ---------------------------------------------------------------------------


class TestCenteredSystem:
    def test_default_construction(self):
        sys = CenteredSystem()
        assert sys.h_position == pytest.approx(-1.0)
        assert sys.h_prime_position == pytest.approx(1.0)
        assert sys.focal_length == pytest.approx(2.0)

    def test_custom_principal_planes(self):
        sys = CenteredSystem(h_position=-0.5, h_prime_position=0.8, focal_length=3.0)
        assert sys.h_position == pytest.approx(-0.5)
        assert sys.h_prime_position == pytest.approx(0.8)

    def test_transfer_matrix_unit_determinant(self):
        sys = CenteredSystem(focal_length=3.0)
        M = sys.get_transfer_matrix()
        assert np.linalg.det(M) == pytest.approx(1.0, abs=1e-10)

    def test_transfer_matrix_uses_focal_length_tracker(self):
        sys = CenteredSystem(focal_length=2.0)
        M = sys.get_transfer_matrix()
        assert M[1, 0] == pytest.approx(-0.5, abs=1e-10)

    def test_is_not_mirror(self):
        sys = CenteredSystem()
        assert sys.is_mirror() is False

    def test_is_ray_inside_system_between_boundaries(self):
        sys = CenteredSystem(h_position=-1.0, h_prime_position=1.0)
        assert sys.is_ray_inside_system(
            np.array([0.0, 0.0, 0.0]), np.array([1.0, 0.0, 0.0])
        )

    def test_is_ray_inside_system_outside(self):
        sys = CenteredSystem(h_position=-1.0, h_prime_position=1.0)
        assert not sys.is_ray_inside_system(
            np.array([5.0, 0.0, 0.0]), np.array([1.0, 0.0, 0.0])
        )


# ---------------------------------------------------------------------------
# Eye
# ---------------------------------------------------------------------------


class TestEye:
    def test_default_construction(self):
        eye = Eye()
        assert eye.focal_length == pytest.approx(2.0)
        assert eye.lens_diameter == pytest.approx(1.0)
        assert eye.pupil_diameter == pytest.approx(0.4)
        assert eye.include_pupil is True

    def test_lens_is_converging(self):
        eye = Eye()
        assert isinstance(eye.lens, ConvergingLens)

    def test_retina_is_arc_beam_stop(self):
        eye = Eye()
        assert isinstance(eye.retina, ArcBeamStop)

    def test_pupil_is_circular_aperture_when_included(self):
        eye = Eye(include_pupil=True)
        assert isinstance(eye.pupil, CircularAperture)

    def test_pupil_is_none_when_excluded(self):
        eye = Eye(include_pupil=False)
        assert eye.pupil is None

    def test_optical_elements_with_pupil(self):
        eye = Eye(include_pupil=True)
        elements = eye.get_optical_elements()
        # Order: lens, pupil, retina
        assert len(elements) == 3
        assert elements[0] is eye.lens
        assert elements[1] is eye.pupil
        assert elements[2] is eye.retina

    def test_optical_elements_without_pupil(self):
        eye = Eye(include_pupil=False)
        elements = eye.get_optical_elements()
        assert len(elements) == 2
        assert elements[0] is eye.lens
        assert elements[1] is eye.retina

    def test_set_focal_length_propagates_to_lens(self):
        eye = Eye(focal_length=2.0)
        eye.set_focal_length(2.5)
        assert eye.focal_length == pytest.approx(2.5)
        assert eye.lens.focal_length == pytest.approx(2.5)

    def test_set_focal_length_returns_self(self):
        eye = Eye()
        assert eye.set_focal_length(2.5) is eye

    def test_set_pupil_diameter(self):
        eye = Eye(pupil_diameter=0.4)
        eye.set_pupil_diameter(0.6)
        assert eye.pupil_diameter == pytest.approx(0.6)
        assert eye.pupil.aperture_radius == pytest.approx(0.3)

    def test_set_pupil_diameter_no_pupil_is_safe(self):
        """set_pupil_diameter should not crash on an Eye without a pupil."""
        eye = Eye(include_pupil=False)
        result = eye.set_pupil_diameter(0.5)
        assert result is eye

    def test_animate_focal_length_returns_playable(self):
        """Returned object must be playable by Scene.play."""
        eye = Eye(focal_length=2.0)
        anim = eye.animate_focal_length(2.5, run_time=1.0)
        assert anim is not None
        assert hasattr(anim, "build") or hasattr(anim, "begin")

    def test_retina_radius_depends_on_focal_length(self):
        """A longer focal length → larger retina radius (geometric scaling)."""
        eye_short = Eye(focal_length=1.5)
        eye_long = Eye(focal_length=3.0)
        assert eye_long.retina_radius > eye_short.retina_radius
