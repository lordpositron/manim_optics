"""
Test ray bundle animation methods
"""

import numpy as np
from manim import *
from manim_optics import ConvergingLens, RayBundle


class TestRayAnimations(Scene):
    def construct(self):
        """Test different animation methods for ray bundles"""

        # Create a lens
        lens = ConvergingLens(focal_length=2.0, height=2.0, show_focal_points=True)
        lens.shift(RIGHT * 0)

        title = Text("Ray Bundle Animations", font_size=32).to_edge(UP)
        self.add(title, lens)

        # Test 1: animate_fade_in
        subtitle1 = Text("1. Fade In", font_size=24).next_to(title, DOWN)
        self.play(Write(subtitle1))

        rays1 = RayBundle(
            start_points=[np.array([-5, y, 0]) for y in np.linspace(-0.8, 0.8, 5)],
            direction_angle_deg=[0] * 5,
            optical_elements=[lens],
            color=YELLOW,
            stroke_width=2,
        )
        # Don't add to scene - animate_fade_in will add via FadeIn

        self.play(rays1.animate_fade_in(run_time=1.5))
        self.wait(1)

        # Clean up
        self.play(
            rays1.animate_uncreate(run_time=0.5), FadeOut(subtitle1, run_time=0.5)
        )

        # Test 2: animate_create (right to left)
        subtitle2 = Text("2. Create (Right to Left)", font_size=24).next_to(title, DOWN)
        self.play(Write(subtitle2))

        rays2 = RayBundle(
            start_points=[np.array([-5, y, 0]) for y in np.linspace(-0.8, 0.8, 5)],
            direction_angle_deg=[0] * 5,
            optical_elements=[lens],
            color=GREEN,
            stroke_width=2,
        )

        self.play(rays2.animate_create(run_time=2, lag_ratio=0.1))
        self.wait(1)

        # Clean up
        self.play(
            rays2.animate_uncreate(run_time=0.5), FadeOut(subtitle2, run_time=0.5)
        )

        # Test 3: animate_propagation (improved fade-in)
        subtitle3 = Text("3. Propagation (Sequential)", font_size=24).next_to(
            title, DOWN
        )
        self.play(Write(subtitle3))

        rays3 = RayBundle(
            start_points=[np.array([-5, y, 0]) for y in np.linspace(-0.8, 0.8, 5)],
            direction_angle_deg=[0] * 5,
            optical_elements=[lens],
            color=BLUE,
            stroke_width=2,
        )
        # Add to scene first - animate_propagation sets opacity to 0 then fades in
        self.add(rays3)

        self.play(rays3.animate_propagation(run_time=1.5, lag_ratio=0.08))
        self.wait(1)

        # Clean up
        self.play(
            rays3.animate_uncreate(run_time=0.5), FadeOut(subtitle3, run_time=0.5)
        )
        self.wait(0.5)


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
