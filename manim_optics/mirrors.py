"""
Mirrors - Mirror implementations
=================================

This module provides mirror classes for optical simulations.
"""

from abc import abstractmethod

import numpy as np
from manim import *

from .base import OpticalElement


class Mirror(OpticalElement):
    """
    Base class for mirrors.

    Implements specular reflection: angle of incidence = angle of reflection

    For mirrors, the refractive index is virtually inverted:
    n_after = -n_before (this models the path reversal)
    """

    def __init__(self, refractive_index: float = 1.0, **kwargs):
        # For mirrors, n_after = -n_before (virtual inversion)
        super().__init__(
            refractive_index_before=refractive_index,
            refractive_index_after=-refractive_index,
            **kwargs,
        )

    def is_mirror(self) -> bool:
        """Return True since this is a mirror."""
        return True

    @abstractmethod
    def get_normal_at(self, point: np.ndarray) -> np.ndarray:
        """Get the normal vector at a point on the mirror surface."""
        pass

    def get_transfer_matrix(self) -> np.ndarray:
        """
        Get the ABCD transfer matrix for a plane mirror.

        For a plane mirror: [[1, 0], [0, -1]]
        The reflection inverts the angle.
        """
        return np.array([[1.0, 0.0], [0.0, -1.0]])

    def propagate_ray(
        self,
        ray_start: np.ndarray,
        ray_direction: np.ndarray,
        intersection_point: np.ndarray,
    ) -> tuple:
        """
        Calculate reflected ray direction using the law of reflection.

        Reflection formula: R = D - 2(D·N)N
        where D is incident direction and N is surface normal
        """
        normal = self.get_normal_at(intersection_point)

        # Ensure normal points toward the incident ray
        if np.dot(ray_direction, normal) > 0:
            normal = -normal

        # Reflection: R = D - 2(D·N)N
        reflected = ray_direction - 2 * np.dot(ray_direction, normal) * normal

        # Normalize
        reflected = reflected / np.linalg.norm(reflected)

        return reflected, True


class PlaneMirror(Mirror):
    """
    Plane (flat) mirror.

    A vertical mirror that reflects rays according to the law of reflection.
    """

    def __init__(
        self,
        height: float = 3.0,
        refractive_index: float = 1.0,
        coating_side: str = "right",
        coating_count: int = 5,
        coating_angle_deg: float = 45.0,
        coating_length_ratio: float = 0.05,
        stroke_width: float = 4.0,
        coating_stroke_width: float | None = None,
        mirror_color=GREY_A,
        coating_color=GREY_C,
        **kwargs,
    ):
        """
        Initialize a plane mirror.

        Parameters
        ----------
        height : float
            Height of the mirror
        refractive_index : float
            Refractive index of the medium (default: 1.0 for air)
        coating_side : str
            Side where coating indicators are drawn ("left" or "right")
        coating_count : int
            Number of coating indicators along the mirror
        coating_angle_deg : float
            Orientation of coating indicators in degrees (default: 45°)
        coating_length_ratio : float
            Indicator length as a fraction of mirror height (default: 0.05)
        stroke_width : float
            Stroke width of the mirror line (default: 4)
        coating_stroke_width : float, optional
            Stroke width of the coating indicators (defaults to mirror stroke width)
        mirror_color : color
            Color of the mirror line
        coating_color : color
            Color of the coating indicators
        """
        super().__init__(refractive_index=refractive_index, **kwargs)
        self.mirror_height = height
        self.coating_side = coating_side
        self.coating_count = coating_count
        self.coating_angle_deg = coating_angle_deg
        self.coating_length_ratio = coating_length_ratio
        self.stroke_width = stroke_width
        self.coating_stroke_width = (
            stroke_width if coating_stroke_width is None else coating_stroke_width
        )
        self.mirror_color = mirror_color
        self.coating_color = coating_color

        # Create visual representation
        self._create_mirror_visual()

    def _create_mirror_visual(self):
        """Create the visual representation of the mirror."""
        # Mirror surface (thick line)
        mirror_line = Line(
            UP * self.mirror_height / 2,
            DOWN * self.mirror_height / 2,
            stroke_width=self.stroke_width,
            color=self.mirror_color,
        )

        # Reflective coating indicator (small lines)
        if self.coating_count > 0:
            line_length = self.mirror_height * self.coating_length_ratio
            angle = self.coating_angle_deg * DEGREES
            direction = np.array([np.cos(angle), np.sin(angle), 0.0])
            side_sign = -1.0 if self.coating_side == "left" else 1.0
            offset = side_sign * 0.02 * self.mirror_height

            for i in range(self.coating_count):
                y = (-self.mirror_height / 2) + (
                    i + 0.5
                ) * self.mirror_height / self.coating_count
                center = np.array([offset, y, 0.0])
                start_pos = center - 0.5 * line_length * direction
                end_pos = center + 0.5 * line_length * direction
                small_line = Line(
                    start_pos,
                    end_pos,
                    stroke_width=self.coating_stroke_width,
                    color=self.coating_color,
                )
                self.add(small_line)

        self.mirror_line = mirror_line
        self.add(mirror_line)

    def get_optical_plane_position(self) -> np.ndarray:
        """
        Get the position of the optical plane (the mirror line).

        Overrides the base method because the VGroup center can include
        coating indicators, which would give an incorrect position.
        """
        return self.mirror_line.get_center()

    def intersect(self, ray_start: np.ndarray, ray_direction: np.ndarray) -> tuple:
        """Calculate intersection with the mirror plane."""
        # Mirror is a vertical plane at x = mirror_center_x
        mirror_center = self.get_optical_plane_position()
        mirror_x = mirror_center[0]

        if abs(ray_direction[0]) < 1e-10:
            return None, False

        t = (mirror_x - ray_start[0]) / ray_direction[0]

        if t < 0:
            return None, False

        intersection = ray_start + t * ray_direction

        # Check if within mirror height
        mirror_y = mirror_center[1]
        if abs(intersection[1] - mirror_y) > self.mirror_height / 2:
            return None, False

        return intersection, True

    def get_normal_at(self, point: np.ndarray) -> np.ndarray:
        """
        Get the normal to the mirror at a given point.

        For a vertical plane mirror, the normal is always horizontal (LEFT).
        """
        return LEFT  # Normal pointing to the left (toward incident rays from right)


