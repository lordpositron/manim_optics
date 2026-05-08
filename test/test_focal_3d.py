from manim import *

from manim_optics import RayBundle3D, ThinLens3D


class TestFocal3DSimple(ThreeDScene):
    """
    Test simple de focalisation 3D.

    Vue de profil avec :
    - Faisceau parallèle avec petit angle
    - Lentille 3D
    - Trait au plan focal pour vérifier la convergence
    """

    def construct(self):
        # Paramètres
        f = 3.0  # Distance focale
        lens_position = ORIGIN
        aperture = 2.0

        # Axes de référence (optionnel pour debug)
        axes = ThreeDAxes(
            x_range=[-5, 10],
            y_range=[-3, 3],
            z_range=[-3, 3],
            x_length=15,
            y_length=6,
            z_length=6,
        )
        self.add(axes)

        # Lentille 3D en mode simple
        # Normal pointant vers la droite (direction X)
        lens = ThinLens3D(
            focal_length=f,
            aperture_radius=aperture,
            position=lens_position,
            normal_vector=RIGHT,  # Plan perpendiculaire à l'axe X
            display_mode="simple",
            color=BLUE,
            opacity=0.5,
            show_focal_points=True,
        )

        # Plan focal (trait vertical au foyer image)
        focal_plane = Line3D(
            start=np.array([f, -3, 0]),
            end=np.array([f, 3, 0]),
            color=RED,
            stroke_width=3,
        )

        # Label pour le plan focal
        focal_label = Text("Plan focal", font_size=24, color=RED)
        focal_label.rotate(90 * DEGREES, axis=OUT)
        focal_label.rotate(90 * DEGREES, axis=RIGHT)
        focal_label.next_to(focal_plane, UP, buff=0.3)

        # Faisceau parallèle avec petit angle
        # 5 rayons étalés verticalement (en Y)
        N_rays = 5
        start_x = -5
        angle_deg = 5  # Petit angle en degrés

        # Direction avec petit angle dans le plan XY
        direction = np.array(
            [np.cos(angle_deg * DEGREES), np.sin(angle_deg * DEGREES), 0]
        )

        ray_starts = [np.array([start_x, y, 0]) for y in np.linspace(-1.5, 1.5, N_rays)]

        ray_bundle = RayBundle3D(
            start_points=ray_starts,
            direction_vector=direction,
            optical_elements=[lens],
            color=YELLOW,
            stroke_width=3,
            max_length=15,
        )

        # Configuration de la caméra - vue de profil (depuis le côté)
        # On regarde depuis l'axe Z vers l'origine
        self.set_camera_orientation(
            phi=90 * DEGREES,  # Vue horizontale
            theta=-90 * DEGREES,  # Depuis l'axe Z
            zoom=0.8,
        )

        # Animation
        self.play(FadeIn(lens))
        self.play(Create(focal_plane))
        self.add(focal_label)
        self.wait(0.5)

        self.play(Create(ray_bundle), run_time=2)
        self.wait(2)


class TestFocal3DParallel(ThreeDScene):
    """
    Test avec faisceau parfaitement parallèle à l'axe optique.
    Les rayons doivent tous converger au foyer.
    """

    def construct(self):
        # Paramètres
        f = 4.0
        lens_position = ORIGIN
        aperture = 2.5

        # Axes
        axes = ThreeDAxes(
            x_range=[-5, 10],
            y_range=[-4, 4],
            z_range=[-4, 4],
        )
        self.add(axes)

        # Lentille
        lens = ThinLens3D(
            focal_length=f,
            aperture_radius=aperture,
            position=lens_position,
            normal_vector=RIGHT,
            display_mode="simple",
            color=BLUE_E,
            opacity=0.6,
            show_focal_points=True,
        )

        # Plan focal avec grille
        focal_plane_vertical = Line3D(
            start=np.array([f, -4, 0]),
            end=np.array([f, 4, 0]),
            color=RED,
            stroke_width=2,
        )

        focal_plane_horizontal = Line3D(
            start=np.array([f, 0, -4]),
            end=np.array([f, 0, 4]),
            color=RED,
            stroke_width=2,
        )

        # Faisceau parfaitement parallèle
        # Grille de rayons
        N = 5
        ray_starts = [
            np.array([-6, y, z])
            for y in np.linspace(-2, 2, N)
            for z in np.linspace(-2, 2, N)
        ]

        ray_bundle = RayBundle3D(
            start_points=ray_starts,
            direction_vector=RIGHT,  # Parallèle à l'axe optique
            optical_elements=[lens],
            color=YELLOW,
            stroke_width=2,
            max_length=12,
        )

        # Vue de profil
        self.set_camera_orientation(
            phi=90 * DEGREES,
            theta=-90 * DEGREES,
            zoom=0.6,
        )

        self.play(FadeIn(lens))
        self.play(Create(focal_plane_vertical), Create(focal_plane_horizontal))
        self.wait(0.5)

        self.play(Create(ray_bundle), run_time=2)
        self.wait(1)

        # Rotation de la caméra pour voir en 3D
        self.move_camera(
            phi=70 * DEGREES,
            theta=-45 * DEGREES,
            run_time=2,
        )
        self.wait(2)


class TestFocal3DComparison(ThreeDScene):
    """
    Comparaison côte à côte : lentille convergente vs divergente.
    """

    def construct(self):
        f = 3.0

        # Lentille convergente
        lens_conv = ThinLens3D(
            focal_length=f,
            aperture_radius=1.5,
            position=np.array([0, 2, 0]),
            normal_vector=RIGHT,
            display_mode="simple",
            color=BLUE,
            opacity=0.5,
            show_focal_points=True,
        )

        # Lentille divergente
        lens_div = ThinLens3D(
            focal_length=-f,  # Négatif pour divergente
            aperture_radius=1.5,
            position=np.array([0, -2, 0]),
            normal_vector=RIGHT,
            display_mode="simple",
            color=RED,
            opacity=0.5,
            show_focal_points=True,
        )

        # Plans focaux
        focal_conv = Line3D(
            start=np.array([f, 0.5, 0]),
            end=np.array([f, 3.5, 0]),
            color=BLUE,
            stroke_width=2,
        )

        focal_div = Line3D(
            start=np.array([-f, -3.5, 0]),
            end=np.array([-f, -0.5, 0]),
            color=RED,
            stroke_width=2,
        )

        # Faisceaux parallèles
        N = 5
        ray_starts_conv = [np.array([-5, 2 + y, 0]) for y in np.linspace(-1, 1, N)]

        ray_starts_div = [np.array([-5, -2 + y, 0]) for y in np.linspace(-1, 1, N)]

        rays_conv = RayBundle3D(
            start_points=ray_starts_conv,
            direction_vector=RIGHT,
            optical_elements=[lens_conv],
            color=YELLOW,
            stroke_width=2,
            max_length=10,
        )

        rays_div = RayBundle3D(
            start_points=ray_starts_div,
            direction_vector=RIGHT,
            optical_elements=[lens_div],
            color=ORANGE,
            stroke_width=2,
            max_length=10,
        )

        # Axes
        axes = ThreeDAxes()
        self.add(axes)

        # Vue de profil
        self.set_camera_orientation(
            phi=90 * DEGREES,
            theta=-90 * DEGREES,
            zoom=0.5,
        )

        # Animation
        self.play(FadeIn(lens_conv), FadeIn(lens_div))
        self.play(Create(focal_conv), Create(focal_div))
        self.wait(0.5)

        self.play(Create(rays_conv), Create(rays_div), run_time=2)
        self.wait(2)
