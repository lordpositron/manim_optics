"""
Dynamic Ray System - Automatic ray tracing with updaters
=========================================================

This module implements rays that automatically update their paths when
optical elements move or change.
"""

from __future__ import annotations

import numpy as np
from manim import *
from typing import List, Optional, Union, Callable, Tuple, TYPE_CHECKING
from numpy.typing import NDArray

if TYPE_CHECKING:
    from .base import OpticalElement


class DynamicRay(VMobject):
    """
    A ray that automatically recalculates its path when optical elements move.

    The ray uses Manim's updater system to recompute its trajectory at every
    frame, enabling dynamic and interactive optical simulations.

    Key features:
    - Automatic path recalculation
    - Supports multiple optical elements
    - Handles reflections and refractions
    - Maximum ray segments to prevent infinite loops
    """

    def __init__(
        self,
        start_point: Union[NDArray[np.floating], Mobject],
        direction: Union[NDArray[np.floating], Callable[[], NDArray[np.floating]]],
        optical_elements: Optional[List[OpticalElement]] = None,
        max_segments: int = 10,
        ray_length: float = 100.0,
        color: str = YELLOW,
        stroke_width: float = 2,
        opacity: float = 1.0,
        **kwargs,
    ):
        """
        Initialize a dynamic ray.

        Parameters
        ----------
        start_point : np.ndarray or Mobject
            Starting position of the ray. Can be:
            - A numpy array for a fixed position
            - A Mobject whose position will be tracked dynamically
        direction : np.ndarray or callable
            Initial direction vector (will be normalized). Can be:
            - A numpy array for a fixed direction
            - A callable that returns the direction vector
        optical_elements : List[OpticalElement]
            List of optical elements the ray can interact with
        max_segments : int
            Maximum number of ray segments (prevents infinite loops)
        ray_length : float
            Length of ray segments when no intersection occurs
        color : str
            Color of the ray
        stroke_width : float
            Thickness of the ray line
        """
        super().__init__(**kwargs)

        # Store parameters (can be static or dynamic)
        self.start_point_source = start_point
        self.direction_source = direction
        self.optical_elements = optical_elements or []
        self.max_segments = max_segments
        self.ray_length = ray_length
        self.opacity = opacity

        # Visual properties
        self.set_stroke(color=color, width=stroke_width, opacity=opacity)

        # Calculate initial path
        self._update_ray_path(None)

        # Add updater for automatic recalculation
        self.add_updater(self._update_ray_path)

    def _update_ray_path(self, mobject: Optional[Mobject], dt: float = 0) -> None:
        """
        Updater function that recalculates the ray path.

        This is called automatically by Manim at every frame.
        """
        # Get current start position (dynamic or static)
        if isinstance(self.start_point_source, (VMobject, Mobject)):
            current_start = self.start_point_source.get_center()
        elif callable(self.start_point_source):
            current_start = self.start_point_source()
        else:
            current_start = np.array(self.start_point_source)

        # Get current direction (dynamic or static)
        if callable(self.direction_source):
            current_direction = self.direction_source()
        else:
            current_direction = np.array(self.direction_source)

        # Normalize direction
        current_direction = current_direction / np.linalg.norm(current_direction)

        # Memory: track which CenteredSystems have already been traversed
        # This prevents re-interaction after teleportation (H' before H case)
        traversed_systems = set()

        points = []
        current_pos = current_start.copy()
        current_dir = current_direction.copy()

        points.append(current_pos)

        for segment_idx in range(self.max_segments):
            # Find the nearest intersection with any optical element
            nearest_intersection = None
            nearest_distance = float("inf")
            nearest_element = None

            for element in self.optical_elements:
                # Skip elements that have already been traversed (for CenteredSystem)
                # Use id() to identify unique instances
                if id(element) in traversed_systems:
                    continue

                intersection, has_intersection = element.intersect(
                    current_pos, current_dir
                )

                if has_intersection and intersection is not None:
                    distance = np.linalg.norm(intersection - current_pos)
                    if (
                        distance > 1e-6 and distance < nearest_distance
                    ):  # Avoid self-intersection
                        nearest_distance = distance
                        nearest_intersection = intersection
                        nearest_element = element

            if nearest_element is not None:
                # Ray hits an optical element
                points.append(nearest_intersection)

                # Calculate new direction after interaction (optionally with teleport)
                propagation_result = nearest_element.propagate_ray(
                    current_pos, current_dir, nearest_intersection
                )

                # Unpack propagation result (supports optional teleport point)
                if (
                    isinstance(propagation_result, tuple)
                    and len(propagation_result) == 3
                ):
                    new_direction, continues, teleport_point = propagation_result
                else:
                    new_direction, continues = propagation_result
                    teleport_point = None

                if not continues:
                    # Ray is absorbed
                    break

                # If a teleport point is provided (e.g., CenteredSystem), add it
                if teleport_point is not None:
                    points.append(teleport_point)
                    current_pos = teleport_point
                    # Mark this element as traversed (only for systems with teleportation)
                    traversed_systems.add(id(nearest_element))
                else:
                    current_pos = nearest_intersection

                # Update direction for next segment
                current_dir = new_direction
            else:
                # No intersection - extend ray in current direction
                end_point = current_pos + current_dir * self.ray_length
                points.append(end_point)
                break

        # Update the visual path
        if len(points) >= 2:
            # Build list of segments, potentially splitting them if needed
            all_segments = []

            for i in range(len(points) - 1):
                p1 = points[i]
                p2 = points[i + 1]

                # Check if any element wants to split this segment
                segment_parts = [
                    (p1, p2, True, False)
                ]  # Default: one visible solid segment

                for element in self.optical_elements:
                    if hasattr(element, "split_segment_at_boundaries"):
                        # Element can split segments (like CenteredSystem)
                        segment_parts = element.split_segment_at_boundaries(p1, p2)
                        break

                # Add all parts to our list
                all_segments.extend(segment_parts)

            # Now render only the visible segments with their styles
            visible_segments = [
                (p1, p2, dashed) for p1, p2, visible, dashed in all_segments if visible
            ]

            # Collect new submobjects in a list
            new_submobjects = []

            if len(visible_segments) == 0:
                # Nothing to show - clear everything
                self.set_submobjects([])
                self.clear_points()
            else:
                # Group segments by style (solid/dashed) and continuity
                # Clear point data
                self.clear_points()

                i = 0
                while i < len(visible_segments):
                    p1, p2, dashed = visible_segments[i]
                    current_group = [p1, p2]
                    current_dashed = dashed

                    # Look ahead for continuous segments with same style
                    j = i + 1
                    while j < len(visible_segments):
                        prev_end = visible_segments[j - 1][1]
                        curr_start = visible_segments[j][0]
                        curr_dashed = visible_segments[j][2]

                        # If continuous and same style
                        if (
                            np.allclose(prev_end, curr_start, atol=1e-4)
                            and curr_dashed == current_dashed
                        ):
                            current_group.append(visible_segments[j][1])
                            j += 1
                        else:
                            break

                    # Create line for this group
                    if current_dashed:
                        # Dashed line with consistent dash spacing
                        # Calculate total length of the path
                        total_length = 0.0
                        for k in range(len(current_group) - 1):
                            total_length += np.linalg.norm(
                                current_group[k + 1] - current_group[k]
                            )

                        # Fixed physical dash and gap sizes for visual consistency
                        dash_size = 0.1  # Each dash is 0.1 units
                        gap_size = 0.1  # Each gap is 0.1 units
                        dash_period = dash_size + gap_size  # Total period = 0.2 units

                        # Calculate number of dashes based on total length
                        # Use minimum of 3 to ensure visibility even for short segments
                        num_dashes = max(3, int(total_length / dash_period))

                        # Calculate dashed_ratio to get exact dash size
                        # dashed_ratio = dash_size / dash_period
                        dashed_ratio = dash_size / dash_period  # = 0.5

                        base_vmobject = VMobject().set_points_as_corners(current_group)
                        line = DashedVMobject(
                            base_vmobject,
                            num_dashes=num_dashes,
                            dashed_ratio=dashed_ratio,
                        )
                        # Ensure stroke properties are preserved
                        line.set_stroke(
                            color=self.get_stroke_color(),
                            width=self.get_stroke_width(),
                            opacity=self.get_stroke_opacity(),
                        )
                        # Force stroke on all submobjects of DashedVMobject
                        for submob in line.submobjects:
                            submob.set_stroke(
                                color=self.get_stroke_color(),
                                width=self.get_stroke_width(),
                                opacity=self.get_stroke_opacity(),
                            )
                    else:
                        # Solid line

                        line = VMobject()
                        line.set_points_as_corners(current_group)
                        line.set_stroke(
                            color=self.get_stroke_color(),
                            width=self.get_stroke_width(),
                            opacity=self.get_stroke_opacity(),
                        )
                    new_submobjects.append(line)

                    # Move to next group
                    i = j

                # Create a temporary VGroup with new segments and become it
                # This ensures old submobjects are removed from the scene
                temp_ray = VGroup(*new_submobjects)
                temp_ray.set_stroke(
                    color=self.get_stroke_color(),
                    width=self.get_stroke_width(),
                    opacity=self.get_stroke_opacity(),
                )
                self.become(temp_ray)
        else:
            # Fallback: just draw a straight line
            if isinstance(self.start_point_source, (VMobject, Mobject)):
                fallback_start = self.start_point_source.get_center()
            else:
                fallback_start = np.array(self.start_point_source)

            if callable(self.direction_source):
                fallback_dir = self.direction_source()
            else:
                fallback_dir = np.array(self.direction_source)

            fallback_dir = fallback_dir / np.linalg.norm(fallback_dir)

            self.set_points_as_corners(
                [fallback_start, fallback_start + fallback_dir * self.ray_length]
            )

    def set_optical_elements(self, optical_elements: List[OpticalElement]) -> None:
        """Update the list of optical elements and recalculate the ray path.

        Parameters
        ----------
        optical_elements : List[OpticalElement]
            New list of optical elements
        """
        self.optical_elements = optical_elements
        # Force immediate recalculation
        self._update_ray_path(None)

    def add_optical_element(self, element: OpticalElement) -> None:
        """Add an optical element to the ray's interaction list.

        Parameters
        ----------
        element : OpticalElement
            Element to add
        """
        if element not in self.optical_elements:
            self.optical_elements.append(element)
            self._update_ray_path(None)

    def remove_optical_element(self, element: OpticalElement) -> None:
        """Remove an optical element from the ray's interaction list.

        Parameters
        ----------
        element : OpticalElement
            Element to remove
        """
        if element in self.optical_elements:
            self.optical_elements.remove(element)
            self._update_ray_path(None)

    def stop_updating(self) -> None:
        """Remove the updater to freeze the ray."""
        self.clear_updaters()

    def resume_updating(self, recursive: bool = True) -> None:
        """Re-add the updater to make the ray dynamic again."""
        self.add_updater(self._update_ray_path)
        # Call parent implementation for any submobjects
        super().resume_updating(recursive=recursive)

    def animate_propagation(self, run_time: float = 2.0, rate_func=linear) -> Animation:
        """
        Animate the ray propagating along its path with fade-in effect.

        The animation shows the ray appearing gradually while maintaining
        its correct trajectory throughout.

        Parameters
        ----------
        run_time : float
            Duration of the animation
        rate_func : function
            Rate function for the animation (default: linear)

        Returns
        -------
        Animation
            Animation that reveals the ray
        """
        # Force path update before animation to ensure correct trajectory
        self._update_ray_path(None)

        # Store current opacity
        original_opacity = self.get_stroke_opacity()

        # Set to invisible
        self.set_stroke(opacity=0)

        # Return fade-in animation
        return self.animate(run_time=run_time, rate_func=rate_func).set_stroke(
            opacity=original_opacity if original_opacity > 0 else 1
        )

    def get_vertex_index_from_pos(self, pos: NDArray[np.floating]) -> NDArray:
        """
        Given an x-coordinate, return the next vertex point of the ray.
        """
        points = self.get_points()

        idx = -1
        for i, p in enumerate(points[::-1]):
            if np.isclose(p[0], pos[0], 1e-6):
                idx = len(points) - i - 1
                return idx


