"""
Mirrors - Mirror implementations
=================================

This module provides mirror classes for optical simulations.
"""

from abc import abstractmethod

import numpy as np
from manim import DEGREES, Dot, GREY_A, GREY_C, Line, UP, DOWN, LEFT, RIGHT

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
        coating_side: str = "left",
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
            Side of the reflective surface ("left" or "right", default: "right").
            The coating/hatching indicators are drawn on the OPPOSITE side.
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
            # coating_side is the reflective surface side; hatching goes on the opposite side
            side_sign = 1.0 if self.coating_side == "left" else -1.0
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
    - R > 0: Concave mirror (converging) — center of curvature on the same side as incident rays
    - R < 0: Convex mirror  (diverging)  — center of curvature on the opposite side

    In paraxial optics, f = R/2.

    Transfer matrix: [[1, 0], [-2/R, 1]]
    """

    def __init__(
        self,
        radius_of_curvature: float = 4.0,
        height: float = 3.0,
        refractive_index: float = 1.0,
        aperture_angle: float = 60 * DEGREES,
        facing: str = "left",
        stroke_width: float = 4.0,
        mirror_color=GREY_A,
        coating_color=GREY_C,
        coating_count: int = 5,
        tip_length: float = 0.3,
        show_focal_point: bool = True,
        **kwargs,
    ):
        """
        Initialize a spherical mirror.

        Parameters
        ----------
        radius_of_curvature : float
            Radius of curvature R (positive = concave/converging, negative = convex/diverging)
        height : float
            Height of the mirror aperture
        refractive_index : float
            Refractive index of the medium (default: 1.0 for air)
        aperture_angle : float
            Angular aperture of the mirror (in radians)
        facing : str
            Direction the reflective surface faces — where incident rays come from.
            - "left"  (default): reflective surface faces left,  rays arrive from the left
            - "right": reflective surface faces right, rays arrive from the right
            Visual consequences:
            - Hatching (croisillons) appears on the OPPOSITE side
            - Half-arrow tips appear on the CONCAVE side (facing × sign(R))
        stroke_width : float
            Stroke width of the mirror line
        mirror_color : color
            Color of the mirror line and tips
        coating_color : color
            Color of the hatching lines
        coating_count : int
            Number of hatching lines
        tip_length : float
            Length of the half-arrow tips at the extremities
        show_focal_point : bool
            Whether to display the focal point dot
        """
        super().__init__(refractive_index=refractive_index, **kwargs)
        self.radius_of_curvature = radius_of_curvature
        self.mirror_height = height
        self.aperture_angle = aperture_angle
        self.facing = facing
        self.stroke_width = stroke_width
        self.mirror_color = mirror_color
        self.coating_color = coating_color
        self.coating_count = coating_count
        self.tip_length = tip_length
        self.show_focal_point = show_focal_point

        self._create_mirror_visual()

    def _create_mirror_visual(self):
        """Create the visual representation of the spherical mirror.

        - Hatching: on the back side (opposite to self.facing)
        - Half-arrows: on the concave side (facing × sign(R)), pointing outward
        - Focal point: facing_x_sign × R/2  (real focus for concave, virtual for convex)
        """
        tip_angle = 30 * DEGREES
        top_pos = UP * self.mirror_height / 2
        bottom_pos = DOWN * self.mirror_height / 2

        # +1 if facing right, -1 if facing left (Manim x-axis convention)
        facing_x = 1.0 if self.facing == "right" else -1.0

        # Mirror surface line
        mirror_line = Line(
            top_pos,
            bottom_pos,
            stroke_width=self.stroke_width,
            color=self.mirror_color,
        )

        # Hatching on the BACK side (opposite to facing)
        # back_x = -facing_x
        # hatch_offset = back_x * 0.02 * self.mirror_height
        hatch_offset = mirror_line.get_center()[0]
        hatch_length = self.mirror_height / self.coating_count * 0.6
        hatch_dir = np.array([np.cos(45 * DEGREES), np.sin(45 * DEGREES), 0.0]) * facing_x
        for i in range(self.coating_count):
            y = (-self.mirror_height / 2) + (i + 0.5) * self.mirror_height / self.coating_count
            center = np.array([hatch_offset, y, 0.0])
            self.add(Line(
                center ,
                center +  hatch_length * hatch_dir,
                stroke_width=2,
                color=self.coating_color,
            ))

        # Half-arrows on the CONCAVE side, always pointing outward.
        # concave_x = facing_x * sign(R):
        #   facing="left"  + R>0 (concave) → concave_x = -1 → LEFT  (bowl opens left)
        #   facing="left"  + R<0 (convex)  → concave_x = +1 → RIGHT (hollow on right)
        #   facing="right" + R>0 (concave) → concave_x = +1 → RIGHT
        #   facing="right" + R<0 (convex)  → concave_x = -1 → LEFT
        concave_x = facing_x * np.sign(self.radius_of_curvature)
        concave_vec = np.array([concave_x, 0.0, 0.0])
        top_tip = Line(
            top_pos,
            top_pos + concave_vec * self.tip_length * np.sin(tip_angle)
                     + UP * self.tip_length * np.cos(tip_angle),
            stroke_width=self.stroke_width,
            color=self.mirror_color,
        )
        bottom_tip = Line(
            bottom_pos,
            bottom_pos + concave_vec * self.tip_length * np.sin(tip_angle)
                        + DOWN * self.tip_length * np.cos(tip_angle),
            stroke_width=self.stroke_width,
            color=self.mirror_color,
        )

        # Focal point: x = facing_x * R/2
        # Concave (R>0): focus on the incident side (same as facing direction)
        # Convex  (R<0): virtual focus on the back side
        focal_x = facing_x * (self.radius_of_curvature / 2)
        focal_point = Dot(
            np.array([focal_x, 0.0, 0.0]),
            color=self.mirror_color,
            radius=0.05,
        )
        focal_point.set_opacity(1.0 if self.show_focal_point else 0.0)

        self.mirror_line = mirror_line
        self.top_tip = top_tip
        self.bottom_tip = bottom_tip
        self.focal_point = focal_point
        self.add(mirror_line, top_tip, bottom_tip, focal_point)

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
        mirror_center = self.mirror_line.get_center()
        mirror_x = mirror_center[0]

        if abs(ray_direction[0]) < 1e-10:
            return None, False

        t = (mirror_x - ray_start[0]) / ray_direction[0]

        if t < 0:
            return None, False

        intersection = ray_start + t * ray_direction

        mirror_y = mirror_center[1]
        if abs(intersection[1] - mirror_y) > self.mirror_height / 2:
            return None, False

        return intersection, True

    def get_normal_at(self, point: np.ndarray) -> np.ndarray:
        """Normal points in the facing direction (toward incident rays)."""
        return LEFT if self.facing == "left" else RIGHT

    def get_transfer_matrix(self) -> np.ndarray:
        """ABCD transfer matrix: [[1, 0], [-2/R, 1]]"""
        return np.array([[1.0, 0.0], [-2.0 / self.radius_of_curvature, 1.0]])

    def propagate_ray(
        self,
        ray_start: np.ndarray,
        ray_direction: np.ndarray,
        intersection_point: np.ndarray,
    ) -> tuple:
        """
        Calculate reflected ray direction using paraxial ABCD matrix formalism.

        θ is always normalised to the +x convention before the ABCD matrix,
        then converted back to the physical reflected direction.
        """
        mirror_center = self.mirror_line.get_center()
        mirror_y_axis = mirror_center[1]

        y_in = intersection_point[1] - mirror_y_axis

        if abs(ray_direction[0]) > 1e-10:
            theta_in = ray_direction[1] / ray_direction[0]
        else:
            theta_in = np.sign(ray_direction[1]) * 1e6

        # Normalise theta to +x convention (ABCD matrix assumes ray going in +x)
        direction_sign = 1.0 if ray_direction[0] >= 0 else -1.0
        theta_in_norm = theta_in * direction_sign

        M = self.get_transfer_matrix()
        state_out = M @ np.array([y_in, theta_in_norm])
        theta_out_norm = state_out[1]

        # Physical direction: [reflected_x, theta_out_norm, 0].
        # theta_out_norm is the paraxial slope dy/dx in the unfolded +x convention;
        # using it directly gives the correct focal convergence (NOT *reflected_x).
        reflected_x = -direction_sign
        new_direction = np.array([reflected_x, theta_out_norm, 0.0])
        new_direction = new_direction / np.linalg.norm(new_direction)

        return new_direction, True
