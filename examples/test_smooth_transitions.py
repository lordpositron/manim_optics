"""
Test scene comparing abrupt vs smooth optical element transitions
"""

from manim import *

from manim_optics import *


class TestAbruptTransition(Scene):
    """Sans animation - transition abrupte"""

    def construct(self):
        # Create rays
        rays = RayBundle(
            start_points=np.array([-6, 0, 0]),
            directions=[
                np.array([1, 0.3, 0]),
                np.array([1, 0.15, 0]),
                np.array([1, 0, 0]),
                np.array([1, -0.15, 0]),
                np.array([1, -0.3, 0]),
            ],
            optical_elements=[],
            color=YELLOW,
        )

        lens = ConvergingLens(focal_length=2.5, height=3, color=BLUE).shift(LEFT * 1)

        self.play(rays.animate_propagation())
        self.wait()

        # ABRUPT: Add element without animation
        self.play(Create(lens))
        rays.add_optical_element(lens)  # Changement brusque !
        self.wait(2)

        # ABRUPT: Remove element
        self.play(FadeOut(lens))
        rays.remove_optical_element(lens)
        self.wait(2)


class TestSmoothTransition(Scene):
    """Avec animation - transition douce"""

    def construct(self):
        # Create rays
        rays = RayBundle(
            start_points=np.array([-6, 0, 0]),
            directions=[
                np.array([1, 0.3, 0]),
                np.array([1, 0.15, 0]),
                np.array([1, 0, 0]),
                np.array([1, -0.15, 0]),
                np.array([1, -0.3, 0]),
            ],
            optical_elements=[],
            color=YELLOW,
        )

        lens = ConvergingLens(focal_length=2.5, height=3, color=BLUE).shift(LEFT * 1)

        self.play(rays.animate_propagation())
        self.wait()

        # SMOOTH: Add element with animation
        self.play(
            Create(lens),
            rays.animate_add_optical_element(lens, run_time=3.0),
        )
        self.wait(2)

        # SMOOTH: Remove element with animation
        self.play(
            FadeOut(lens),
            rays.animate_remove_optical_element(lens, run_time=3.0),
        )
        self.wait(2)


class TestMultipleElements(Scene):
    """Test avec plusieurs éléments - transitions douces"""

    def construct(self):
        rays = RayBundle(
            start_points=np.array([-6, 0, 0]),
            directions=[
                np.array([1, 0.4, 0]),
                np.array([1, 0.2, 0]),
                np.array([1, 0, 0]),
                np.array([1, -0.2, 0]),
                np.array([1, -0.4, 0]),
            ],
            optical_elements=[],
            color=YELLOW,
        )

        self.play(rays.animate_propagation())
        self.wait()

        # Add first lens smoothly
        lens1 = ConvergingLens(focal_length=2, height=3, color=BLUE).shift(LEFT * 2)
        self.play(
            Create(lens1),
            rays.animate_add_optical_element(lens1, run_time=0.8),
        )
        self.wait()

        # Add second element smoothly
        lens2 = DivergingLens(focal_length=-2, height=3, color=RED).shift(RIGHT * 1)
        self.play(
            Create(lens2),
            rays.animate_add_optical_element(lens2, run_time=0.8),
        )
        self.wait()

        # Add mirror smoothly
        mirror = PlaneMirror(height=3, color=GREEN).shift(RIGHT * 4)
        self.play(
            Create(mirror),
            rays.animate_add_optical_element(mirror, run_time=0.8),
        )
        self.wait()

        # Remove first lens smoothly
        self.play(
            FadeOut(lens1),
            rays.animate_remove_optical_element(lens1, run_time=0.8),
        )
        self.wait(2)


class TestSequentialRays(Scene):
    """Test avec lag_ratio pour effet séquentiel"""

    def construct(self):
        rays = RayBundle(
            start_points=np.array([-6, 0, 0]),
            directions=[
                np.array([1, 0.5, 0]),
                np.array([1, 0.25, 0]),
                np.array([1, 0, 0]),
                np.array([1, -0.25, 0]),
                np.array([1, -0.5, 0]),
            ],
            optical_elements=[],
            color=YELLOW,
        )

        self.play(rays.animate_propagation())
        self.wait()

        lens = ConvergingLens(focal_length=2.5, height=4, color=BLUE)

        # Transition séquentielle (lag_ratio = 0.1)
        self.play(
            Create(lens),
            rays.animate_add_optical_element(lens, run_time=1.5, lag_ratio=0.1),
        )
        self.wait(2)

        # Remove séquentiel
        self.play(
            FadeOut(lens),
            rays.animate_remove_optical_element(lens, run_time=1.5, lag_ratio=0.1),
        )
        self.wait(2)


class TestSingleRaySmooth(Scene):
    """Test avec un seul rayon"""

    def construct(self):
        ray = DynamicRay(
            start_point=np.array([-6, 0, 0]),
            direction=np.array([1, 0.3, 0]),
            optical_elements=[],
            color=YELLOW,
        )

        self.play(ray.animate_propagation())
        self.wait()

        # Add lens smoothly
        lens = ConvergingLens(focal_length=2, height=3, color=BLUE)
        self.play(
            Create(lens),
            ray.animate_add_optical_element(lens, run_time=0.8),
        )
        self.wait()

        # Add mirror smoothly
        mirror = (
            PlaneMirror(height=3, color=GREEN).shift(RIGHT * 3).rotate(15 * DEGREES)
        )
        self.play(
            Create(mirror),
            ray.animate_add_optical_element(mirror, run_time=0.8),
        )
        self.wait()

        # Remove lens
        self.play(
            FadeOut(lens),
            ray.animate_remove_optical_element(lens, run_time=0.8),
        )
        self.wait(2)