class RayBundle(VGroup):
    """
    A collection of rays with flexible start points and directions.

    Supports three modes:
    1. Same start point, different directions (diverging from a point)
    2. Different start points, same direction (parallel rays)
    3. Different start points AND different directions (custom bundle)
    """

    def __init__(
        self,
        start_points: Optional[
            Union[
                NDArray[np.floating],
                Mobject,
                List[Union[NDArray[np.floating], Mobject]],
            ]
        ] = None,
        directions: Optional[
            Union[NDArray[np.floating], List[NDArray[np.floating]]]
        ] = None,
        direction_vector: Optional[
            Union[NDArray[np.floating], List[NDArray[np.floating]]]
        ] = None,
        direction_angle_rad: Optional[Union[float, List[float]]] = None,
        direction_angle_deg: Optional[Union[float, List[float]]] = None,
        num_rays: Optional[int] = None,
        optical_elements: Optional[List[OpticalElement]] = None,
        **ray_kwargs,
    ):
        """
        Initialize a bundle of rays.

        Parameters
        ----------
        start_points : np.ndarray, Mobject, or List
            - Single point (np.ndarray or Mobject): all rays start from same point
            - List of points: each ray has its own start point
        directions : np.ndarray or List[np.ndarray]
            Direction vector(s). Can be:
            - Single direction: all rays have same direction
            - List of directions: each ray has its own direction
        direction_vector : np.ndarray or List[np.ndarray]
            Alias for directions (for clarity)
        direction_angle_rad : float or List[float]
            Direction as angle(s) in radians (trigonometric sense)
        direction_angle_deg : float or List[float]
            Direction as angle(s) in degrees (trigonometric sense)
        num_rays : int
            Number of rays (used with angle ranges)
        optical_elements : List[OpticalElement]
            Optical elements to interact with
        **ray_kwargs
            Additional arguments passed to DynamicRay

        Examples
        --------
        # Diverging from a point with different angles
        bundle = RayBundle(
            start_points=ORIGIN,
            direction_angle_deg=[0, 30, 60, 90],
            optical_elements=[lens]
        )

        # Parallel rays (different starts, same direction)
        bundle = RayBundle(
            start_points=[LEFT*2+UP, LEFT*2, LEFT*2+DOWN],
            direction_vector=RIGHT,
            optical_elements=[lens]
        )

        # Custom: each ray has its own start and direction
        bundle = RayBundle(
            start_points=[pt1, pt2, pt3],
            directions=[dir1, dir2, dir3],
            optical_elements=[lens]
        )
        """
        super().__init__()

        # Extract opacity from ray_kwargs if present (to apply after ray creation)
        bundle_opacity = ray_kwargs.pop("opacity", None)

        # Create angle offset tracker (additive to base angles)
        self.angle_offset_tracker = ValueTracker(0)
        self.y_offset_tracker = ValueTracker(0)

        # Store base angles/directions for dynamic recalculation
        self._base_direction_angle_deg = direction_angle_deg
        self._base_direction_angle_rad = direction_angle_rad
        self._base_direction_vector = direction_vector
        self._base_directions = directions

        # Process direction input (priority: angle_deg > angle_rad > vector > directions)
        if direction_angle_deg is not None:
            processed_directions = self._angles_to_vectors(
                direction_angle_deg, degrees=True
            )
        elif direction_angle_rad is not None:
            processed_directions = self._angles_to_vectors(
                direction_angle_rad, degrees=False
            )
        elif direction_vector is not None:
            processed_directions = direction_vector
        elif directions is not None:
            processed_directions = directions
        else:
            # Default: horizontal direction
            processed_directions = RIGHT

        # Normalize directions to list
        if isinstance(processed_directions, (list, tuple)):
            dir_list = processed_directions
        else:
            # Single direction for all rays
            dir_list = [processed_directions]

        # Process start points
        if start_points is None:
            start_points = ORIGIN

        # Normalize start points to list
        if isinstance(start_points, (list, tuple)):
            start_list = start_points
        elif isinstance(start_points, (VMobject, Mobject)):
            # Single Mobject - all rays start from it
            start_list = [start_points]
        else:
            # Single numpy array - all rays start from it
            start_list = [start_points]

        # Determine number of rays
        max_len = max(len(start_list), len(dir_list))

        # Expand lists if needed
        if len(start_list) == 1 and max_len > 1:
            # Same start for all rays
            start_list = start_list * max_len
        if len(dir_list) == 1 and max_len > 1:
            # Same direction for all rays
            dir_list = dir_list * max_len

        # Check compatibility
        if len(start_list) != len(dir_list):
            raise ValueError(
                f"Incompatible number of start points ({len(start_list)}) "
                f"and directions ({len(dir_list)})"
            )

        # Create rays with dynamic directions if using angles
        self.rays = []
        if optical_elements is None:
            self.optical_elements = []
        else:
            self.optical_elements = optical_elements

        # Store base directions for angle-based bundles
        self._base_dir_list = (
            dir_list.copy() if isinstance(dir_list, list) else [dir_list]
        )

        # Store base start points for y-offset tracking
        self._base_start_list = start_list.copy()

        for idx, (start, base_direction) in enumerate(zip(start_list, dir_list)):
            # If we have angle-based directions, make them dynamic
            if (
                self._base_direction_angle_deg is not None
                or self._base_direction_angle_rad is not None
            ):
                # Create a closure that captures the index and base direction
                def make_dynamic_direction(base_dir, ray_idx):
                    def get_direction():
                        # Get current angle offset
                        offset_deg = self.angle_offset_tracker.get_value()

                        # Calculate base angle from base direction
                        base_angle_rad = np.arctan2(base_dir[1], base_dir[0])

                        # Add offset and create new direction
                        new_angle_rad = base_angle_rad + np.deg2rad(offset_deg)
                        return np.array(
                            [np.cos(new_angle_rad), np.sin(new_angle_rad), 0]
                        )

                    return get_direction

                direction = make_dynamic_direction(base_direction, idx)
            else:
                direction = base_direction

            # Make start point dynamic to apply y_offset
            # Create a closure that captures the base start point
            def make_dynamic_start(base_start, ray_idx):
                def get_start():
                    # Get current y offset
                    y_offset = self.y_offset_tracker.get_value()

                    # Get base position
                    if isinstance(base_start, (VMobject, Mobject)):
                        base_pos = base_start.get_center()
                    else:
                        base_pos = np.array(base_start)

                    # Apply y offset
                    return base_pos + np.array([0, y_offset, 0])

                return get_start

            # Use dynamic start point
            start_point = make_dynamic_start(start, idx)

            ray = DynamicRay(
                start_point=start_point,
                direction=direction,
                optical_elements=self.optical_elements,
                **ray_kwargs,
            )
            self.rays.append(ray)
            self.add(ray)

        # Apply bundle opacity to all rays after creation
        if bundle_opacity is not None:
            self.set_opacity(bundle_opacity)

    def _angles_to_vectors(
        self,
        angles: Union[float, List[float], Tuple[float, ...], NDArray[np.floating]],
        degrees: bool = False,
    ) -> Union[NDArray[np.floating], List[NDArray[np.floating]]]:
        """Convert angle(s) to direction vector(s)."""
        # Check if it's an iterable (list, tuple, or numpy array)
        if isinstance(angles, (list, tuple, np.ndarray)):
            vectors = []
            for angle in angles:
                rad = np.deg2rad(angle) if degrees else angle
                vectors.append(np.array([np.cos(rad), np.sin(rad), 0]))
            return vectors
        else:
            # Single angle (scalar)
            rad = np.deg2rad(angles) if degrees else angles
            return np.array([np.cos(rad), np.sin(rad), 0])

    def set_optical_elements(self, optical_elements: List[OpticalElement]) -> None:
        """Update the list of optical elements for all rays in the bundle.

        Parameters
        ----------
        optical_elements : List[OpticalElement]
            New list of optical elements
        """
        self.optical_elements = optical_elements
        for ray in self.rays:
            ray.set_optical_elements(optical_elements)

    def add_optical_element(self, element: OpticalElement) -> None:
        """Add an optical element to all rays in the bundle.

        Parameters
        ----------
        element : OpticalElement
            Element to add
        """
        if element not in self.optical_elements:
            self.optical_elements.append(element)
        for ray in self.rays:
            ray.add_optical_element(element)

    def add_optical_elements(self, elements: List[OpticalElement]) -> None:
        """Add multiple optical elements to all rays in the bundle.

        Parameters
        ----------
        elements : List[OpticalElement]
            Elements to add
        """
        for element in elements:
            self.add_optical_element(element)

    def remove_optical_element(self, element: OpticalElement) -> None:
        """Remove an optical element from all rays in the bundle.

        Parameters
        ----------
        element : OpticalElement
            Element to remove
        """
        if element in self.optical_elements:
            self.optical_elements.remove(element)
        for ray in self.rays:
            ray.remove_optical_element(element)

    def remove_optical_elements(self, elements: List[OpticalElement]) -> None:
        """Remove multiple optical elements from all rays in the bundle.

        Parameters
        ----------
        elements : List[OpticalElement]
            Elements to remove
        """
        for element in elements:
            self.remove_optical_element(element)

    def stop_updating(self) -> None:
        """Stop all rays from updating."""
        for ray in self.rays:
            ray.stop_updating()

    def resume_updating(self, recursive: bool = True) -> None:
        """Resume updating for all rays."""
        for ray in self.rays:
            ray.resume_updating(recursive=recursive)

    def set_opacity(self, opacity: float, family: bool = True) -> "RayBundle":
        """
        Set the opacity of all rays in the bundle.

        Parameters
        ----------
        opacity : float
            Opacity value (0 = transparent, 1 = opaque)
        family : bool
            If True, applies to all submobjects (default: True)

        Returns
        -------
        RayBundle
            Self (for chaining)
        """
        for ray in self.rays:
            ray.set_stroke(opacity=opacity)
            ray.opacity = opacity
        return self

    def set_stroke(self, color=None, width=None, opacity=None, **kwargs) -> "RayBundle":
        """
        Set stroke properties for all rays in the bundle.

        Parameters
        ----------
        color : str, optional
            Color of the rays
        width : float, optional
            Stroke width of the rays
        opacity : float, optional
            Opacity of the rays
        **kwargs
            Additional stroke properties

        Returns
        -------
        RayBundle
            Self (for chaining)
        """
        # Check if rays exist (they won't exist during __init__)
        if not hasattr(self, "rays"):
            return self

        for ray in self.rays:
            ray.set_stroke(color=color, width=width, opacity=opacity, **kwargs)
            if opacity is not None:
                ray.opacity = opacity
        return self

    def animate_propagation(
        self, run_time: float = 2.0, lag_ratio: float = 0.04, rate_func=linear
    ) -> AnimationGroup:
        """
        Animate all rays appearing with a fade-in effect.

        This animation preserves updaters and ensures rays have correct
        trajectories throughout the animation.

        Parameters
        ----------
        run_time : float
            Duration of the animation for each ray
        lag_ratio : float
            Delay between starting each ray's animation (0 = all together, 1 = sequential)
        rate_func : function
            Rate function for the animation

        Returns
        -------
        AnimationGroup
            Group of animations for all rays
        """
        # Force all rays to update their paths first
        for ray in self.rays:
            ray._update_ray_path(None)

        # Set all rays to invisible initially
        for ray in self.rays:
            ray.set_stroke(opacity=0)

        # Animate opacity to 1 for all rays
        return AnimationGroup(
            *[
                ray.animate(run_time=run_time, rate_func=rate_func).set_stroke(
                    opacity=1
                )
                for ray in self.rays
            ],
            lag_ratio=lag_ratio,
        )

    def animate_create(
        self, run_time: float = 2.0, lag_ratio: float = 0.04, rate_func=linear
    ) -> AnimationGroup:
        """Animate rays appearing from right to left (following propagation direction).

        Creates a 'wave' effect where rays appear to propagate through the system.
        All rays appear simultaneously but with a sequential reveal along their paths.

        Parameters
        ----------
        run_time : float
            Duration of the animation
        lag_ratio : float
            Delay between starting each ray's animation
        rate_func : function
            Rate function for the animation

        Returns
        -------
        AnimationGroup
            Group of Create animations for all rays

        Example
        -------
        >>> rays = RayBundle(...)
        >>> scene.play(rays.animate_create(run_time=2))
        """
        # Force all rays to update their paths first
        for ray in self.rays:
            ray._update_ray_path(None)

        # Store original opacities
        original_opacities = [ray.get_stroke_opacity() for ray in self.rays]

        # Set all rays to invisible
        for ray in self.rays:
            ray.set_stroke(opacity=0)

        # Use ray.animate() to preserve updaters
        return AnimationGroup(
            *[
                ray.animate(run_time=run_time, rate_func=rate_func).set_stroke(
                    opacity=original_opacities[i] if original_opacities[i] > 0 else 1
                )
                for i, ray in enumerate(self.rays)
            ],
            lag_ratio=lag_ratio,
        )

    def animate_fade_in(
        self, run_time: float = 1.0, lag_ratio: float = 0.0
    ) -> AnimationGroup:
        """Animate rays fading in with correct trajectories.

        Simple fade-in animation where all rays appear gradually.
        More subtle than animate_propagation.

        Parameters
        ----------
        run_time : float
            Duration of the fade-in
        lag_ratio : float
            Delay between starting each ray's fade (usually 0 for simultaneous)

        Returns
        -------
        AnimationGroup
            Group of FadeIn animations

        Example
        -------
        >>> rays = RayBundle(...)
        >>> scene.play(rays.animate_fade_in(run_time=1))
        """
        # Force all rays to update their paths first
        for ray in self.rays:
            ray._update_ray_path(None)

        # Store original opacities
        original_opacities = [ray.get_stroke_opacity() for ray in self.rays]

        # Set all rays to invisible
        for ray in self.rays:
            ray.set_stroke(opacity=0)

        # Use ray.animate() to preserve updaters
        return AnimationGroup(
            *[
                ray.animate(run_time=run_time).set_stroke(
                    opacity=original_opacities[i] if original_opacities[i] > 0 else 1
                )
                for i, ray in enumerate(self.rays)
            ],
            lag_ratio=lag_ratio,
        )

    def animate_uncreate(
        self, run_time: float = 1.0, lag_ratio: float = 0.0
    ) -> AnimationGroup:
        """Animate rays disappearing (reverse of animate_create).

        Parameters
        ----------
        run_time : float
            Duration of the animation
        lag_ratio : float
            Delay between starting each ray's animation

        Returns
        -------
        AnimationGroup
            Group of Uncreate animations

        Example
        -------
        >>> scene.play(rays.animate_uncreate(run_time=1))
        """
        return AnimationGroup(
            *[Uncreate(ray, run_time=run_time) for ray in self.rays],
            lag_ratio=lag_ratio,
        )

    def get_image_formation(
        self, optical_element_index: int = 0, **kwargs
    ) -> "ImageFormation":
        """
        Create an ImageFormation object to analyze and visualize image formation.

        This is a convenience method that creates an ImageFormation instance
        for this ray bundle.

        Parameters
        ----------
        optical_element_index : int
            Index of optical element after which to analyze
        **kwargs
            Additional arguments passed to ImageFormation

        Returns
        -------
        ImageFormation
            Object containing image analysis and visualization

        Example
        -------
        >>> bundle = RayBundle(...)
        >>> image = bundle.get_image_formation(optical_element_index=0)
        >>> scene.add(image)
        >>> # Image position updates automatically
        >>> print(image.get_image_position())
        """
        return ImageFormation(
            ray_bundle=self, optical_element_index=optical_element_index, **kwargs
        )

    def get_optical_elements_positions(
        self, index=None
    ) -> Union[List[np.ndarray], np.ndarray]:
        """
        Get the positions of the optical elements in the ray bundle.

        Parameters
        ----------
        index : int, optional
            If provided, returns the position of the optical element at this index.

        Returns
        -------
        List[np.ndarray] or np.ndarray
            List of positions of all optical elements, or position of specified element.
        """
        positions = []
        for element in self.optical_elements:
            # Use get_optical_plane_position() instead of get_center()
            # to get the correct position of the optical plane
            if hasattr(element, "get_optical_plane_position"):
                positions.append(element.get_optical_plane_position())
            else:
                positions.append(element.get_center())

        if index >= len(self.optical_elements):
            return None

        if index is not None:
            return positions[index]

        return positions


