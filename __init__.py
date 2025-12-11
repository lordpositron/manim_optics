"""
Manim Optics - Dynamic optical ray tracing for Manim
=====================================================

A package for creating dynamic optical simulations with automatic ray updates.

Features:
- Thin lenses (converging and diverging)
- Plane mirrors
- Dynamic ray tracing with automatic updates
- Paraxial optics calculations

Author: Corentin Nannini
Date: December 2025
"""

from .optical_elements import (
    OpticalElement,
    ThinLens,
    ConvergingLens,
    DivergingLens,
    Mirror,
    PlaneMirror,
)

from .rays import (
    DynamicRay,
    RayBundle,
    PrincipalRays,
    create_parallel_bundle,
    create_diverging_bundle,
    RayExtension,
    find_ray_intersection,
    ImageMarker,
    ImageFormation,
    find_focal_point_from_rays,
)

from .scene_utils import (
    OpticalScene,
    create_object_arrow,
    create_image_arrow,
    calculate_image_position,
)

__version__ = "0.1.0"

__all__ = [
    # Optical elements
    "OpticalElement",
    "ThinLens",
    "ConvergingLens",
    "DivergingLens",
    "Mirror",
    "PlaneMirror",
    # Rays
    "DynamicRay",
    "RayBundle",
    "PrincipalRays",
    "create_parallel_bundle",
    "create_diverging_bundle",
    "RayExtension",
    "find_ray_intersection",
    "find_focal_point_from_rays",
    "ImageMarker",
    "ImageFormation",
    # Scene utilities
    "OpticalScene",
    "create_object_arrow",
    "create_image_arrow",
    "calculate_image_position",
]
