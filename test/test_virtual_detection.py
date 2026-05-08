"""
Test de détection des images virtuelles vs réelles pour différentes configurations.
"""

import numpy as np
from manim import *

from manim_optics import (
    ImageFormation,
    SphericalMirror,
    ThinLens,
    create_parallel_bundle,
)


class TestVirtualDetection(Scene):
    def construct(self):
        # Test 1: Miroir CONCAVE (R > 0) avec rayons parallèles
        # Image RÉELLE devant le miroir → PAS d'extension
        print("\n=== TEST 1: MIROIR CONCAVE (image réelle) ===")
        mirror_concave = SphericalMirror(
            position=np.array([3, 0, 0]),
            radius_of_curvature=3,  # Concave, f = 1.5
            height=4,
            side="left",
        )

        rays1 = create_parallel_bundle(
            start_x=-2,
            y_range=(-1.5, 1.5),
            num_rays=3,
            direction_vector=np.array([1, 0, 0]),
            optical_elements=[mirror_concave],
        )

        image1 = ImageFormation(
            ray_bundle=rays1,
            optical_element_index=0,
            show_extensions=True,
            show_focal_point=True,
        )

        img_pos1 = image1.get_image_position()
        print(f"Miroir concave: image at {img_pos1}")
        print("  Should be REAL (x < 3) → NO extensions")

        # Test 2: Miroir CONVEXE (R < 0) avec rayons parallèles
        # Image VIRTUELLE derrière le miroir → AVEC extension
        print("\n=== TEST 2: MIROIR CONVEXE (image virtuelle) ===")
        mirror_convex = SphericalMirror(
            position=np.array([3, 2, 0]),
            radius_of_curvature=-3,  # Convexe, f = -1.5
            height=4,
            side="left",
        )

        rays2 = create_parallel_bundle(
            start_x=-2,
            y_range=(0.5, 3.5),
            num_rays=3,
            direction_vector=np.array([1, 0, 0]),
            optical_elements=[mirror_convex],
        )

        image2 = ImageFormation(
            ray_bundle=rays2,
            optical_element_index=0,
            show_extensions=True,
            show_focal_point=True,
        )

        img_pos2 = image2.get_image_position()
        print(f"Miroir convexe: image at {img_pos2}")
        print("  Should be VIRTUAL (x > 3) → WITH extensions")

        # Test 3: Lentille CONVERGENTE (f > 0) avec objet loin
        # Image RÉELLE après la lentille → PAS d'extension
        print("\n=== TEST 3: LENTILLE CONVERGENTE (image réelle) ===")
        lens_conv = ThinLens(
            position=np.array([3, -2, 0]),
            focal_length=1.5,
            height=4,
        )

        rays3 = create_parallel_bundle(
            start_x=-2,
            y_range=(-3.5, -0.5),
            num_rays=3,
            direction_vector=np.array([1, 0, 0]),
            optical_elements=[lens_conv],
        )

        image3 = ImageFormation(
            ray_bundle=rays3,
            optical_element_index=0,
            show_extensions=True,
            show_focal_point=True,
        )

        img_pos3 = image3.get_image_position()
        print(f"Lentille convergente: image at {img_pos3}")
        print("  Should be REAL (x > 3) → NO extensions")

        # Test 4: Lentille DIVERGENTE (f < 0) avec rayons parallèles
        # Image VIRTUELLE avant la lentille → AVEC extension
        print("\n=== TEST 4: LENTILLE DIVERGENTE (image virtuelle) ===")
        lens_div = ThinLens(
            position=np.array([-3, 0, 0]),
            focal_length=-1.5,
            height=4,
        )

        rays4 = create_parallel_bundle(
            start_x=-8,
            y_range=(-1.5, 1.5),
            num_rays=3,
            direction_vector=np.array([1, 0, 0]),
            optical_elements=[lens_div],
        )

        image4 = ImageFormation(
            ray_bundle=rays4,
            optical_element_index=0,
            show_extensions=True,
            show_focal_point=True,
        )

        img_pos4 = image4.get_image_position()
        print(f"Lentille divergente: image at {img_pos4}")
        print("  Should be VIRTUAL (x < -3) → WITH extensions")

        # Add all to scene
        self.add(mirror_concave, rays1, image1)
        self.add(mirror_convex, rays2, image2)
        self.add(lens_conv, rays3, image3)
        self.add(lens_div, rays4, image4)

        self.wait(0.1)

        # Vérifier les extensions
        print("\n=== VERIFICATION DES EXTENSIONS ===")
        extensions_data = [
            ("Miroir concave (réelle)", image1, False),
            ("Miroir convexe (virtuelle)", image2, True),
            ("Lentille convergente (réelle)", image3, False),
            ("Lentille divergente (virtuelle)", image4, True),
        ]

        for name, img_formation, should_have_ext in extensions_data:
            has_extensions = False
            for ext in img_formation.extended_rays:
                if ext.get_opacity() > 0:
                    has_extensions = True
                    break

            status = "✓" if has_extensions == should_have_ext else "✗"
            print(
                f"{status} {name}: extensions={has_extensions} (attendu={should_have_ext})"
            )
