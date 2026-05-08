from manim import *

from manim_optics import RayBundle3D, ThinLens3D


class TestDynamic3D(ThreeDScene):
    """
    Test de mise à jour dynamique des rayons 3D.

    Les rayons se recalculent automatiquement quand la lentille bouge.
    """

    def construct(self):
        # Axes
        axes = ThreeDAxes(
            x_range=[-8, 12],
            y_range=[-4, 4],
            z_range=[-3, 3],
        )
        self.add(axes)

        # Lentille convergente
        f = 3.0
        lens = ThinLens3D(
            focal_length=f,
            aperture_radius=2.0,
            position=ORIGIN,
            normal_vector=RIGHT,
            display_mode="simple",
            color=BLUE,
            opacity=0.5,
            show_focal_points=True,
        )

        # Plan focal
        focal_line = Line3D(
            start=np.array([f, -4, 0]),
            end=np.array([f, 4, 0]),
            color=RED,
            stroke_width=2,
        )

        # Faisceau de rayons avec auto_update=True
        N = 5
        ray_starts = [np.array([-6, y, 0]) for y in np.linspace(-1.5, 1.5, N)]

        rays = RayBundle3D(
            start_points=ray_starts,
            direction_vector=RIGHT,
            optical_elements=[lens],
            color=YELLOW,
            stroke_width=3,
            max_length=12,
            auto_update=True,  # Mise à jour automatique !
        )

        # Vue de profil
        self.set_camera_orientation(
            phi=90 * DEGREES,
            theta=-90 * DEGREES,
            zoom=0.6,
        )

        # Animation initiale
        self.play(FadeIn(lens), Create(focal_line))
        self.wait(0.3)
        self.play(Create(rays))
        self.wait(1)

        # Déplacer la lentille vers la droite
        # Les rayons se mettent à jour automatiquement !
        self.play(
            lens.animate.shift(RIGHT * 2),
            focal_line.animate.shift(RIGHT * 2),
            run_time=3,
        )
        self.wait(1)

        # Déplacer vers le haut
        self.play(
            lens.animate.shift(UP * 1.5), focal_line.animate.shift(UP * 1.5), run_time=2
        )
        self.wait(1)

        # Revenir à l'origine
        self.play(
            lens.animate.move_to(ORIGIN),
            focal_line.animate.shift(DOWN * 1.5 + LEFT * 2),
            run_time=2,
        )
        self.wait(2)


class TestDynamic3DRotation(ThreeDScene):
    """
    Test avec rotation de la lentille.

    Les rayons s'adaptent à l'orientation de la lentille.
    """

    def construct(self):
        # Axes
        axes = ThreeDAxes()
        self.add(axes)

        # Lentille qui peut tourner
        lens = ThinLens3D(
            focal_length=3.0,
            aperture_radius=1.5,
            position=ORIGIN,
            normal_vector=RIGHT,
            display_mode="simple",
            color=BLUE_E,
            opacity=0.6,
            show_focal_points=True,
        )

        # Rayons venant de la gauche
        rays = RayBundle3D(
            start_points=[
                np.array([-5, y, z]) for y in [-1, 0, 1] for z in [-0.5, 0, 0.5]
            ],
            direction_vector=RIGHT,
            optical_elements=[lens],
            color=YELLOW,
            stroke_width=2,
            max_length=10,
            auto_update=True,
        )

        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        self.play(FadeIn(lens))
        self.play(Create(rays))
        self.wait(1)

        # Faire tourner la lentille autour de l'axe Y
        # Note: Pour vraiment changer l'orientation optique, il faudrait
        # modifier lens.normal directement, mais ici on démontre le principe
        self.play(Rotate(lens, angle=30 * DEGREES, axis=UP), run_time=2)
        self.wait(1)

        self.play(Rotate(lens, angle=-60 * DEGREES, axis=UP), run_time=3)
        self.wait(2)