class PrincipalRays(VGroup):
    """
    The three principal rays for a thin lens:
    1. Parallel ray (passes through far focal point after lens)
    2. Central ray (passes through lens center unchanged)
    3. Focal ray (passes through near focal point, exits parallel)

    These rays are essential for geometric optics constructions.
    """

    def __init__(
        self,
        object_point: Union[NDArray[np.floating], Mobject],
        lens: "ThinLens",
        **kwargs,
    ):
        """
        Initialize the three principal rays from an object point through a lens.

        Parameters
        ----------
        object_point : np.ndarray or Mobject
            Point on the object (can be a Mobject to track dynamically)
        lens : ThinLens
            The lens to trace through
        """
        super().__init__()

        # Store references for dynamic updates
        self.object_point_source = object_point
        self.lens = lens

        # Ray 1: Parallel to optical axis → passes through far focal point
        parallel_ray = DynamicRay(
            start_point=object_point,
            direction=RIGHT,
            optical_elements=[lens],
            color=RED,
            **kwargs,
        )

        # Ray 2: Through lens center → continues straight
        # Direction needs to be calculated dynamically
        def center_direction():
            if isinstance(object_point, (VMobject, Mobject)):
                obj_pos = object_point.get_center()
            else:
                obj_pos = np.array(object_point)
            lens_center = lens.get_center()
            direction = lens_center - obj_pos
            return direction / np.linalg.norm(direction)

        center_ray = DynamicRay(
            start_point=object_point,
            direction=center_direction,
            optical_elements=[lens],
            color=GREEN,
            **kwargs,
        )

        # Ray 3: Through near focal point → exits parallel
        # Direction needs to be calculated dynamically
        def focal_direction():
            if isinstance(object_point, (VMobject, Mobject)):
                obj_pos = object_point.get_center()
            else:
                obj_pos = np.array(object_point)
            lens_center = lens.get_center()

            if lens.focal_length > 0:
                focal_point = lens_center + LEFT * lens.focal_length
            else:
                focal_point = lens_center + RIGHT * abs(lens.focal_length)

            direction = focal_point - obj_pos
            return direction / np.linalg.norm(direction)

        focal_ray = DynamicRay(
            start_point=object_point,
            direction=focal_direction,
            optical_elements=[lens],
            color=BLUE,
            **kwargs,
        )

        self.parallel_ray = parallel_ray
        self.center_ray = center_ray
        self.focal_ray = focal_ray

        self.add(parallel_ray, center_ray, focal_ray)


