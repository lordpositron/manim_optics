"""
Debug test for focal length animation issue
"""

import numpy as np
from manim import *
from manim_optics import ConvergingLens, RayBundle


class TestFocalDebug(Scene):
    def construct(self):
        # Create a simple lens at x=0
        lens = ConvergingLens(focal_length=2.0, height=2.0, show_focal_points=True)
        lens.move_to(ORIGIN)

        # Add a visual marker at lens position (should stay fixed)
        lens_marker = Line(
            UP * 1.5, DOWN * 1.5, color=RED, stroke_width=6, stroke_opacity=0.3
        )
        lens_marker.move_to(ORIGIN)

        # Create a single central ray for precise observation
        rays = RayBundle(
            start_points=[np.array([-5, 0.5, 0])],
            direction_angle_deg=[0],
            optical_elements=[lens],
            color=YELLOW,
            stroke_width=3,
        )

        # Add lens position marker (should stay at x=0)
        position_text = always_redraw(
            lambda: Text(
                f"Lens x = {lens.get_center()[0]:.3f}", font_size=18, color=GREEN
            ).to_corner(UL, buff=0.5)
        )

        # Add focal length info
        focal_text = always_redraw(
            lambda: Text(f"f = {lens.focal_length:.3f}", font_size=18).next_to(
                position_text, DOWN, aligned_edge=LEFT, buff=0.2
            )
        )

        # Add tracker value for debugging
        tracker_text = always_redraw(
            lambda: Text(
                f"tracker = {lens.focal_length_tracker.get_value():.3f}",
                font_size=18,
                color=RED,
            ).next_to(focal_text, DOWN, aligned_edge=LEFT, buff=0.2)
        )

        # Add intersection point marker
        def get_ray_intersection():
            points = rays.rays[0].get_points()
            if len(points) >= 2:
                # Find the bend point (should be at lens)
                for i in range(len(points) - 1):
                    p1, p2 = points[i], points[i + 1]
                    # Check if there's a direction change (bend)
                    if i > 0:
                        p0 = points[i - 1]
                        dir1 = (p1 - p0) / np.linalg.norm(p1 - p0 + 1e-10)
                        dir2 = (p2 - p1) / np.linalg.norm(p2 - p1 + 1e-10)
                        angle_diff = np.arccos(np.clip(np.dot(dir1, dir2), -1, 1))
                        if angle_diff > 0.01:  # Significant bend
                            return p1
            return ORIGIN

        intersection_dot = always_redraw(
            lambda: Dot(get_ray_intersection(), color=BLUE, radius=0.08)
        )

        intersection_x_text = always_redraw(
            lambda: Text(
                f"Bend x = {get_ray_intersection()[0]:.3f}", font_size=18, color=BLUE
            ).next_to(tracker_text, DOWN, aligned_edge=LEFT, buff=0.2)
        )

        self.add(
            lens_marker,
            lens,
            rays,
            position_text,
            focal_text,
            tracker_text,
            intersection_dot,
            intersection_x_text,
        )
        self.wait(1)

        # Animate focal length DECREASE (should bend AT x=0)
        self.play(lens.animate_focal_length(1.0, run_time=3))
        self.wait(1)

        # Animate focal length INCREASE (should still bend AT x=0)
        self.play(lens.animate_focal_length(3.0, run_time=3))
        self.wait(1)
