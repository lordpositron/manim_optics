"""
Optical Elements - Base classes and implementations for lenses and mirrors
==========================================================================

This module provides the base architecture for optical elements with support
for future extensions to more complex optics.
"""

from abc import ABC, abstractmethod
import numpy as np
from manim import *


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

        # Create arrow tips at extremities using simple lines
        tip_length = 0.3  # Length of arrow tip lines
        tip_angle = 30 * DEGREES  # Angle of arrow tips

        # Top extremity position
        top_pos = UP * self.lens_height / 2
        bottom_pos = DOWN * self.lens_height / 2

        if self.focal_length > 0:
            # Converging lens: >< (arrows pointing outward)
            # Top extremity: arrows pointing outward (up-right and up-left)
            top_right_tip = Line(
                top_pos,
                top_pos + rotate_vector(DOWN * tip_length, tip_angle, OUT),
                stroke_width=3,
                color=self.color,
            )
            top_left_tip = Line(
                top_pos,
                top_pos + rotate_vector(DOWN * tip_length, -tip_angle, OUT),
                stroke_width=3,
                color=self.color,
            )

            # Bottom extremity: arrows pointing outward (down-right and down-left)
            bottom_right_tip = Line(
                bottom_pos,
                bottom_pos + rotate_vector(UP * tip_length, -tip_angle, OUT),
                stroke_width=3,
                color=self.color,
            )
            bottom_left_tip = Line(
                bottom_pos,
                bottom_pos + rotate_vector(UP * tip_length, tip_angle, OUT),
                stroke_width=3,
                color=self.color,
            )

        else:
            # Diverging lens: <> (arrows pointing inward)
            # Top extremity: arrows pointing inward (down-right and down-left)
            top_right_tip = Line(
                top_pos,
                top_pos + rotate_vector(DOWN * tip_length, -tip_angle, OUT),
                stroke_width=3,
                color=self.color,
            )
            top_left_tip = Line(
                top_pos,
                top_pos + rotate_vector(DOWN * tip_length, tip_angle, OUT),
                stroke_width=3,
                color=self.color,
            )

            # Bottom extremity: arrows pointing inward (up-right and up-left)
            bottom_right_tip = Line(
                bottom_pos,
                bottom_pos + rotate_vector(UP * tip_length, tip_angle, OUT),
                stroke_width=3,
                color=self.color,
            )
            bottom_left_tip = Line(
                bottom_pos,
                bottom_pos + rotate_vector(UP * tip_length, -tip_angle, OUT),
                stroke_width=3,
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
