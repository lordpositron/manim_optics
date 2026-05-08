manim_optics.centered_system
============================

.. py:module:: manim_optics.centered_system

.. autoapi-nested-parse::

   CenteredSystem - Optical centered system with principal planes
   ================================================================

   This module provides the CenteredSystem class for modeling complex optical systems
   using principal planes (H, H') and nodal points (N, N').



Classes
-------

.. autoapisummary::

   manim_optics.centered_system.CenteredSystem


Module Contents
---------------

.. py:class:: CenteredSystem(h_position: float = -1.0, h_prime_position: float = 1.0, focal_length: float = 2.0, height: float = 3.0, left_boundary_position: float = None, left_boundary_height: float = None, right_boundary_position: float = None, right_boundary_height: float = None, boundary_curvature: float = 0.7, refractive_index_before: float = 1.0, refractive_index_after: float = 1.0, h_color=WHITE, h_stroke_width: float = 3, h_dash_length: float = 0.1, boundary_color=BLUE_D, boundary_stroke_width: float = 3, show_labels: bool = True, show_focal_points: bool = True, focal_point_color=YELLOW, label_color=WHITE, **kwargs)

   Bases: :py:obj:`manim_optics.base.OpticalElement`


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


   .. py:attribute:: h_position_tracker


   .. py:attribute:: h_prime_position_tracker


   .. py:attribute:: focal_length_tracker


   .. py:attribute:: h_position
      :value: -1.0



   .. py:attribute:: h_prime_position
      :value: 1.0



   .. py:attribute:: focal_length
      :value: 2.0



   .. py:attribute:: system_height
      :value: 3.0



   .. py:attribute:: left_boundary_position


   .. py:attribute:: left_boundary_height


   .. py:attribute:: right_boundary_position


   .. py:attribute:: right_boundary_height


   .. py:attribute:: h_color


   .. py:attribute:: h_stroke_width
      :value: 3



   .. py:attribute:: h_dash_length
      :value: 0.1



   .. py:attribute:: boundary_color


   .. py:attribute:: boundary_stroke_width
      :value: 3



   .. py:attribute:: show_labels
      :value: True



   .. py:attribute:: show_focal_points
      :value: True



   .. py:attribute:: focal_point_color


   .. py:attribute:: label_color


   .. py:attribute:: boundary_curvature
      :value: 0.7



   .. py:method:: get_optical_plane_position() -> numpy.ndarray

      Get position of the optical center (midpoint between H and H').

      :returns: Position of the optical center
      :rtype: np.ndarray



   .. py:method:: compute_image_position(object_position: numpy.ndarray) -> numpy.ndarray

      Compute the image position for a given object position.

      Uses the current system parameters (H, H', focal length) and
      a paraxial thin-lens relation with principal planes.

      :param object_position: Object position in scene coordinates.
      :type object_position: np.ndarray

      :returns: Image position in scene coordinates.
      :rtype: np.ndarray



   .. py:method:: intersect(ray_start: numpy.ndarray, ray_direction: numpy.ndarray) -> tuple

      Calculate intersection with principal plane H only.

      The CenteredSystem interacts ONLY with H (the object-side principal plane).
      H' is purely a teleportation target. The traversed_systems memory in rays.py
      ensures the system is only traversed once.

      :param ray_start: Starting position of the ray
      :type ray_start: np.ndarray
      :param ray_direction: Direction vector of the ray
      :type ray_direction: np.ndarray

      :returns: (intersection_point, has_intersection) where ``intersection_point`` is
                the hit point on H.
      :rtype: tuple



   .. py:method:: propagate_ray(ray_start: numpy.ndarray, ray_direction: numpy.ndarray, intersection_point: numpy.ndarray) -> tuple

      Propagate ray through principal planes H → H'.

      The ray has hit H (from intersect). We calculate the deflection using
      paraxial optics and teleport to H' at the same height. The ray then
      exits the system from H'.

      :param ray_start: Starting position of the ray
      :type ray_start: np.ndarray
      :param ray_direction: Direction vector of the ray
      :type ray_direction: np.ndarray
      :param intersection_point: Point at H (from intersect)
      :type intersection_point: np.ndarray

      :returns: (new_direction, continues, teleport_point)
                - new_direction: direction after system (from H')
                - continues: True (ray continues)
                - teleport_point: point at H' where the outgoing ray starts (same height as H)
      :rtype: tuple



   .. py:method:: should_hide_segment(point1: numpy.ndarray, point2: numpy.ndarray) -> bool

      Check if a ray segment should be hidden (between H and H').

      A segment crossing through the system (from before H to H') should be split:
      the part going to H is visible, the part from H to H' should be hidden.

      :param point1: Start point of segment
      :type point1: np.ndarray
      :param point2: End point of segment
      :type point2: np.ndarray

      :returns: True if segment should be hidden
      :rtype: bool



   .. py:method:: split_segment_at_boundaries(point1: numpy.ndarray, point2: numpy.ndarray) -> list

      Split a segment that crosses through the system into visible/invisible parts.

      Uses real arc intersection instead of simple x-position checks.

      Returns a list of tuples (p1, p2, visible, dashed) where:
      - visible is a boolean (True = show, False = hide)
      - dashed is a boolean (True = dashed style, False = solid style)

      :param point1: Start point of segment
      :type point1: np.ndarray
      :param point2: End point of segment
      :type point2: np.ndarray

      :returns: [(start, end, visible, dashed), ...] segments
      :rtype: list of tuples



   .. py:method:: get_transfer_matrix() -> numpy.ndarray

      Get ABCD transfer matrix for the centered system.

      For principal planes separated by distance d with focal length f:
      The system acts like a thin lens with modifications for separation.

      :returns: 2x2 ABCD matrix
      :rtype: np.ndarray



   .. py:method:: is_ray_inside_system(point: numpy.ndarray, ray_direction: numpy.ndarray) -> bool

      Check if a point is inside the optical system (between boundaries).

      A ray is inside if it's between the left and right boundaries.

      :param point: Point to check
      :type point: np.ndarray
      :param ray_direction: Direction of ray (for determining if entering or exiting)
      :type ray_direction: np.ndarray

      :returns: True if point is inside the system
      :rtype: bool



   .. py:method:: set_plane_style(color=None, stroke_width=None, dash_length=None)

      Update the style of principal planes H and H'.

      :param color: New color for planes
      :type color: color, optional
      :param stroke_width: New stroke width
      :type stroke_width: float, optional
      :param dash_length: New dash length
      :type dash_length: float, optional

      :returns: Self (for chaining)
      :rtype: CenteredSystem



   .. py:method:: toggle_labels(show: bool = None)

      Show or hide H and H' labels.

      :param show: If None, toggles current state. Otherwise sets to show/hide.
      :type show: bool, optional

      :returns: Self (for chaining)
      :rtype: CenteredSystem



   .. py:method:: toggle_focal_points(show: bool = None)

      Show or hide focal points F and F'.

      :param show: If None, toggles current state. Otherwise sets to show/hide.
      :type show: bool, optional

      :returns: Self (for chaining)
      :rtype: CenteredSystem



   .. py:method:: create_animation(run_time: float = 1.5) -> manim.AnimationGroup

      Create an elegant appearance animation for the system.

      Sequence:
      1. Boundaries grow from center
      2. Principal planes fade in
      3. Labels and focal points appear

      :param run_time: Duration of the animation
      :type run_time: float

      :returns: Appearance animation
      :rtype: AnimationGroup



   .. py:method:: fade_out_animation(run_time: float = 1.0) -> manim.AnimationGroup

      Create an elegant disappearance animation for the system.

      :param run_time: Duration of the animation
      :type run_time: float

      :returns: Disappearance animation
      :rtype: AnimationGroup



   .. py:method:: shift(*vectors)

      Shift the system while keeping trackers and visuals in sync.

      This updates the H/H' trackers (x-shift) and moves the visual offset (y/z).



   .. py:method:: interpolate(mobject1, mobject2, alpha, *args, **kwargs)

      Interpolate state during animations to keep trackers synchronized.

      This ensures rays update continuously when using obj.animate.shift(...).



   .. py:method:: animate_h_position(new_h_position: float, run_time: float = 1.0)

      Animate H by driving its ValueTracker (updater remains active).



   .. py:method:: animate_h_prime_position(new_h_prime_position: float, run_time: float = 1.0)

      Animate H' by driving its ValueTracker (updater remains active).



   .. py:method:: animate_focal_length(new_focal_length: float, run_time: float = 1.0)

      Animate focal length via its ValueTracker (updater remains active).



   .. py:method:: animate_system_position(new_h: float, new_h_prime: float, run_time: float = 1.0)

      Animate H and H' together via their trackers (updater remains active).



   .. py:method:: set_h_position(h_position: float)

      Set H position immediately without animation.



   .. py:method:: set_h_prime_position(h_prime_position: float)

      Set H' position immediately without animation.



   .. py:method:: set_focal_length(focal_length: float)

      Set focal length immediately without animation.



