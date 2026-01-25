"""
Test custom boundary positions and heights for CenteredSystem
"""

from manim import *
from manim_optics import CenteredSystem, DynamicRay
import numpy as np


class TestCustomBoundaries(Scene):
    """Test with custom boundary positions and heights."""

    def construct(self):
        # Système avec boundaries personnalisées
        # Boundary gauche plus grande et décalée
        # Boundary droite plus petite
        system = CenteredSystem(
            h_position=-1.0,
            h_prime_position=1.0,
            focal_length=3.0,
            height=3.0,  # Hauteur par défaut des plans H et H'
            left_boundary_position=-2.0,  # Boundary gauche décalée à gauche
            left_boundary_height=4.0,  # Plus grande
            right_boundary_position=1.5,  # Boundary droite décalée à droite
            right_boundary_height=2.5,  # Plus petite
            boundary_curvature=0.8,
            show_labels=True,
            show_focal_points=True,
        )

        self.add(system)
        self.wait()

        # Ajouter quelques rayons pour voir l'effet
        rays = VGroup()

        # Ray 1: parallèle en haut
        ray1 = DynamicRay(
            start_point=np.array([-5.0, 1.0, 0.0]),
            direction=RIGHT,
            optical_elements=[system],
            color=RED,
            ray_length=8.0,
        )
        rays.add(ray1)

        # Ray 2: parallèle au centre
        ray2 = DynamicRay(
            start_point=np.array([-5.0, 0.0, 0.0]),
            direction=RIGHT,
            optical_elements=[system],
            color=GREEN,
            ray_length=8.0,
        )
        rays.add(ray2)

        # Ray 3: parallèle en bas
        ray3 = DynamicRay(
            start_point=np.array([-5.0, -0.8, 0.0]),
            direction=RIGHT,
            optical_elements=[system],
            color=BLUE,
            ray_length=8.0,
        )
        rays.add(ray3)

        self.play(*[Create(ray) for ray in rays])
        self.wait(2)


class TestAsymmetricBoundaries(Scene):
    """Test système avec boundaries très asymétriques."""

    def construct(self):
        # Système asymétrique: petite entrée, grande sortie
        system = CenteredSystem(
            h_position=0.0,
            h_prime_position=2.0,
            focal_length=2.5,
            height=3.0,
            left_boundary_position=-0.5,  # Proche de H
            left_boundary_height=2.0,  # Petite entrée
            right_boundary_position=3.0,  # Loin de H'
            right_boundary_height=4.5,  # Grande sortie
            boundary_curvature=1.0,
            show_labels=True,
            show_focal_points=True,
            boundary_color=PURPLE,
        )

        self.add(system)
        self.wait()

        # Plusieurs rayons
        rays = VGroup()
        for y_pos in np.linspace(-0.8, 0.8, 5):
            ray = DynamicRay(
                start_point=np.array([-3.0, y_pos, 0.0]),
                direction=RIGHT,
                optical_elements=[system],
                color=interpolate_color(BLUE, RED, (y_pos + 0.8) / 1.6),
                ray_length=7.0,
            )
            rays.add(ray)

        self.play(*[Create(ray) for ray in rays], run_time=2)
        self.wait(2)


class TestBoundariesAtPlanes(Scene):
    """Test avec boundaries exactement sur les plans principaux."""

    def construct(self):
        # Boundaries alignées avec H et H'
        system = CenteredSystem(
            h_position=-1.5,
            h_prime_position=1.5,
            focal_length=2.0,
            height=3.5,
            left_boundary_position=-1.5,  # Exactement sur H
            left_boundary_height=3.5,
            right_boundary_position=1.5,  # Exactement sur H'
            right_boundary_height=3.5,
            boundary_curvature=0.6,
            show_labels=True,
            show_focal_points=True,
        )

        self.add(system)
        self.wait()

        # Ray traversant
        ray = DynamicRay(
            start_point=np.array([-4.0, 0.7, 0.0]),
            direction=RIGHT,
            optical_elements=[system],
            color=YELLOW,
            ray_length=8.0,
            stroke_width=4,
        )

        self.play(Create(ray))
        self.wait(2)
