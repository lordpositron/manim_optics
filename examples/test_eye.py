"""
Test Eye Model - Demonstration of the eye optical system
"""

import numpy as np
from manim import *

from manim_optics import (
    ArcBeamStop,
    CircularAperture,
    Eye,
    LineBeamStop,
    RayBundle,
)


class TestEyeModel(Scene):
    def construct(self):
        # Create eye model
        eye = Eye(
            focal_length=2.0,
            lens_diameter=1.0,
            pupil_diameter=1,
            include_pupil=True,
        )
        eye.shift(RIGHT * 2)

        # Create light source from the left (distant object)
        source_positions = [np.array([-5, y, 0]) for y in np.linspace(-0.5, 0.5, 5)]

        # Create ray bundle
        rays = RayBundle(
            start_points=source_positions,
            direction_angle_deg=[0] * 5,  # Parallel rays
            optical_elements=eye.get_optical_elements(),
            color=YELLOW,
            stroke_width=2,
        )

        # Add to scene
        self.add(eye, rays)

        # Grid for reference
        grid = NumberPlane(
            x_range=[-7, 7],
            y_range=[-4, 4],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.2,
            },
        )
        self.add(grid)

        # Labels
        title = Text("Eye Model - Optical Ray Tracing", font_size=28).to_edge(UP)
        self.add(title)

        # Info about components
        info = (
            VGroup(
                Text(f"Focal length: {eye.focal_length}", font_size=20),
                Text(f"Pupil diameter: {eye.pupil_diameter}", font_size=20),
                Text(f"Retina radius: {eye.retina_radius}", font_size=20),
            )
            .arrange(DOWN, aligned_edge=LEFT)
            .to_corner(UL, buff=0.5)
        )
        self.add(info)

        self.wait(1)


class TestBeamStops(Scene):
    """Test all beam stop types with variable sizes"""

    def construct(self):
        title = Text("Beam Stops - Variable Sizes", font_size=32).to_edge(UP)
        self.add(title)

        # Test 1: LineBeamStop with different heights
        self.test_line_beam_stop()
        self.wait(2)
        self.clear()
        self.add(title)

        # Test 2: CircularAperture with different radii
        self.test_circular_aperture()
        self.wait(2)
        self.clear()
        self.add(title)

        # Test 3: ArcBeamStop with different sizes
        self.test_arc_beam_stop()
        self.wait(2)

    def test_line_beam_stop(self):
        """Test LineBeamStop with different heights"""
        subtitle = Text("LineBeamStop - Variable Heights", font_size=24).shift(UP * 3)
        self.add(subtitle)

        heights = [1.5, 2.5, 3.5]
        positions = [LEFT * 4, ORIGIN, RIGHT * 4]

        for height, pos in zip(heights, positions):
            # Create line stop
            line_stop = LineBeamStop(height=height, color=GREY_D)
            line_stop.shift(pos)

            # Create rays
            rays = RayBundle(
                start_points=[
                    np.array([pos[0] - 3, y, 0]) for y in np.linspace(-2, 2, 9)
                ],
                direction_angle_deg=[0] * 9,
                optical_elements=[line_stop],
                color=YELLOW,
                stroke_width=2,
            )

            # Label
            label = Text(f"h={height}", font_size=18).next_to(line_stop, DOWN, buff=0.3)

            self.add(line_stop, rays, label)

    def test_circular_aperture(self):
        """Test CircularAperture with different radii"""
        subtitle = Text("CircularAperture - Variable Radii", font_size=24).shift(UP * 3)
        self.add(subtitle)

        radii = [0.3, 0.6, 0.9]
        positions = [LEFT * 4, ORIGIN, RIGHT * 4]

        for radius, pos in zip(radii, positions):
            # Create aperture
            aperture = CircularAperture(radius=radius, color=BLUE_D)
            aperture.shift(pos)

            # Create rays
            rays = RayBundle(
                start_points=[
                    np.array([pos[0] - 3, y, 0]) for y in np.linspace(-1.5, 1.5, 9)
                ],
                direction_angle_deg=[0] * 9,
                optical_elements=[aperture],
                color=YELLOW,
                stroke_width=2,
            )

            # Label
            label = Text(f"r={radius}", font_size=18).next_to(aperture, DOWN, buff=0.5)

            self.add(aperture, rays, label)

    def test_arc_beam_stop(self):
        """Test ArcBeamStop with different sizes"""
        subtitle = Text("ArcBeamStop - Variable Radii & Angles", font_size=24).shift(
            UP * 3
        )
        self.add(subtitle)

        configs = [
            (1.5, 90 * DEGREES, LEFT * 4),
            (2.0, 120 * DEGREES, ORIGIN),
            (2.5, 150 * DEGREES, RIGHT * 4),
        ]

        for radius, angle, pos in configs:
            # Create arc stop
            arc_stop = ArcBeamStop(
                radius=radius,
                arc_angle=angle,
                color=RED_D,
                stroke_width=4,
            )
            # By default, arc's rightmost point (face) is at x=radius
            # We want to position the face at pos[0]
            # So shift by (pos[0] - radius)
            arc_stop.shift(pos + RIGHT * (-radius))

            # Create rays
            rays = RayBundle(
                start_points=[
                    np.array([pos[0] - 3, y, 0]) for y in np.linspace(-1.5, 1.5, 9)
                ],
                direction_angle_deg=[0] * 9,
                optical_elements=[arc_stop],
                color=YELLOW,
                stroke_width=2,
            )

            # Label
            label = Text(
                f"r={radius}\nθ={int(angle * 180 / np.pi)}°", font_size=16
            ).next_to(arc_stop, DOWN, buff=0.3)

            self.add(arc_stop, rays, label)


