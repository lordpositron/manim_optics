from manim import *
from manim_optics import ThinLens3D, RayBundle3D


class TestTrackers3D(ThreeDScene):
    """
    Test de tous les trackers de ThinLens3D.

    Démontre les animations de :
    - focal_length
    - aperture_radius
    - position
    - normal_vector (orientation)
    """

    def construct(self):
        # Axes
        axes = ThreeDAxes(x_range=[-6, 10], y_range=[-5, 5], z_range=[-3, 3])
        self.add(axes)

        # Lentille avec tous les trackers
        lens = ThinLens3D(
            focal_length=3.0,
            aperture_radius=1.5,
            position=ORIGIN,
            normal_vector=RIGHT,
            display_mode="simple",
            color=BLUE,
            opacity=0.5,
            show_focal_points=True,
        )

        # Rayons avec auto-update
        rays = RayBundle3D(
            start_points=[np.array([-5, y, 0]) for y in np.linspace(-1.2, 1.2, 5)],
            direction_vector=RIGHT,
            optical_elements=[lens],
            color=YELLOW,
            stroke_width=2,
            max_length=12,
            auto_update=True,
        )

        # Vue de profil
        self.set_camera_orientation(
            phi=90 * DEGREES,
            theta=-90 * DEGREES,
            zoom=0.6,
        )

        # Textes pour afficher les valeurs
        focal_text = always_redraw(
            lambda: Text(
                f"f = {lens.focal_length_tracker.get_value():.2f}",
                font_size=28,
                color=BLUE,
            )
            .to_corner(UL)
            .rotate(90 * DEGREES, axis=OUT)
            .rotate(90 * DEGREES, axis=RIGHT)
        )

        aperture_text = always_redraw(
            lambda: Text(
                f"R = {lens.aperture_radius_tracker.get_value():.2f}",
                font_size=28,
                color=GREEN,
            ).next_to(focal_text, DOWN, buff=0.3, aligned_edge=LEFT)
        )

        # Animation initiale
        self.play(FadeIn(lens))
        self.play(Create(rays))
        self.add(focal_text, aperture_text)
        self.wait(1)

        # Test 1: Changer la focale
        self.play(lens.animate_focal_length(5.0, run_time=2))
        self.wait(1)

        self.play(lens.animate_focal_length(2.0, run_time=2))
        self.wait(1)

        # Test 2: Changer le rayon d'ouverture
        # Les rayons extérieurs devraient être bloqués
        self.play(lens.animate_aperture_radius(0.8, run_time=2))
        self.wait(1)

        self.play(lens.animate_aperture_radius(2.0, run_time=2))
        self.wait(1)

        # Remettre les valeurs initiales
        self.play(
            lens.animate_focal_length(3.0, run_time=1),
            lens.animate_aperture_radius(1.5, run_time=1),
        )
        self.wait(1)


class TestPosition3D(ThreeDScene):
    """Test de l'animation de position."""

    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)

        lens = ThinLens3D(
            focal_length=2.5,
            aperture_radius=1.5,
            position=ORIGIN,
            normal_vector=RIGHT,
            display_mode="simple",
            color=PURPLE,
            opacity=0.6,
            show_focal_points=True,
        )

        rays = RayBundle3D(
            start_points=[np.array([-6, y, 0]) for y in np.linspace(-1, 1, 4)],
            direction_vector=RIGHT,
            optical_elements=[lens],
            color=YELLOW,
            stroke_width=3,
            max_length=10,
            auto_update=True,
        )

        self.set_camera_orientation(
            phi=90 * DEGREES,
            theta=-90 * DEGREES,
            zoom=0.6,
        )

        self.play(FadeIn(lens))
        self.play(Create(rays))
        self.wait(1)

        # Déplacer la lentille via les trackers
        self.play(lens.animate_position(np.array([2, 0, 0]), run_time=2))
        self.wait(1)

        self.play(lens.animate_position(np.array([2, 2, 0]), run_time=2))
        self.wait(1)

        self.play(lens.animate_position(np.array([0, 0, 0]), run_time=2))
        self.wait(2)


