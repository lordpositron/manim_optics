"""
CenteredSystem - Optical centered system with principal planes
================================================================

This module provides the CenteredSystem class for modeling complex optical systems
using principal planes (H, H') and nodal points (N, N').
"""

import numpy as np
from manim import *

from .base import OpticalElement


class CenteredSystem(OpticalElement):
    """
    Centered optical system represented by principal planes H and H'.

    This class models complex optical systems (like multi-lens systems) using
    the principal planes formalism. Rays arriving at plane H are teleported
    to the same height at plane H', implementing the principal planes behavior.

    Components:
    - Principal planes H and H' (vertical dashed lines)
    - Physical boundaries (curved surfaces using ArcPolygon)
    - Focal points F and F' (optional)
    - Nodal points N and N' (depend on refractive indices)

    The visual representation shows the system boundaries while ray tracing
    uses the principal planes for optical calculations.
    """

    def __init__(
        self,
        h_position: float = -1.0,
        h_prime_position: float = 1.0,
        focal_length: float = 2.0,
        height: float = 3.0,
        left_boundary_position: float = None,
        left_boundary_height: float = None,
        right_boundary_position: float = None,
        right_boundary_height: float = None,
        boundary_curvature: float = 0.7,
        refractive_index_before: float = 1.0,
        refractive_index_after: float = 1.0,
        h_color=WHITE,
        h_stroke_width: float = 3,
        h_dash_length: float = 0.1,
        boundary_color=BLUE_D,
        boundary_stroke_width: float = 3,
        show_labels: bool = True,
        show_focal_points: bool = True,
        focal_point_color=YELLOW,
        label_color=WHITE,
        **kwargs,
    ):
        """
        Initialize a centered optical system.

        Parameters
        ----------
        h_position : float
            X-position of principal plane H
        h_prime_position : float
            X-position of principal plane H'
        focal_length : float
            Focal length of the system (for F and F' positions)
        height : float
            Height of the principal planes and system (default boundary height)
        left_boundary_position : float, optional
            X-position of left boundary (if None, uses h_position)
        left_boundary_height : float, optional
            Height of left boundary (if None, uses height)
        right_boundary_position : float, optional
            X-position of right boundary (if None, uses h_prime_position)
        right_boundary_height : float, optional
            Height of right boundary (if None, uses height)
        boundary_curvature : float
            Curvature factor for boundaries (multiplier for height)
            Higher values = more curved. Default: 0.7
        refractive_index_before : float
            Refractive index before the system
        refractive_index_after : float
            Refractive index after the system
        h_color : color
            Color of principal planes
        h_stroke_width : float
            Stroke width of principal planes
        h_dash_length : float
            Dash length for principal plane lines
        boundary_color : color
            Color of boundary curves
        boundary_stroke_width : float
            Stroke width of boundary curves
        show_labels : bool
            Whether to show H and H' labels
        show_focal_points : bool
            Whether to show focal points F and F'
        focal_point_color : color
            Color of focal points
        label_color : color
            Color of labels
        """
        super().__init__(
            refractive_index_before=refractive_index_before,
            refractive_index_after=refractive_index_after,
            **kwargs,
        )

        # Store initial values
        self._initial_h_position = h_position
        self._initial_h_prime_position = h_prime_position
        self._initial_focal_length = focal_length

        # Create ValueTrackers for animatable parameters
        self.h_position_tracker = ValueTracker(h_position)
        self.h_prime_position_tracker = ValueTracker(h_prime_position)
        self.focal_length_tracker = ValueTracker(focal_length)

        # Current values (synchronized with trackers)
        self.h_position = h_position
        self.h_prime_position = h_prime_position
        self.focal_length = focal_length
        self.system_height = height

        # Visual offset for shifting the whole system in the scene (y/z only)
        self._visual_offset = np.array([0.0, 0.0, 0.0])

        # Boundary positions and heights (use defaults if not specified)
        self.left_boundary_position = (
            left_boundary_position if left_boundary_position is not None else h_position
        )
        self.left_boundary_height = (
            left_boundary_height if left_boundary_height is not None else height
        )
        self.right_boundary_position = (
            right_boundary_position
            if right_boundary_position is not None
            else h_prime_position
        )
        self.right_boundary_height = (
            right_boundary_height if right_boundary_height is not None else height
        )

        # Store initial boundary positions for relative updates
        self._initial_left_boundary_position = self.left_boundary_position
        self._initial_right_boundary_position = self.right_boundary_position

        self.h_color = h_color
        self.h_stroke_width = h_stroke_width
        self.h_dash_length = h_dash_length
        self.boundary_color = boundary_color
        self.boundary_stroke_width = boundary_stroke_width
        self.show_labels = show_labels
        self.show_focal_points = show_focal_points
        self.focal_point_color = focal_point_color
        self.label_color = label_color
        self.boundary_curvature = boundary_curvature

        # Internal state for ray tracing
        self._last_h_intersection = None

        # Create visual representation
        self._create_visual()

        # Add updater to synchronize tracked values and update visuals
        self.add_updater(self._update_from_trackers)

    def _generate_boundary_arc(
        self, x_position: float, boundary_height: float, is_left: bool = True
    ):
        """
        Generate boundary arc for ArcBetweenPoints.

        Parameters
        ----------
        x_position : float
            X-position of the boundary center
        boundary_height : float
            Height of the boundary
        is_left : bool
            If True, bulge points left; if False, bulge points right

        Returns
        -------
        tuple
            (top_point, bottom_point, radius)
        """
        # Endpoints at top and bottom of boundary
        top_point = (
            np.array([x_position, boundary_height / 2, 0.0]) + self._visual_offset
        )
        bottom_point = (
            np.array([x_position, -boundary_height / 2, 0.0]) + self._visual_offset
        )

        # Radius for the arc (larger = more curved)
        # Using height as base, multiply by curvature factor
        radius = boundary_height * self.boundary_curvature

        # Sign determines bulge direction
        # Positive radius: arc bulges to the LEFT
        # Negative radius: arc bulges to the RIGHT
        #
        # For symmetric appearance:
        # - Left boundary at x=-2: bulge LEFT (away) = positive radius
        # - Right boundary at x=+2: bulge LEFT (toward center) = NEGATIVE radius
        # This makes rays pass through similar arc positions
        if not is_left:
            radius = -radius  # Flip sign for right boundary

        return top_point, bottom_point, radius

    def _create_visual(self):
        """Create visual representation of the centered system."""
        # 1. Principal planes H and H' (dashed vertical lines)
        self.h_plane = DashedLine(
            UP * self.system_height / 2,
            DOWN * self.system_height / 2,
            dash_length=self.h_dash_length,
            stroke_color=self.h_color,
            stroke_width=self.h_stroke_width,
        )
        self.h_plane.shift(RIGHT * self.h_position + self._visual_offset)

        self.h_prime_plane = DashedLine(
            UP * self.system_height / 2,
            DOWN * self.system_height / 2,
            dash_length=self.h_dash_length,
            stroke_color=self.h_color,
            stroke_width=self.h_stroke_width,
        )
        self.h_prime_plane.shift(RIGHT * self.h_prime_position + self._visual_offset)

        self.add(self.h_plane, self.h_prime_plane)

        # 2. Labels H and H'
        if self.show_labels:
            self.h_label = Text("H", color=self.label_color, font_size=24)
            self.h_label.always.next_to(self.h_plane, DOWN, buff=0.2)

            self.h_prime_label = Text("H'", color=self.label_color, font_size=24)
            self.h_prime_label.always.next_to(self.h_prime_plane, DOWN, buff=0.2)

            self.add(self.h_label, self.h_prime_label)
        else:
            self.h_label = None
            self.h_prime_label = None

        # 3. Boundary curves (physical extent of system)
        # Left boundary - bulge to the left (outward)
        top_l, bottom_l, radius_l = self._generate_boundary_arc(
            self.left_boundary_position, self.left_boundary_height, is_left=True
        )

        self.left_boundary = ArcBetweenPoints(
            top_l,
            bottom_l,
            radius=radius_l,  # Positive radius makes it bulge left (outward)
            stroke_color=self.boundary_color,
            stroke_width=self.boundary_stroke_width,
            fill_opacity=0,
        )
        # Store the signed radius separately (ArcBetweenPoints converts to abs value)
        self.left_boundary.signed_radius = radius_l
        self.add(self.left_boundary)

        # Right boundary - bulge to the right (outward)
        top_r, bottom_r, radius_r = self._generate_boundary_arc(
            self.right_boundary_position, self.right_boundary_height, is_left=False
        )

        self.right_boundary = ArcBetweenPoints(
            top_r,
            bottom_r,
            radius=radius_r,  # Negative radius makes it bulge right (outward)
            stroke_color=self.boundary_color,
            stroke_width=self.boundary_stroke_width,
            fill_opacity=0,
        )
        # Store the signed radius separately (ArcBetweenPoints converts to abs value)
        self.right_boundary.signed_radius = radius_r
        self.add(self.right_boundary)
        self.add(self.right_boundary)

        # 4. Focal points F and F'
        if self.show_focal_points:
            self._create_focal_points()
        else:
            self.f_point = None
            self.f_prime_point = None

    def _create_focal_points(self):
        """Create and add focal point markers."""
        # F is at distance focal_length to the left of H
        f_position = self.h_position - self.focal_length
        self.f_point = Dot(
            point=np.array([f_position, 0.0, 0.0]) + self._visual_offset,
            color=self.focal_point_color,
            radius=0.05,
        )

        # F' is at distance focal_length to the right of H'
        f_prime_position = self.h_prime_position + self.focal_length
        self.f_prime_point = Dot(
            point=np.array([f_prime_position, 0.0, 0.0]) + self._visual_offset,
            color=self.focal_point_color,
            radius=0.05,
        )

        self.add(self.f_point, self.f_prime_point)

        # Labels for focal points
        f_label = Text("F", color=self.focal_point_color, font_size=20)
        f_label.always.next_to(self.f_point, DOWN, buff=0.2)

        f_prime_label = Text("F'", color=self.focal_point_color, font_size=20)
        f_prime_label.always.next_to(self.f_prime_point, DOWN, buff=0.2)

        self.add(f_label, f_prime_label)

    def get_optical_plane_position(self) -> np.ndarray:
        """
        Get position of the optical center (midpoint between H and H').

        Returns
        -------
        np.ndarray
            Position of the optical center
        """
        h = self._get_current_h_position()
        h_prime = self._get_current_h_prime_position()
        center_x = (h + h_prime) / 2
        return np.array([center_x, self._get_current_optical_axis_y(), 0.0])

    def _get_current_h_position(self) -> float:
        """Get current H position from live geometry when available."""
        if hasattr(self, "h_plane") and self.h_plane is not None:
            return float(self.h_plane.get_center()[0])
        return float(self.h_position_tracker.get_value())

    def _get_current_h_prime_position(self) -> float:
        """Get current H' position from live geometry when available."""
        if hasattr(self, "h_prime_plane") and self.h_prime_plane is not None:
            return float(self.h_prime_plane.get_center()[0])
        return float(self.h_prime_position_tracker.get_value())

    def _get_current_optical_axis_y(self) -> float:
        """Get current optical-axis y from live geometry when available."""
        if hasattr(self, "h_plane") and self.h_plane is not None:
            return float(self.h_plane.get_center()[1])
        return float(self._visual_offset[1])

    def _get_current_focal_length(self) -> float:
        """Get current focal length from tracker."""
        return float(self.focal_length_tracker.get_value())

    def _get_current_boundary_positions(self) -> tuple:
        """Get current left/right boundary x-positions from live geometry."""
        left_x = self.left_boundary_position
        right_x = self.right_boundary_position
        if hasattr(self, "left_boundary") and self.left_boundary is not None:
            left_x = float(self.left_boundary.get_start()[0])
        if hasattr(self, "right_boundary") and self.right_boundary is not None:
            right_x = float(self.right_boundary.get_start()[0])
        return left_x, right_x

    def compute_image_position(self, object_position: np.ndarray) -> np.ndarray:
        """
        Compute the image position for a given object position.

        Uses the current system parameters (H, H', focal length) and
        a paraxial thin-lens relation with principal planes.

        Parameters
        ----------
        object_position : np.ndarray
            Object position in scene coordinates.

        Returns
        -------
        np.ndarray
            Image position in scene coordinates.
        """
        h = self._get_current_h_position()
        h_prime = self._get_current_h_prime_position()
        f = self._get_current_focal_length()

        object_position = np.array(object_position, dtype=float)
        x_obj = object_position[0]
        optical_axis_y = self._get_current_optical_axis_y()
        y_obj = object_position[1] - optical_axis_y

        # Object distance from H (positive if object is on the left side)
        s = h - x_obj
        if abs(s) < 1e-10:
            return np.array([np.nan, np.nan, np.nan])

        # Thin lens formula: 1/f = 1/s + 1/s'
        inv_sp = (1.0 / f) - (1.0 / s)
        if abs(inv_sp) < 1e-10:
            s_prime = np.inf
        else:
            s_prime = 1.0 / inv_sp

        # Image position relative to H'
        x_img = h_prime + s_prime

        # Transverse magnification
        m = -s_prime / s if np.isfinite(s_prime) else np.inf
        y_img = m * y_obj if np.isfinite(m) else np.nan

        return np.array([x_img, y_img + optical_axis_y, 0.0])

    def intersect(self, ray_start: np.ndarray, ray_direction: np.ndarray) -> tuple:
        """
        Calculate intersection with principal plane H only.

        The CenteredSystem interacts ONLY with H (the object-side principal plane).
        H' is purely a teleportation target. The traversed_systems memory in rays.py
        ensures the system is only traversed once.

        Parameters
        ----------
        ray_start : np.ndarray
            Starting position of the ray
        ray_direction : np.ndarray
            Direction vector of the ray

        Returns
        -------
        tuple
            (intersection_point, has_intersection) where ``intersection_point`` is
            the hit point on H.
        """
        if abs(ray_direction[0]) < 1e-10:
            return None, False  # Ray parallel to H

        # Calculate intersection with H only
        h = self._get_current_h_position()
        t_h = (h - ray_start[0]) / ray_direction[0]

        if t_h <= 0:
            return None, False  # H is behind the ray

        # Calculate intersection point at H
        intersection_h = ray_start + t_h * ray_direction

        # Check if within system height (relative to visual offset)
        y_offset = self._get_current_optical_axis_y()
        if abs(intersection_h[1] - y_offset) > self.system_height / 2:
            return None, False  # Outside system boundaries

        # Store the intersection height for propagation
        self._h_intersection_height = intersection_h[1] - y_offset

        return intersection_h, True

    def propagate_ray(
        self,
        ray_start: np.ndarray,
        ray_direction: np.ndarray,
        intersection_point: np.ndarray,
    ) -> tuple:
        """
        Propagate ray through principal planes H → H'.

        The ray has hit H (from intersect). We calculate the deflection using
        paraxial optics and teleport to H' at the same height. The ray then
        exits the system from H'.

        Parameters
        ----------
        ray_start : np.ndarray
            Starting position of the ray
        ray_direction : np.ndarray
            Direction vector of the ray
        intersection_point : np.ndarray
            Point at H (from intersect)

        Returns
        -------
        tuple
            (new_direction, continues, teleport_point)
            - new_direction: direction after system (from H')
            - continues: True (ray continues)
            - teleport_point: point at H' where the outgoing ray starts (same height as H)
        """
        # Get the intersection height at H
        y_offset = self._get_current_optical_axis_y()
        y_intersection = getattr(
            self, "_h_intersection_height", intersection_point[1] - y_offset
        )

        # Calculate new direction using paraxial approximation
        # The system acts like a thin lens at the principal planes
        tan_theta_in = (
            ray_direction[1] / ray_direction[0] if abs(ray_direction[0]) > 1e-10 else 0
        )
        tan_theta_out = tan_theta_in - y_intersection / self._get_current_focal_length()

        # New direction (normalized)
        new_direction = np.array([1.0, tan_theta_out, 0.0])
        new_direction = new_direction / np.linalg.norm(new_direction)

        # Teleport to H' at the SAME height as the intersection with H
        teleport_point = np.array(
            [
                self._get_current_h_prime_position(),
                y_intersection + y_offset,
                0.0,
            ]
        )

        return new_direction, True, teleport_point

    def should_hide_segment(self, point1: np.ndarray, point2: np.ndarray) -> bool:
        """
        Check if a ray segment should be hidden (between H and H').

        A segment crossing through the system (from before H to H') should be split:
        the part going to H is visible, the part from H to H' should be hidden.

        Parameters
        ----------
        point1 : np.ndarray
            Start point of segment
        point2 : np.ndarray
            End point of segment

        Returns
        -------
        bool
            True if segment should be hidden
        """
        # Splitting is handled by `split_segment_at_boundaries`; this hook is
        # kept for API compatibility but currently never hides any segment.
        return False

    def _intersect_arc_boundary(
        self, ray_start: np.ndarray, ray_direction: np.ndarray, arc
    ) -> tuple:
        """
        Calculate intersection between a ray and an arc boundary.

        Similar to ArcBeamStop.intersect() but for ArcBetweenPoints.

        Parameters
        ----------
        ray_start : np.ndarray
            Ray starting point (3D)
        ray_direction : np.ndarray
            Ray direction vector (3D)
        arc : ArcBetweenPoints
            The boundary arc

        Returns
        -------
        tuple
            (intersection_point, found) where found is True if intersection exists
        """
        # Get arc parameters from the Manim ArcBetweenPoints object
        start_pt = arc.get_start()
        end_pt = arc.get_end()

        # ArcBetweenPoints stores radius as an attribute (but converts to abs!)
        # Use signed_radius if available (set when creating boundaries)
        if hasattr(arc, "signed_radius"):
            arc_radius = arc.signed_radius
        elif hasattr(arc, "radius"):
            arc_radius = arc.radius
        else:
            return None, False

        # Work in 2D
        ray_start_2d = ray_start[:2]
        ray_dir_2d = ray_direction[:2]

        # Normalize direction
        ray_dir_2d_norm = np.linalg.norm(ray_dir_2d)
        if ray_dir_2d_norm < 1e-10:
            return None, False
        ray_dir_2d = ray_dir_2d / ray_dir_2d_norm

        # Calculate arc center using perpendicular bisector method
        midpoint = (start_pt[:2] + end_pt[:2]) / 2
        chord_vec = end_pt[:2] - start_pt[:2]
        chord_length = np.linalg.norm(chord_vec)

        if chord_length < 1e-10:
            return None, False

        # Perpendicular to chord
        perp = np.array([-chord_vec[1], chord_vec[0]]) / chord_length

        # Distance from midpoint to center
        abs_radius = abs(arc_radius)
        if chord_length > 2 * abs_radius:
            return None, False

        h = np.sqrt(abs_radius**2 - (chord_length / 2) ** 2)

        # Center position (sign depends on radius)
        center_2d = midpoint + (h if arc_radius > 0 else -h) * perp

        # Ray-circle intersection
        to_start = ray_start_2d - center_2d
        proj_length = np.dot(to_start, ray_dir_2d)
        closest_point = ray_start_2d - proj_length * ray_dir_2d
        dist_to_ray = np.linalg.norm(center_2d - closest_point)

        if dist_to_ray > abs_radius + 1e-6:
            return None, False

        # Calculate intersection points
        half_chord_int = (
            np.sqrt(abs_radius**2 - dist_to_ray**2) if dist_to_ray < abs_radius else 0
        )
        t1 = -proj_length - half_chord_int
        t2 = -proj_length + half_chord_int

        # Helper to check if angle is within arc range
        def angle_between(target, start, end):
            """Check if target angle is between start and end angles."""
            target = target % (2 * np.pi)
            start = start % (2 * np.pi)
            end = end % (2 * np.pi)

            if start <= end:
                return start <= target <= end
            else:
                return target >= start or target <= end

        # Check both intersections
        for t in [t1, t2]:
            if t < 1e-6:  # Skip behind ray start
                continue

            intersection_2d = ray_start_2d + t * ray_dir_2d

            # Check if point is on the arc
            to_intersection = intersection_2d - center_2d
            to_start_pt = start_pt[:2] - center_2d
            to_end_pt = end_pt[:2] - center_2d

            angle_intersection = np.arctan2(to_intersection[1], to_intersection[0])
            angle_start = np.arctan2(to_start_pt[1], to_start_pt[0])
            angle_end = np.arctan2(to_end_pt[1], to_end_pt[0])

            # For negative radius, the arc goes the OTHER way (swap start/end)
            if arc_radius < 0:
                angle_start, angle_end = angle_end, angle_start

            if angle_between(angle_intersection, angle_start, angle_end):
                intersection_3d = np.array(
                    [intersection_2d[0], intersection_2d[1], 0.0]
                )
                return intersection_3d, True

        return None, False

    def split_segment_at_boundaries(
        self, point1: np.ndarray, point2: np.ndarray
    ) -> list:
        """
        Split a segment that crosses through the system into visible/invisible parts.

        Uses real arc intersection instead of simple x-position checks.

        Returns a list of tuples (p1, p2, visible, dashed) where:
        - visible is a boolean (True = show, False = hide)
        - dashed is a boolean (True = dashed style, False = solid style)

        Parameters
        ----------
        point1 : np.ndarray
            Start point of segment
        point2 : np.ndarray
            End point of segment

        Returns
        -------
        list of tuples
            [(start, end, visible, dashed), ...] segments
        """
        x1, x2 = point1[0], point2[0]
        h = self._get_current_h_position()
        h_prime = self._get_current_h_prime_position()
        left_boundary_x, right_boundary_x = self._get_current_boundary_positions()

        # Direction vector for intersection calculations
        segment_direction = point2 - point1
        segment_length = np.linalg.norm(segment_direction)
        if segment_length < 1e-10:
            # Degenerate segment
            return [(point1, point2, True, False)]
        segment_direction = segment_direction / segment_length

        # CRITICAL: Teleportation ONLY occurs from H to H' in the direction of ray travel
        # If the ray encounters H' before H, it should remain VISIBLE until it reaches H
        # Use a slightly relaxed tolerance to handle floating-point precision issues during animations
        tolerance = 1e-5

        # Determine ray direction (from point1 to point2)
        ray_going_right = x2 > x1

        # Check if H and H' are both in this segment
        min_x = min(x1, x2)
        max_x = max(x1, x2)
        h_in_segment = min_x - tolerance <= h <= max_x + tolerance
        hprime_in_segment = min_x - tolerance <= h_prime <= max_x + tolerance

        # Teleportation occurs ONLY if:
        # 1. Both H and H' are in the segment
        # 2. The ray encounters H BEFORE H' (in the direction of travel)
        if ray_going_right:
            # Ray goes left-to-right: H must be before H' for teleportation
            crosses_h_to_hprime = h_in_segment and hprime_in_segment and (h < h_prime)
        else:
            # Ray goes right-to-left: H must be after H' for teleportation
            crosses_h_to_hprime = h_in_segment and hprime_in_segment and (h > h_prime)

        # Teleportation detection complete

        # Debug: log segments that should teleport
        if crosses_h_to_hprime:
            pass  # Teleportation detected

        # Check intersections with boundaries
        left_intersection, left_found = self._intersect_arc_boundary(
            point1, segment_direction, self.left_boundary
        )
        right_intersection, right_found = self._intersect_arc_boundary(
            point1, segment_direction, self.right_boundary
        )

        # Filter intersections that are actually within this segment
        def is_within_segment(inter_point, p1, p2):
            """Check if intersection point is between p1 and p2."""
            if inter_point is None:
                return False
            # Calculate parameter t along segment
            seg_vec = p2 - p1
            to_inter = inter_point - p1
            t = np.dot(to_inter, seg_vec) / (np.dot(seg_vec, seg_vec) + 1e-10)
            return -1e-6 < t < 1.0 + 1e-6

        if left_found and not is_within_segment(left_intersection, point1, point2):
            left_found = False
        if right_found and not is_within_segment(right_intersection, point1, point2):
            right_found = False

        # Build list of split points in order along segment
        split_points = []

        if left_found:
            split_points.append(("left", left_intersection))

        if crosses_h_to_hprime:
            # Calculate actual intersection heights with H and H' planes
            # Linear interpolation along the segment
            if abs(x2 - x1) > 1e-10:
                t_h = (h - x1) / (x2 - x1)
                y_at_h = point1[1] + t_h * (point2[1] - point1[1])
                point_at_h = np.array([h, y_at_h, 0.0])
                point_at_hprime = np.array([h_prime, y_at_h, 0.0])
            else:
                # Vertical segment - use same y
                point_at_h = np.array([h, point1[1], 0.0])
                point_at_hprime = np.array([h_prime, point1[1], 0.0])
            split_points.append(("h", point_at_h))
            split_points.append(("hprime", point_at_hprime))

        if right_found:
            split_points.append(("right", right_intersection))

        # Sort split points by x-coordinate
        split_points.sort(key=lambda item: item[1][0])

        # Determine ray direction for correct processing order
        ray_going_right = x2 > x1
        if not ray_going_right:
            # Ray going left: reverse the split points to process in ray direction
            split_points.reverse()

        # Build segments
        if not split_points:
            # No intersections - determine style based on position
            x_mid = (x1 + x2) / 2
            is_inside = left_boundary_x <= x_mid <= right_boundary_x
            return [(point1, point2, True, is_inside)]

        # Create segments between split points
        result = []
        current_point = point1

        # Determine initial state: are we starting inside or outside boundaries?
        # Check if point1 x-position is within the boundary arc region
        is_inside_boundaries = left_boundary_x <= x1 <= right_boundary_x

        i = 0
        while i < len(split_points):
            label, split_point = split_points[i]

            if label == "left":
                # Before left boundary: solid (outside)
                result.append((current_point, split_point, True, False))
                current_point = split_point
                is_inside_boundaries = True  # Now inside after crossing left boundary
                i += 1

            elif label == "h":
                # Before H: use current inside/outside state
                dashed = is_inside_boundaries
                # Only add segment if there's actually distance to cover
                if np.linalg.norm(split_point - current_point) > 1e-6:
                    result.append((current_point, split_point, True, dashed))

                # Check for teleportation: H→H' only (not H'→H)
                if i + 1 < len(split_points):
                    next_label = split_points[i + 1][0]
                    if next_label == "hprime":
                        # H → H' teleportation: invisible segment
                        entry_point = split_point
                        exit_point = split_points[i + 1][1]
                        result.append((entry_point, exit_point, False, False))
                        current_point = exit_point
                        i += 2  # Skip both h and hprime
                    else:
                        # No teleportation, just crossed H alone
                        current_point = split_point
                        i += 1
                else:
                    # Last point, no teleportation possible
                    current_point = split_point
                    i += 1

            elif label == "hprime":
                # Arrived at H' WITHOUT having encountered H yet
                # This means ray crosses H' on its way to H → stay VISIBLE (no teleportation)
                dashed = is_inside_boundaries
                if np.linalg.norm(split_point - current_point) > 1e-6:
                    result.append((current_point, split_point, True, dashed))

                # Continue from H' without teleportation
                current_point = split_point
                i += 1

            elif label == "right":
                # Before right boundary: dashed (inside)
                result.append((current_point, split_point, True, True))
                current_point = split_point
                is_inside_boundaries = (
                    False  # Now outside after crossing right boundary
                )
                i += 1

        # Add final segment after last split point
        if np.linalg.norm(point2 - current_point) > 1e-6:
            # After last event: use current inside/outside state
            result.append((current_point, point2, True, is_inside_boundaries))

        # SAFETY CHECK: Ensure NO visible segment exists between the two principal planes
        # This is critical - any segment between H and H' MUST be invisible (regardless of order)
        verified_result = []
        min_principal = min(h, h_prime)
        max_principal = max(h, h_prime)

        for seg_start, seg_end, visible, dashed in result:
            seg_x1, seg_x2 = seg_start[0], seg_end[0]
            seg_min_x = min(seg_x1, seg_x2)
            seg_max_x = max(seg_x1, seg_x2)

            # Check if this segment overlaps the forbidden zone [min_principal, max_principal]
            overlaps_forbidden = (seg_min_x < max_principal) and (
                seg_max_x > min_principal
            )

            if overlaps_forbidden and visible:
                # This segment crosses the forbidden zone
                # If it spans exactly from one principal plane to the other, force invisible
                is_teleport_segment = (
                    abs(seg_x1 - min_principal) < 1e-4
                    and abs(seg_x2 - max_principal) < 1e-4
                ) or (
                    abs(seg_x1 - max_principal) < 1e-4
                    and abs(seg_x2 - min_principal) < 1e-4
                )
                if is_teleport_segment:
                    # This is the teleportation segment - force invisible
                    verified_result.append((seg_start, seg_end, False, dashed))
                else:
                    # This shouldn't happen - log and keep as is
                    verified_result.append((seg_start, seg_end, visible, dashed))
            else:
                verified_result.append((seg_start, seg_end, visible, dashed))

        return verified_result

    def get_transfer_matrix(self) -> np.ndarray:
        """
        Get ABCD transfer matrix for the centered system.

        For principal planes separated by distance d with focal length f:
        The system acts like a thin lens with modifications for separation.

        Returns
        -------
        np.ndarray
            2x2 ABCD matrix
        """
        # Simplified: treat as thin lens at optical center
        focal = self._get_current_focal_length()
        return np.array([[1.0, 0.0], [-1.0 / focal, 1.0]])

    def is_ray_inside_system(
        self, point: np.ndarray, ray_direction: np.ndarray
    ) -> bool:
        """
        Check if a point is inside the optical system (between boundaries).

        A ray is inside if it's between the left and right boundaries.

        Parameters
        ----------
        point : np.ndarray
            Point to check
        ray_direction : np.ndarray
            Direction of ray (for determining if entering or exiting)

        Returns
        -------
        bool
            True if point is inside the system
        """
        x = point[0]

        # Get approximate x positions of boundaries
        left_x = self.left_boundary.get_center()[0]
        right_x = self.right_boundary.get_center()[0]

        # Simple check: between the two boundaries
        if left_x <= x <= right_x:
            return True
        return False

    def set_plane_style(
        self,
        color=None,
        stroke_width=None,
        dash_length=None,
    ):
        """
        Update the style of principal planes H and H'.

        Parameters
        ----------
        color : color, optional
            New color for planes
        stroke_width : float, optional
            New stroke width
        dash_length : float, optional
            New dash length

        Returns
        -------
        CenteredSystem
            Self (for chaining)
        """
        if color is not None:
            self.h_color = color
            self.h_plane.set_color(color)
            self.h_prime_plane.set_color(color)

        if stroke_width is not None:
            self.h_stroke_width = stroke_width
            self.h_plane.set_stroke(width=stroke_width)
            self.h_prime_plane.set_stroke(width=stroke_width)

        if dash_length is not None:
            self.h_dash_length = dash_length
            # Recreate dashed lines with new dash length
            # (Manim doesn't support dynamic dash length changes easily)

        return self

    def toggle_labels(self, show: bool = None):
        """
        Show or hide H and H' labels.

        Parameters
        ----------
        show : bool, optional
            If None, toggles current state. Otherwise sets to show/hide.

        Returns
        -------
        CenteredSystem
            Self (for chaining)
        """
        if show is None:
            show = not self.show_labels

        self.show_labels = show

        if self.h_label is not None:
            if show:
                self.h_label.set_opacity(1)
                self.h_prime_label.set_opacity(1)
            else:
                self.h_label.set_opacity(0)
                self.h_prime_label.set_opacity(0)

        return self

    def toggle_focal_points(self, show: bool = None):
        """
        Show or hide focal points F and F'.

        Parameters
        ----------
        show : bool, optional
            If None, toggles current state. Otherwise sets to show/hide.

        Returns
        -------
        CenteredSystem
            Self (for chaining)
        """
        if show is None:
            show = not self.show_focal_points

        self.show_focal_points = show

        if self.f_point is not None:
            if show:
                self.f_point.set_opacity(1)
                self.f_prime_point.set_opacity(1)
            else:
                self.f_point.set_opacity(0)
                self.f_prime_point.set_opacity(0)

        return self

    def create_animation(self, run_time: float = 1.5) -> AnimationGroup:
        """
        Create an elegant appearance animation for the system.

        Sequence:
        1. Boundaries grow from center
        2. Principal planes fade in
        3. Labels and focal points appear

        Parameters
        ----------
        run_time : float
            Duration of the animation

        Returns
        -------
        AnimationGroup
            Appearance animation
        """
        animations = []

        # Boundaries grow
        animations.append(GrowFromCenter(self.left_boundary))
        animations.append(GrowFromCenter(self.right_boundary))

        # Planes fade in
        animations.append(FadeIn(self.h_plane))
        animations.append(FadeIn(self.h_prime_plane))

        # Labels
        if self.show_labels and self.h_label is not None:
            animations.append(FadeIn(self.h_label))
            animations.append(FadeIn(self.h_prime_label))

        # Focal points
        if self.show_focal_points and self.f_point is not None:
            animations.append(FadeIn(self.f_point))
            animations.append(FadeIn(self.f_prime_point))

        return AnimationGroup(*animations, lag_ratio=0.1, run_time=run_time)

    def fade_out_animation(self, run_time: float = 1.0) -> AnimationGroup:
        """
        Create an elegant disappearance animation for the system.

        Parameters
        ----------
        run_time : float
            Duration of the animation

        Returns
        -------
        AnimationGroup
            Disappearance animation
        """
        return AnimationGroup(
            *[FadeOut(mob) for mob in self.submobjects],
            lag_ratio=0.05,
            run_time=run_time,
        )

    def _manual_update_visual(self):
        """Manually update visual without the updater (used during animations)."""
        # Get current values from trackers
        new_h = self.h_position_tracker.get_value()
        new_h_prime = self.h_prime_position_tracker.get_value()
        new_focal = self.focal_length_tracker.get_value()

        # Update stored values
        self.h_position = new_h
        self.h_prime_position = new_h_prime
        self.focal_length = new_focal

        # Update boundary positions
        h_offset = new_h - self._initial_h_position
        h_prime_offset = new_h_prime - self._initial_h_prime_position
        self.left_boundary_position = self._initial_left_boundary_position + h_offset
        self.right_boundary_position = (
            self._initial_right_boundary_position + h_prime_offset
        )

        # 1) Move principal planes with visual offset
        self.h_plane.move_to(
            np.array([self.h_position, 0.0, 0.0]) + self._visual_offset
        )
        self.h_prime_plane.move_to(
            np.array([self.h_prime_position, 0.0, 0.0]) + self._visual_offset
        )

        # 2) Update labels
        if self.h_label is not None:
            self.h_label.next_to(self.h_plane, DOWN, buff=0.2)
        if self.h_prime_label is not None:
            self.h_prime_label.next_to(self.h_prime_plane, DOWN, buff=0.2)

        # 3) Update boundaries geometry
        top_l, bottom_l, radius_l = self._generate_boundary_arc(
            self.left_boundary_position, self.left_boundary_height, is_left=True
        )
        new_left = ArcBetweenPoints(
            top_l,
            bottom_l,
            radius=radius_l,
            stroke_color=self.boundary_color,
            stroke_width=self.boundary_stroke_width,
            fill_opacity=0,
        )
        new_left.signed_radius = radius_l
        self.left_boundary.become(new_left)

        top_r, bottom_r, radius_r = self._generate_boundary_arc(
            self.right_boundary_position, self.right_boundary_height, is_left=False
        )
        new_right = ArcBetweenPoints(
            top_r,
            bottom_r,
            radius=radius_r,
            stroke_color=self.boundary_color,
            stroke_width=self.boundary_stroke_width,
            fill_opacity=0,
        )
        new_right.signed_radius = radius_r
        self.right_boundary.become(new_right)

        # 4) Update focal points
        if self.show_focal_points and self.f_point is not None:
            f_position = self.h_position - self.focal_length
            f_prime_position = self.h_prime_position + self.focal_length
            self.f_point.move_to(np.array([f_position, 0.0, 0.0]) + self._visual_offset)
            self.f_prime_point.move_to(
                np.array([f_prime_position, 0.0, 0.0]) + self._visual_offset
            )

    def _update_from_trackers(self, mobject):
        """
        Updater to synchronize values from ValueTrackers and update visuals.
        """
        # Get current values from trackers
        new_h = self.h_position_tracker.get_value()
        new_h_prime = self.h_prime_position_tracker.get_value()
        new_focal = self.focal_length_tracker.get_value()

        # Check if anything changed
        changed = (
            abs(new_h - self.h_position) > 1e-6
            or abs(new_h_prime - self.h_prime_position) > 1e-6
            or abs(new_focal - self.focal_length) > 1e-6
        )

        if not changed:
            return

        # Update stored values
        self.h_position = new_h
        self.h_prime_position = new_h_prime
        self.focal_length = new_focal

        # Update boundary positions (maintain relative offset from initial)
        h_offset = new_h - self._initial_h_position
        h_prime_offset = new_h_prime - self._initial_h_prime_position
        self.left_boundary_position = self._initial_left_boundary_position + h_offset
        self.right_boundary_position = (
            self._initial_right_boundary_position + h_prime_offset
        )

        # 1) Move principal planes
        self.h_plane.move_to(
            np.array([self.h_position, 0.0, 0.0]) + self._visual_offset
        )
        self.h_prime_plane.move_to(
            np.array([self.h_prime_position, 0.0, 0.0]) + self._visual_offset
        )

        # 2) Update labels
        if self.h_label is not None:
            self.h_label.next_to(self.h_plane, DOWN, buff=0.2)
        if self.h_prime_label is not None:
            self.h_prime_label.next_to(self.h_prime_plane, DOWN, buff=0.2)

        # 3) Update boundaries geometry (become on submobjects only)
        top_l, bottom_l, radius_l = self._generate_boundary_arc(
            self.left_boundary_position, self.left_boundary_height, is_left=True
        )
        new_left = ArcBetweenPoints(
            top_l,
            bottom_l,
            radius=radius_l,
            stroke_color=self.boundary_color,
            stroke_width=self.boundary_stroke_width,
            fill_opacity=0,
        )
        new_left.signed_radius = radius_l
        self.left_boundary.become(new_left)

        top_r, bottom_r, radius_r = self._generate_boundary_arc(
            self.right_boundary_position, self.right_boundary_height, is_left=False
        )
        new_right = ArcBetweenPoints(
            top_r,
            bottom_r,
            radius=radius_r,
            stroke_color=self.boundary_color,
            stroke_width=self.boundary_stroke_width,
            fill_opacity=0,
        )
        new_right.signed_radius = radius_r
        self.right_boundary.become(new_right)

        # 4) Update focal points
        if self.show_focal_points and self.f_point is not None:
            f_position = self.h_position - self.focal_length
            f_prime_position = self.h_prime_position + self.focal_length
            self.f_point.move_to(np.array([f_position, 0.0, 0.0]) + self._visual_offset)
            self.f_prime_point.move_to(
                np.array([f_prime_position, 0.0, 0.0]) + self._visual_offset
            )

    def shift(self, *vectors):
        """
        Shift the system while keeping trackers and visuals in sync.

        This updates the H/H' trackers (x-shift) and moves the visual offset (y/z).
        """
        if len(vectors) == 0:
            return self

        total_shift = np.sum(np.array(vectors), axis=0)
        dx, dy, dz = total_shift

        if abs(dx) > 1e-10:
            new_h = self.h_position_tracker.get_value() + dx
            new_h_prime = self.h_prime_position_tracker.get_value() + dx

            self.h_position_tracker.set_value(new_h)
            self.h_prime_position_tracker.set_value(new_h_prime)

            self.h_position = new_h
            self.h_prime_position = new_h_prime

            self._initial_h_position += dx
            self._initial_h_prime_position += dx
            self.left_boundary_position += dx
            self.right_boundary_position += dx
            self._initial_left_boundary_position += dx
            self._initial_right_boundary_position += dx

        if abs(dy) > 1e-10 or abs(dz) > 1e-10:
            self._visual_offset = self._visual_offset + np.array([0.0, dy, dz])

        self._manual_update_visual()
        return self

    def interpolate(self, mobject1, mobject2, alpha, *args, **kwargs):
        """
        Interpolate state during animations to keep trackers synchronized.

        This ensures rays update continuously when using obj.animate.shift(...).
        """
        super().interpolate(mobject1, mobject2, alpha, *args, **kwargs)

        # Keep cached scalar state coherent with the interpolated geometry.
        self.h_position = self._get_current_h_position()
        self.h_prime_position = self._get_current_h_prime_position()
        self._visual_offset[1] = self._get_current_optical_axis_y()

        left_x, right_x = self._get_current_boundary_positions()
        self.left_boundary_position = left_x
        self.right_boundary_position = right_x

        # Focal length remains tracker-driven.
        self.focal_length = self._get_current_focal_length()

    def animate_h_position(self, new_h_position: float, run_time: float = 1.0):
        """Animate H by driving its ValueTracker (updater remains active)."""
        return self.h_position_tracker.animate(run_time=run_time).set_value(
            new_h_position
        )

    def animate_h_prime_position(
        self, new_h_prime_position: float, run_time: float = 1.0
    ):
        """Animate H' by driving its ValueTracker (updater remains active)."""
        return self.h_prime_position_tracker.animate(run_time=run_time).set_value(
            new_h_prime_position
        )

    def animate_focal_length(self, new_focal_length: float, run_time: float = 1.0):
        """Animate focal length via its ValueTracker (updater remains active)."""
        return self.focal_length_tracker.animate(run_time=run_time).set_value(
            new_focal_length
        )

    def animate_system_position(
        self, new_h: float, new_h_prime: float, run_time: float = 1.0
    ):
        """Animate H and H' together via their trackers (updater remains active)."""
        return AnimationGroup(
            self.h_position_tracker.animate(run_time=run_time).set_value(new_h),
            self.h_prime_position_tracker.animate(run_time=run_time).set_value(
                new_h_prime
            ),
            lag_ratio=0.0,
        )

    def set_h_position(self, h_position: float):
        """Set H position immediately without animation."""
        self.h_position = h_position
        self.h_position_tracker.set_value(h_position)
        return self

    def set_h_prime_position(self, h_prime_position: float):
        """Set H' position immediately without animation."""
        self.h_prime_position = h_prime_position
        self.h_prime_position_tracker.set_value(h_prime_position)
        return self

    def set_focal_length(self, focal_length: float):
        """Set focal length immediately without animation."""
        self.focal_length = focal_length
        self.focal_length_tracker.set_value(focal_length)
        return self
