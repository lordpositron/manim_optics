import numpy as np
from manim import *

from manim_optics import (
    ImageFormation,
    SphericalMirror,
    create_parallel_bundle,
)


class TestMirrorExtensions(Scene):
    def construct(self):
        # Create a convex mirror: R = -3, f = -1.5
        # Mirror at x = 3, focal point at x = 3 - 1.5 = 1.5
        # Virtual image should be at x = 4.5 for object at infinity
        mirror = SphericalMirror(
            position=np.array([3, 0, 0]),
            radius_of_curvature=-3,  # Convex mirror
            height=4,
            side="left",  # Reflective side facing left
        )

        # Create parallel rays from the left
        rays = create_parallel_bundle(
            start_x=-5,
            y_range=(-1.5, 1.5),
            num_rays=4,
            direction_vector=np.array([1, 0, 0]),
            optical_elements=[mirror],
        )

        # Create image formation visualization
        image_viz = ImageFormation(
            ray_bundle=rays,
            optical_element_index=0,
            show_extensions=True,
            show_focal_point=True,
            show_image_arrow=True,
        )

        self.add(mirror, rays, image_viz)
        self.wait(0.1)

        # Get the image position
        image_pos = image_viz.get_image_position()
        print(f"Image position: {image_pos}")

        # Check extension points
        for i, ext in enumerate(image_viz.extended_rays):
            points = ext.get_points()
            if len(points) > 0:
                print(f"Extension {i}: {len(points)} points")
                print(f"  First point: {points[0]}")
                print(f"  Last point: {points[-1]}")
