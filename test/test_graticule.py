"""
Test scenes for Graticule classes
"""

from manim import *
from manim_optics import *


class TestLinearGraticule(Scene):
    """Test the LinearGraticule class"""

    def construct(self):
        # Create a simple linear graticule
        graticule = LinearGraticule(
            length=8,
            unit_length=0.5,
            primary_interval=2,
            secondary_interval=1,
            color=BLUE,
        )

        # Animate appearance
        self.play(graticule.create_animation(run_time=2))
        self.wait()

        # Test with different settings
        graticule2 = LinearGraticule(
            direction=UP,
            length=6,
            unit_length=0.4,
            primary_interval=5,
            secondary_interval=1,
            tick_position="outside",
            color=GREEN,
            show_labels=True,
            decimal_places=0,
        )
        graticule2.shift(RIGHT * 4)

        self.play(graticule2.create_animation(run_time=2))
        self.wait()

        # Fade out
        self.play(graticule.fade_out_animation(), graticule2.fade_out_animation())
        self.wait()


class TestCrossGraticule(Scene):
    """Test the CrossGraticule class"""

    def construct(self):
        # Create cross graticule (Cartesian axes style)
        cross = CrossGraticule(
            length=10,
            unit_length=0.5,
            primary_interval=2,
            secondary_interval=1,
            tick_position="centered",
            color=WHITE,
            show_labels=True,
            decimal_places=0,
        )

        # Animate appearance
        self.play(cross.create_animation(run_time=2.5, lag_ratio=0.1))
        self.wait()

        # Add a point to measure
        point = Dot([2, 1.5, 0], color=YELLOW, radius=0.1)
        point_label = Text("Point", font_size=20, color=YELLOW).next_to(point, UR)

        self.play(FadeIn(point), Write(point_label))
        self.wait()

        # Fade out
        self.play(FadeOut(VGroup(cross, point, point_label)))
        self.wait()


class TestGridGraticule(Scene):
    """Test the GridGraticule class"""

    def construct(self):
        # Create grid graticule
        grid = GridGraticule(
            width=10,
            height=6,
            unit_length=0.5,
            primary_interval=2,
            secondary_interval=1,
            color=BLUE_D,
            grid_stroke_width=0.8,
            show_labels=True,
            decimal_places=0,
        )

        # Animate appearance
        self.play(grid.create_animation(run_time=3, lag_ratio=0.02))
        self.wait()

        # Add some objects to show the grid's utility
        circle = Circle(radius=1.5, color=YELLOW, stroke_width=3)
        circle.shift(LEFT * 2 + UP * 0.5)

        square = Square(side_length=2, color=RED, stroke_width=3)
        square.shift(RIGHT * 2 + DOWN * 0.5)

        self.play(Create(circle), Create(square))
        self.wait()

        # Fade out
        self.play(FadeOut(VGroup(grid, circle, square)))
        self.wait()


class TestGraticuleVariations(Scene):
    """Test various graticule configurations"""

    def construct(self):
        # Different tick positions
        configs = [
            ("Inside", "inside", LEFT * 4),
            ("Centered", "centered", ORIGIN),
            ("Outside", "outside", RIGHT * 4),
        ]

        graticules = []
        labels = []

        for name, position, shift in configs:
            grat = LinearGraticule(
                length=4,
                unit_length=0.4,
                primary_interval=2,
                secondary_interval=1,
                tick_position=position,
                color=BLUE,
                show_labels=False,
            )
            grat.shift(shift)
            graticules.append(grat)

            label = Text(name, font_size=24).next_to(grat, DOWN, buff=0.5)
            labels.append(label)

        # Animate all
        self.play(
            *[g.create_animation(run_time=1.5) for g in graticules],
            *[Write(l) for l in labels],
        )
        self.wait(2)

        # Clear
        self.play(
            *[FadeOut(g) for g in graticules],
            *[FadeOut(l) for l in labels],
        )
        self.wait()


class TestGraticuleWithOptics(Scene):
    """Test graticule with optical elements"""

    def construct(self):
        # Title
        title = Text("Graticule + Optics", font_size=32).to_edge(UP)
        self.add(title)

        # Create a grid background
        grid = GridGraticule(
            width=12,
            height=6,
            unit_length=0.5,
            primary_interval=2,
            secondary_interval=1,
            color=GREY_D,
            grid_stroke_width=0.5,
            show_labels=False,
        )

        self.play(grid.create_animation(run_time=1.5, lag_ratio=0.01))

        # Add a lens
        lens = ConvergingLens(focal_length=2.0, height=3.0, color=BLUE_C)
        lens.shift(RIGHT * 1)

        # Add rays
        rays = RayBundle(
            start_points=[np.array([-5, y, 0]) for y in np.linspace(-1, 1, 5)],
            direction_angle_deg=[0] * 5,
            optical_elements=[lens],
            color=YELLOW,
            stroke_width=2,
        )

        self.play(lens.create())
        self.play(rays.animate_propagation(run_time=2))
        self.wait()

        # Add measurement graticule at focal point
        focal_graticule = LinearGraticule(
            direction=UP,
            length=4,
            unit_length=0.5,
            primary_interval=1,
            secondary_interval=0.5,
            tick_position="centered",
            color=RED,
            show_labels=True,
            decimal_places=1,
            label_font_size=14,
        )
        focal_graticule.shift(RIGHT * 3)

        self.play(focal_graticule.create_animation(run_time=1))
        self.wait(2)

        # Fade all
        self.play(FadeOut(VGroup(grid, lens, rays, focal_graticule)))
        self.wait()


class TestGraticuleAngles(Scene):
    """Test graticule with different angles"""

    def construct(self):
        # Title
        title = Text("Angled Graticules", font_size=36).to_edge(UP)
        self.add(title)

        # Graticule with angled ticks
        grat1 = LinearGraticule(
            length=6,
            unit_length=0.5,
            primary_interval=2,
            secondary_interval=1,
            tick_angle=60 * DEGREES,  # 60° ticks
            color=BLUE,
            show_labels=True,
            decimal_places=0,
        )
        grat1.shift(UP * 1.5)

        # Graticule with global rotation
        grat2 = LinearGraticule(
            length=6,
            unit_length=0.5,
            primary_interval=2,
            secondary_interval=1,
            global_angle=30 * DEGREES,  # Entire graticule rotated 30°
            color=GREEN,
            show_labels=True,
            decimal_places=0,
        )
        grat2.shift(DOWN * 1.5)

        label1 = Text("Tick angle: 60°", font_size=20).next_to(grat1, DOWN, buff=0.3)
        label2 = Text("Global rotation: 30°", font_size=20).next_to(
            grat2, DOWN, buff=0.3
        )

        self.play(
            grat1.create_animation(run_time=2),
            grat2.create_animation(run_time=2),
            Write(label1),
            Write(label2),
        )
        self.wait(2)

        self.play(FadeOut(VGroup(grat1, grat2, label1, label2)))
        self.wait()