class TestDynamic3DFocalChange(ThreeDScene):
    """
    Test avec changement de focale dynamique.

    Nécessite d'ajouter un ValueTracker à ThinLens3D (comme en 2D).
    Pour l'instant, on démontre le déplacement.
    """

    def construct(self):
        # Configuration
        axes = ThreeDAxes(x_range=[-6, 10], y_range=[-4, 4])
        self.add(axes)

        # Deux lentilles qui vont se croiser
        lens1 = ThinLens3D(
            focal_length=2.5,
            aperture_radius=1.5,
            position=np.array([-2, 0, 0]),
            normal_vector=RIGHT,
            display_mode="simple",
            color=BLUE,
            opacity=0.4,
        )

        lens2 = ThinLens3D(
            focal_length=3.0,
            aperture_radius=1.2,
            position=np.array([3, 0, 0]),
            normal_vector=RIGHT,
            display_mode="simple",
            color=GREEN,
            opacity=0.4,
        )

        # Rayons à travers les deux lentilles
        rays = RayBundle3D(
            start_points=[np.array([-5, y, 0]) for y in np.linspace(-1, 1, 5)],
            direction_vector=RIGHT,
            optical_elements=[lens1, lens2],
            color=YELLOW,
            stroke_width=2,
            max_length=8,
            auto_update=True,
        )

        self.set_camera_orientation(
            phi=90 * DEGREES,
            theta=-90 * DEGREES,
            zoom=0.7,
        )

        self.play(FadeIn(lens1), FadeIn(lens2))
        self.play(Create(rays))
        self.wait(1)

        # Rapprocher les lentilles
        self.play(
            lens1.animate.shift(RIGHT * 1), lens2.animate.shift(LEFT * 1), run_time=3
        )
        self.wait(1)

        # Les éloigner
        self.play(
            lens1.animate.shift(LEFT * 2), lens2.animate.shift(RIGHT * 2), run_time=3
        )
        self.wait(1)

        # Les rapprocher à nouveau
        self.play(
            lens1.animate.shift(RIGHT * 1), lens2.animate.shift(LEFT * 1), run_time=2
        )
        self.wait(2)


class TestDynamic3DComplex(ThreeDScene):
    """
    Scène complexe avec plusieurs éléments en mouvement.
    """

    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)

        # Plusieurs lentilles
        lenses = VGroup(
            *[
                ThinLens3D(
                    focal_length=2.0 + i * 0.5,
                    aperture_radius=1.0,
                    position=np.array([i * 2 - 2, 0, 0]),
                    normal_vector=RIGHT,
                    display_mode="simple",
                    color=[BLUE, GREEN, PURPLE][i],
                    opacity=0.5,
                )
                for i in range(3)
            ]
        )

        # Rayons à travers toutes les lentilles
        rays = RayBundle3D(
            start_points=[np.array([-4, y, 0]) for y in [-0.5, 0, 0.5]],
            direction_vector=RIGHT,
            optical_elements=list(lenses),
            color=YELLOW,
            stroke_width=2,
            max_length=12,
            auto_update=True,
        )

        self.set_camera_orientation(
            phi=90 * DEGREES,
            theta=-90 * DEGREES,
            zoom=0.5,
        )

        self.play(FadeIn(lenses))
        self.play(Create(rays))
        self.wait(1)

        # Animation complexe: les lentilles dansent
        self.play(
            lenses[0].animate.shift(UP * 0.5),
            lenses[1].animate.shift(DOWN * 0.5),
            lenses[2].animate.shift(UP * 0.3),
            run_time=2,
        )
        self.wait(0.5)

        self.play(
            lenses[0].animate.shift(DOWN * 1),
            lenses[1].animate.shift(UP * 1),
            lenses[2].animate.shift(DOWN * 0.6),
            run_time=2,
        )
        self.wait(0.5)

        # Retour
        self.play(
            *[
                lens.animate.move_to(np.array([i * 2 - 2, 0, 0]))
                for i, lens in enumerate(lenses)
            ],
            run_time=2,
        )
        self.wait(2)
