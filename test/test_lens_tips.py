from manim import *

from manim_optics import ConvergingLens, DivergingLens


class TestLensTips(Scene):
    def construct(self):
        # Converging lens
        lens1 = ConvergingLens(focal_length=3.0, height=4.0, color=RED)
        lens1.shift(LEFT * 3)

        # Diverging lens
        lens2 = DivergingLens(focal_length=-3.0, height=4.0, color=BLUE)
        lens2.shift(RIGHT * 3)

        # Labels
        label1 = Text("Convergente", font_size=24).next_to(lens1, DOWN)
        label2 = Text("Divergente", font_size=24).next_to(lens2, DOWN)

        self.add(lens1, lens2, label1, label2)

        # Grid for reference
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

        # Debug: print lens1 components
        print("\n=== LENS1 (Converging) ===")
        print(f"Number of submobjects: {len(lens1.submobjects)}")
        for i, submob in enumerate(lens1.submobjects):
            print(f"  [{i}] {type(submob).__name__}")
            if hasattr(submob, "get_start") and hasattr(submob, "get_end"):
                print(f"      Start: {submob.get_start()}")
                print(f"      End: {submob.get_end()}")
                print(f"      Stroke width: {submob.get_stroke_width()}")
                print(f"      Color: {submob.get_color()}")

        self.wait(1)
