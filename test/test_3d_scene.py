from manim import *
from manim_optics import ThinLens3D, RayBundle3D

eiffel_path = r"/Users/corentinnannini/sDrive/BIO IO/Script vidéos à venir/eiffel.svg"


class Test3DOptics(ThreeDScene):
    """Test des éléments optiques 3D avec ton exemple de Tour Eiffel."""

    def construct(self):
        # Axes de référence
        line_x = Line3D(start=[-10, 0, 0], end=[10, 0, 0], color=RED, stroke_width=1)
        line_y = Line3D(start=[0, 0, 0], end=[0, 100, 0], color=GREEN, stroke_width=1)
        self.add(line_x, line_y)

        # Charger la Tour Eiffel
        svg = SVGMobject(
            eiffel_path,
            fill_opacity=0,
            stroke_width=2,
            stroke_color=YELLOW,
        )
        svg.scale(10)
        svg.shift(-svg.get_bottom())
        bottom_center = svg.get_bottom()

        # Orienter la Tour vers le haut (axe Y)
        svg.rotate(90 * DEGREES, axis=RIGHT, about_point=bottom_center)

        # Point lumineux sur la Tour
        light = Dot3D(color=WHITE, stroke_color=YELLOW)
        light.next_to(svg, OUT, buff=0)
        self.add(light)

        # Configuration caméra initiale
        self.set_camera_orientation(
            frame_center=svg.get_center(),
            phi=60 * DEGREES,
            theta=60 * DEGREES,
            zoom=0.3,
            focal_distance=150,
        )

        self.play(Create(svg))
        self.wait(0.2)

        # Paramètres du faisceau et de la lentille
        N_ray = 7
        bundle_height = 2.0
        f = 5

        # Lentille 3D en mode simple (cercle)
        lens_simple = ThinLens3D(
            focal_length=f,
            aperture_radius=15,
            position=np.array([0, 5, 20]),
            normal_vector=UP,  # Normal vers le haut
            display_mode="simple",
            color=WHITE,
            opacity=0.5,
        )

        # Points de départ du faisceau (étalés en Z)
        ray_start_points = [
            np.array(
                [
                    light.get_center()[0],
                    light.get_center()[1],
                    light.get_center()[2] + j,
                ]
            )
            for j in np.linspace(-bundle_height / 2, bundle_height / 2, N_ray)
        ]

        # Faisceau de rayons 3D
        ray_bundle = RayBundle3D(
            start_points=ray_start_points,
            direction_vector=UP,
            optical_elements=[lens_simple],
            color=YELLOW_E,
            stroke_width=2,
        )

        self.play(Create(ray_bundle), FadeIn(lens_simple))
        self.wait(1)

        # # Lentille 3D en mode détaillé (surfaces)
        lens_detailed = ThinLens3D(
            focal_length=f,
            aperture_radius=1.5,
            position=np.array([0, 20, 0]),
            normal_vector=UP,
            display_mode="detailed",
            thickness=0.2,
            R1=10,
            R2=10,
            color=BLUE_E,
            opacity=0.6,
            show_focal_points=True,
        )

        # self.play(Create(lens_detailed))
        # self.wait(1)

        # Déplacer la caméra pour mieux voir
        self.move_camera(
            frame_center=lens_detailed.get_center(),
            phi=85 * DEGREES,
            theta=20 * DEGREES,
            zoom=1,
            run_time=2,
        )

        # Image de la Tour Eiffel
        svg_img = SVGMobject(
            eiffel_path,
            fill_opacity=0,
            stroke_width=2,
            stroke_color=YELLOW,
        )
        svg_img.scale(1)
        svg_img.shift(-svg_img.get_bottom())
        svg_img.rotate(90 * DEGREES, axis=RIGHT, about_point=svg_img.get_bottom())
        svg_img.rotate(180 * DEGREES, axis=UP, about_point=svg_img.get_bottom())
        svg_img.shift((lens_detailed.get_center()[1] + f) * UP)

        self.play(Create(svg_img))
        self.wait(2)


class Test3DLensRotation(ThreeDScene):
    """Test d'une lentille avec rotation arbitraire."""

    def construct(self):
        # Axes
        axes = ThreeDAxes(x_range=[-5, 5], y_range=[-5, 5], z_range=[-5, 5])
        self.add(axes)

        # Lentille orientée à 45° dans le plan XY
        lens_angled = ThinLens3D(
            focal_length=3.0,
            aperture_radius=2.0,
            position=ORIGIN,
            normal_vector=np.array([1, 1, 0]),  # Diagonale dans XY
            display_mode="simple",
            color=BLUE,
            opacity=0.7,
            show_focal_points=True,
        )

        # Faisceau arrivant de côté
        ray_bundle = RayBundle3D(
            start_points=[np.array([-4, 0, z]) for z in np.linspace(-1, 1, 5)],
            direction_vector=RIGHT,
            optical_elements=[lens_angled],
            color=YELLOW,
            stroke_width=3,
        )

        self.set_camera_orientation(phi=70 * DEGREES, theta=45 * DEGREES)

        self.play(FadeIn(lens_angled))
        self.play(Create(ray_bundle))

        self.wait(1)
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)
        self.stop_ambient_camera_rotation()
        self.wait(1)


class Test3DDetailedLens(ThreeDScene):
    """Test du mode detailed avec surfaces biconvexes."""

    def construct(self):
        axes = ThreeDAxes(x_range=[-3, 3], y_range=[-3, 3], z_range=[-3, 3])
        self.add(axes)

        # Lentille biconvexe détaillée
        lens = ThinLens3D(
            focal_length=2.5,
            aperture_radius=1.5,
            position=ORIGIN,
            normal_vector=RIGHT,  # Normal vers la droite
            display_mode="detailed",
            thickness=0.3,
            R1=8,
            R2=8,
            color=BLUE_E,
            opacity=0.7,
            show_focal_points=True,
        )

        # Faisceau parallèle
        ray_bundle = RayBundle3D(
            start_points=[
                np.array([-4, y, z])
                for y in [-1, -0.5, 0, 0.5, 1]
                for z in [-1, -0.5, 0, 0.5, 1]
            ],
            direction_vector=RIGHT,
            optical_elements=[lens],
            color=RED,
            stroke_width=2,
            max_length=10,
        )

        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES, zoom=0.8)

        self.play(FadeIn(lens))
        self.wait(0.5)
        self.play(Create(ray_bundle), run_time=2)

        self.wait(1)
        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(8)
        self.stop_ambient_camera_rotation()
        self.wait(1)
