"""
Debug test for 3D focal length verification
"""

import numpy as np
from manim import *
from manim_optics import ThinLens3D, RayBundle3D


class TestFocalDebug(ThreeDScene):
    """
    Test mathématique précis de la focalisation 3D.

    Trace 2 rayons parallèles et calcule analytiquement leur intersection.
    Si la lentille fonctionne correctement, l'intersection doit être
    exactement à la distance focale.
    """

    def construct(self):
        # Paramètres
        f = 5.0  # Distance focale
        lens_position = ORIGIN
        aperture = 3.0

        # Lentille 3D
        lens = ThinLens3D(
            focal_length=f,
            aperture_radius=aperture,
            position=lens_position,
            normal_vector=RIGHT,
            display_mode="simple",
            color=BLUE,
            opacity=0.3,
            show_focal_points=True,
        )

        # Deux rayons parallèles à des hauteurs différentes
        h1 = 1.0  # Hauteur du rayon 1
        h2 = -0.5  # Hauteur du rayon 2

        ray1_start = np.array([-8, h1, 0])
        ray2_start = np.array([-8, h2, 0])

        direction = RIGHT  # Parallèle à l'axe optique

        # Tracer les rayons manuellement pour avoir le contrôle
        # Avant la lentille
        ray1_before = Line3D(
            start=ray1_start,
            end=np.array([0, h1, 0]),
            color=YELLOW,
            stroke_width=3,
        )

        ray2_before = Line3D(
            start=ray2_start,
            end=np.array([0, h2, 0]),
            color=ORANGE,
            stroke_width=3,
        )

        # Calculer manuellement la propagation après la lentille
        # Pour un rayon parallèle à hauteur h :
        # Direction après : d_y = -h/f, d_x = 1 (avant normalisation)
        # Point de passage : (0, h, 0)

        # Rayon 1 après lentille
        intersection1 = np.array([0, h1, 0])
        # Direction initiale dans le repère local de la lentille
        # u = UP, v = OUT, n = RIGHT
        # h dans le repère local : h_u = h1, h_v = 0
        # d_u initial = 0, d_v = 0, d_n = 1
        # deviation_u = -h1 / (f * 1) = -h1/f
        # new_d_u = 0 + (-h1/f) = -h1/f
        # new direction = -h1/f * UP + 1 * RIGHT = [1, -h1/f, 0]

        dir1_after = np.array([1, -h1 / f, 0])
        dir1_after_norm = dir1_after / np.linalg.norm(dir1_after)

        # Rayon 2 après lentille
        intersection2 = np.array([0, h2, 0])
        dir2_after = np.array([1, -h2 / f, 0])
        dir2_after_norm = dir2_after / np.linalg.norm(dir2_after)

        # Prolonger les rayons après la lentille
        ray1_after = Line3D(
            start=intersection1,
            end=intersection1 + 10 * dir1_after_norm,
            color=YELLOW,
            stroke_width=3,
        )

        ray2_after = Line3D(
            start=intersection2,
            end=intersection2 + 10 * dir2_after_norm,
            color=ORANGE,
            stroke_width=3,
        )

        # Calculer l'intersection des deux rayons
        # Rayon 1 : P1 = (0, h1, 0) + t1 * (1, -h1/f, 0)
        # Rayon 2 : P2 = (0, h2, 0) + t2 * (1, -h2/f, 0)
        # À l'intersection : P1 = P2
        # Pour x : 0 + t1*1 = 0 + t2*1 => t1 = t2 = t
        # Pour y : h1 + t*(-h1/f) = h2 + t*(-h2/f)
        #         h1 - t*h1/f = h2 - t*h2/f
        #         h1 - h2 = t*h1/f - t*h2/f
        #         h1 - h2 = t*(h1 - h2)/f
        #         f = t
        # Donc l'intersection est à t = f
        # Position : (f, h1 - h1*f/f, 0) = (f, 0, 0)

        t_intersection = f
        intersection_point = np.array([f, 0, 0])

        # Vérification par calcul
        p1_at_t = intersection1 + t_intersection * dir1_after_norm
        p2_at_t = intersection2 + t_intersection * dir2_after_norm

        print(f"\n{'='*50}")
        print(f"VÉRIFICATION MATHÉMATIQUE DE LA FOCALISATION")
        print(f"{'='*50}")
        print(f"Distance focale de la lentille : f = {f}")
        print(f"Hauteur rayon 1 : h1 = {h1}")
        print(f"Hauteur rayon 2 : h2 = {h2}")
        print(f"\nDirection rayon 1 après lentille : {dir1_after_norm}")
        print(f"Direction rayon 2 après lentille : {dir2_after_norm}")
        print(f"\nIntersection théorique à t = {t_intersection}")
        print(f"Point théorique : ({f}, 0, 0)")
        print(f"\nRayon 1 à t={t_intersection} : {p1_at_t}")
        print(f"Rayon 2 à t={t_intersection} : {p2_at_t}")
        print(f"Distance entre les deux : {np.linalg.norm(p1_at_t - p2_at_t):.6f}")
        print(f"{'='*50}\n")

        # Marqueur au point focal théorique
        focal_marker = Sphere(radius=0.1, color=RED)
        focal_marker.move_to(np.array([f, 0, 0]))

        # Marqueurs aux positions calculées
        marker1 = Sphere(radius=0.05, color=YELLOW)
        marker1.move_to(p1_at_t)

        marker2 = Sphere(radius=0.05, color=ORANGE)
        marker2.move_to(p2_at_t)

        # Textes avec les mesures
        text_focal = Text(f"f = {f}", font_size=24, color=RED)
        text_focal.rotate(90 * DEGREES, axis=OUT)
        text_focal.rotate(90 * DEGREES, axis=RIGHT)
        text_focal.next_to(focal_marker, UP, buff=0.3)

        # Ligne au plan focal
        focal_line = Line3D(
            start=np.array([f, -4, 0]),
            end=np.array([f, 4, 0]),
            color=RED,
            stroke_width=2,
            stroke_opacity=0.5,
        )

        # Axes de référence
        axes = ThreeDAxes(
            x_range=[-10, 12],
            y_range=[-4, 4],
            z_range=[-3, 3],
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y", z_label="z")

        self.add(axes, axes_labels)

        # Vue de profil
        self.set_camera_orientation(
            phi=90 * DEGREES,
            theta=-90 * DEGREES,
            zoom=0.6,
        )

        # Animation
        self.play(FadeIn(lens))
        self.play(Create(focal_line))
        self.wait(0.3)

        self.play(
            Create(ray1_before),
            Create(ray2_before),
        )
        self.wait(0.5)

        self.play(
            Create(ray1_after),
            Create(ray2_after),
            run_time=1.5,
        )
        self.wait(0.5)

        self.play(
            FadeIn(focal_marker),
            FadeIn(marker1),
            FadeIn(marker2),
        )
        self.add(text_focal)

        self.wait(2)

        # Maintenant utiliser RayBundle3D pour comparer
        print("\nTEST AVEC RayBundle3D :")

        rays_test = RayBundle3D(
            start_points=[ray1_start, ray2_start],
            direction_vector=RIGHT,
            optical_elements=[lens],
            color=GREEN,
            stroke_width=2,
            max_length=12,
        )

        self.play(FadeOut(ray1_before), FadeOut(ray2_before))
        self.play(FadeOut(ray1_after), FadeOut(ray2_after))
        self.wait(0.3)

        self.play(Create(rays_test))

        self.wait(3)


class TestFocalSimplified(ThreeDScene):
    """Version ultra-simplifiée avec affichage des calculs."""

    def construct(self):
        f = 4.0
        h = 1.0  # Hauteur du rayon

        # Lentille
        lens = ThinLens3D(
            focal_length=f,
            aperture_radius=2.0,
            position=ORIGIN,
            normal_vector=RIGHT,
            display_mode="simple",
            color=BLUE,
            opacity=0.4,
            show_focal_points=True,
        )

        # Un seul rayon parallèle
        ray_start = np.array([-6, h, 0])

        # Avant lentille
        ray_before = Line3D(
            start=ray_start,
            end=np.array([0, h, 0]),
            color=YELLOW,
            stroke_width=4,
        )

        # Direction théorique après
        # Pour h=1, f=4 : direction = [1, -1/4, 0]
        # Le rayon doit passer par (f, 0, 0)
        target = np.array([f, 0, 0])
        direction_after = target - np.array([0, h, 0])
        direction_after = direction_after / np.linalg.norm(direction_after)

        print(f"\nRayon à hauteur h={h}, focale f={f}")
        print(f"Direction théorique après lentille : {direction_after}")
        print(f"Doit passer par ({f}, 0, 0)")

        ray_after_theory = Line3D(
            start=np.array([0, h, 0]),
            end=target + 2 * direction_after,
            color=GREEN,
            stroke_width=4,
        )

        # Rayon avec RayBundle3D
        ray_bundle = RayBundle3D(
            start_points=[ray_start],
            direction_vector=RIGHT,
            optical_elements=[lens],
            color=RED,
            stroke_width=3,
            max_length=10,
        )

        # Marqueurs
        focal_point = Dot3D(point=target, color=RED, radius=0.15)

        # Axes
        axes = ThreeDAxes(x_range=[-8, 10], y_range=[-3, 3])
        self.add(axes)

        self.set_camera_orientation(
            phi=90 * DEGREES,
            theta=-90 * DEGREES,
            zoom=0.7,
        )

        self.play(FadeIn(lens))
        self.play(FadeIn(focal_point))
        self.wait(0.3)

        # Rayon théorique (vert)
        self.play(Create(ray_before))
        self.wait(0.3)
        self.play(Create(ray_after_theory))
        self.wait(1)

        # Rayon calculé par RayBundle3D (rouge)
        self.play(FadeOut(ray_before), FadeOut(ray_after_theory))
        self.wait(0.3)
        self.play(Create(ray_bundle))

        self.wait(3)
