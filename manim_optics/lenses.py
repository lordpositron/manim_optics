"""
Lenses - Thin lens implementations
==================================

This module provides lens classes for optical simulations.
"""

import numpy as np
from manim import *
from .base import OpticalElement


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
        tip_length: float = 0.3,
        stroke_width: float = 3,
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
        self.tip_length = tip_length
        self.stroke_width = stroke_width

        # Create visual representation
        self._create_lens_visual()

    def _create_lens_visual(self):
        """Create the visual representation of the lens."""
        # Vertical line representing the lens
        lens_line = Line(
            UP * self.lens_height / 2,
            DOWN * self.lens_height / 2,
            stroke_width=self.stroke_width,
            color=self.color,
        )

        # Create arrow tips at extremities
        tip_length = self.tip_length  # Length of arrow tip lines
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
                stroke_width=self.stroke_width,
                color=self.color,
            )
            # Left tip: from top going down-left
            top_left_tip = Line(
                top_pos,
                top_pos
                + LEFT * tip_length * np.sin(tip_angle)
                + DOWN * tip_length * np.cos(tip_angle),
                stroke_width=self.stroke_width,
                color=self.color,
            )

            # Bottom extremity: arrows pointing outward (forming an inverted V pointing down-out)
            # Right tip: from bottom going up-right
            bottom_right_tip = Line(
                bottom_pos,
                bottom_pos
                + RIGHT * tip_length * np.sin(tip_angle)
                + UP * tip_length * np.cos(tip_angle),
                stroke_width=self.stroke_width,
                color=self.color,
            )
            # Left tip: from bottom going up-left
            bottom_left_tip = Line(
                bottom_pos,
                bottom_pos
                + LEFT * tip_length * np.sin(tip_angle)
                + UP * tip_length * np.cos(tip_angle),
                stroke_width=self.stroke_width,
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
                stroke_width=self.stroke_width,
                color=self.color,
            )
            # Left tip: from top going down-right (vers le centre)
            top_left_tip = Line(
                top_pos,
                top_pos
                + RIGHT * tip_length * np.sin(tip_angle)
                + DOWN * tip_length * np.cos(tip_angle),
                stroke_width=self.stroke_width,
                color=self.color,
            )

            # Bottom extremity: arrows pointing inward (forming a V pointing up-in)
            # Right tip: from bottom going up-left (vers le centre)
            bottom_right_tip = Line(
                bottom_pos,
                bottom_pos
                + LEFT * tip_length * np.sin(tip_angle)
                + UP * tip_length * np.cos(tip_angle),
                stroke_width=self.stroke_width,
                color=self.color,
            )
            # Left tip: from bottom going up-right (vers le centre)
            bottom_left_tip = Line(
                bottom_pos,
                bottom_pos
                + RIGHT * tip_length * np.sin(tip_angle)
                + UP * tip_length * np.cos(tip_angle),
                stroke_width=self.stroke_width,
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
