"""
Tests for `manim_optics.scene_utils` — scene helpers and arrow utilities.
"""

import math

import numpy as np
import pytest

pytest.importorskip("manim", reason="Manim not installed")

from manim import VGroup  # noqa: E402

from manim_optics import (  # noqa: E402
    OpticalScene,
    calculate_image_position,
    create_image_arrow,
    create_object_arrow,
)


# ---------------------------------------------------------------------------
# calculate_image_position — extra coverage of magnification & sign rules
# ---------------------------------------------------------------------------


class TestCalculateImagePosition:
    def test_object_at_2f_returns_unit_magnification(self):
        image_dist, mag, is_real = calculate_image_position(4.0, 2.0)
        assert image_dist == pytest.approx(4.0)
        assert mag == pytest.approx(-1.0)
        assert is_real is True

    def test_diverging_lens_virtual_image(self):
        image_dist, mag, is_real = calculate_image_position(3.0, -2.0)
        assert is_real is False
        assert image_dist < 0
        assert mag > 0

    def test_object_at_focal_image_at_infinity(self):
        image_dist, _, _ = calculate_image_position(2.0, 2.0)
        assert math.isinf(image_dist)

    def test_zero_object_distance_infinity(self):
        image_dist, _, _ = calculate_image_position(0.0, 2.0)
        assert math.isinf(image_dist)

    @pytest.mark.parametrize("p,f,sign", [(3.0, 2.0, -1), (1.0, 2.0, +1)])
    def test_magnification_sign(self, p, f, sign):
        _, mag, _ = calculate_image_position(p, f)
        assert np.sign(mag) == sign


# ---------------------------------------------------------------------------
# create_object_arrow / create_image_arrow
# ---------------------------------------------------------------------------


class TestObjectArrow:
    def test_returns_vgroup(self):
        result = create_object_arrow(np.array([0.0, 0.0, 0.0]))
        assert isinstance(result, VGroup)

    def test_has_two_components(self):
        """VGroup contains arrow + label."""
        result = create_object_arrow(np.array([0.0, 0.0, 0.0]))
        assert len(result) == 2


class TestImageArrow:
    def test_returns_vgroup(self):
        result = create_image_arrow(np.array([2.0, 0.0, 0.0]))
        assert isinstance(result, VGroup)

    def test_inverted_flips_height(self):
        """When inverted=True, arrow points downward."""
        from manim import Arrow

        result = create_image_arrow(
            np.array([2.0, 0.0, 0.0]), height=1.0, inverted=True
        )
        # First component is the arrow
        arrow = result[0]
        assert isinstance(arrow, Arrow)
        # End y < start y when inverted
        start_y = arrow.get_start()[1]
        end_y = arrow.get_end()[1]
        assert end_y < start_y


# ---------------------------------------------------------------------------
# OpticalScene
# ---------------------------------------------------------------------------


class TestOpticalScene:
    def test_invalid_theme_raises(self):
        scene = OpticalScene()
        with pytest.raises(ValueError):
            scene.set_theme("rainbow")

    def test_setup_optical_axis_creates_line(self):
        scene = OpticalScene()
        scene.setup_optical_axis(length=10.0, animate=False)
        from manim import Line

        assert isinstance(scene.optical_axis, Line)
