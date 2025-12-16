"""
Base Optical Element - Abstract base class for all optical elements
===================================================================

This module provides the base OpticalElement class and utility functions.
"""

from abc import ABC, abstractmethod
import numpy as np
from manim import *


def rotate_vector_2d(vector: np.ndarray, angle: float) -> np.ndarray:
    """
    Rotate a 2D vector by an angle around the z-axis.

    Parameters
    ----------
    vector : np.ndarray
        The vector to rotate (3D, but rotation is in xy-plane)
    angle : float
        Angle in radians

    Returns
    -------
    np.ndarray
        Rotated vector
    """
    cos_a = np.cos(angle)
    sin_a = np.sin(angle)
    x, y = vector[0], vector[1]
    return np.array([x * cos_a - y * sin_a, x * sin_a + y * cos_a, vector[2]])


class OpticalElement(VGroup, ABC):
    """
    Abstract base class for all optical elements.

    This class provides the interface that all optical elements must implement
    to work with the dynamic ray tracing system.

    Future extensions can inherit from this class to add:
    - Thick lenses
    - Curved mirrors
    - Prisms
    - Complex optical systems
    """

    def __init__(
        self,
        refractive_index_before: float = 1.0,
        refractive_index_after: float = 1.0,
        **kwargs
    ):
        super().__init__(**kwargs)
        self._optical_axis = RIGHT  # Default optical axis direction
        self.n_before = refractive_index_before  # Refractive index before element
        self.n_after = refractive_index_after  # Refractive index after element

    @abstractmethod
    def intersect(self, ray_start: np.ndarray, ray_direction: np.ndarray) -> tuple:
        """
        Calculate intersection point(s) of a ray with this optical element.

        Parameters
        ----------
        ray_start : np.ndarray
            Starting point of the ray
        ray_direction : np.ndarray
            Direction vector of the ray (normalized)

        Returns
        -------
        tuple
            (intersection_point, has_intersection)
            - intersection_point: np.ndarray or None
            - has_intersection: bool
        """
        pass

    @abstractmethod
    def propagate_ray(
        self,
        ray_start: np.ndarray,
        ray_direction: np.ndarray,
        intersection_point: np.ndarray,
    ) -> tuple:
        """
        Calculate the new ray direction after interaction with this element.

        Parameters
        ----------
        ray_start : np.ndarray
            Starting point of the incoming ray
        ray_direction : np.ndarray
            Direction of the incoming ray
        intersection_point : np.ndarray
            Point where the ray intersects this element

        Returns
        -------
        tuple
            (new_direction, continues)
            - new_direction: np.ndarray (normalized direction vector)
            - continues: bool (whether the ray continues or is absorbed)
        """
        pass

    def get_normal_at(self, point: np.ndarray) -> np.ndarray:
        """
        Get the normal vector at a given point on the optical element.

        Parameters
        ----------
        point : np.ndarray
            Point on the surface of the element

        Returns
        -------
        np.ndarray
            Normal vector at the point (normalized)
        """
        # Default implementation for planar elements
        return UP

    def get_center(self) -> np.ndarray:
        """Get the center position of the optical element."""
        return super().get_center()

    def get_optical_plane_position(self) -> np.ndarray:
        """
        Get the position of the optical plane (where rays interact).

        For most elements, this is the same as get_center().
        Override this in subclasses if the optical plane differs from the VGroup center.

        Returns
        -------
        np.ndarray
            Position of the optical plane
        """
        return self.get_center()

    def is_mirror(self) -> bool:
        """
        Check if this optical element is a mirror (reflects rays).

        Returns
        -------
        bool
            True if this is a mirror, False otherwise
        """
        return False

    def create(self, run_time: float = 1.0) -> Animation:
        """
        Create an animation for the appearance of this optical element.

        Parameters
        ----------
        run_time : float
            Duration of the animation

        Returns
        -------
        Animation
            Animation object to be played
        """
        return FadeIn(self, run_time=run_time)

    @abstractmethod
    def get_transfer_matrix(self) -> np.ndarray:
        """
        Get the ABCD transfer matrix for this optical element.

        The transfer matrix relates input ray state [y, θ] to output state:
        [y_out]   [A B] [y_in]
        [θ_out] = [C D] [θ_in]

        Returns
        -------
        np.ndarray
            2x2 transfer matrix
        """
        pass
