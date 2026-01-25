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
        **kwargs
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
            **kwargs
        )

        self.h_position = h_position
        self.h_prime_position = h_prime_position
        self.focal_length = focal_length
        self.system_height = height

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
        top_point = np.array([x_position, boundary_height / 2, 0.0])
        bottom_point = np.array([x_position, -boundary_height / 2, 0.0])

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
        self.h_plane.shift(RIGHT * self.h_position)

        self.h_prime_plane = DashedLine(
            UP * self.system_height / 2,
            DOWN * self.system_height / 2,
            dash_length=self.h_dash_length,
            stroke_color=self.h_color,
            stroke_width=self.h_stroke_width,
        )
        self.h_prime_plane.shift(RIGHT * self.h_prime_position)

        self.add(self.h_plane, self.h_prime_plane)

        # 2. Labels H and H'
        if self.show_labels:
            self.h_label = Text("H", color=self.label_color, font_size=24)
            self.h_label.next_to(self.h_plane, DOWN, buff=0.2)

            self.h_prime_label = Text("H'", color=self.label_color, font_size=24)
            self.h_prime_label.next_to(self.h_prime_plane, DOWN, buff=0.2)

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
            point=np.array([f_position, 0.0, 0.0]),
            color=self.focal_point_color,
            radius=0.05,
        )

        # F' is at distance focal_length to the right of H'
        f_prime_position = self.h_prime_position + self.focal_length
        self.f_prime_point = Dot(
            point=np.array([f_prime_position, 0.0, 0.0]),
            color=self.focal_point_color,
            radius=0.05,
        )

        self.add(self.f_point, self.f_prime_point)

        # Labels for focal points
        f_label = Text("F", color=self.focal_point_color, font_size=20)
        f_label.next_to(self.f_point, DOWN, buff=0.1)

        f_prime_label = Text("F'", color=self.focal_point_color, font_size=20)
        f_prime_label.next_to(self.f_prime_point, DOWN, buff=0.1)

        self.add(f_label, f_prime_label)

    def get_optical_plane_position(self) -> np.ndarray:
        """
        Get position of the optical center (midpoint between H and H').

        Returns
        -------
        np.ndarray
            Position of the optical center
        """
        center_x = (self.h_position + self.h_prime_position) / 2
        return np.array([center_x, 0.0, 0.0])

    def intersect(self, ray_start: np.ndarray, ray_direction: np.ndarray) -> tuple:
        """
        Calculate intersection with principal plane H.

        For ray tracing purposes, we return H' as the intersection point to implement
        the "teleportation" behavior. The ray hits H, but we return H' so the next
        segment starts from there.

        Parameters
        ----------
        ray_start : np.ndarray
            Starting position of the ray
        ray_direction : np.ndarray
            Direction vector of the ray

        Returns
        -------
        tuple
            (intersection_point, has_intersection) where:
            - intersection_point: position at H' (same height as ray would hit H)
            - has_intersection: bool indicating if intersection exists
        """
        # Intersection with plane H (vertical plane at x = h_position)
        if abs(ray_direction[0]) < 1e-10:
            return None, False  # Ray parallel to H

        t = (self.h_position - ray_start[0]) / ray_direction[0]

        if t < 0:
            return None, False  # Intersection behind ray start

        intersection_h = ray_start + t * ray_direction

        # Check if within system height
        if abs(intersection_h[1]) > self.system_height / 2:
            return None, False  # Outside system boundaries

        # Store the H intersection for calculations
        self._last_h_intersection = intersection_h

        # Return H' position (teleportation) - same height but at H' x-position
        intersection_h_prime = np.array(
            [self.h_prime_position, intersection_h[1], 0.0]  # Same height as at H
        )

        return intersection_h_prime, True

    def propagate_ray(
        self,
        ray_start: np.ndarray,
        ray_direction: np.ndarray,
        intersection_point: np.ndarray,
    ) -> tuple:
        """
        Propagate ray through principal planes.

        The intersection_point here is actually H' (from our intersect method).
        We use the stored H intersection to calculate the proper deflection.

        This method also marks that the segment between H and H' should be hidden
        by storing segment info in a special attribute.

        Parameters
        ----------
        ray_start : np.ndarray
            Starting position of the ray
        ray_direction : np.ndarray
            Direction vector of the ray
        intersection_point : np.ndarray
            Point at H' (returned by intersect)

        Returns
        -------
        tuple
            (new_direction, continues)
            - new_direction: direction after system (from H')
            - continues: True (ray continues)
        """
        # Get the actual H intersection (stored by intersect method)
        if hasattr(self, "_last_h_intersection"):
            y_intersection = self._last_h_intersection[1]
        else:
            # Fallback: use intersection_point height
            y_intersection = intersection_point[1]

        # Calculate new direction using thin lens approximation
        # Paraxial approximation
        tan_theta_in = (
            ray_direction[1] / ray_direction[0] if abs(ray_direction[0]) > 1e-10 else 0
        )
        tan_theta_out = tan_theta_in - y_intersection / self.focal_length

        # New direction
        new_direction = np.array([1.0, tan_theta_out, 0.0])
        new_direction = new_direction / np.linalg.norm(new_direction)

        return new_direction, True

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
        x1, x2 = point1[0], point2[0]

        # Debug logging

        # Check if this is a segment that crosses through the system
        # From before/at H to at/after H'
        crosses_into_system = x1 <= self.h_position and x2 >= self.h_prime_position

        if crosses_into_system:
            # This segment needs to be split in rays.py
            # We mark it for splitting but don't hide it entirely here
            return False

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

        # Direction vector for intersection calculations
        segment_direction = point2 - point1
        segment_length = np.linalg.norm(segment_direction)
        if segment_length < 1e-10:
            # Degenerate segment
            return [(point1, point2, True, False)]
        segment_direction = segment_direction / segment_length

        # Check if segment crosses H and H' planes
        # A segment "crosses" if it goes through (strictly) or ends exactly at the boundary
        crosses_h = ((x1 < self.h_position < x2) or (x2 < self.h_position < x1) or 
                     abs(x2 - self.h_position) < 1e-6 or abs(x1 - self.h_position) < 1e-6)
        crosses_hprime = ((x1 < self.h_prime_position < x2) or (x2 < self.h_prime_position < x1) or
                          abs(x2 - self.h_prime_position) < 1e-6 or abs(x1 - self.h_prime_position) < 1e-6)
        
        # Only add H/H' splits if segment actually spans from before H to after H'
        # This handles the teleportation case
        spans_h_to_hprime = ((x1 <= self.h_position and x2 >= self.h_prime_position) or
                              (x1 >= self.h_prime_position and x2 <= self.h_position))
        crosses_h_to_hprime = crosses_h and crosses_hprime and spans_h_to_hprime
        
        # Check intersections with boundaries
        left_intersection, left_found = self._intersect_arc_boundary(
            point1, segment_direction, self.left_boundary
        )
        right_intersection, right_found = self._intersect_arc_boundary(
            point1, segment_direction, self.right_boundary
        )

        print(f"\nDEBUG split_segment: ({x1:.2f}, {point1[1]:.2f}) → ({x2:.2f}, {point2[1]:.2f})")
        print(f"  Segment direction: {segment_direction[:2]}")
        print(f"  Left intersection: {left_found}, pos={left_intersection[:2] if left_found else 'None'}")
        print(f"  Right intersection: {right_found}, pos={right_intersection[:2] if right_found else 'None'}")

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
            print(f"  Left intersection REJECTED (not within segment)")
            left_found = False
        if right_found and not is_within_segment(right_intersection, point1, point2):
            print(f"  Right intersection REJECTED (not within segment)")
            right_found = False

        # Build list of split points in order along segment
        split_points = []

        if left_found:
            print(f"  Added LEFT split point at x={left_intersection[0]:.2f}")
            split_points.append(("left", left_intersection))

        if crosses_h_to_hprime:
            point_at_h = np.array([self.h_position, point2[1], 0.0])
            point_at_hprime = np.array([self.h_prime_position, point2[1], 0.0])
            print(f"  Added H/H' split points at x={self.h_position:.2f} and x={self.h_prime_position:.2f}")
            split_points.append(("h", point_at_h))
            split_points.append(("hprime", point_at_hprime))

        if right_found:
            print(f"  Added RIGHT split point at x={right_intersection[0]:.2f}")
            split_points.append(("right", right_intersection))

        # Sort split points by x-coordinate
        split_points.sort(key=lambda item: item[1][0])
        
        print(f"  Split points after sorting: {[(label, x[0]) for label, x in split_points]}")
        print(f"  Building segments from split points (initial is_inside={self.left_boundary_position <= x1 <= self.right_boundary_position}):")

        # Build segments
        if not split_points:
            # No intersections - determine style based on position
            x_mid = (x1 + x2) / 2
            is_inside = (
                self.left_boundary_position <= x_mid <= self.right_boundary_position
            )
            return [(point1, point2, True, is_inside)]

        # Create segments between split points
        result = []
        current_point = point1
        current_x = x1

        # Determine initial state: are we starting inside or outside boundaries?
        # Check if point1 x-position is within the boundary arc region
        is_inside_boundaries = (
            self.left_boundary_position <= x1 <= self.right_boundary_position
        )

        i = 0
        while i < len(split_points):
            label, split_point = split_points[i]
            
            if label == "left":
                # Before left boundary: solid (outside)
                print(f"    [left] ({current_x:.2f}→{split_point[0]:.2f}) solid (before boundary)")
                result.append((current_point, split_point, True, False))
                current_point = split_point
                current_x = split_point[0]
                is_inside_boundaries = True  # Now inside after crossing left boundary
                i += 1
                
            elif label == "h":
                # Before H: use current inside/outside state
                dashed = is_inside_boundaries
                print(f"    [h] ({current_x:.2f}→{split_point[0]:.2f}) {'dashed' if dashed else 'solid'} (is_inside={is_inside_boundaries})")
                result.append((current_point, split_point, True, dashed))
                
                # Check if next point is hprime (teleportation)
                if i + 1 < len(split_points) and split_points[i + 1][0] == "hprime":
                    h_point = split_point
                    hprime_point = split_points[i + 1][1]
                    print(f"    [hprime] ({h_point[0]:.2f}→{hprime_point[0]:.2f}) INVISIBLE")
                    result.append((h_point, hprime_point, False, False))
                    current_point = hprime_point
                    current_x = hprime_point[0]
                    i += 2  # Skip both h and hprime
                else:
                    current_point = split_point
                    current_x = split_point[0]
                    i += 1
                    
            elif label == "hprime":
                # hprime without h should not happen, but handle it
                print(f"    [hprime standalone] ({current_x:.2f}→{split_point[0]:.2f})")
                current_point = split_point
                current_x = split_point[0]
                i += 1
                
            elif label == "right":
                # Before right boundary: dashed (inside)
                print(f"    [right] ({current_x:.2f}→{split_point[0]:.2f}) dashed (inside, before right boundary)")
                result.append((current_point, split_point, True, True))
                current_point = split_point
                current_x = split_point[0]
                is_inside_boundaries = False  # Now outside after crossing right boundary
                i += 1

        # Add final segment after last split point
        if current_x < x2 - 1e-6:
            # After last event: use current inside/outside state
            print(f"    [final] ({current_x:.2f}→{x2:.2f}) {'dashed' if is_inside_boundaries else 'solid'} (is_inside={is_inside_boundaries})")
            result.append((current_point, point2, True, is_inside_boundaries))
        
        print(f"  → {len(result)} segments total")
        return result

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
        return np.array([[1.0, 0.0], [-1.0 / self.focal_length, 1.0]])

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
            run_time=run_time
        )