def create_parallel_bundle(
    num_rays: int = 5,
    spacing: float = 0.5,
    start_x: float = -5.0,
    direction: NDArray[np.floating] = RIGHT,
    optical_elements: Optional[List[OpticalElement]] = None,
    **ray_kwargs,
) -> RayBundle:
    """
    Helper function to create a bundle of evenly-spaced parallel rays.

    Parameters
    ----------
    num_rays : int
        Number of rays in the bundle
    spacing : float
        Vertical spacing between rays
    start_x : float
        X-coordinate where rays start
    direction : np.ndarray
        Direction of all rays
    optical_elements : List[OpticalElement]
        Optical elements to interact with
    **ray_kwargs
        Additional arguments for DynamicRay

    Returns
    -------
    RayBundle
        A bundle of parallel rays
    """
    start_points = []
    for i in range(num_rays):
        y = (i - (num_rays - 1) / 2) * spacing
        start_points.append(np.array([start_x, y, 0]))

    return RayBundle(
        start_points=start_points,
        direction_vector=direction,
        optical_elements=optical_elements,
        **ray_kwargs,
    )


def create_diverging_bundle(
    source_point: Union[NDArray[np.floating], Mobject],
    angle_range_deg: Tuple[float, float] = (-30, 30),
    num_rays: int = 5,
    optical_elements: Optional[List[OpticalElement]] = None,
    **ray_kwargs,
) -> RayBundle:
    """
    Helper function to create rays diverging from a point.

    Parameters
    ----------
    source_point : np.ndarray or Mobject
        Point from which all rays emanate
    angle_range_deg : tuple
        (min_angle, max_angle) in degrees
    num_rays : int
        Number of rays
    optical_elements : List[OpticalElement]
        Optical elements to interact with
    **ray_kwargs
        Additional arguments for DynamicRay

    Returns
    -------
    RayBundle
        A bundle of diverging rays
    """
    angles = np.linspace(angle_range_deg[0], angle_range_deg[1], num_rays)

    return RayBundle(
        start_points=source_point,
        direction_angle_deg=list(angles),
        optical_elements=optical_elements,
        **ray_kwargs,
    )


