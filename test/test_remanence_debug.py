"""
Test simple pour débugger la rémanence
"""

import numpy as np
from manim import *

from manim_optics import CenteredSystem, DynamicRay


class TestRemanenceSimple(Scene):
    """Test simple: un système qui bouge."""

    def construct(self):
        # Create centered system
        system = CenteredSystem(
            h_position=-1.0,
            h_prime_position=1.0,
            focal_length=2.0,
            height=2.0,
            show_labels=False,
            show_focal_points=False,
        )

        # Un seul rayon
        ray = DynamicRay(
            start_point=np.array([-4.0, 0.5, 0.0]),
            direction=RIGHT,
            optical_elements=[system],
            color=YELLOW,
        )

        # Afficher
        self.play(
            FadeIn(system),
            Create(ray),
        )
        self.wait(0.5)

        # Animation: juste changer H
        self.play(system.animate_h_position(0.0, run_time=1.0))
        self.wait(1)
