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

# Base classes
from .base import OpticalElement, rotate_vector_2d

# Lenses
from .lenses import ThinLens, ConvergingLens, DivergingLens

# Mirrors
from .mirrors import Mirror, PlaneMirror, SphericalMirror

# Beam Stops
from .beam_stops import BeamStop, LineBeamStop, CircularAperture, ArcBeamStop

# Eye
from .eye import Eye

# Centered System
from .centered_system import CenteredSystem

# 3D Optics
from .optics_3d import OpticalElement3D, ThinLens3D, RayBundle3D

# Rays
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

# Scene utilities
from .scene_utils import (
    OpticalScene,
    create_object_arrow,
    create_image_arrow,
    calculate_image_position,
)

# Miscellaneous utilities
from .miscellaneous import (
    Graticule,
    LinearGraticule,
    CrossGraticule,
    GridGraticule,
)

__version__ = "0.1.0"

__all__ = [
    # Base
    "OpticalElement",
    "rotate_vector_2d",
    # Lenses
    "ThinLens",
    "ConvergingLens",
    "DivergingLens",
    # Mirrors
    "Mirror",
    "PlaneMirror",
    "SphericalMirror",
    # Beam stops
    "BeamStop",
    "LineBeamStop",
    "CircularAperture",
    "ArcBeamStop",
    # Composite systems
    "Eye",
    "CenteredSystem",
    # 3D Optics
    "OpticalElement3D",
    "ThinLens3D",
    "RayBundle3D",
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
    # Miscellaneous
    "Graticule",
    "LinearGraticule",
    "CrossGraticule",
    "GridGraticule",
]