class RayExtension(VMobject):
    """
    Extension of a ray shown as a dashed line.

    Useful for showing virtual images or where rays would continue
    between optical elements.
    """

    def __init__(
        self,
        ray: DynamicRay,
        element_idx: NDArray[np.floating] = None,
        ray_bundle: RayBundle = None,
        image_pos: ValueTracker = None,
        color: Optional[str] = None,
        overshoot: float = 1.1,
        **kwargs,
    ):
        """
        Initialize a ray extension.

        Parameters
        ----------
        ray : DynamicRay
            The ray to extend
        extension_length : float
            How far to extend the ray
        segment_index : int
            Which segment of the ray to extend (-1 for last segment)
        direction : str
            "forward" to extend in ray direction, "backward" to extend opposite, "auto"
            to extend the ray after the element to the image position (any direction)
        color : str
            Color of the extension (defaults to ray color with reduced opacity)
        """
        super().__init__(**kwargs)
        self.ray = ray
        self.element_idx = element_idx
        self.ray_bundle = ray_bundle
        self.image_pos = image_pos
        self.overshoot = overshoot

        # Visual properties
        if color is None:
            color = ray.get_color()
        self.set_stroke(color=color, width=ray.get_stroke_width() * 0.7)
        self.set_stroke(opacity=0.7)
        self.set_style(stroke_opacity=0.8)
        self.set_opacity(0)

        # Calculate initial extension
        self._update_extension(None)

        # Add updater
        self.add_updater(self._update_extension)

    def _is_virtual_image(
        self,
        element_pos: np.ndarray,
        next_element_pos: Optional[np.ndarray],
        image_pos: float,
        is_mirror: bool,
    ) -> bool:
        """
        Determine if the image is virtual (requires extension visualization).

        Critères:
        - Pour une lentille (transmission):
          * Image virtuelle si image est AVANT la lentille (image_pos < element_pos)
          * Image réelle si image est APRÈS la lentille

        - Pour un miroir (réflexion):
          * Image virtuelle si image est DERRIÈRE le miroir (image_pos > element_pos)
          * Image réelle si image est DEVANT le miroir (image_pos < element_pos)

        - Si l'image est entre deux éléments optiques:
          * Image réelle (pas d'extension nécessaire)

        Parameters
        ----------
        element_pos : np.ndarray
            Position of the current optical element
        next_element_pos : Optional[np.ndarray]
            Position of the next optical element (None if last)
        image_pos : float
            X-position of the image
        is_mirror : bool
            Whether the element is a mirror

        Returns
        -------
        bool
            True if image is virtual (show extensions), False if real (no extensions)
        """
        # Cas 1: Image entre deux éléments optiques → image réelle
        if next_element_pos is not None:
            if element_pos[0] < image_pos < next_element_pos[0]:
                # Image entre les deux éléments → réelle
                return False
            elif element_pos[0] > image_pos > next_element_pos[0]:
                # Image entre les deux éléments (ordre inverse) → réelle
                return False

        # Cas 2: Dernier élément ou image hors de l'intervalle
        if is_mirror:
            # Pour un miroir:
            # - Image réelle si DEVANT le miroir (du côté incident)
            # - Image virtuelle si DERRIÈRE le miroir
            # En convention: rayons viennent de la gauche, miroir réfléchit vers la gauche
            # Image réelle: x < element_x (devant)
            # Image virtuelle: x > element_x (derrière)
            return image_pos > element_pos[0]
        else:
            # Pour une lentille (transmission):
            # - Image réelle si APRÈS la lentille (rayons passent réellement)
            # - Image virtuelle si AVANT la lentille
            return image_pos < element_pos[0]

    def _update_extension(self, mobject: Optional[Mobject], dt: float = 0) -> None:
        """Update the extension line based on ray position."""

        element_pos = self.ray_bundle.get_optical_elements_positions(
            index=self.element_idx
        )
        next_element_pos = self.ray_bundle.get_optical_elements_positions(
            index=self.element_idx + 1
        )
        is_last_element = next_element_pos is None

        # Get the optical element to check if it's a mirror
        if self.ray_bundle.optical_elements and 0 <= self.element_idx < len(
            self.ray_bundle.optical_elements
        ):
            element = self.ray_bundle.optical_elements[self.element_idx]
            is_mirror = element.is_mirror()
        else:
            is_mirror = False

        # Determine if image is virtual using the new robust method
        image_pos_value = self.image_pos.get_value()
        is_virtual = self._is_virtual_image(
            element_pos, next_element_pos, image_pos_value, is_mirror
        )

        if not is_virtual:
            # Image réelle → pas d'extension
            self.set_opacity(0)
            self.direction = "none"
            self.extension_length = 0
            self.become(VectorizedPoint())
            return

        # Image virtuelle → afficher l'extension
        self.set_opacity(1)

        # Déterminer la direction de l'extension
        if is_mirror:
            # Pour miroir avec image virtuelle (derrière le miroir)
            self.direction = (
                "forward"  # Extension vers l'arrière (vers l'image derrière)
            )
            self.extension_length = abs(image_pos_value - element_pos[0])
        else:
            # Pour lentille avec image virtuelle (avant la lentille)
            self.direction = "backward"  # Extension vers l'arrière (vers l'image avant)
            self.extension_length = abs(image_pos_value - element_pos[0])

        # Get ray points
        ray_points = self.ray.get_points()

        if len(ray_points) < 2:
            self.become(VectorizedPoint())
            return

        # Get the segment to extend
        num_points = len(ray_points)
        if self.element_idx == -1:
            # Last segment
            start_point = ray_points[-2] if num_points >= 2 else ray_points[0]
            end_point = ray_points[-1]
        else:
            # Specific segment
            idx = self.ray.get_vertex_index_from_pos(element_pos)
            if idx is None:
                self.become(VectorizedPoint())
                return

            # For mirrors with virtual images behind (direction="forward" and is_last_element),
            # we need to extend toward the virtual image position, not just extend the incident ray
            if self.direction == "forward" and is_last_element:
                # For virtual image: draw line from mirror toward the focal point
                # Find the intersection point on the mirror
                mirror_x = element_pos[0]

                # The intersection point is at idx (or close to it)
                # Find the point at the mirror
                intersection_point = ray_points[idx]

                # Calculate the focal point where all rays converge
                # This gives us the full 3D position including y coordinate
                focal_point = find_focal_point_from_rays(
                    self.ray_bundle, element_index=self.element_idx
                )

                if focal_point is None:
                    self.become(VectorizedPoint())
                    return

                start_point = intersection_point
                end_point = focal_point
            else:
                # Normal case: use the segment after the element
                start_point, end_point = ray_points[idx], ray_points[idx + 1]

        # Calculate direction
        segment_dir = end_point - start_point
        if np.linalg.norm(segment_dir) < 1e-10:
            self.become(VectorizedPoint())
            return

        segment_dir = segment_dir / np.linalg.norm(segment_dir)

        if self.direction == "forward":
            # For virtual images behind mirrors: we already have start and end points
            # pointing toward the image. Just extend slightly beyond.
            if is_last_element:
                # Extend from mirror to beyond the image
                extension_start = start_point
                extension_end = end_point  # Already at image position
            else:
                # Normal forward: extend from end_point in the direction of the segment
                extension_start = end_point
                extension_end = (
                    end_point + segment_dir * self.extension_length * self.overshoot
                )
        elif self.direction == "backward":
            # Extend backward from start_point
            extension_start = (
                start_point - segment_dir * self.extension_length * self.overshoot
            )
            extension_end = start_point
        else:
            # No extension
            self.become(VectorizedPoint())
            return

        # Create dashed line
        if self.get_stroke_opacity() > 0:
            dashed = DashedLine(
                extension_start,
                extension_end,
                dash_length=0.1,
                stroke_width=self.ray.get_stroke_width(),
                color=self.ray.get_color(),
                stroke_opacity=0.7,
            )
            self.become(dashed)
        else:
            self.become(VectorizedPoint())


