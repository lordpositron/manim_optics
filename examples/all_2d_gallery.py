"""
Gallery 2D — all manim_optics 2D elements in one film.
=======================================================
Sections:
  01 — Ray Bundles
  02 — Thin Lenses
  03 — Beam Stops
  04 — Mirrors
  05 — Eye Model
  06 — Graticules
"""

import numpy as np
from manim import *

from manim_optics import *


class Gallery2D(OpticalScene):
    """Full 2-D showcase of manim_optics elements."""

    ANIM_TIME = 0.5
    TEXT_TIME = 0.2

    # ─── helpers ──────────────────────────────────────────────────────────

    def _clear(self):
        if self.mobjects:
            self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)

    def _title(self, num: int, title: str):
        t = Text(f"{num:02d} — {title}", font_size=44, color=WHITE, weight=BOLD)
        self.play(Write(t), run_time=0.5)
        self.wait(0.7)
        self.play(FadeOut(t), run_time=0.4)

    def _label(self, text: str) -> Text:
        lbl = Text(text, font_size=32, color=GREY_A).to_corner(UL, buff=0.3)
        self.play(FadeIn(lbl), run_time=0.3)
        return lbl

    def _ann(self, text: str) -> Text:
        ann = Text(text, font_size=24, color=YELLOW_A).to_corner(DR, buff=0.3)
        self.play(FadeIn(ann), run_time=0.25)
        return ann

    # ─── 01 — Ray Bundles ─────────────────────────────────────────────────

    def scene_01_ray_bundles(self):
        self._title(1, "Ray Bundles")
        self.play(self.get_optical_axis_animation(), run_time=self.ANIM_TIME)

        # Parallel bundle — offset trackers
        lbl = self._label("Parallel bundle — y_offset_tracker & angle_offset_tracker")
        bundle = RayBundle(
            start_points=[np.array([-6, y, 0]) for y in np.linspace(-1.5, 1.5, 7)],
            direction_angle_deg=0,
            optical_elements=[],
            color=YELLOW_E,
            stroke_width=2,
        )
        self.play(bundle.animate_propagation(run_time=self.ANIM_TIME))
        self.wait(self.TEXT_TIME)

        ann = self._ann("y_offset_tracker")
        self.play(
            bundle.y_offset_tracker.animate.set_value(1.3), run_time=self.ANIM_TIME
        )
        self.play(
            bundle.y_offset_tracker.animate.set_value(-1.3), run_time=self.ANIM_TIME
        )
        self.play(
            bundle.y_offset_tracker.animate.set_value(0.0), run_time=self.ANIM_TIME
        )
        self.play(FadeOut(ann), run_time=self.TEXT_TIME)

        ann2 = self._ann("angle_offset_tracker")
        self.play(
            bundle.angle_offset_tracker.animate.set_value(15), run_time=self.ANIM_TIME
        )
        self.play(
            bundle.angle_offset_tracker.animate.set_value(-15), run_time=self.ANIM_TIME
        )
        self.play(
            bundle.angle_offset_tracker.animate.set_value(0.0), run_time=self.ANIM_TIME
        )
        self.play(FadeOut(ann2), run_time=self.TEXT_TIME)
        self.play(FadeOut(bundle), FadeOut(lbl), run_time=self.TEXT_TIME)

        # Diverging bundle from a Mobject source
        lbl2 = self._label("Diverging bundle from a Mobject source")
        source = Dot(np.array([-3.5, 0, 0]), color=WHITE, radius=0.1)
        self.play(FadeIn(source), run_time=0.3)
        div_bundle = RayBundle(
            start_points=source,
            direction_angle_deg=list(np.linspace(-22, 22, 9)),
            optical_elements=[],
            color=TEAL,
            stroke_width=2,
        )
        self.play(div_bundle.animate_propagation(run_time=0.9))
        self.wait(0.3)

        ann3 = self._ann("source Mobject moves → rays follow")
        self.play(
            source.animate.move_to(np.array([-3.5, 1.2, 0])), run_time=self.ANIM_TIME
        )
        self.play(
            source.animate.move_to(np.array([-3.5, -1.2, 0])), run_time=self.ANIM_TIME
        )
        self.play(
            source.animate.move_to(np.array([-3.5, 0.0, 0])), run_time=self.ANIM_TIME
        )

        ann2 = self._ann("angle_offset_tracker")
        self.play(
            div_bundle.angle_offset_tracker.animate.set_value(15),
            run_time=self.ANIM_TIME,
        )
        self.play(
            div_bundle.angle_offset_tracker.animate.set_value(-15),
            run_time=self.ANIM_TIME,
        )
        self.play(
            div_bundle.angle_offset_tracker.animate.set_value(0.0),
            run_time=self.ANIM_TIME,
        )
        self.play(FadeOut(ann2), run_time=self.TEXT_TIME)
        self.play(FadeOut(div_bundle), FadeOut(lbl2), run_time=self.TEXT_TIME)
        self.play(FadeOut(ann3), run_time=self.ANIM_TIME)
        self.wait(self.TEXT_TIME)
        self._clear()

    # ─── 02 — Thin Lenses ─────────────────────────────────────────────────

    def scene_02_lenses(self):
        self._title(2, "Thin Lenses")
        self.play(self.get_optical_axis_animation(), run_time=self.TEXT_TIME)

        # ConvergingLens — focal_length_tracker & position
        lbl = self._label("ConvergingLens — focal_length_tracker & position")
        lens = ConvergingLens(focal_length=2.5, height=3.5, color=WHITE)
        lens.shift(RIGHT * 1.0)
        f_lbl = always_redraw(
            lambda: Tex(
                f"$f'$ = {lens.focal_length_tracker.get_value():.1f}",
                font_size=24,
                color=BLUE_B,
            ).move_to(lens.get_optical_plane_position() + DOWN * 2.2)
        )
        bundle = RayBundle(
            start_points=[np.array([-6, y, 0]) for y in np.linspace(-1.4, 1.4, 7)],
            direction_angle_deg=0,
            optical_elements=[lens],
            color=YELLOW_E,
            stroke_width=2,
        )
        self.play(Create(lens), Write(f_lbl), run_time=self.ANIM_TIME)
        self.play(bundle.animate_propagation(run_time=self.ANIM_TIME))
        self.wait(self.TEXT_TIME)

        ann = self._ann("focal_length_tracker")
        self.play(
            lens.focal_length_tracker.animate.set_value(4.5), run_time=self.ANIM_TIME
        )
        self.play(
            lens.focal_length_tracker.animate.set_value(1.5), run_time=self.ANIM_TIME
        )
        self.play(
            lens.focal_length_tracker.animate.set_value(2.5), run_time=self.ANIM_TIME
        )
        self.play(FadeOut(ann), run_time=self.ANIM_TIME)

        ann2 = self._ann("lens.animate.shift()")
        self.play(lens.animate.shift(LEFT * 2.5), run_time=self.ANIM_TIME)
        self.play(lens.animate.shift(RIGHT * 2.5), run_time=self.ANIM_TIME)
        self.play(
            FadeOut(ann2),
            FadeOut(f_lbl),
            FadeOut(bundle),
            FadeOut(lbl),
            run_time=self.ANIM_TIME,
        )

        # Image formation
        lbl2 = self._label("Image formation — diverging source")
        source = Dot(np.array([-4.5, 0.9, 0]), color=WHITE, radius=0.08)
        source.set_opacity(0)
        self.add(source)
        div_bundle = RayBundle(
            start_points=source,
            direction_angle_deg=list(np.linspace(-10, 5, 9)),
            optical_elements=[lens],
            color=YELLOW,
            stroke_width=2,
        )
        self.play(div_bundle.animate_propagation(run_time=self.ANIM_TIME))
        self.play(
            source.animate.move_to(np.array([-2.5, -0.8, 0])),
            run_time=self.ANIM_TIME * 1.2,
        )
        self.wait(self.TEXT_TIME)
        self.play(
            source.animate.move_to(np.array([-1.5, 0.4, 0])),
            run_time=self.ANIM_TIME * 1.2,
        )
        self.wait(self.TEXT_TIME)
        self.play(FadeOut(div_bundle), FadeOut(lbl2), run_time=self.TEXT_TIME)

        # DivergingLens
        lbl3 = self._label("DivergingLens")
        self.play(FadeOut(lens), run_time=self.TEXT_TIME)
        div_lens = DivergingLens(focal_length=-2.5, height=4, color=WHITE)
        div_lens.shift(RIGHT * 0.5)
        par_bundle = RayBundle(
            start_points=[np.array([-6, y, 0]) for y in np.linspace(-1.4, 1.4, 7)],
            direction_angle_deg=0,
            optical_elements=[div_lens],
            color=YELLOW_E,
            stroke_width=2,
        )
        self.play(Create(div_lens), run_time=self.ANIM_TIME)
        self.play(par_bundle.animate_propagation(run_time=self.ANIM_TIME))
        self.wait(self.TEXT_TIME)
        ann = self._ann("focal_length_tracker")
        self.play(
            div_lens.focal_length_tracker.animate.set_value(-4.5),
            run_time=self.ANIM_TIME,
        )
        self.play(
            div_lens.focal_length_tracker.animate.set_value(-1.5),
            run_time=self.ANIM_TIME,
        )
        self.play(
            div_lens.focal_length_tracker.animate.set_value(-2.5),
            run_time=self.ANIM_TIME,
        )
        self.play(FadeOut(ann), run_time=self.ANIM_TIME)
        self.play(FadeOut(par_bundle), FadeOut(lbl3), run_time=self.TEXT_TIME)

        # Two lenses in series
        lbl4 = self._label("Two lenses in series")
        lens2 = ConvergingLens(focal_length=2.0, height=4.0, color=WHITE)
        lens2.shift(LEFT * 3.0)
        relay_bundle = RayBundle(
            start_points=[np.array([-6, y, 0]) for y in np.linspace(-1.2, 1.2, 7)],
            direction_angle_deg=0,
            optical_elements=[lens2, div_lens],
            color=TEAL,
            stroke_width=2,
        )
        self.play(Create(lens2), run_time=self.ANIM_TIME)
        self.play(relay_bundle.animate_propagation(run_time=self.ANIM_TIME))
        self.wait(self.TEXT_TIME)
        self.play(lens2.animate.shift(RIGHT * 1), run_time=self.ANIM_TIME)
        self.wait(self.TEXT_TIME)
        self.play(div_lens.animate.shift(RIGHT * 1.5), run_time=self.ANIM_TIME)
        self.wait(self.TEXT_TIME)
        self._clear()

    # ─── 03 — Beam Stops ──────────────────────────────────────────────────

    def scene_03_beam_stops(self):
        self._title(3, "Beam Stops")
        self.play(self.get_optical_axis_animation(), run_time=self.ANIM_TIME)

        lens = ConvergingLens(focal_length=3.0, height=4.5, color=WHITE)
        lens.shift(RIGHT * 1.5)
        self.play(Create(lens), run_time=self.ANIM_TIME)

        # CircularAperture upstream
        lbl = self._label("CircularAperture upstream — radius_tracker")
        aperture = CircularAperture(radius=0.7, total_length=5)
        aperture.shift(LEFT * 1.0)
        bundle = RayBundle(
            start_points=[np.array([-6, y, 0]) for y in np.linspace(-2.0, 2.0, 11)],
            direction_angle_deg=0,
            optical_elements=[aperture, lens],
            color=YELLOW_E,
            stroke_width=2,
        )
        self.play(Create(aperture), run_time=self.ANIM_TIME)
        self.play(bundle.animate_propagation(run_time=self.ANIM_TIME))
        self.wait(self.TEXT_TIME)

        ann = self._ann("radius_tracker grows / shrinks")
        self.play(
            aperture.radius_tracker.animate.set_value(1.8), run_time=self.ANIM_TIME * 2
        )
        self.play(
            aperture.radius_tracker.animate.set_value(0.15), run_time=self.ANIM_TIME * 2
        )
        self.play(
            aperture.radius_tracker.animate.set_value(0.7), run_time=self.ANIM_TIME * 2
        )
        self.play(
            FadeOut(ann),
            FadeOut(bundle),
            FadeOut(aperture),
            FadeOut(lbl),
            run_time=self.TEXT_TIME,
        )

        # LineBeamStop as screen
        lbl2 = self._label("LineBeamStop — screen / detector after lens")
        screen = LineBeamStop(height=4.0)
        screen.shift(RIGHT * 4.5)
        bundle2 = RayBundle(
            start_points=[np.array([-6, y, 0]) for y in np.linspace(-1.5, 1.5, 7)],
            direction_angle_deg=0,
            optical_elements=[lens, screen],
            color=ORANGE,
            stroke_width=2,
        )
        self.play(Create(screen), run_time=self.ANIM_TIME)
        self.play(bundle2.animate_propagation(run_time=self.ANIM_TIME))
        self.wait(self.TEXT_TIME)

        ann2 = self._ann("screen.animate.shift() — scan focus")
        self.play(screen.animate.shift(LEFT * 1.5), run_time=self.ANIM_TIME)
        self.play(screen.animate.shift(RIGHT * 1.5), run_time=self.ANIM_TIME)
        self.play(
            FadeOut(ann2),
            FadeOut(bundle2),
            FadeOut(lbl2),
            FadeOut(screen),
            run_time=self.TEXT_TIME,
        )

        # ArcBeamStop as curved detector
        lbl3 = self._label("ArcBeamStop — curved detector / retina")
        arc_stop = ArcBeamStop(radius=3.0, arc_angle=100 * DEGREES)
        arc_stop.shift(RIGHT * 1.5)
        bundle3 = RayBundle(
            start_points=[np.array([-6, y, 0]) for y in np.linspace(-1.5, 1.5, 7)],
            direction_angle_deg=0,
            optical_elements=[lens, arc_stop],
            color=TEAL,
            stroke_width=2,
        )
        self.play(Create(arc_stop), run_time=self.ANIM_TIME)
        self.play(bundle3.animate_propagation(run_time=self.ANIM_TIME))
        self.play(arc_stop.animate.shift(LEFT * 1.0), run_time=self.ANIM_TIME)
        self.wait(self.TEXT_TIME)
        self._clear()

    # ─── 04 — Mirrors ─────────────────────────────────────────────────────

    def scene_04_mirrors(self):
        self._title(4, "Mirrors")
        self.play(self.get_optical_axis_animation(), run_time=self.ANIM_TIME)

        # PlaneMirror
        lbl = self._label("PlaneMirror — diverging source bundle")
        mirror = PlaneMirror(height=4.0)
        mirror.shift(RIGHT * 2.5)
        source = Dot(np.array([-2.5, 0, 0]), color=WHITE, radius=0.1)
        bundle = RayBundle(
            start_points=source,
            direction_angle_deg=list(np.linspace(-15, 15, 7)),
            optical_elements=[mirror],
            color=YELLOW_E,
            stroke_width=2,
        )
        self.play(Create(mirror), FadeIn(source), run_time=self.ANIM_TIME)
        self.play(bundle.animate_propagation(run_time=self.ANIM_TIME))
        self.wait(self.TEXT_TIME)

        ann = self._ann("mirror.animate.shift()")
        self.play(mirror.animate.shift(LEFT * 2.0), run_time=self.ANIM_TIME)
        self.play(mirror.animate.shift(RIGHT * 2.0), run_time=self.ANIM_TIME)

        self.play(mirror.tilt_tracker.animate.set_value(30), run_time=self.ANIM_TIME)
        self.wait(self.TEXT_TIME)
        self.play(mirror.tilt_tracker.animate.set_value(-30), run_time=self.ANIM_TIME)
        self.wait(self.TEXT_TIME)
        self.play(mirror.tilt_tracker.animate.set_value(0), run_time=self.ANIM_TIME)
        self.play(
            FadeOut(ann),
            FadeOut(bundle),
            FadeOut(source),
            FadeOut(lbl),
            run_time=self.TEXT_TIME,
        )

        # SphericalMirror concave
        lbl2 = self._label("SphericalMirror concave — parallel bundle converges")
        self.play(FadeOut(mirror), run_time=self.ANIM_TIME)
        sph = SphericalMirror(radius_of_curvature=-6.0, height=5, facing="left")
        sph.shift(RIGHT * 3)
        par_bundle = RayBundle(
            start_points=[np.array([-6, y, 0]) for y in np.linspace(-1.4, 1.4, 7)],
            direction_angle_deg=0,
            optical_elements=[sph],
            color=TEAL,
            stroke_width=2,
        )
        self.play(Create(sph), run_time=self.ANIM_TIME)
        self.play(par_bundle.animate_propagation(run_time=self.ANIM_TIME))
        self.play(sph.tilt_tracker.animate.set_value(30), run_time=self.ANIM_TIME)
        self.wait(self.TEXT_TIME)
        self.play(sph.tilt_tracker.animate.set_value(-30), run_time=self.ANIM_TIME)
        self.wait(self.TEXT_TIME)
        self.play(sph.tilt_tracker.animate.set_value(0), run_time=self.ANIM_TIME)
        self.wait(self.TEXT_TIME)

        self.play(FadeOut(par_bundle), FadeOut(lbl2), run_time=self.TEXT_TIME)
        self._clear()

    # ─── 05 — Eye Model ───────────────────────────────────────────────────

    def scene_05_eye(self):
        self._title(5, "Eye Model")
        self.play(self.get_optical_axis_animation(), run_time=self.ANIM_TIME)
        lbl = self._label("Eye — emmetropic at rest  ·  animate_focal_length")

        eye = Eye(
            focal_length=5,
            pupil_diameter=1.2,
            lens_diameter=2,
            focal_delta=-0.05,
            show_cornea=True,
        )
        eye.shift(RIGHT * 1.5)
        bundle = RayBundle(
            start_points=[np.array([-6, y, 0]) for y in np.linspace(-0.7, 0.7, 7)],
            direction_angle_deg=0,
            optical_elements=eye.get_optical_elements(),
            color=YELLOW_E,
            stroke_width=2,
        )
        self.play(Create(eye, lag_ratio=0.1), run_time=1.0)
        self.play(bundle.animate_propagation(run_time=0.9))
        self.wait(0.3)

        ann = self._ann("animate_focal_length() — accommodation")
        self.play(eye.animate_focal_length(4), run_time=1.5)
        self.wait(0.3)
        self.play(eye.animate_focal_length(6), run_time=1.5)
        self.wait(0.3)
        self.play(eye.animate_focal_length(5), run_time=1.5)
        self.wait(0.3)
        self.play(FadeOut(ann), run_time=0.2)

        # Off-axis diverging bundle
        self.play(FadeOut(bundle), FadeOut(lbl), run_time=0.3)
        lbl2 = self._label("Off-axis diverging bundle")
        source = Dot(np.array([-5.5, 1.0, 0]), color=WHITE, radius=0.08)
        source.set_opacity(0)
        self.add(source)
        bundle2 = RayBundle(
            start_points=source,
            direction_angle_deg=list(np.linspace(-12, -6, 7)),
            optical_elements=eye.get_optical_elements(),
            color=YELLOW,
            stroke_width=2,
        )
        self.play(bundle2.animate_propagation(run_time=0.9))
        self.wait(0.5)
        self.play(eye.animate_focal_length(2.9), run_time=1.5)
        self.wait(0.3)
        self.play(
            source.animate.move_to(np.array([-5.5, -1.0, 0])),
            bundle2.angle_offset_tracker.animate.set_value(18),
            run_time=1.5,
        )
        self.wait(0.3)
        self._clear()

    # ─── 06 — Graticules ──────────────────────────────────────────────────

    def scene_06_graticules(self):
        self._title(6, "Graticules")

        # LinearGraticule
        lbl = self._label("LinearGraticule — vertical & horizontal")
        lin_v = LinearGraticule(
            direction=UP,
            length=4.0,
            unit_length=1,
            primary_interval=1,
            secondary_interval=0.1,
            tick_angle=90 * DEGREES,
            color=YELLOW,
            show_labels=True,
            decimal_places=1,
        )
        lin_v.shift(LEFT * 3.5)
        lin_h = LinearGraticule(
            direction=RIGHT,
            length=6.0,
            unit_length=1,
            primary_interval=1,
            secondary_interval=0.1,
            tick_angle=90 * DEGREES,
            color=TEAL,
            show_labels=True,
            decimal_places=0,
        )

        self.play(
            lin_v.create_animation(run_time=0.8), lin_h.create_animation(run_time=0.8)
        )
        self.wait(0.8)
        self.play(FadeOut(lin_v), FadeOut(lin_h), FadeOut(lbl), run_time=0.4)

        # CrossGraticule
        lbl2 = self._label("CrossGraticule — two perpendicular axes")
        cross = CrossGraticule(
            length=6,
            unit_length=1,
            primary_interval=1,
            secondary_interval=0.1,
            color=WHITE,
            show_labels=True,
            decimal_places=0,
        )
        self.play(cross.create_animation(run_time=0.8))
        self.wait(0.8)
        self.play(FadeOut(cross), FadeOut(lbl2), run_time=0.4)

        # GridGraticule
        lbl3 = self._label("GridGraticule — 2-D reference grid")

        grid = GridGraticule(
            length=6,
            unit_length=1,
            primary_interval=1,
            secondary_interval=0.1,
            color=GREY_B,
            show_labels=False,
        )
        self.play(grid.create_animation(run_time=0.8))
        self.wait(0.8)
        self.play(FadeOut(grid), FadeOut(lbl3), run_time=0.4)
        self.wait(0.3)


class GalleryRay(Gallery2D):
    def construct(self):
        self.scene_01_ray_bundles()


class GalleryLens(Gallery2D):
    def construct(self):
        self.scene_02_lenses()


class GalleryBeamStop(Gallery2D):
    def construct(self):
        self.scene_03_beam_stops()


class GalleryMirror(Gallery2D):
    def construct(self):
        self.scene_04_mirrors()


class GalleryEyeModel(Gallery2D):
    def construct(self):
        self.scene_05_eye()


class GalleryGraticules(Gallery2D):
    def construct(self):
        self.scene_06_graticules()
