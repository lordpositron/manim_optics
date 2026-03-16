"""
Test ray bundle animation methods
"""

import numpy as np
from manim import *
from manim_optics import ConvergingLens, RayBundle


class TestRayAnimations(Scene):
    """
    Simple demonstration of ray bundle animations.

    Based on README example: animate rays appearing and focal length changes.
    Shows the core feature of manim_optics: rays automatically track lens changes.
    """

    def construct(self):
        # Setup: lens with focal points visible
        lens = ConvergingLens(focal_length=2.0, height=2.0, show_focal_points=True)

        # Ray bundle: parallel rays from the left
        rays = RayBundle(
            start_points=[np.array([-5, y, 0]) for y in np.linspace(-0.8, 0.8, 5)],
            direction_angle_deg=[0] * 5,
            optical_elements=[lens],
            color=YELLOW,
            stroke_width=2,
        )

        # Add to scene and animate rays appearing
        self.add(lens)
        self.play(rays.animate_fade_in(run_time=1.0))
        self.wait(0.5)

        # Animate focal length: rays automatically track
        self.play(lens.animate_focal_length(3.0, run_time=2.0))
        self.wait(1)

        # Change back to shorter focal length
        self.play(lens.animate_focal_length(1.5, run_time=2.0))
        self.wait(1)


class TestDynamicRayWithFocal(Scene):
    """Test that rays maintain correct trajectory during focal length animation"""

    def construct(self):
        lens = ConvergingLens(focal_length=2.0, height=2.0, show_focal_points=True)

        title = Text("Rays with Focal Animation", font_size=32).to_edge(UP)
        self.add(title, lens)

        # Create rays - they should appear with correct trajectory
        rays = RayBundle(
            start_points=[np.array([-5, y, 0]) for y in np.linspace(-0.5, 0.5, 3)],
            direction_angle_deg=[0] * 3,
            optical_elements=[lens],
            color=YELLOW,
            stroke_width=2,
        )

        # Animate rays appearing - should have correct trajectory immediately
        self.play(rays.animate_fade_in(run_time=1))
        self.wait(1)

        # Change focal length - rays should stay correct
        self.play(lens.animate_focal_length(3.0, run_time=2))
        self.wait(1)

        # Change back
        self.play(lens.animate_focal_length(1.5, run_time=2))
        self.wait(1)