def find_ray_intersection(
    ray1: DynamicRay,
    ray2: DynamicRay,
    segment1: int = -1,
    segment2: int = -1,
    max_distance: float = 100.0,
) -> Optional[NDArray[np.floating]]:
    """
    Find the intersection point of two rays.

    This calculates where two ray segments would intersect if extended.
    Useful for finding image positions.

    Parameters
    ----------
    ray1, ray2 : DynamicRay
        The two rays to intersect
    segment1, segment2 : int
        Which segments to use (-1 for last segment)
    max_distance : float
        Maximum distance to search for intersection

    Returns
    -------
    np.ndarray or None
        Intersection point, or None if rays are parallel
    """
    # Get points from rays
    points1 = ray1.get_points()
    points2 = ray2.get_points()

    if len(points1) < 2 or len(points2) < 2:
        return None

    # Get segment points
    if segment1 == -1:
        p1_start, p1_end = points1[-2], points1[-1]
    else:
        idx = min(segment1, len(points1) - 2)
        p1_start, p1_end = points1[idx], points1[idx + 1]

    if segment2 == -1:
        p2_start, p2_end = points2[-2], points2[-1]
    else:
        idx = min(segment2, len(points2) - 2)
        p2_start, p2_end = points2[idx], points2[idx + 1]

    # Calculate directions
    d1 = p1_end - p1_start
    d2 = p2_end - p2_start

    # Normalize
    d1_norm = np.linalg.norm(d1)
    d2_norm = np.linalg.norm(d2)

    if d1_norm < 1e-10 or d2_norm < 1e-10:
        return None

    d1 = d1 / d1_norm
    d2 = d2 / d2_norm

    # Line intersection in 2D (ignore z)
    # Ray 1: P1 = p1_end + t1 * d1
    # Ray 2: P2 = p2_end + t2 * d2
    # Solve: p1_end + t1 * d1 = p2_end + t2 * d2

    # In 2D: [d1.x  -d2.x] [t1] = [p2_end.x - p1_end.x]
    #        [d1.y  -d2.y] [t2]   [p2_end.y - p1_end.y]

    det = d1[0] * (-d2[1]) - d1[1] * (-d2[0])

    if abs(det) < 1e-10:
        # Rays are parallel
        return None

    diff = p2_end - p1_end
    t1 = (diff[0] * (-d2[1]) - diff[1] * (-d2[0])) / det

    # Check if intersection is within reasonable distance
    if abs(t1) > max_distance:
        return None

    # Calculate intersection point
    intersection = p1_end + t1 * d1

    return intersection