class TestOrientation3D(ThreeDScene):
    """Test de l'animation d'orientation (vecteur normal)."""

    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)

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
            color=RED,
            stroke_width=2,
            max_length=8,
            auto_update=True,
        )

        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        self.play(FadeIn(lens))
        self.play(Create(rays))
        self.wait(1)

        # Faire tourner la lentille en changeant son vecteur normal
        # Rotation de 45° dans le plan XY
        new_normal_1 = np.array([1, 1, 0])
        self.play(lens.animate_normal_vector(new_normal_1, run_time=3))
        self.wait(1)

        # Rotation vers le haut
        new_normal_2 = np.array([1, 0, 1])
        self.play(lens.animate_normal_vector(new_normal_2, run_time=3))
        self.wait(1)

        # Retour à la normale vers la droite
        self.play(lens.animate_normal_vector(RIGHT, run_time=2))
        self.wait(2)


class TestCombined3D(ThreeDScene):
    """
    Test combiné avec plusieurs propriétés animées simultanément.
    """

    def construct(self):
        axes = ThreeDAxes(x_range=[-8, 12], y_range=[-5, 5])
        self.add(axes)

        lens = ThinLens3D(
            focal_length=3.0,
            aperture_radius=1.5,
            position=ORIGIN,
            normal_vector=RIGHT,
            display_mode="simple",
            color=TEAL,
            opacity=0.6,
            show_focal_points=True,
        )

        rays = RayBundle3D(
            start_points=[np.array([-6, y, 0]) for y in np.linspace(-1.5, 1.5, 6)],
            direction_vector=RIGHT,
            optical_elements=[lens],
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

        self.play(FadeIn(lens), Create(rays))
        self.wait(1)

        # Animation complexe: tout change en même temps !
        self.play(
            lens.animate_focal_length(5.0, run_time=3),
            lens.animate_position(np.array([3, 1, 0]), run_time=3),
            lens.animate_aperture_radius(2.5, run_time=3),
        )
        self.wait(1)

        # Autre combinaison
        self.play(
            lens.animate_focal_length(2.0, run_time=2),
            lens.animate_position(np.array([1, -1, 0]), run_time=2),
            lens.animate_aperture_radius(1.0, run_time=2),
        )
        self.wait(1)

        # Retour aux valeurs initiales
        self.play(
            lens.animate_focal_length(3.0, run_time=2),
            lens.animate_position(ORIGIN, run_time=2),
            lens.animate_aperture_radius(1.5, run_time=2),
        )
        self.wait(2)


class TestSetMethods3D(ThreeDScene):
    """
    Test des méthodes set_* (changement immédiat sans animation).
    """

    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)

        lens = ThinLens3D(
            focal_length=3.0,
            aperture_radius=1.5,
            position=ORIGIN,
            normal_vector=RIGHT,
            display_mode="simple",
            color=ORANGE,
            opacity=0.6,
            show_focal_points=True,
        )

        rays = RayBundle3D(
            start_points=[np.array([-5, y, 0]) for y in np.linspace(-1, 1, 5)],
            direction_vector=RIGHT,
            optical_elements=[lens],
            color=YELLOW,
            stroke_width=2,
            max_length=10,
            auto_update=True,
        )

        self.set_camera_orientation(
            phi=90 * DEGREES,
            theta=-90 * DEGREES,
            zoom=0.6,
        )

        self.play(FadeIn(lens), Create(rays))
        self.wait(1)

        # Changements instantanés (sans animation)
        lens.set_focal_length(5.0)
        self.wait(0.1)

        lens.set_position_3d(np.array([2, 0, 0]))
        self.wait(0.1)

        lens.set_aperture_radius(2.5)
        self.wait(1)

        # Plusieurs changements rapides
        for f in [4.0, 3.0, 2.5, 3.5, 3.0]:
            lens.set_focal_length(f)
            self.wait(0.3)

        self.wait(2)
