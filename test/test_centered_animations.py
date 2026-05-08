"""
Test animations with CenteredSystem and DynamicRay
===================================================

Test 3 types of animations:
1. Fixed rays, moving system
2. Fixed rays, changing focal length
3. Fixed system, changing ray directions
"""

import numpy as np
from manim import *

from manim_optics import CenteredSystem, DynamicRay


class TestSystemMoving(Scene):
    """Animation 1: Rayons fixes, système se déplace."""

    def construct(self):
        # Create coordinate grid for reference
        grid = NumberPlane(
            x_range=[-6, 10, 1],
            y_range=[-3, 3, 1],
            x_length=16,
            y_length=6,
            background_line_style={"stroke_opacity": 0.3},
        )
        grid.add_coordinates()
        self.add(grid)

        # Create centered system
        system = CenteredSystem(
            h_position=1.0,
            h_prime_position=-1.0,
            focal_length=3.0,
            height=3.0,
            left_boundary_position=-1.5,
            right_boundary_position=1.5,
            show_labels=True,
            show_focal_points=True,
        )

        # Create two fixed rays
        ray1 = DynamicRay(
            start_point=np.array([-5.0, 0.5, 0.0]),
            direction=RIGHT,
            optical_elements=[system],
            color=YELLOW,
        )

        ray2 = DynamicRay(
            start_point=np.array([-5.0, 1.0, 0.0]),
            direction=RIGHT + DOWN * 0.2,
            optical_elements=[system],
            color=BLUE,
        )

        # Show initial state
        self.play(
            system.create(),
            Create(ray1),
            Create(ray2),
        )
        self.wait(0.5)

        # Animation: Move system to the right
        self.play(system.animate_system_position(1.0, 3.0, run_time=2.0))
        self.wait(0.5)

        # Animation: Move system back to center
        self.play(system.animate_system_position(-0.5, 1.5, run_time=2.0))
        self.wait(1)


class TestFocalLengthChanging(Scene):
    """Animation 2: Rayons fixes, focale change."""

    def construct(self):
        # Create coordinate grid for reference
        grid = NumberPlane(
            x_range=[-6, 10, 1],
            y_range=[-3, 3, 1],
            x_length=16,
            y_length=6,
            background_line_style={"stroke_opacity": 0.3},
        )
        grid.add_coordinates()
        self.add(grid)

        # Create centered system
        system = CenteredSystem(
            h_position=-1.0,
            h_prime_position=1.0,
            focal_length=3.0,
            height=3.0,
            show_labels=True,
            show_focal_points=True,
        )

        # Create two fixed rays
        ray1 = DynamicRay(
            start_point=np.array([-5.0, 0.5, 0.0]),
            direction=RIGHT,
            optical_elements=[system],
            color=YELLOW,
        )

        ray2 = DynamicRay(
            start_point=np.array([-5.0, 1.0, 0.0]),
            direction=RIGHT + DOWN * 0.2,
            optical_elements=[system],
            color=BLUE,
        )

        # Show initial state
        self.play(
            system.create(),
            Create(ray1),
            Create(ray2),
        )
        self.wait(0.5)

        # Animation: Increase focal length (system becomes weaker)
        self.play(system.animate_focal_length(5.0, run_time=2.0))
        self.wait(0.5)

        # Animation: Decrease focal length (system becomes stronger)
        self.play(system.animate_focal_length(2.0, run_time=2.0))
        self.wait(0.5)

        # Animation: Back to original
        self.play(system.animate_focal_length(3.0, run_time=2.0))
        self.wait(1)


