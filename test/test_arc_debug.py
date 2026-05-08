"""
Debug scene for ArcBeamStop intersection testing
"""

import numpy as np
from manim import *

from manim_optics import *


class DebugArcIntersection(Scene):
    """Visual debug of arc-ray intersection"""

    def construct(self):
        # Create arc at a specific position
        arc = ArcBeamStop(
            radius=2.0,
            arc_angle=120 * DEGREES,
            color=RED,
            stroke_width=6,
        )
        arc.shift(RIGHT * 1)  # Move arc to the right

        # Add arc to scene
        self.add(arc)

        # Show center of curvature
        center_dot = Dot(arc._curvature_center, color=YELLOW, radius=0.08)
        center_label = Text("Center", font_size=16).next_to(center_dot, DOWN)
        self.add(center_dot, center_label)

        # Draw the full circle (dashed) to show curvature
        full_circle = Circle(
            radius=arc.arc_radius,
            color=YELLOW,
            stroke_width=1,
            stroke_opacity=0.3,
        )
        full_circle.move_to(arc._curvature_center)
        self.add(full_circle)

        # Test rays at different heights
        test_rays = []
        y_positions = np.linspace(-2, 2, 9)

        for y in y_positions:
            ray_start = np.array([-4, y, 0])
            ray_dir = np.array([1, 0, 0])

            # Get intersection info
            intersection, hit = arc.intersect(ray_start, ray_dir)
            debug_info = arc.get_debug_info(ray_start, ray_dir)

            # Draw ray
            if hit:
                # Ray stops at intersection
                ray_line = Line(ray_start, intersection, color=GREEN, stroke_width=2)
                # Mark intersection point
                hit_dot = Dot(intersection, color=GREEN, radius=0.05)
                self.add(ray_line, hit_dot)
            else:
                # Ray continues
                ray_end = ray_start + ray_dir * 8
                ray_line = Line(ray_start, ray_end, color=BLUE, stroke_width=2)
                self.add(ray_line)

            # Print debug info
            print(f"\nRay at y={y:.2f}:")
            print(f"  Hit: {hit}")
            if hit:
                print(f"  Intersection: {intersection[:2]}")
            print(f"  Distance to ray: {debug_info['distance_to_ray']:.3f}")
            if "intersections" in debug_info:
                for int_info in debug_info["intersections"]:
                    print(f"  Intersection {int_info['index']}:")
                    print(f"    t={int_info['t']:.3f}")
                    print(f"    angle={int_info['angle_deg']:.1f}°")
                    print(f"    in range: {int_info['in_arc_range']}")

        # Add title
        title = Text("ArcBeamStop Intersection Debug", font_size=24).to_edge(UP)
        self.add(title)

        # Add info
        info = (
            VGroup(
                Text(f"Arc radius: {arc.arc_radius}", font_size=16),
                Text(f"Arc angle: {np.degrees(arc.arc_angle):.0f}°", font_size=16),
                Text(
                    f"Center: ({arc._curvature_center[0]:.1f}, {arc._curvature_center[1]:.1f})",
                    font_size=16,
                ),
            )
            .arrange(DOWN, aligned_edge=LEFT)
            .to_corner(UL, buff=0.5)
        )
        self.add(info)

        self.wait(1)


class TestArcWithRayBundle(Scene):
    """Test ArcBeamStop with actual RayBundle"""

    def construct(self):
        # Create arc
        arc = ArcBeamStop(
            radius=2.0,
            arc_angle=120 * DEGREES,
            color=RED_D,
            stroke_width=4,
        )
        arc.shift(RIGHT * 2)

        # Show center
        center_dot = Dot(arc._curvature_center, color=YELLOW, radius=0.06)

        # Create rays
        rays = RayBundle(
            start_points=[np.array([-3, y, 0]) for y in np.linspace(-2, 2, 11)],
            direction_angle_deg=[0] * 11,
            optical_elements=[arc],
            color=YELLOW,
            stroke_width=2,
        )

        # Grid for reference
        grid = NumberPlane(
            x_range=[-5, 6],
            y_range=[-3, 3],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            },
        )

        self.add(grid, arc, center_dot, rays)

        # Title
        title = Text("ArcBeamStop with RayBundle", font_size=28).to_edge(UP)
        self.add(title)

        self.wait(1)


class CompareOldVsNew(Scene):
    """Compare different positioning methods"""

    def construct(self):
        # Method 1: Direct shift
        arc1 = ArcBeamStop(radius=1.5, arc_angle=90 * DEGREES, color=RED)
        arc1.shift(LEFT * 3 + UP * 1)

        center1 = Dot(arc1._curvature_center, color=YELLOW, radius=0.06)
        label1 = Text("shift()", font_size=16).next_to(arc1, DOWN)

        # Method 2: Create at origin then shift in steps
        arc2 = ArcBeamStop(radius=1.5, arc_angle=90 * DEGREES, color=GREEN)
        arc2.shift(UP * 1)
        arc2.shift(RIGHT * 3)

        center2 = Dot(arc2._curvature_center, color=YELLOW, radius=0.06)
        label2 = Text("shift() x2", font_size=16).next_to(arc2, DOWN)

        # Add rays to both
        for arc, x_offset in [(arc1, -3), (arc2, 3)]:
            for y in [-1, 0, 1]:
                ray_start = np.array([x_offset - 2, y + 1, 0])
                ray_dir = np.array([1, 0, 0])
                intersection, hit = arc.intersect(ray_start, ray_dir)

                if hit:
                    ray = Line(ray_start, intersection, color=GREEN, stroke_width=2)
                    dot = Dot(intersection, color=GREEN, radius=0.04)
                    self.add(ray, dot)
                else:
                    ray = Line(
                        ray_start, ray_start + ray_dir * 4, color=BLUE, stroke_width=2
                    )
                    self.add(ray)

        self.add(arc1, center1, label1, arc2, center2, label2)

        title = Text("ArcBeamStop Positioning Methods", font_size=24).to_edge(UP)
        self.add(title)

        self.wait(1)