# ImageMarker a supprimer
class ImageMarker(VGroup):
    """
    A dynamic arrow that marks the image position formed by ray intersection.

    The arrow starts from the optical axis and points to the image position.
    Automatically updates position when rays move.
    """

    def __init__(
        self,
        ray1: DynamicRay,
        ray2: DynamicRay,
        segment1: int = -1,
        segment2: int = -1,
        optical_axis_y: float = 0.0,
        color: str = GREEN,
        show_label: bool = True,
        **kwargs,
    ):
        """
        Initialize an image marker.

        Parameters
        ----------
        ray1, ray2 : DynamicRay
            The rays whose intersection defines the image
        segment1, segment2 : int
            Which segments to use for intersection
        optical_axis_y : float
            Y-coordinate of the optical axis (where arrow starts)
        color : str
            Color of the image marker
        show_label : bool
            Whether to show the "Image" label
        """
        super().__init__(**kwargs)

        self.ray1 = ray1
        self.ray2 = ray2
        self.segment1 = segment1
        self.segment2 = segment2
        self.optical_axis_y = optical_axis_y
        self.marker_color = color
        self.show_label = show_label

        # Create arrow (will be updated)
        self.arrow = Arrow(start=ORIGIN, end=UP, buff=0, color=color, stroke_width=3)
        self.add(self.arrow)

        # Label
        if show_label:
            self.label = Text("Image", font_size=16, color=color)
            self.add(self.label)
        else:
            self.label = None

        # Update initial position
        self._update_position(None)

        # Add updater
        self.add_updater(self._update_position)

    def _update_position(self, mobject: Optional[Mobject], dt: float = 0) -> None:
        """Update marker position based on ray intersection."""
        intersection = find_ray_intersection(
            self.ray1, self.ray2, self.segment1, self.segment2
        )

        if intersection is not None:
            # Arrow starts from optical axis at the x-position of the image
            start_point = np.array([intersection[0], self.optical_axis_y, 0])
            end_point = intersection

            # Only show arrow if there's a height difference
            height = abs(end_point[1] - start_point[1])
            if height > 0.05:  # Minimum height threshold
                self.arrow.put_start_and_end_on(start_point, end_point)

                # Position label at the tip
                if self.label is not None:
                    if end_point[1] > start_point[1]:
                        self.label.next_to(self.arrow, UP, buff=0.1)
                    else:
                        self.label.next_to(self.arrow, DOWN, buff=0.1)

                self.set_opacity(1)
            else:
                # Image is on the optical axis - hide arrow
                self.set_opacity(0)
        else:
            # Hide if no intersection
            self.set_opacity(0)


