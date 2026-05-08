"""
Simple debug test for CenteredSystem ray hiding
"""

import numpy as np
from manim import *

from manim_optics import CenteredSystem, DynamicRay


class DebugTwoRays(Scene):
    """Simple test with just two rays to debug hiding."""

    def construct(self):
        # Add a grid for better visualization of coordinates
        grid = NumberPlane(
            x_range=[-5, 10, 1],
            y_range=[-3, 3, 1],
            x_length=15,
            y_length=6,
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            },
            axis_config={
                "stroke_color": BLUE_D,
                "stroke_width": 2,
            },
        )
        grid.add_coordinates()
        self.add(grid)

        # Create a simple centered system with boundaries BEFORE H and H'
        system = CenteredSystem(
            h_position=-1.0,
            h_prime_position=1.0,
            focal_length=2.0,
            height=3.0,
            left_boundary_position=-2.0,  # Boundary before H
            right_boundary_position=2.0,  # Boundary after H'
            show_labels=True,
            show_focal_points=True,
            h_color=YELLOW,
            boundary_color=BLUE,
        )

        self.add(system)
        self.wait(0.5)

        # Ray 1: Parallel to axis (y=0.5)
        print("\n=== Creating Ray 1 (parallel) ===")
        ray1 = DynamicRay(
            start_point=np.array([-4.0, 0.5, 0.0]),
            direction=RIGHT,
            optical_elements=[system],
            color=RED,
            ray_length=8.0,
            stroke_width=4,
        )

        # Ray 2: Slightly inclined
        print("\n=== Creating Ray 2 (inclined) ===")
        direction_inclined = np.array([1.0, -0.2, 0.0])
        direction_inclined = direction_inclined / np.linalg.norm(direction_inclined)

        ray2 = DynamicRay(
            start_point=np.array([-4.0, 1.0, 0.0]),
            direction=direction_inclined,
            optical_elements=[system],
            color=GREEN,
            ray_length=8.0,
            stroke_width=4,
        )

        self.play(Create(ray1), Create(ray2))
        self.wait(1)
