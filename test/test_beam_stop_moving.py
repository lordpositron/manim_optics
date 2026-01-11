from manim import *
import sys

sys.path.insert(0, "/Users/corentinnannini/Documents/manim_test")

from manim_optics import *

# config.frame_rate = 25


class PrincipeOculaire(OpticalScene, MovingCameraScene):
    def construct(self):
        # self.set_theme("light")
        self.add_debugging_grid()
        optical_axis_animation = self.get_optical_axis_animation()

        reticule = LinearGraticule(
            direction=UP,
            length=2.2,
            unit_length=0.5,
            primary_interval=2,
            secondary_interval=0.2,
            tick_angle=90 * DEGREES,
            color=WHITE,
            show_labels=False,
            decimal_places=0,
        )

        reticule_text = Text("Réticule", font_size=24, color=WHITE)

        f = 5
        shift = 3.5
        pos_image = Dot([-shift - f / 4, 1, 0], color=WHITE)
        pos_image.set_opacity(0.0)

        arrow_obj = Arrow(
            start=[pos_image.get_center()[0], 0, 0],
            end=pos_image.get_center(),
            color=BLUE,
            stroke_width=4,
            buff=0,
        )
        text_obj = Text("Image", font_size=24, color=BLUE)
        text_obj.next_to(arrow_obj, UP, buff=0.2)

        reticule.shift(LEFT * (shift + f / 4))
        reticule_text.next_to(reticule, DOWN)

        F_oc = Tex(
            r"$F_\text{oc}$",
            font_size=32,
            color=WHITE,
        )
        F_oc.next_to(arrow_obj, DOWN, buff=0.2)

        background_rectangle = BackgroundRectangle(
            F_oc, color=BLACK, fill_opacity=0.9, buff=0.1
        )

        lens = ConvergingLens(
            focal_length=f, height=3.1, color=WHITE, show_focal_points=False
        )
        lens.shift(LEFT * shift)

        lens2 = ConvergingLens(
            focal_length=f, height=3, color=WHITE, show_focal_points=False
        )
        lens2.shift(RIGHT * (f * 2 / 3 - shift))

        eye = Eye(
            focal_length=3.2,
            pupil_diameter=1,
            lens_diameter=1.5,
            focal_delta=-0.05,
            show_cornea=True,
        )
        # self.bring_to_back(eye)
        eye.shift(RIGHT * 1.5)

        optical_elements = [lens, lens2]  # , *eye.get_optical_elements()]

        oc_body_path = (
            "/Users/corentinnannini/sDrive/BIO IO/VIDEO 1 - OCULAIRE/occ_body.svg"
        )
        oc_body = SVGMobject(oc_body_path, height=4.7)
        oc_body.shift(LEFT * 2.7)

        N_ray = 25
        bundle_height = 4.0
        x_start_pos = -5

        oeil_text = Text("Œil emmétrope au repos", font_size=24, color=WHITE)
        oeil_text.next_to(eye.retina, UP)

        self.add(pos_image)

        ray_bundle = RayBundle(
            start_points=[pos_image for _ in range(N_ray)],
            direction_angle_deg=[i for i in np.linspace(-12, 12, N_ray)],
            optical_elements=optical_elements,
            color=GREEN_E,
            stroke_width=2,
        )

        ray_bundle_2 = RayBundle(
            start_points=[pos_image.get_center() + DOWN for _ in range(N_ray)],
            direction_angle_deg=[i for i in np.linspace(-12, 12, N_ray)],
            optical_elements=optical_elements,
            color=TEAL_E,
            stroke_width=2,
        )

        ray_bundle_3 = RayBundle(
            start_points=[pos_image.get_center() + DOWN * 2 for _ in range(N_ray)],
            direction_angle_deg=[i for i in np.linspace(-12, 12, N_ray)],
            optical_elements=optical_elements,
            color=YELLOW_E,
            stroke_width=2,
        )

        self.play(
            optical_axis_animation,
            Create(reticule),
            Write(reticule_text),
            run_time=0.1,
            lag_ratio=0.1,
        )
        self.play(
            Create(background_rectangle),
            Write(F_oc),
            Flash(F_oc.get_center(), color=WHITE, flash_radius=0.3),
            Create(oc_body),
            run_time=1.2,
            lag_ratio=0.1,
        )
        self.pause(0.1)

        self.play(
            lens.create(),
            lens2.create(),
            # Create(arrow_obj),
            # Write(text_obj),
            run_time=1,
            lag_ratio=0.1,
        )
        # self.bring_to_back(eye)

        self.pause(0.1)
        self.play(
            ray_bundle.animate_propagation(run_time=1, lag_ratio=0.02),
            ray_bundle_2.animate_propagation(run_time=1, lag_ratio=0.02),
            ray_bundle_3.animate_propagation(run_time=1, lag_ratio=0.02),
            run_time=0.1,
        )

        self.pause(0.1)
        self.camera.frame.save_state()

        self.play(
            self.camera.frame.animate.move_to(RIGHT * 2).set(width=18), run_time=1
        )

        self.pause(1)

        eye.shift(RIGHT * 12)

        ray_bundle.add_optical_elements(eye.get_optical_elements())
        ray_bundle_2.add_optical_elements(eye.get_optical_elements())
        ray_bundle_3.add_optical_elements(eye.get_optical_elements())
        self.play(Create(eye), run_time=1)

        self.pause(0.1)

        self.play(eye.animate.shift(LEFT * 6), run_time=2)

        self.pause(0.1)

        self.play(eye.animate.shift(LEFT * 6), Restore(self.camera.frame), run_time=2)

        self.pause(1)
        # Write(oeil_text),
        # Create(eye),
