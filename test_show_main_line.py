"""
Test scene to demonstrate show_main_line parameter
"""

from manim import *
from manim_optics import *


class TestShowMainLine(Scene):
    """Compare graticules with and without main line"""

    def construct(self):
        # LinearGraticule comparison
        grat_no_line = LinearGraticule(
            length=6,
            unit_length=0.5,
            primary_interval=2,
            secondary_interval=1,
            show_main_line=False,  # Default - graduations only
            color=BLUE,
        ).shift(UP * 2)

        grat_with_line = LinearGraticule(
            length=6,
            unit_length=0.5,
            primary_interval=2,
            secondary_interval=1,
            show_main_line=True,  # Show the axis line
            color=GREEN,
        ).shift(DOWN * 0.5)

        self.play(
            grat_no_line.create_animation(),
            grat_with_line.create_animation()
        )
        self.wait(2)


class TestShowMainLineCross(Scene):
    """Compare cross graticules with and without main lines"""

    def construct(self):
        # Without main lines (default)
        cross_no_lines = CrossGraticule(
            x_length=8,
            y_length=6,
            unit_length=0.5,
            primary_interval=2,
            secondary_interval=1,
            show_main_line=False,
            color=BLUE,
        ).shift(LEFT * 3.5)

        # With main lines
        cross_with_lines = CrossGraticule(
            x_length=8,
            y_length=6,
            unit_length=0.5,
            primary_interval=2,
            secondary_interval=1,
            show_main_line=True,
            color=GREEN,
        ).shift(RIGHT * 3.5)

        self.play(
            cross_no_lines.create_animation(),
            cross_with_lines.create_animation()
        )
        self.wait(2)


class TestShowMainLineGrid(Scene):
    """Compare grid graticules with and without frame"""

    def construct(self):
        # Without frame (default)
        grid_no_frame = GridGraticule(
            width=6,
            height=5,
            unit_length=0.5,
            primary_interval=2,
            secondary_interval=1,
            show_main_line=False,
            color=BLUE,
        ).shift(LEFT * 3.5)

        # With frame
        grid_with_frame = GridGraticule(
            width=6,
            height=5,
            unit_length=0.5,
            primary_interval=2,
            secondary_interval=1,
            show_main_line=True,
            color=GREEN,
        ).shift(RIGHT * 3.5)

        self.play(
            grid_no_frame.create_animation(),
            grid_with_frame.create_animation()
        )
        self.wait(2)