class TestEyeAccommodation(Scene):
    """Test eye accommodation (changing focal length)"""

    def construct(self):
        # Create eye
        eye = Eye(
            focal_length=2.0,
            lens_diameter=1.2,
            pupil_diameter=0.5,
            include_pupil=True,
        )
        eye.shift(RIGHT * 2)
        N = 15
        # Distant object (parallel rays)
        rays_distant = RayBundle(
            start_points=[np.array([-5, y, 0]) for y in np.linspace(-0.4, 0.4, N)],
            direction_angle_deg=[0] * N,
            optical_elements=eye.get_optical_elements(),
            color=YELLOW,
            stroke_width=2,
        )

        self.add(eye, rays_distant)

        title = Text("Eye Accommodation", font_size=32).to_edge(UP)
        status = Text("Viewing distant object", font_size=24).next_to(title, DOWN)
        self.add(title, status)

        self.wait(1)

        # Change focal length (accommodation for near object)
        new_status = Text("Accommodating for near object", font_size=24).next_to(
            title, DOWN
        )
        self.play(
            eye.animate_focal_length(1.5, run_time=2),
            Transform(status, new_status),
            run_time=2,
        )

        self.wait(1)

        # Dilate pupil
        new_status2 = Text("Pupil dilation", font_size=24).next_to(title, DOWN)
        self.play(
            eye.animate_pupil_diameter(0.8, run_time=2),
            Transform(status, new_status2),
            run_time=2,
        )

        self.wait(1)


class TestApertureCustomization(Scene):
    """Test CircularAperture customization options"""

    def construct(self):
        title = Text("CircularAperture - Customization Options", font_size=32).to_edge(
            UP
        )
        self.add(title)

        # Test 1: Different radii (opening sizes)
        subtitle1 = Text("Different Opening Sizes", font_size=20).shift(UP * 2.5)
        self.add(subtitle1)

        radii = [0.3, 0.6, 0.9]
        x_positions = [-4, 0, 4]

        for radius, x_pos in zip(radii, x_positions):
            aperture = CircularAperture(
                radius=radius,
                total_length=3.0,
                line_color=BLUE,
                line_stroke_width=4,
            )
            aperture.shift(RIGHT * x_pos + UP * 0.5)

            # Rays to show blocking
            rays = RayBundle(
                start_points=[
                    np.array([x_pos - 2, y, 0]) for y in np.linspace(-1.2, 1.2, 7)
                ],
                direction_angle_deg=[0] * 7,
                optical_elements=[aperture],
                color=YELLOW,
                stroke_width=2,
            )

            label = Text(f"radius={radius}", font_size=16).next_to(
                aperture, DOWN, buff=0.3
            )
            self.add(aperture, rays, label)

        # Test 2: Different line parameters
        subtitle2 = Text("Different Line Styles", font_size=20).shift(DOWN * 1)
        self.add(subtitle2)

        configs = [
            (RED, 2, "Red, thin"),
            (GREEN, 6, "Green, thick"),
            (PURPLE, 10, "Purple, very thick"),
        ]

        for i, (color, stroke, desc) in enumerate(configs):
            x_pos = -4 + i * 4
            aperture = CircularAperture(
                radius=0.5,
                total_length=2.5,
                line_color=color,
                line_stroke_width=stroke,
            )
            aperture.shift(RIGHT * x_pos + DOWN * 2)

            label = Text(desc, font_size=14).next_to(aperture, DOWN, buff=0.3)
            self.add(aperture, label)

        self.wait(1)
