"""
Optical Elements - Base classes and implementations for lenses and mirrors
==========================================================================

This module provides the base architecture for optical elements with support
for future extensions to more complex optics.
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


class ThinLens(OpticalElement):
    """
    Base class for thin lenses (paraxial approximation).

    In the thin lens approximation:
    - The lens has negligible thickness
    - Small angle approximation: sin(θ) ≈ θ
    - All refraction happens at the principal plane

    The focal length convention:
    - f > 0: converging lens
    - f < 0: diverging lens
    """

    def __init__(
        self,
        focal_length: float = 2.0,
        height: float = 3.0,
        refractive_index_before: float = 1.0,
        refractive_index_after: float = 1.0,
        color=BLUE,
        **kwargs
    ):
        """
        Initialize a thin lens.

        Parameters
        ----------
        focal_length : float
            Focal length of the lens (positive for converging, negative for diverging)
        height : float
            Height of the lens
        refractive_index_before : float
            Refractive index before the lens (default: 1.0 for air)
        refractive_index_after : float
            Refractive index after the lens (default: 1.0 for air)
        """
        super().__init__(
            refractive_index_before=refractive_index_before,
            refractive_index_after=refractive_index_after,
            **kwargs
        )
        self.focal_length = focal_length
        self.lens_height = height
        self.color = color

        # Create visual representation
        self._create_lens_visual()

    def _create_lens_visual(self):
        """Create the visual representation of the lens."""
        # Vertical line representing the lens
        lens_line = Line(
            UP * self.lens_height / 2,
            DOWN * self.lens_height / 2,
            stroke_width=4,
            color=self.color,
        )

        # Create arrow tips at extremities
        tip_length = 0.3  # Length of arrow tip lines
        tip_angle = 30 * DEGREES  # Angle of arrow tips

        # Top extremity position
        top_pos = UP * self.lens_height / 2
        bottom_pos = DOWN * self.lens_height / 2

        if self.focal_length > 0:
            # Converging lens: >< (arrows pointing outward)
            # Top extremity: arrows pointing outward (forming a V pointing up-out)
            # Right tip: from top going down-right
            top_right_tip = Line(
                top_pos,
                top_pos
                + RIGHT * tip_length * np.sin(tip_angle)
                + DOWN * tip_length * np.cos(tip_angle),
                stroke_width=4,
                color=self.color,
            )
            # Left tip: from top going down-left
            top_left_tip = Line(
                top_pos,
                top_pos
                + LEFT * tip_length * np.sin(tip_angle)
                + DOWN * tip_length * np.cos(tip_angle),
                stroke_width=4,
                color=self.color,
            )

            # Bottom extremity: arrows pointing outward (forming an inverted V pointing down-out)
            # Right tip: from bottom going up-right
            bottom_right_tip = Line(
                bottom_pos,
                bottom_pos
                + RIGHT * tip_length * np.sin(tip_angle)
                + UP * tip_length * np.cos(tip_angle),
                stroke_width=4,
                color=self.color,
            )
            # Left tip: from bottom going up-left
            bottom_left_tip = Line(
                bottom_pos,
                bottom_pos
                + LEFT * tip_length * np.sin(tip_angle)
                + UP * tip_length * np.cos(tip_angle),
                stroke_width=4,
                color=self.color,
            )

        else:
            # Diverging lens: <> (arrows pointing inward)
            # Top extremity: arrows pointing inward (forming an inverted V pointing down-in)
            # Right tip: from top going down-left (vers le centre)
            top_right_tip = Line(
                top_pos,
                top_pos
                + LEFT * tip_length * np.sin(tip_angle)
                + DOWN * tip_length * np.cos(tip_angle),
                stroke_width=4,
                color=self.color,
            )
            # Left tip: from top going down-right (vers le centre)
            top_left_tip = Line(
                top_pos,
                top_pos
                + RIGHT * tip_length * np.sin(tip_angle)
                + DOWN * tip_length * np.cos(tip_angle),
                stroke_width=4,
                color=self.color,
            )

            # Bottom extremity: arrows pointing inward (forming a V pointing up-in)
            # Right tip: from bottom going up-left (vers le centre)
            bottom_right_tip = Line(
                bottom_pos,
                bottom_pos
                + LEFT * tip_length * np.sin(tip_angle)
                + UP * tip_length * np.cos(tip_angle),
                stroke_width=4,
                color=self.color,
            )
            # Left tip: from bottom going up-right (vers le centre)
            bottom_left_tip = Line(
                bottom_pos,
                bottom_pos
                + RIGHT * tip_length * np.sin(tip_angle)
                + UP * tip_length * np.cos(tip_angle),
                stroke_width=4,
                color=self.color,
            )

        # Add focal points markers (small dots)
        if self.focal_length > 0:
            left_focal = Dot(
                LEFT * abs(self.focal_length), color=self.color, radius=0.05
            )
            right_focal = Dot(
                RIGHT * abs(self.focal_length), color=self.color, radius=0.05
            )
        else:
            left_focal = Dot(
                LEFT * abs(self.focal_length), color=self.color, radius=0.05
            )
            right_focal = Dot(
                RIGHT * abs(self.focal_length), color=self.color, radius=0.05
            )
        # Store components for animation
        self.lens_line = lens_line
        self.top_right_tip = top_right_tip
        self.top_left_tip = top_left_tip
        self.bottom_right_tip = bottom_right_tip
        self.bottom_left_tip = bottom_left_tip
        self.left_focal = left_focal
        self.right_focal = right_focal

        self.add(
            lens_line,
            top_right_tip,
            top_left_tip,
            bottom_right_tip,
            bottom_left_tip,
            left_focal,
            right_focal,
        )

    def create(self, run_time: float = 1.0) -> AnimationGroup:
        """
        Create an animation for the appearance of the lens.

        The arrows grow from the center of the lens outward.

        Parameters
        ----------
        run_time : float
            Duration of the animation

        Returns
        -------
        AnimationGroup
            Animation showing the lens appearing
        """
        # Store original positions
        center = self.get_center()

        # Create copies at center for initial state
        top_center = center + UP * self.lens_height / 2
        bottom_center = center + DOWN * self.lens_height / 2

        # Save final positions
        final_lens_line = self.lens_line.copy()
        final_top_right = self.top_right_tip.copy()
        final_top_left = self.top_left_tip.copy()
        final_bottom_right = self.bottom_right_tip.copy()
        final_bottom_left = self.bottom_left_tip.copy()

        # Move tips to center
        self.lens_line.put_start_and_end_on(center + UP * 0, center + DOWN * 0)
        self.top_right_tip.put_start_and_end_on(top_center, top_center)
        self.top_left_tip.put_start_and_end_on(top_center, top_center)
        self.bottom_right_tip.put_start_and_end_on(bottom_center, bottom_center)
        self.bottom_left_tip.put_start_and_end_on(bottom_center, bottom_center)

        # # Make focal points invisible initially
        # self.left_focal.set_opacity(0)
        # self.right_focal.set_opacity(0)

        # Create animations
        return AnimationGroup(
            Transform(self.lens_line, final_lens_line, run_time=run_time),
            Transform(self.top_right_tip, final_top_right, run_time=run_time),
            Transform(self.top_left_tip, final_top_left, run_time=run_time),
            Transform(self.bottom_right_tip, final_bottom_right, run_time=run_time),
            Transform(self.bottom_left_tip, final_bottom_left, run_time=run_time),
            FadeIn(self.left_focal, run_time=run_time * 0.5),
            FadeIn(self.right_focal, run_time=run_time * 0.5),
            lag_ratio=0.05,
        )

    def intersect(self, ray_start: np.ndarray, ray_direction: np.ndarray) -> tuple:
        """
        Calculate intersection with the lens plane.

        For a thin lens, we find where the ray crosses the vertical plane
        at the lens center.
        """
        # Lens is a vertical plane at x = lens_center_x
        lens_center = self.get_center()
        lens_x = lens_center[0]

        # Ray equation: P(t) = ray_start + t * ray_direction
        # We want P(t).x = lens_x

        if abs(ray_direction[0]) < 1e-10:
            # Ray is parallel to lens plane
            return None, False

        t = (lens_x - ray_start[0]) / ray_direction[0]

        if t < 0:
            # Intersection is behind the ray start
            return None, False

        intersection = ray_start + t * ray_direction

        # Check if intersection is within lens height
        lens_y = lens_center[1]
        if abs(intersection[1] - lens_y) > self.lens_height / 2:
            return None, False

        return intersection, True

    def get_transfer_matrix(self) -> np.ndarray:
        """
        Get the ABCD transfer matrix for a thin lens.

        For a thin lens: [[1, 0], [-1/f, 1]]
        where f is the focal length.
        """
        return np.array([[1.0, 0.0], [-1.0 / self.focal_length, 1.0]])

    def propagate_ray(
        self,
        ray_start: np.ndarray,
        ray_direction: np.ndarray,
        intersection_point: np.ndarray,
    ) -> tuple:
        """
        Apply thin lens equation using ABCD transfer matrix formalism.

        The ray state is represented as [y, θ] where:
        - y = height relative to optical axis
        - θ = angle of ray (in paraxial approximation: θ ≈ sin(θ) ≈ tan(θ))

        Transfer matrix for thin lens: [[1, 0], [-1/f, 1]]
        """
        lens_center = self.get_center()
        lens_y_axis = lens_center[1]

        # Input ray state
        y_in = intersection_point[1] - lens_y_axis  # Height relative to optical axis

        # Angle θ in paraxial approximation: θ ≈ tan(θ) = dy/dx
        # For normalized direction vector, θ ≈ direction[1] / direction[0]
        if abs(ray_direction[0]) > 1e-10:
            theta_in = ray_direction[1] / ray_direction[0]
        else:
            # Nearly vertical ray
            theta_in = np.sign(ray_direction[1]) * 1e6

        # Apply transfer matrix
        M = self.get_transfer_matrix()
        state_in = np.array([y_in, theta_in])
        state_out = M @ state_in

        y_out = state_out[0]
        theta_out = state_out[1]

        # Convert output angle back to direction vector
        # Direction: [1, θ, 0] (then normalize)
        # In paraxial approximation: direction ≈ [1, θ, 0]
        new_direction = np.array([1.0, theta_out, 0.0])
        new_direction = new_direction / np.linalg.norm(new_direction)

        return new_direction, True


class ConvergingLens(ThinLens):
    """Converging (convex) lens with positive focal length."""

    def __init__(self, focal_length: float = 2.0, **kwargs):
        """
        Initialize a converging lens.

        Parameters
        ----------
        focal_length : float
            Focal length (must be positive)
        """
        if focal_length <= 0:
            raise ValueError("Converging lens must have positive focal length")
        super().__init__(focal_length=focal_length, **kwargs)


class DivergingLens(ThinLens):
    """Diverging (concave) lens with negative focal length."""

    def __init__(self, focal_length: float = -2.0, **kwargs):
        """
        Initialize a diverging lens.

        Parameters
        ----------
        focal_length : float
            Focal length (must be negative)
        """
        if focal_length >= 0:
            raise ValueError("Diverging lens must have negative focal length")
        super().__init__(focal_length=focal_length, **kwargs)


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
            **kwargs
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

    def __init__(self, height: float = 3.0, refractive_index: float = 1.0, **kwargs):
        """
        Initialize a plane mirror.

        Parameters
        ----------
        height : float
            Height of the mirror
        refractive_index : float
            Refractive index of the medium (default: 1.0 for air)
        """
        super().__init__(refractive_index=refractive_index, **kwargs)
        self.mirror_height = height

        # Create visual representation
        self._create_mirror_visual()

    def _create_mirror_visual(self):
        """Create the visual representation of the mirror."""
        # Mirror surface (thick line)
        mirror_line = Line(
            UP * self.mirror_height / 2,
            DOWN * self.mirror_height / 2,
            stroke_width=6,
            color=GREY_A,
        )

        # Reflective coating indicator (small lines)
        num_lines = 5
        for i in range(num_lines):
            y = (i - num_lines / 2 + 0.5) * self.mirror_height / num_lines
            small_line = Line(
                LEFT * 0.1 + UP * y, ORIGIN + UP * y, stroke_width=2, color=GREY_C
            )
            self.add(small_line)

        self.add(mirror_line)

    def intersect(self, ray_start: np.ndarray, ray_direction: np.ndarray) -> tuple:
        """Calculate intersection with the mirror plane."""
        # Mirror is a vertical plane at x = mirror_center_x
        mirror_center = self.get_center()
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
        **kwargs
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


# ==============================================================================
# Beam Stops - Elements that block rays
# ==============================================================================


class BeamStop(OpticalElement):
    """
    Base class for elements that stop/block light rays.

    BeamStops do not refract or reflect light - they simply absorb it.
    When a ray intersects a BeamStop, it is marked as terminated.

    Subclasses must implement:
    - intersect(): Determine if ray hits the stop
    - Visual representation
    """

    def __init__(self, **kwargs):
        """Initialize a beam stop."""
        super().__init__(
            refractive_index_before=1.0, refractive_index_after=1.0, **kwargs
        )

    def get_transfer_matrix(self) -> np.ndarray:
        """
        BeamStops don't have a transfer matrix as they terminate rays.

        Returns identity matrix (though it shouldn't be used).
        """
        return np.array([[1.0, 0.0], [0.0, 1.0]])

    def propagate_ray(
        self,
        ray_start: np.ndarray,
        ray_direction: np.ndarray,
        intersection_point: np.ndarray,
    ) -> tuple:
        """
        BeamStop terminates the ray - no propagation.

        Parameters
        ----------
        ray_start : np.ndarray
            Starting position of the ray
        ray_direction : np.ndarray
            Direction vector of the ray
        intersection_point : np.ndarray
            Point where ray intersects the beam stop

        Returns
        -------
        tuple
            (None, False) indicating the ray is stopped
        """
        return None, False

    def is_mirror(self) -> bool:
        """BeamStops are not mirrors."""
        return False


class LineBeamStop(BeamStop):
    """
    Vertical line that stops rays.

    Useful for modeling:
    - Screens
    - Detectors
    - Hard aperture edges
    """

    def __init__(
        self, height: float = 3.0, color=GREY_D, stroke_width: float = 6, **kwargs
    ):
        """
        Initialize a line beam stop.

        Parameters
        ----------
        height : float
            Height of the stopping line
        color : str
            Color of the line
        stroke_width : float
            Width of the line
        """
        super().__init__(**kwargs)
        self.stop_height = height
        self.color = color
        self.stroke_width = stroke_width

        # Create visual representation
        self._create_visual()

    def _create_visual(self):
        """Create visual representation as a thick vertical line."""
        stop_line = Line(
            UP * self.stop_height / 2,
            DOWN * self.stop_height / 2,
            stroke_width=self.stroke_width,
            color=self.color,
        )
        self.stop_line = stop_line
        self.add(stop_line)

    def intersect(self, ray_start: np.ndarray, ray_direction: np.ndarray) -> tuple:
        """
        Check if ray intersects the vertical line.

        Parameters
        ----------
        ray_start : np.ndarray
            Starting point of the ray
        ray_direction : np.ndarray
            Direction vector of the ray

        Returns
        -------
        tuple
            (intersection_point, True) if hit, (None, False) otherwise
        """
        # Line is vertical at x = center
        line_x = self.get_center()[0]

        if abs(ray_direction[0]) < 1e-10:
            # Ray is parallel to line
            return None, False

        # Calculate intersection parameter
        t = (line_x - ray_start[0]) / ray_direction[0]

        if t < 0:
            # Intersection behind ray start
            return None, False

        intersection = ray_start + t * ray_direction

        # Check if within height
        line_y = self.get_center()[1]
        if abs(intersection[1] - line_y) > self.stop_height / 2:
            return None, False

        return intersection, True


class CircularAperture(BeamStop):
    """
    Circular aperture/diaphragm that blocks rays outside a circle.

    Rays passing through the center (within radius) are NOT stopped.
    Rays hitting the opaque region (outside radius) ARE stopped.

    Useful for modeling:
    - Iris/pupil of the eye
    - Diaphragms
    - Circular stops
    """

    def __init__(
        self,
        radius: float = 0.5,
        total_length: float = None,
        line_color=GREY_D,
        line_stroke_width: float = 4,
        **kwargs
    ):
        """
        Initialize a circular aperture.

        Parameters
        ----------
        radius : float
            Radius of the aperture opening (vertical half-height)
        total_length : float, optional
            Total horizontal length of the blocking lines
            If None, defaults to 8 * radius
        line_color : str
            Color of the blocking lines
        line_stroke_width : float
            Stroke width of the blocking lines
        """
        super().__init__(**kwargs)
        self.aperture_radius = radius
        self.total_length = total_length if total_length is not None else 8 * radius
        self.line_color = line_color
        self.line_stroke_width = line_stroke_width

        # Create visual representation
        self._create_visual()

    def _create_visual(self):
        """Create visual as two vertical line segments with gap in the center for the aperture."""
        # The aperture is a circular opening viewed from the front
        # We show it as two vertical line segments:
        # - Top segment: from y = d/2 to y = D/2
        # - Bottom segment: from y = -D/2 to y = -d/2
        # Where D = total_length and d = 2*radius (aperture diameter)

        D = self.total_length
        d = 2 * self.aperture_radius

        if d >= D:
            # Opening is larger than total length, nothing to show
            return

        # Top blocking line segment (from d/2 to D/2)
        top_line = Line(
            UP * d / 2,
            UP * D / 2,
            color=self.line_color,
            stroke_width=self.line_stroke_width,
        )

        # Bottom blocking line segment (from -d/2 to -D/2)
        bottom_line = Line(
            DOWN * d / 2,
            DOWN * D / 2,
            color=self.line_color,
            stroke_width=self.line_stroke_width,
        )

        # Add both lines
        self.top_line = top_line
        self.bottom_line = bottom_line
        self.add(top_line, bottom_line)

    def intersect(self, ray_start: np.ndarray, ray_direction: np.ndarray) -> tuple:
        """
        Check if ray hits the opaque region (outside aperture radius).

        The aperture is in the xy-plane at z=0.

        Parameters
        ----------
        ray_start : np.ndarray
            Starting point of the ray
        ray_direction : np.ndarray
            Direction vector of the ray

        Returns
        -------
        tuple
            (intersection_point, True) if ray is BLOCKED (outside radius)
            (None, False) if ray PASSES THROUGH (inside radius)
        """
        # Aperture plane is vertical at x = center
        aperture_x = self.get_center()[0]
        aperture_y = self.get_center()[1]

        if abs(ray_direction[0]) < 1e-10:
            # Ray is parallel to aperture plane
            return None, False

        # Calculate intersection with vertical plane
        t = (aperture_x - ray_start[0]) / ray_direction[0]

        if t < 0:
            # Intersection behind ray start
            return None, False

        intersection = ray_start + t * ray_direction

        # Calculate distance from aperture center
        dy = intersection[1] - aperture_y
        distance_from_center = abs(dy)

        # Ray is blocked if OUTSIDE the aperture radius
        if distance_from_center > self.aperture_radius:
            return intersection, True
        else:
            # Ray passes through - not blocked
            return None, False


class ArcBeamStop(BeamStop):
    """
    Arc (portion of circle) that stops rays - useful for modeling curved screens/retina.

    The arc is centered at a point and has a radius of curvature.
    Rays hitting the arc are stopped (absorbed).

    Useful for modeling:
    - Retina of the eye
    - Curved detectors
    - Curved screens
    """

    def __init__(
        self,
        radius: float = 2.0,
        arc_angle: float = 120 * DEGREES,
        color=RED_D,
        stroke_width: float = 4,
        **kwargs
    ):
        """
        Initialize an arc beam stop.

        Parameters
        ----------
        radius : float
            Radius of curvature of the arc
        arc_angle : float
            Angular extent of the arc (in radians)
        color : str
            Color of the arc
        stroke_width : float
            Width of the arc line
        """
        super().__init__(**kwargs)
        self.arc_radius = radius
        self.arc_angle = arc_angle
        self.color = color
        self.stroke_width = stroke_width

        # Track center of curvature (origin initially, will move with shifts)
        self.curvature_center = np.array([0.0, 0.0, 0.0])

        # Create visual representation
        self._create_visual()

    def _create_visual(self):
        """Create visual as a curved arc."""
        # Create arc centered at origin, then position it
        arc = Arc(
            radius=self.arc_radius,
            start_angle=-self.arc_angle / 2,
            angle=self.arc_angle,
            color=self.color,
            stroke_width=self.stroke_width,
        )
        self.arc = arc
        self.add(arc)

    def intersect(self, ray_start: np.ndarray, ray_direction: np.ndarray) -> tuple:
        """
        Check if ray intersects the arc.

        Simplified approximation: treat arc as circle segment in 2D.

        Parameters
        ----------
        ray_start : np.ndarray
            Starting point of the ray
        ray_direction : np.ndarray
            Direction vector of the ray

        Returns
        -------
        tuple
            (intersection_point, True) if hit, (None, False) otherwise
        """
        # Calculate center of curvature from arc geometry
        # The arc was created at origin, then shifted
        # The center point at angle=0 of the arc is at distance arc_radius from origin
        # After shifting, we need to find where the origin (center of curvature) ended up

        # Get the current position of the arc
        # The arc spans from start_angle to start_angle+angle
        # The center angle (0 degrees, pointing to the right) gives us a reference point
        # This point is at (arc_radius, 0) from the curvature center

        # Use the arc object's position to infer curvature center
        # The arc center (bounding box center) is not the same as curvature center
        # But we can get arc points and work backwards
        arc_points = self.arc.get_all_points()
        if len(arc_points) == 0:
            return None, False

        # Find the rightmost point (this is at angle=0, the reference)
        rightmost_idx = np.argmax(arc_points[:, 0])
        reference_point = arc_points[rightmost_idx][:2]  # 2D

        # The curvature center is at distance arc_radius to the LEFT of this point
        arc_center_2d = reference_point - np.array([self.arc_radius, 0])

        # Convert to 2D for intersection calculation
        ray_start_2d = ray_start[:2]
        ray_dir_2d = ray_direction[:2]

        # Ray-circle intersection using quadratic formula
        # Ray: P = P0 + t*d
        # Circle: |P - C|^2 = R^2
        # Substitute: |P0 + t*d - C|^2 = R^2

        oc = ray_start_2d - arc_center_2d
        a = np.dot(ray_dir_2d, ray_dir_2d)
        b = 2 * np.dot(oc, ray_dir_2d)
        c = np.dot(oc, oc) - self.arc_radius**2

        discriminant = b**2 - 4 * a * c

        if discriminant < 0:
            # No intersection with circle
            return None, False

        # Two solutions (ray can intersect circle at two points)
        t1 = (-b - np.sqrt(discriminant)) / (2 * a)
        t2 = (-b + np.sqrt(discriminant)) / (2 * a)

        # Check both intersections to see which (if any) are in the arc range
        valid_intersections = []

        for t_val in [t1, t2]:
            if t_val > 1e-10:  # Must be forward from ray start
                # Calculate intersection point
                intersection_2d = ray_start_2d + t_val * ray_dir_2d

                # Check if within arc angle range
                rel_pos = intersection_2d - arc_center_2d
                angle = np.arctan2(rel_pos[1], rel_pos[0])

                # Normalize angle to [-π, π]
                angle = np.arctan2(np.sin(angle), np.cos(angle))

                # Check if within arc range
                half_angle = self.arc_angle / 2
                if -half_angle <= angle <= half_angle:
                    valid_intersections.append((t_val, intersection_2d, angle))

        if len(valid_intersections) == 0:
            # No valid intersection
            return None, False

        # Take the closest valid intersection (smallest t)
        valid_intersections.sort(key=lambda x: x[0])
        t, intersection_2d, angle = valid_intersections[0]

        intersection = np.array([intersection_2d[0], intersection_2d[1], 0])
        return intersection, True


# ==============================================================================
# Eye - Composite optical system
# ==============================================================================


class Eye(VGroup):
    """
    Simplified model of an eye for optical simulations.

    Components:
    - Lens (cornea + crystalline lens simplified as thin lens)
    - Optional CircularAperture (pupil/iris)
    - ArcBeamStop (retina - curved detector)

    All components are positioned relative to the lens center.
    Use get_optical_elements() to get the ordered list for ray tracing.
    """

    def __init__(
        self,
        focal_length: float = 2.0,
        lens_diameter: float = 1.0,
        pupil_diameter: float = 0.4,
        retina_radius: float = 2.3,
        retina_angle: float = 100 * DEGREES,
        include_pupil: bool = True,
        lens_color=BLUE_C,
        pupil_color=GREY_C,
        retina_color=RED_D,
        **kwargs
    ):
        """
        Initialize an eye model.

        Parameters
        ----------
        focal_length : float
            Focal length of the eye lens (cornea + crystalline)
        lens_diameter : float
            Diameter (height) of the lens
        pupil_diameter : float
            Diameter of the pupil aperture
        retina_radius : float
            Radius of curvature of the retina
        retina_angle : float
            Angular extent of the retina (in radians)
        include_pupil : bool
            Whether to include a pupil aperture
        lens_color : str
            Color of the lens
        pupil_color : str
            Color of the pupil
        retina_color : str
            Color of the retina
        """
        super().__init__(**kwargs)

        self.focal_length = focal_length
        self.lens_diameter = lens_diameter
        self.pupil_diameter = pupil_diameter
        self.retina_radius = retina_radius
        self.retina_angle = retina_angle
        self.include_pupil = include_pupil

        # Create components
        self._create_eye_components(lens_color, pupil_color, retina_color)

    def _create_eye_components(self, lens_color, pupil_color, retina_color):
        """Create and position all eye components."""

        # 1. Lens (at origin, center of reference)
        self.lens = ConvergingLens(
            focal_length=self.focal_length,
            height=self.lens_diameter,
            color=lens_color,
        )
        self.lens.move_to(ORIGIN)
        self.add(self.lens)

        # 2. Optional pupil (just after lens)
        if self.include_pupil:
            pupil_offset = 0.05  # Small offset from lens
            # Pupil opening is the actual pupil diameter
            self.pupil = CircularAperture(
                radius=self.pupil_diameter / 2,
                total_length=self.lens_diameter * 1.5,
                line_color=pupil_color,
                line_stroke_width=4,
            )

            self.pupil.shift(RIGHT * pupil_offset)
            self.add(self.pupil)
        else:
            self.pupil = None

        # 3. Retina (curved detector at back of eye)
        # Position it so the light focuses on it
        # For a simple model: retina is approximately at focal length from lens
        # Reduced to 90% for better visual positioning
        retina_distance = self.focal_length * 0.9

        self.retina = ArcBeamStop(
            radius=self.retina_radius,
            arc_angle=self.retina_angle,
            color=retina_color,
        )
        # The arc is created with points at radius R from origin
        # The closest point to the lens (at angle=0) is at x=R
        # We want this point at retina_distance from the lens
        # So we shift by (retina_distance - R)
        self.retina.shift(RIGHT * (retina_distance - self.retina_radius))
        self.add(self.retina)

    def get_optical_elements(self):
        """
        Get ordered list of optical elements for ray tracing.

        Returns
        -------
        list
            [lens, pupil (optional), retina] in order of interaction
        """
        elements = [self.lens]

        if self.pupil is not None:
            elements.append(self.pupil)

        elements.append(self.retina)

        return elements

    def set_focal_length(self, new_focal: float):
        """
        Update the focal length of the eye lens.

        This simulates accommodation (changing focus).

        Parameters
        ----------
        new_focal : float
            New focal length
        """
        self.focal_length = new_focal
        self.lens.focal_length = new_focal
        return self

    def set_pupil_diameter(self, new_diameter: float):
        """
        Update pupil diameter (simulates dilation/constriction).

        Parameters
        ----------
        new_diameter : float
            New pupil diameter
        """
        if self.pupil is not None:
            self.pupil_diameter = new_diameter
            self.pupil.aperture_radius = new_diameter / 2
            # Recreate visual
            self.pupil.remove(*self.pupil.submobjects)
            self.pupil._create_visual()
        return self