class SphericalMirror(Mirror):
    """
    Spherical mirror with a given radius of curvature.

    Uses paraxial approximation and ABCD matrix formalism.

    Convention for radius of curvature R:
    - R > 0: Concave mirror (center of curvature is in the direction of incident light)
    - R < 0: Convex mirror (center of curvature is opposite to incident light)

    In paraxial optics, the focal length of a spherical mirror is f = R/2.

    Transfer matrix for spherical mirror: [[1, 0], [-2/R, 1]]
    """

    def __init__(
        self,
        radius_of_curvature: float = 4.0,
        height: float = 3.0,
        refractive_index: float = 1.0,
        aperture_angle: float = 60 * DEGREES,
        side: str = "left",
        **kwargs,
    ):
        """
        Initialize a spherical mirror.

        Parameters
        ----------
        radius_of_curvature : float
            Radius of curvature R (positive for concave, negative for convex)
        height : float
            Height of the mirror aperture
        refractive_index : float
            Refractive index of the medium (default: 1.0 for air)
        aperture_angle : float
            Angular aperture of the mirror (in radians)
        side : str
            Side where the reflective surface is ("left" or "right")
            - "left": rays come from the right, reflect back to the right
            - "right": rays come from the left, reflect back to the left
        """
        super().__init__(refractive_index=refractive_index, **kwargs)
        self.radius_of_curvature = radius_of_curvature
        self.mirror_height = height
        self.aperture_angle = aperture_angle
        self.side = side

        # Create visual representation
        self._create_mirror_visual()

    def _create_mirror_visual(self):
        """Create the visual representation of the spherical mirror.

        In the paraxial approximation, the mirror is represented as a plane.
        The curvature only affects the transfer matrix, not the geometry.
        """
        # Mirror surface (vertical line, like plane mirror)
        mirror_line = Line(
            UP * self.mirror_height / 2,
            DOWN * self.mirror_height / 2,
            stroke_width=6,
            color=GREY_A,
        )

        # Reflective coating indicator (diagonal lines at 45° on the back side)
        num_lines = 5
        line_length = 0.2

        if self.side == "left":
            # Reflective surface on the left, diagonal lines on the right (back side)
            for i in range(num_lines):
                y = (i - num_lines / 2 + 0.5) * self.mirror_height / num_lines
                # 45° lines going from bottom-left to top-right
                start_pos = RIGHT * 0.05 + UP * (y - line_length / 2)
                end_pos = RIGHT * (0.05 + line_length) + UP * (y + line_length / 2)
                small_line = Line(
                    start_pos,
                    end_pos,
                    stroke_width=2,
                    color=GREY_C,
                )
                self.add(small_line)
            # Focal point on the left
            focal_length = self.radius_of_curvature / 2
            focal_point = Dot(LEFT * abs(focal_length), color=GREY_A, radius=0.05)
        else:
            # Reflective surface on the right, diagonal lines on the left (back side)
            for i in range(num_lines):
                y = (i - num_lines / 2 + 0.5) * self.mirror_height / num_lines
                # 45° lines going from bottom-right to top-left
                start_pos = LEFT * 0.05 + UP * (y - line_length / 2)
                end_pos = LEFT * (0.05 + line_length) + UP * (y + line_length / 2)
                small_line = Line(
                    start_pos,
                    end_pos,
                    stroke_width=2,
                    color=GREY_C,
                )
                self.add(small_line)
            # Focal point on the right
            focal_length = self.radius_of_curvature / 2
            focal_point = Dot(RIGHT * abs(focal_length), color=GREY_A, radius=0.05)

        self.mirror_line = mirror_line
        self.focal_point = focal_point
        self.add(mirror_line, focal_point)

    def get_optical_plane_position(self) -> np.ndarray:
        """
        Get the position of the optical plane (the mirror line).

        Overrides the base method because the VGroup center includes the focal point,
        which would give an incorrect position.
        """
        return self.mirror_line.get_center()

    def intersect(self, ray_start: np.ndarray, ray_direction: np.ndarray) -> tuple:
        """
        Calculate intersection with the mirror plane.

        In the paraxial approximation, the mirror is treated as a plane.
        The curvature only affects the transfer matrix.
        """
        # Mirror is a vertical plane at x = mirror_line center x position
        # Use the mirror_line position, not the VGroup center (which includes focal point)
        mirror_center = self.mirror_line.get_center()
        mirror_x = mirror_center[0]

        if abs(ray_direction[0]) < 1e-10:
            # Ray is parallel to mirror plane
            return None, False

        t = (mirror_x - ray_start[0]) / ray_direction[0]

        if t < 0:
            # Intersection is behind the ray start
            return None, False

        intersection = ray_start + t * ray_direction

        # Check if intersection is within mirror height
        mirror_y = mirror_center[1]
        if abs(intersection[1] - mirror_y) > self.mirror_height / 2:
            return None, False

        return intersection, True

    def get_normal_at(self, point: np.ndarray) -> np.ndarray:
        """
        Get the normal to the mirror plane.

        In the paraxial approximation, the mirror is a vertical plane.
        Normal points toward the reflective side.
        """
        if self.side == "left":
            return LEFT  # Normal points left (reflective side)
        else:
            return RIGHT  # Normal points right (reflective side)

    def get_transfer_matrix(self) -> np.ndarray:
        """
        Get the ABCD transfer matrix for a spherical mirror.

        For a spherical mirror with radius of curvature R:
        [[1, 0], [-2/R, 1]]

        The focal length is f = R/2
        """
        return np.array([[1.0, 0.0], [-2.0 / self.radius_of_curvature, 1.0]])

    def propagate_ray(
        self,
        ray_start: np.ndarray,
        ray_direction: np.ndarray,
        intersection_point: np.ndarray,
    ) -> tuple:
        """
        Calculate reflected ray direction using paraxial ABCD matrix formalism.

        The ray state is [y, θ] where:
        - y = height relative to optical axis
        - θ = angle (paraxial: θ ≈ tan(θ) ≈ dy/dx)

        Transfer matrix for spherical mirror: [[1, 0], [-2/R, 1]]

        For a mirror, reflection inverts the horizontal direction.
        """
        # Use mirror_line center, not VGroup center
        mirror_center = self.mirror_line.get_center()
        mirror_y_axis = mirror_center[1]

        # Input ray state
        y_in = intersection_point[1] - mirror_y_axis

        # Angle in paraxial approximation: θ ≈ tan(θ) = dy/dx
        if abs(ray_direction[0]) > 1e-10:
            theta_in = ray_direction[1] / ray_direction[0]
        else:
            theta_in = np.sign(ray_direction[1]) * 1e6

        # Apply transfer matrix for spherical mirror
        M = self.get_transfer_matrix()
        state_in = np.array([y_in, theta_in])
        state_out = M @ state_in

        y_out = state_out[0]
        theta_out = state_out[1]

        # For a mirror, the ray is reflected back
        # Determine direction based on which side the mirror is on
        if self.side == "left":
            # Mirror on left: rays from right are reflected back to right
            # Incident from right (+x): direction ≈ [1, θ_in, 0]
            # Reflected to right: direction ≈ [-1, -θ_out, 0]
            new_direction = np.array([-1.0, -theta_out, 0.0])
        else:
            # Mirror on right: rays from left are reflected back to left
            # Incident from left (+x): direction ≈ [1, θ_in, 0]
            # Reflected to left: direction ≈ [-1, -θ_out, 0]
            new_direction = np.array([-1.0, -theta_out, 0.0])

        new_direction = new_direction / np.linalg.norm(new_direction)

        return new_direction, True
