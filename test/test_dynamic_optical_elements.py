"""
Test scene to demonstrate dynamic optical element updates
"""

from manim import *
from manim_optics import *


class TestDynamicOpticalElements(Scene):
    """Test updating optical elements during a scene"""

    def construct(self):
        # Create a ray bundle
        rays = RayBundle(
            start_points=np.array([-6, 0, 0]),
            directions=[
                np.array([1, 0.3, 0]),
                np.array([1, 0.15, 0]),
                np.array([1, 0, 0]),
                np.array([1, -0.15, 0]),
                np.array([1, -0.3, 0]),
            ],
            optical_elements=[],  # Start with no elements
            color=YELLOW,
        )

        # Create optical elements
        lens1 = ConvergingLens(focal_length=2, height=3, color=BLUE).shift(LEFT * 2)
        lens2 = DivergingLens(focal_length=-2, height=3, color=RED).shift(RIGHT * 2)
        mirror = PlaneMirror(height=3, color=GREEN).shift(RIGHT * 4)

        # Show rays without any optical elements
        self.play(rays.animate_propagation())
        self.wait()

        # Add first lens
        self.play(Create(lens1))
        rays.add_optical_element(lens1)
        self.wait(2)

        # Add second lens
        self.play(Create(lens2))
        rays.add_optical_element(lens2)
        self.wait(2)

        # Add mirror
        self.play(Create(mirror))
        rays.add_optical_element(mirror)
        self.wait(2)

        # Remove first lens
        self.play(FadeOut(lens1))
        rays.remove_optical_element(lens1)
        self.wait(2)

        # Replace all optical elements
        self.play(FadeOut(lens2), FadeOut(mirror))

        new_lens = ConvergingLens(focal_length=3, height=4, color=PURPLE).shift(
            UP * 0.5
        )
        self.play(Create(new_lens))
        rays.set_optical_elements([new_lens])
        self.wait(2)


class TestDynamicWithMovingElements(Scene):
    """Test that rays update when elements move"""

    def construct(self):
        # Create lens
        lens = ConvergingLens(focal_length=2.5, height=4, color=BLUE)

        # Create rays
        rays = RayBundle(
            start_points=np.array([-6, 0, 0]),
            directions=[
                np.array([1, 0.4, 0]),
                np.array([1, 0.2, 0]),
                np.array([1, 0, 0]),
                np.array([1, -0.2, 0]),
                np.array([1, -0.4, 0]),
            ],
            optical_elements=[lens],
            color=YELLOW,
        )

        self.play(Create(lens), rays.animate_propagation())
        self.wait()

        # Move lens - rays should update automatically
        self.play(lens.animate.shift(RIGHT * 2), run_time=2)
        self.wait()

        # Add a second element dynamically
        mirror = PlaneMirror(height=3, color=GREEN).shift(RIGHT * 4)
        self.play(Create(mirror))
        rays.add_optical_element(mirror)
        self.wait()

        # Move both elements
        self.play(
            lens.animate.shift(UP * 1), mirror.animate.shift(DOWN * 0.5), run_time=2
        )
        self.wait(2)


class TestDynamicSingleRay(Scene):
    """Test dynamic optical elements with a single DynamicRay"""

    def construct(self):
        # Create a single ray
        ray = DynamicRay(
            start_point=np.array([-6, 0, 0]),
            direction=np.array([1, 0.2, 0]),
            optical_elements=[],
            color=YELLOW,
        )

        self.play(ray.animate_propagation())
        self.wait()

        # Add elements one by one
        lens = ConvergingLens(focal_length=2, height=3, color=BLUE).shift(LEFT * 1)
        self.play(Create(lens))
        ray.add_optical_element(lens)
        self.wait()

        mirror = (
            PlaneMirror(height=3, color=GREEN).shift(RIGHT * 2.5).rotate(20 * DEGREES)
        )
        self.play(Create(mirror))
        ray.add_optical_element(mirror)
        self.wait()

        # Remove and replace
        screen = LineBeamStop(height=4, color=RED).shift(RIGHT * 5)
        self.play(FadeOut(mirror), Create(screen))
        ray.remove_optical_element(mirror)
        ray.add_optical_element(screen)
        self.wait(2)
