"""
README Example Scenes - Optimized for GIF export

Each scene corresponds to an example in the README and is designed
to be rendered and exported as an animated GIF.

To render and convert to GIF:

  # 1. Render each scene to MP4 (low quality for fast rendering)
  manim test/test_readme_examples.py Example1_LensBundle -ql -o example1.mp4
  manim test/test_readme_examples.py Example2_AnimatedFocalLength -ql -o example2.mp4
  manim test/test_readme_examples.py Example3_EyeAccommodation -ql -o example3.mp4
  manim test/test_readme_examples.py Example4_PrincipalPlanes -ql -o example4.mp4
  manim test/test_readme_examples.py Example5_RealVsVirtual -ql -o example5.mp4
  manim test/test_readme_examples.py Example6_MeasuredFocus -ql -o example6.mp4
  manim test/test_readme_examples.py Example7_Focal3D -ql -o example7.mp4

  # 2. Convert MP4 to GIF using ffmpeg
  ffmpeg -i example1.mp4 -vf "fps=10,scale=640:-1" example1.gif
  ffmpeg -i example2.mp4 -vf "fps=10,scale=640:-1" example2.gif
  # ... etc for others
"""

import numpy as np
from manim import *
from manim_optics import (
    ConvergingLens,
    RayBundle,
    create_parallel_bundle,
    Eye,
    CenteredSystem,
    DynamicRay,
    SphericalMirror,
    ImageFormation,
    LinearGraticule,
    ThinLens3D,
    RayBundle3D,
)


class Example1_LensBundle(Scene):
    """
    Example 1: Parallel bundle through a converging lens
    Duration: ~3 seconds
    """

    def construct(self):
        lens = ConvergingLens(focal_length=2.0, height=2.8, show_focal_points=True)

        rays = create_parallel_bundle(
            num_rays=5,
            spacing=0.45,
            start_x=-5,
            optical_elements=[lens],
            color=YELLOW,
        )

        self.play(lens.create())
        self.play(rays.animate_create(run_time=1.8, lag_ratio=0.08))
        self.wait(0.5)


class Example2_AnimatedFocalLength(Scene):
    """
    Example 2: Animated focal length with live ray updates
    Duration: ~5 seconds
    """

    def construct(self):
        lens = ConvergingLens(focal_length=2.0, height=2.0, show_focal_points=True)

        rays = RayBundle(
            start_points=[np.array([-5, y, 0]) for y in np.linspace(-0.8, 0.8, 5)],
            direction_angle_deg=[0] * 5,
            optical_elements=[lens],
            color=YELLOW,
            stroke_width=2,
        )

        self.add(lens)
        self.play(rays.animate_fade_in(run_time=1.0))
        self.wait(0.5)
        self.play(lens.animate_focal_length(3.0, run_time=2.0))
        self.wait(0.5)
        self.play(lens.animate_focal_length(1.5, run_time=2.0))
        self.wait(0.5)


class Example3_EyeAccommodation(Scene):
    """
    Example 3: Eye accommodation
    Duration: ~4 seconds
    """

    def construct(self):
        eye = Eye(
            focal_length=2.0,
            lens_diameter=1.2,
            pupil_diameter=0.5,
            include_pupil=True,
        )
        eye.shift(RIGHT * 2)

        rays = RayBundle(
            start_points=[np.array([-5, y, 0]) for y in np.linspace(-0.4, 0.4, 11)],
            direction_angle_deg=[0] * 11,
            optical_elements=eye.get_optical_elements(),
            color=YELLOW,
            stroke_width=2,
        )

        self.add(eye, rays)
        self.wait(0.5)
        self.play(eye.animate_focal_length(1.5, run_time=2.0))
        self.wait(0.5)
        self.play(eye.animate_pupil_diameter(0.8, run_time=1.0))
        self.wait(0.5)


class Example4_PrincipalPlanes(Scene):
    """
    Example 4: Principal planes with CenteredSystem
    Duration: ~3 seconds
    """

    def construct(self):
        system = CenteredSystem(
            h_position=-1.5,
            h_prime_position=1.5,
            focal_length=3.0,
            height=4.0,
            show_labels=True,
            show_focal_points=True,
        )

        ray = DynamicRay(
            start_point=np.array([-6.0, 0.8, 0.0]),
            direction=RIGHT,
            optical_elements=[system],
            color=YELLOW,
            ray_length=12.0,
        )

        self.play(system.create_animation(run_time=1.8))
        self.play(Create(ray))
        self.wait(1)


class Example5_RealVsVirtual(Scene):
    """
    Example 5: Real and virtual image formation
    Duration: ~3 seconds
    """

    def construct(self):
        mirror = SphericalMirror(
            radius_of_curvature=-3,
            height=4,
            side="left",
        )
        mirror.shift(RIGHT * 3)

        rays = create_parallel_bundle(
            num_rays=3,
            spacing=1.0,
            start_x=-2,
            optical_elements=[mirror],
            color=YELLOW,
        )

        image = ImageFormation(
            ray_bundle=rays,
            optical_element_index=0,
            show_extensions=True,
            show_focal_point=True,
        )

        self.add(mirror, rays, image)
        self.wait(2.5)


class Example6_MeasuredFocus(Scene):
    """
    Example 6: Graticule overlay for optical measurements
    Duration: ~3 seconds
    """

    def construct(self):
        lens = ConvergingLens(focal_length=2.0, height=3.0, color=BLUE_C)
        lens.shift(RIGHT)

        rays = RayBundle(
            start_points=[np.array([-5, y, 0]) for y in np.linspace(-1, 1, 5)],
            direction_angle_deg=[0] * 5,
            optical_elements=[lens],
            color=YELLOW,
            stroke_width=2,
        )

        graticule = LinearGraticule(
            direction=UP,
            length=4,
            unit_length=0.5,
            primary_interval=1,
            secondary_interval=0.1,
            tick_position="outside",
            show_labels=True,
            decimal_places=1,
        )
        graticule.shift(RIGHT * 3)

        self.play(lens.create())
        self.add(rays)
        self.play(rays.animate_propagation(run_time=1.8))
        self.play(graticule.create_animation(run_time=1.0))
        self.wait(0.5)


class Example7_Focal3D(ThreeDScene):
    """
    Example 7: 3D focusing
    Duration: ~4 seconds
    """

    def construct(self):
        self.begin_ambient_camera_rotation(rate=0.1)
        lens = ThinLens3D(
            focal_length=4.0,
            aperture_radius=2.5,
            position=ORIGIN,
            normal_vector=RIGHT,
            display_mode="simple",
            color=BLUE_E,
            opacity=0.6,
            show_focal_points=True,
        )

        ray_starts = [np.array([-6, y, 0]) for y in np.linspace(-1.5, 2, 5)]

        rays = RayBundle3D(
            start_points=ray_starts,
            direction_vector=RIGHT,
            optical_elements=[lens],
            color=YELLOW,
            stroke_width=1,
            max_length=12,
        )

        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES, zoom=0.6)
        self.play(FadeIn(lens))
        self.play(Create(rays), run_time=2.0)
        self.wait(1)