class TestRayDirectionChanging(Scene):
    """Animation 3: Système fixe, direction des rayons change."""

    def construct(self):
        # Create coordinate grid for reference
        grid = NumberPlane(
            x_range=[-6, 10, 1],
            y_range=[-3, 3, 1],
            x_length=16,
            y_length=6,
            background_line_style={"stroke_opacity": 0.3},
        )
        grid.add_coordinates()
        self.add(grid)

        # Create centered system (fixed)
        system = CenteredSystem(
            h_position=-1.0,
            h_prime_position=1.0,
            focal_length=3.0,
            height=3.0,
            show_labels=True,
            show_focal_points=True,
        )

        # Create ValueTrackers for ray directions
        ray1_angle_tracker = ValueTracker(0)  # Horizontal
        ray2_angle_tracker = ValueTracker(-11.3)  # ~-0.2 radians

        # Create dynamic rays with direction functions
        def get_ray1_direction():
            angle = ray1_angle_tracker.get_value() * DEGREES
            return np.array([np.cos(angle), np.sin(angle), 0.0])

        def get_ray2_direction():
            angle = ray2_angle_tracker.get_value() * DEGREES
            return np.array([np.cos(angle), np.sin(angle), 0.0])

        ray1 = DynamicRay(
            start_point=np.array([-5.0, 0.5, 0.0]),
            direction=get_ray1_direction,
            optical_elements=[system],
            color=YELLOW,
        )

        ray2 = DynamicRay(
            start_point=np.array([-5.0, 1.0, 0.0]),
            direction=get_ray2_direction,
            optical_elements=[system],
            color=BLUE,
        )

        # Show initial state
        self.play(
            system.create(),
            Create(ray1),
            Create(ray2),
        )
        self.wait(0.5)

        # Animation: Ray 1 tilts down
        self.play(ray1_angle_tracker.animate.set_value(-15), run_time=2.0)
        self.wait(0.5)

        # Animation: Ray 2 tilts up
        self.play(ray2_angle_tracker.animate.set_value(10), run_time=2.0)
        self.wait(0.5)

        # Animation: Both rays return to original
        self.play(
            ray1_angle_tracker.animate.set_value(0),
            ray2_angle_tracker.animate.set_value(-11.3),
            run_time=2.0,
        )
        self.wait(1)


class TestAllAnimationsCombined(Scene):
    """Animation combinée: tout bouge en même temps."""

    def construct(self):
        # Create coordinate grid for reference
        grid = NumberPlane(
            x_range=[-6, 10, 1],
            y_range=[-3, 3, 1],
            x_length=16,
            y_length=6,
            background_line_style={"stroke_opacity": 0.3},
        )
        grid.add_coordinates()
        self.add(grid)

        # Create centered system
        system = CenteredSystem(
            h_position=-1.0,
            h_prime_position=1.0,
            focal_length=3.0,
            height=3.0,
            show_labels=True,
            show_focal_points=True,
        )

        # Create ValueTrackers for ray directions
        ray1_angle_tracker = ValueTracker(0)
        ray2_angle_tracker = ValueTracker(-11.3)

        def get_ray1_direction():
            angle = ray1_angle_tracker.get_value() * DEGREES
            return np.array([np.cos(angle), np.sin(angle), 0.0])

        def get_ray2_direction():
            angle = ray2_angle_tracker.get_value() * DEGREES
            return np.array([np.cos(angle), np.sin(angle), 0.0])

        ray1 = DynamicRay(
            start_point=np.array([-5.0, 0.5, 0.0]),
            direction=get_ray1_direction,
            optical_elements=[system],
            color=YELLOW,
        )

        ray2 = DynamicRay(
            start_point=np.array([-5.0, 1.0, 0.0]),
            direction=get_ray2_direction,
            optical_elements=[system],
            color=BLUE,
        )

        # Show initial state
        self.play(
            system.create(),
            Create(ray1),
            Create(ray2),
        )
        self.wait(0.5)

        # Animation: Tout bouge en même temps !
        self.play(
            system.animate_system_position(0.5, 2.5, run_time=3.0),
            system.animate_focal_length(4.0, run_time=3.0),
            ray1_angle_tracker.animate.set_value(-10),
            ray2_angle_tracker.animate.set_value(5),
            run_time=3.0,
        )
        self.wait(1)
