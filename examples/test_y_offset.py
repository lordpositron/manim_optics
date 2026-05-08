"""
Test scene for y_offset_tracker functionality
"""

from manim import *

from manim_optics import *


class TestYOffsetTracker(Scene):
    """Test dynamic y_offset changes on ray bundle"""

    def construct(self):
        # Create a lens
        lens = ConvergingLens(focal_length=2.0, height=3.0, color=BLUE_C)
        lens.shift(RIGHT * 1)

        # Create ray bundle with y_offset_tracker
        bundle = RayBundle(
            start_points=[np.array([-4, y, 0]) for y in np.linspace(-1, 1, 7)],
            direction_angle_deg=[0] * 7,
            optical_elements=[lens],
            color=YELLOW,
            stroke_width=2,
        )

        # Add objects to scene
        self.add(lens, bundle)

        # Show initial state
        self.wait(0.5)

        # Animate y_offset changing from 0 to 1
        self.play(
            bundle.y_offset_tracker.animate.set_value(1.0), run_time=2, rate_func=smooth
        )
        self.wait(0.5)

        # Animate y_offset changing from 1 to -1
        self.play(
            bundle.y_offset_tracker.animate.set_value(-1.0),
            run_time=3,
            rate_func=smooth,
        )
        self.wait(0.5)

        # Return to 0
        self.play(
            bundle.y_offset_tracker.animate.set_value(0), run_time=2, rate_func=smooth
        )
        self.wait(0.5)


class TestBothOffsets(Scene):
    """Test both y_offset and angle_offset simultaneously"""

    def construct(self):
        # Create a lens
        lens = ConvergingLens(focal_length=2.0, height=3.0, color=BLUE_C)
        lens.shift(RIGHT * 1)

        # Create ray bundle
        bundle = RayBundle(
            start_points=np.array([-4, 0, 0]),
            direction_angle_deg=np.linspace(-20, 20, 9),
            optical_elements=[lens],
            color=YELLOW,
            stroke_width=2,
        )

        # Add to scene
        self.add(lens, bundle)

        # Title
        title = Text("Dynamic Ray Control", font_size=36).to_edge(UP)
        self.add(title)

        self.wait(0.5)

        # Move rays up and rotate them
        self.play(
            bundle.y_offset_tracker.animate.set_value(0.8),
            bundle.angle_offset_tracker.animate.set_value(15),
            run_time=2,
            rate_func=smooth,
        )
        self.wait(0.5)

        # Move rays down and rotate opposite direction
        self.play(
            bundle.y_offset_tracker.animate.set_value(-0.8),
            bundle.angle_offset_tracker.animate.set_value(-15),
            run_time=3,
            rate_func=smooth,
        )
        self.wait(0.5)

        # Return to center
        self.play(
            bundle.y_offset_tracker.animate.set_value(0),
            bundle.angle_offset_tracker.animate.set_value(0),
            run_time=2,
            rate_func=smooth,
        )
        self.wait(1)
