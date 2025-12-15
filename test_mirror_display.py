import numpy as np
from manim import *
from manim_optics import SphericalMirror


class TestMirrorDisplay(Scene):
    def construct(self):
        # Test different mirror configurations

        # Concave mirror (R > 0), side left
        mirror1 = SphericalMirror(
            position=np.array([-4, 0, 0]),
            radius_of_curvature=3,
            height=4,
            side="left",
        )

        # Convex mirror (R < 0), side left
        mirror2 = SphericalMirror(
            position=np.array([0, 0, 0]),
            radius_of_curvature=-3,
            height=4,
            side="left",
        )

        # Concave mirror (R > 0), side right
        mirror3 = SphericalMirror(
            position=np.array([4, 0, 0]),
            radius_of_curvature=3,
            height=4,
            side="right",
        )

        # Add labels
        label1 = Text("Concave\nside=left", font_size=16).next_to(
            mirror1, DOWN, buff=0.3
        )
        label2 = Text("Convex\nside=left", font_size=16).next_to(
            mirror2, DOWN, buff=0.3
        )
        label3 = Text("Concave\nside=right", font_size=16).next_to(
            mirror3, DOWN, buff=0.3
        )

        self.add(mirror1, mirror2, mirror3)
        self.add(label1, label2, label3)

        # Add grid for reference
        grid = NumberPlane(
            x_range=[-7, 7],
            y_range=[-4, 4],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            },
        )
        self.add(grid)

        # Debug: Print mirror components
        print("\n=== MIRROR 1 (Concave, side=left) ===")
        print(f"Number of submobjects: {len(mirror1.submobjects)}")
        for i, submob in enumerate(mirror1.submobjects):
            print(f"  Submobject {i}: {type(submob).__name__}")
            if isinstance(submob, Line):
                print(f"    Start: {submob.get_start()}")
                print(f"    End: {submob.get_end()}")
                print(f"    Length: {submob.get_length()}")
            elif isinstance(submob, Dot):
                print(f"    Center: {submob.get_center()}")
                print(f"    Radius: {submob.radius}")

        print("\n=== MIRROR 2 (Convex, side=left) ===")
        print(f"Number of submobjects: {len(mirror2.submobjects)}")
        for i, submob in enumerate(mirror2.submobjects):
            print(f"  Submobject {i}: {type(submob).__name__}")
            if isinstance(submob, Line):
                print(f"    Start: {submob.get_start()}")
                print(f"    End: {submob.get_end()}")
                print(f"    Length: {submob.get_length()}")

        # Check the mirror_line specifically
        print("\n=== MIRROR_LINE INFO ===")
        print(f"Mirror1 mirror_line: {mirror1.mirror_line}")
        print(f"  Start: {mirror1.mirror_line.get_start()}")
        print(f"  End: {mirror1.mirror_line.get_end()}")
        print(f"  Center: {mirror1.mirror_line.get_center()}")
        print(f"  Length: {mirror1.mirror_line.get_length()}")

        self.wait(1)
