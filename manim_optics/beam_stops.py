"""
Beam Stops - Elements that block/absorb light
=============================================

This module provides beam stop implementations for optical simulations.
"""

import numpy as np
from manim import *
from .base import OpticalElement, rotate_vector_2d


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

        # Ray is blocked if it hits the blocking region
        # Blocking regions: d/2 < |y| < D/2
        # Where d = 2*aperture_radius, D = total_length
        if (
            distance_from_center > self.aperture_radius
            and distance_from_center < self.total_length / 2
        ):
            return intersection, True
        else:
            # Ray passes through aperture or misses entirely
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

        # Store the center of curvature explicitly
        # Initially at origin, updated when shifted
        self._curvature_center = np.array([0.0, 0.0, 0.0])

        # Create visual representation
        self._create_visual()

    def shift(self, *vectors):
        """Override shift to update curvature center."""
        # Apply shift to VGroup
        super().shift(*vectors)

        # Update curvature center
        for vector in vectors:
            self._curvature_center += vector

        return self

    def move_to(self, point_or_mobject, **kwargs):
        """Override move_to to update curvature center."""
        # Get current center before moving
        old_center = self.get_center()

        # Apply move
        super().move_to(point_or_mobject, **kwargs)

        # Calculate displacement and update curvature center
        new_center = self.get_center()
        displacement = new_center - old_center
        self._curvature_center += displacement

        return self

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

        Uses ray-circle intersection, then verifies if the point is within
        the arc's angular range.

        Parameters
        ----------
        ray_start : np.ndarray
            Starting point of the ray (3D)
        ray_direction : np.ndarray
            Direction vector of the ray (3D, should be normalized)

        Returns
        -------
        tuple
            (intersection_point, True) if hit, (None, False) otherwise
        """
        # Work in 2D (xy plane)
        ray_start_2d = ray_start[:2]
        ray_dir_2d = ray_direction[:2]
        center_2d = self._curvature_center[:2]

        # Normalize direction in 2D
        ray_dir_2d_norm = np.linalg.norm(ray_dir_2d)
        if ray_dir_2d_norm < 1e-10:
            return None, False
        ray_dir_2d = ray_dir_2d / ray_dir_2d_norm

        # Ray-circle intersection using geometric approach
        # Vector from center to ray start
        to_start = ray_start_2d - center_2d

        # Project to_start onto ray direction
        proj_length = np.dot(to_start, ray_dir_2d)

        # Closest point on ray to center
        closest_point = ray_start_2d - proj_length * ray_dir_2d

        # Distance from center to closest point
        dist_to_ray = np.linalg.norm(center_2d - closest_point)

        # Check if ray passes close enough to circle
        if dist_to_ray > self.arc_radius + 1e-6:
            return None, False

        # Calculate intersection distance along ray
        # Using Pythagoras: d^2 + dist_to_ray^2 = radius^2
        if dist_to_ray > self.arc_radius:
            # Numerical error, treat as tangent
            half_chord = 0
        else:
            half_chord = np.sqrt(self.arc_radius**2 - dist_to_ray**2)

        # Two potential intersection parameters
        t1 = -proj_length - half_chord
        t2 = -proj_length + half_chord

        # Check both intersection points
        for t in [t1, t2]:
            if t < 1e-6:  # Skip points behind or at ray start
                continue

            # Calculate intersection point
            intersection_2d = ray_start_2d + t * ray_dir_2d

            # Vector from center to intersection
            to_intersection = intersection_2d - center_2d

            # Calculate angle (0 is to the right, positive counterclockwise)
            angle = np.arctan2(to_intersection[1], to_intersection[0])

            # Arc spans from -arc_angle/2 to +arc_angle/2 (centered at 0°)
            half_angle = self.arc_angle / 2

            # Check if angle is within range
            # Need to handle angle wrapping carefully
            if -half_angle <= angle <= half_angle:
                # Hit! Return this intersection
                intersection_3d = np.array(
                    [intersection_2d[0], intersection_2d[1], 0.0]
                )
                return intersection_3d, True

        # No valid intersection within arc range
        return None, False

    def get_debug_info(self, ray_start: np.ndarray, ray_direction: np.ndarray) -> dict:
        """
        Get detailed debug information about ray-arc intersection.

        Returns
        -------
        dict
            Debug information including center, distances, angles, etc.
        """
        ray_start_2d = ray_start[:2]
        ray_dir_2d = ray_direction[:2]
        center_2d = self._curvature_center[:2]

        ray_dir_2d = ray_dir_2d / (np.linalg.norm(ray_dir_2d) + 1e-10)

        to_start = ray_start_2d - center_2d
        proj_length = np.dot(to_start, ray_dir_2d)
        closest_point = ray_start_2d - proj_length * ray_dir_2d
        dist_to_ray = np.linalg.norm(center_2d - closest_point)

        debug_info = {
            "curvature_center": self._curvature_center.copy(),
            "arc_radius": self.arc_radius,
            "arc_angle_deg": np.degrees(self.arc_angle),
            "ray_start": ray_start.copy(),
            "ray_direction": ray_direction.copy(),
            "distance_to_ray": dist_to_ray,
            "closest_point_on_ray": np.array([closest_point[0], closest_point[1], 0.0]),
        }

        if dist_to_ray <= self.arc_radius:
            half_chord = np.sqrt(self.arc_radius**2 - dist_to_ray**2)
            t1 = -proj_length - half_chord
            t2 = -proj_length + half_chord

            intersections = []
            for i, t in enumerate([t1, t2]):
                if t >= 0:
                    int_2d = ray_start_2d + t * ray_dir_2d
                    to_int = int_2d - center_2d
                    angle = np.arctan2(to_int[1], to_int[0])
                    half_angle = self.arc_angle / 2
                    in_range = -half_angle <= angle <= half_angle

                    intersections.append(
                        {
                            "index": i,
                            "t": t,
                            "point": np.array([int_2d[0], int_2d[1], 0.0]),
                            "angle_rad": angle,
                            "angle_deg": np.degrees(angle),
                            "in_arc_range": in_range,
                        }
                    )

            debug_info["intersections"] = intersections

        return debug_info