def find_focal_point_from_rays(
    ray_bundle: RayBundle, element_index: int = -1
) -> Optional[NDArray[np.floating]]:
    """
    Find the focal point from multiple rays using least squares optimization.

    For ideal systems (2 rays), returns exact intersection.
    For non-ideal systems (N rays), finds the point minimizing distance to all rays.

    Parameters
    ----------
    rays : List[DynamicRay]
        List of rays to analyze
    segment_index : int
        Which segment to analyze (-1 for last segment)

    Returns
    -------
    np.ndarray or None
        Focal point position, or None if calculation fails
    """

    rays: List[DynamicRay] = ray_bundle.rays

    # optical_element_position = (
    #     ray_bundle.optical_elements[element_index].get_center()
    #     if ray_bundle.optical_elements
    #     else None
    # )

    optical_element_position = ray_bundle.get_optical_elements_positions(
        index=element_index
    )

    if optical_element_position is None:
        # Filter rays that have passed the optical element
        return None

    if len(rays) < 2:
        return None

    # Exact solution for 2 rays
    if len(rays) == 2:
        return find_ray_intersection(rays[0], rays[1], element_index, element_index)

    # Least squares for N rays
    # We find point P that minimizes sum of squared distances to all ray lines
    # Distance from point P to line (origin O, direction D): ||P - O - ((P-O)·D)D||

    ray_origins = []
    ray_directions = []

    for ray in rays:
        points = ray.get_points()
        if len(points) < 2:
            continue

        # Get segment
        if element_index == -1:
            p_start, p_end = points[-2], points[-1]
        else:
            idx = ray.get_vertex_index_from_pos(optical_element_position)
            if idx is None:
                # Ray doesn't intersect this element, skip it
                continue
            p_start, p_end = points[idx], points[idx + 1]

        direction = p_end - p_start
        direction_norm = np.linalg.norm(direction)
        if direction_norm < 1e-10:
            continue

        direction = direction / direction_norm
        ray_origins.append(p_end[:2])  # 2D only
        ray_directions.append(direction[:2])

    if len(ray_origins) < 2:
        return None

    # Solve least squares: minimize sum_i ||P - O_i - ((P-O_i)·D_i)D_i||^2
    # This reduces to solving a 2x2 linear system
    A = np.zeros((2, 2))
    b = np.zeros(2)

    for origin, direction in zip(ray_origins, ray_directions):
        # Contribution to normal equations
        I_minus_DDT = np.eye(2) - np.outer(direction, direction)
        A += I_minus_DDT
        b += I_minus_DDT @ origin

    try:
        focal_point_2d = np.linalg.solve(A, b)
        return np.array([focal_point_2d[0], focal_point_2d[1], 0])
    except np.linalg.LinAlgError:
        # Singular matrix - rays are parallel
        return None


class ImageFormation(VGroup):
    """
    Analyzes and visualizes image formation from a RayBundle.

    Automatically calculates the focal point where rays converge (or are closest)
    after propagating through an optical element. Provides visual components:
    - Extended rays (dashed lines)
    - Focal point marker
    - Image arrow from optical axis to focal point

    All components update automatically when the bundle changes.

    Attributes
    ----------
    focal_point_dot : Dot
        Marker at the calculated focal point
    image_arrow : Arrow
        Arrow from optical axis to image position
    extended_rays : VGroup
        Dashed ray extensions for visualization
    """

    def __init__(
        self,
        ray_bundle: RayBundle,
        optical_element_index: int = 0,
        extension_length: float = 5.0,
        show_extensions: bool = True,
        show_focal_point: bool = False,
        show_image_arrow: bool = True,
        optical_axis_y: float = 0.0,
        focal_point_color: str = BLUE,
        image_arrow_color: str = BLUE,
        extension_color: Optional[str] = None,
        **kwargs,
    ):
        """
        Initialize image formation analysis.

        Parameters
        ----------
        ray_bundle : RayBundle
            Bundle of rays to analyze
        optical_element_index : int
            Index of optical element after which to analyze (0 = after first element)
            Use -1 for the final segment of all rays
        extension_length : float
            Length of ray extensions
        show_extensions : bool
            Whether to show dashed ray extensions
        show_focal_point : bool
            Whether to show focal point marker
        show_image_arrow : bool
            Whether to show arrow from optical axis to image
        optical_axis_y : float
            Y-coordinate of optical axis
        focal_point_color : str
            Color of focal point marker
        image_arrow_color : str
            Color of image arrow
        extension_color : str
            Color of extensions (None = use ray colors)
        """
        super().__init__(**kwargs)

        self.ray_bundle = ray_bundle
        self.optical_element_index = optical_element_index
        self.extension_length = extension_length
        self.optical_axis_y = optical_axis_y
        self._show_extensions = show_extensions
        self._show_focal_point = show_focal_point
        self._show_image_arrow = show_image_arrow

        self.x_pos_image = ValueTracker(0)

        # Create visual components
        self.extended_rays = VGroup()

        if show_extensions:
            for ray in ray_bundle.rays:
                ext = RayExtension(
                    ray=ray,
                    element_idx=optical_element_index,
                    ray_bundle=ray_bundle,
                    image_pos=self.x_pos_image,
                    color=extension_color,
                )
                self.extended_rays.add(ext)
            self.add(self.extended_rays)

        # Focal point marker
        self.focal_point_dot = Dot(color=focal_point_color, radius=0.08)
        if show_focal_point:
            self.add(self.focal_point_dot)

        # Image arrow
        self.image_arrow = Arrow(
            start=ORIGIN,
            end=UP,
            buff=0,
            color=image_arrow_color,
            stroke_width=3,
        )
        if show_image_arrow:
            self.add(self.image_arrow)

        # Initial update
        self._update_image_position(None)

        # Add updater
        self.add_updater(self._update_image_position)

    def _update_image_position(self, mobject: Optional[Mobject], dt: float = 0) -> None:
        """Update focal point and visualization based on current ray positions."""
        # Calculate focal point
        focal_point = find_focal_point_from_rays(
            self.ray_bundle, element_index=self.optical_element_index
        )

        if focal_point is not None:
            self.x_pos_image.set_value(focal_point[0])

            # Update focal point marker
            if self._show_focal_point:
                self.focal_point_dot.move_to(focal_point)
                self.focal_point_dot.set_opacity(1)

            # Update image arrow
            if self._show_image_arrow:
                axis_point = np.array([focal_point[0], self.optical_axis_y, 0])
                height = abs(focal_point[1] - self.optical_axis_y)

                if height > 0.05:  # Minimum threshold
                    self.image_arrow.put_start_and_end_on(axis_point, focal_point)
                    self.image_arrow.set_opacity(1)
                else:
                    self.image_arrow.set_opacity(0)
        else:
            # Hide if no focal point found
            if self._show_focal_point:
                self.focal_point_dot.set_opacity(0)
            if self._show_image_arrow:
                self.image_arrow.set_opacity(0)

    def get_image_position(self) -> Optional[NDArray[np.floating]]:
        """Get the current calculated image position."""
        return find_focal_point_from_rays(
            self.ray_bundle, element_index=self.optical_element_index
        )
