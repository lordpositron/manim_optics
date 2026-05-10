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
"""

# Base classes
from .base import OpticalElement, rotate_vector_2d

# Beam Stops
from .beam_stops import ArcBeamStop, BeamStop, CircularAperture, LineBeamStop

# Centered System
from .centered_system import CenteredSystem

# Eye
from .eye import Eye

# Lenses
from .lenses import ConvergingLens, DivergingLens, ThinLens

# Real (thick) spherical lenses — exact Snell-Descartes refraction
from .real_lenses import (
    BiconcaveLens,
    BiconvexLens,
    PlanoConcaveLens,
    PlanoConvexLens,
    SphericalLens,
)

# Mirrors
from .mirrors import Mirror, PlaneMirror, SphericalMirror

# Miscellaneous utilities
from .miscellaneous import (
    CrossGraticule,
    Graticule,
    GridGraticule,
    LinearGraticule,
)

# 3D Optics
from .optics_3d import OpticalElement3D, RayBundle3D, ThinLens3D

# Rays
from .rays import (
    DynamicRay,
    ImageFormation,
    ImageMarker,
    PrincipalRays,
    RayBundle,
    RayExtension,
    create_diverging_bundle,
    create_parallel_bundle,
    find_focal_point_from_rays,
    find_ray_intersection,
)

# Scene utilities
from .scene_utils import (
    OpticalScene,
    calculate_image_position,
    create_image_arrow,
    create_object_arrow,
)

__version__ = "0.1.0"

__all__ = [
    # Base
    "OpticalElement",
    "rotate_vector_2d",
    # Thin (ideal) lenses
    "ThinLens",
    "ConvergingLens",
    "DivergingLens",
    # Real spherical thick lenses
    "SphericalLens",
    "BiconvexLens",
    "BiconcaveLens",
    "PlanoConvexLens",
    "PlanoConcaveLens",
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
