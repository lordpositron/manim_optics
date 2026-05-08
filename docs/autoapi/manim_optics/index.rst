manim_optics
============

.. py:module:: manim_optics

.. autoapi-nested-parse::

   Manim Optics - Dynamic optical ray tracing for Manim
   =====================================================

   A package for creating dynamic optical simulations with automatic ray updates.

   Features:
   - Thin lenses (converging and diverging)
   - Plane mirrors
   - Dynamic ray tracing with automatic updates
   - Paraxial optics calculations

   Author: Corentin Nannini



Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/manim_optics/base/index
   /autoapi/manim_optics/beam_stops/index
   /autoapi/manim_optics/centered_system/index
   /autoapi/manim_optics/eye/index
   /autoapi/manim_optics/lenses/index
   /autoapi/manim_optics/mirrors/index
   /autoapi/manim_optics/miscellaneous/index
   /autoapi/manim_optics/optics_3d/index
   /autoapi/manim_optics/rays/index
   /autoapi/manim_optics/scene_utils/index


Classes
-------

.. autoapisummary::

   manim_optics.OpticalElement
   manim_optics.ArcBeamStop
   manim_optics.BeamStop
   manim_optics.CircularAperture
   manim_optics.LineBeamStop
   manim_optics.CenteredSystem
   manim_optics.Eye
   manim_optics.ConvergingLens
   manim_optics.DivergingLens
   manim_optics.ThinLens
   manim_optics.Mirror
   manim_optics.PlaneMirror
   manim_optics.SphericalMirror
   manim_optics.CrossGraticule
   manim_optics.Graticule
   manim_optics.GridGraticule
   manim_optics.LinearGraticule
   manim_optics.OpticalElement3D
   manim_optics.RayBundle3D
   manim_optics.ThinLens3D
   manim_optics.DynamicRay
   manim_optics.ImageFormation
   manim_optics.ImageMarker
   manim_optics.PrincipalRays
   manim_optics.RayBundle
   manim_optics.RayExtension
   manim_optics.OpticalScene


Functions
---------

.. autoapisummary::

   manim_optics.rotate_vector_2d
   manim_optics.create_diverging_bundle
   manim_optics.create_parallel_bundle
   manim_optics.find_focal_point_from_rays
   manim_optics.find_ray_intersection
   manim_optics.calculate_image_position
   manim_optics.create_image_arrow
   manim_optics.create_object_arrow


Package Contents
----------------

.. py:class:: OpticalElement(refractive_index_before: float = 1.0, refractive_index_after: float = 1.0, **kwargs)

   Bases: :py:obj:`manim.VGroup`, :py:obj:`abc.ABC`


   Abstract base class for all optical elements.

   This class provides the interface that all optical elements must implement
   to work with the dynamic ray tracing system.

   Future extensions can inherit from this class to add:
   - Thick lenses
   - Curved mirrors
   - Prisms
   - Complex optical systems


   .. py:attribute:: n_before
      :value: 1.0



   .. py:attribute:: n_after
      :value: 1.0



   .. py:method:: intersect(ray_start: numpy.ndarray, ray_direction: numpy.ndarray) -> tuple
      :abstractmethod:


      Calculate intersection point(s) of a ray with this optical element.

      :param ray_start: Starting point of the ray
      :type ray_start: np.ndarray
      :param ray_direction: Direction vector of the ray (normalized)
      :type ray_direction: np.ndarray

      :returns: (intersection_point, has_intersection)
                - intersection_point: np.ndarray or None
                - has_intersection: bool
      :rtype: tuple



   .. py:method:: propagate_ray(ray_start: numpy.ndarray, ray_direction: numpy.ndarray, intersection_point: numpy.ndarray) -> tuple
      :abstractmethod:


      Calculate the new ray direction after interaction with this element.

      :param ray_start: Starting point of the incoming ray
      :type ray_start: np.ndarray
      :param ray_direction: Direction of the incoming ray
      :type ray_direction: np.ndarray
      :param intersection_point: Point where the ray intersects this element
      :type intersection_point: np.ndarray

      :returns: (new_direction, continues)
                - new_direction: np.ndarray (normalized direction vector)
                - continues: bool (whether the ray continues or is absorbed)
      :rtype: tuple



   .. py:method:: get_normal_at(point: numpy.ndarray) -> numpy.ndarray

      Get the normal vector at a given point on the optical element.

      :param point: Point on the surface of the element
      :type point: np.ndarray

      :returns: Normal vector at the point (normalized)
      :rtype: np.ndarray



   .. py:method:: get_center() -> numpy.ndarray

      Get the center position of the optical element.



   .. py:method:: get_optical_plane_position() -> numpy.ndarray

      Get the position of the optical plane (where rays interact).

      For most elements, this is the same as get_center().
      Override this in subclasses if the optical plane differs from the VGroup center.

      :returns: Position of the optical plane
      :rtype: np.ndarray



   .. py:method:: is_mirror() -> bool

      Check if this optical element is a mirror (reflects rays).

      :returns: True if this is a mirror, False otherwise
      :rtype: bool



   .. py:method:: create(run_time: float = 1.0) -> manim.Animation

      Create an animation for the appearance of this optical element.

      :param run_time: Duration of the animation
      :type run_time: float

      :returns: Animation object to be played
      :rtype: Animation



   .. py:method:: get_transfer_matrix() -> numpy.ndarray
      :abstractmethod:


      Get the ABCD transfer matrix for this optical element.

      The transfer matrix relates input ray state [y, θ] to output state:
      [y_out]   [A B] [y_in]
      [θ_out] = [C D] [θ_in]

      :returns: 2x2 transfer matrix
      :rtype: np.ndarray



.. py:function:: rotate_vector_2d(vector: numpy.ndarray, angle: float) -> numpy.ndarray

   Rotate a 2D vector by an angle around the z-axis.

   :param vector: The vector to rotate (3D, but rotation is in xy-plane)
   :type vector: np.ndarray
   :param angle: Angle in radians
   :type angle: float

   :returns: Rotated vector
   :rtype: np.ndarray


.. py:class:: ArcBeamStop(radius: float = 2.0, arc_angle: float = 120 * DEGREES, stroke_color=RED_D, stroke_width: float = 4, fill_color=None, fill_opacity: float = 0.0, **kwargs)

   Bases: :py:obj:`BeamStop`


   Arc (portion of circle) that stops rays - useful for modeling curved screens/retina.

   The arc is centered at a point and has a radius of curvature.
   Rays hitting the arc are stopped (absorbed).

   Useful for modeling:
   - Retina of the eye
   - Curved detectors
   - Curved screens


   .. py:attribute:: arc_radius
      :value: 2.0



   .. py:attribute:: arc_angle


   .. py:attribute:: stroke_color


   .. py:attribute:: stroke_width
      :value: 4



   .. py:attribute:: fill_color
      :value: None



   .. py:attribute:: fill_opacity
      :value: 0.0



   .. py:method:: get_curvature_center() -> numpy.ndarray

      Calculate the center of curvature dynamically with caching for performance.

      This is computed from the current position of the arc, ensuring
      it works correctly during animations where shift()/move_to() aren't called.
      The result is cached and only recalculated when the arc moves.

      :returns: Current center of curvature in 3D space
      :rtype: np.ndarray



   .. py:method:: intersect(ray_start: numpy.ndarray, ray_direction: numpy.ndarray) -> tuple

      Check if ray intersects the arc.

      Uses ray-circle intersection, then verifies if the point is within
      the arc's angular range.

      :param ray_start: Starting point of the ray (3D)
      :type ray_start: np.ndarray
      :param ray_direction: Direction vector of the ray (3D, should be normalized)
      :type ray_direction: np.ndarray

      :returns: (intersection_point, True) if hit, (None, False) otherwise
      :rtype: tuple



   .. py:method:: get_debug_info(ray_start: numpy.ndarray, ray_direction: numpy.ndarray) -> dict

      Get detailed debug information about ray-arc intersection.

      :returns: Debug information including center, distances, angles, etc.
      :rtype: dict



.. py:class:: BeamStop(**kwargs)

   Bases: :py:obj:`manim_optics.base.OpticalElement`


   Base class for elements that stop/block light rays.

   BeamStops do not refract or reflect light - they simply absorb it.
   When a ray intersects a BeamStop, it is marked as terminated.

   Subclasses must implement:
   - intersect(): Determine if ray hits the stop
   - Visual representation


   .. py:method:: get_transfer_matrix() -> numpy.ndarray

      BeamStops don't have a transfer matrix as they terminate rays.

      Returns identity matrix (though it shouldn't be used).



   .. py:method:: propagate_ray(ray_start: numpy.ndarray, ray_direction: numpy.ndarray, intersection_point: numpy.ndarray) -> tuple

      BeamStop terminates the ray - no propagation.

      :param ray_start: Starting position of the ray
      :type ray_start: np.ndarray
      :param ray_direction: Direction vector of the ray
      :type ray_direction: np.ndarray
      :param intersection_point: Point where ray intersects the beam stop
      :type intersection_point: np.ndarray

      :returns: (None, False) indicating the ray is stopped
      :rtype: tuple



   .. py:method:: is_mirror() -> bool

      BeamStops are not mirrors.



.. py:class:: CircularAperture(radius: float = 0.5, total_length: float = None, line_color=GREY_D, line_stroke_width: float = 4, **kwargs)

   Bases: :py:obj:`BeamStop`


   Circular aperture/diaphragm that blocks rays outside a circle.

   Rays passing through the center (within radius) are NOT stopped.
   Rays hitting the opaque region (outside radius) ARE stopped.

   Useful for modeling:
   - Iris/pupil of the eye
   - Diaphragms
   - Circular stops


   .. py:attribute:: aperture_radius
      :value: 0.5



   .. py:attribute:: radius_tracker


   .. py:attribute:: total_length


   .. py:attribute:: line_color


   .. py:attribute:: line_stroke_width
      :value: 4



   .. py:method:: animate_radius(new_radius: float, run_time: float = 2.0, **kwargs)

      Animate a change in aperture radius (pupil dilation/constriction).

      :param new_radius: Target radius
      :type new_radius: float
      :param run_time: Duration of the animation
      :type run_time: float
      :param \*\*kwargs: Additional arguments for the animation

      :returns: Animation that changes the aperture radius
      :rtype: Animation

      .. rubric:: Example

      >>> aperture = CircularAperture(radius=0.5)
      >>> scene.play(aperture.animate_radius(0.8, run_time=1.0))  # Dilate
      >>> scene.play(aperture.animate_radius(0.3, run_time=1.0))  # Constrict



   .. py:method:: set_radius(radius: float)

      Set aperture radius immediately without animation.

      :param radius: New aperture radius
      :type radius: float

      :returns: Self (for chaining)
      :rtype: CircularAperture



   .. py:method:: intersect(ray_start: numpy.ndarray, ray_direction: numpy.ndarray) -> tuple

      Check if ray hits the opaque region (outside aperture radius).

      The aperture is in the xy-plane at z=0.

      :param ray_start: Starting point of the ray
      :type ray_start: np.ndarray
      :param ray_direction: Direction vector of the ray
      :type ray_direction: np.ndarray

      :returns: (intersection_point, True) if ray is BLOCKED (outside radius)
                (None, False) if ray PASSES THROUGH (inside radius)
      :rtype: tuple



   .. py:method:: get_top_coordinates() -> numpy.ndarray

      Get the top coordinate of the aperture opening.



   .. py:method:: get_bottom_coordinates() -> numpy.ndarray

      Get the bottom coordinate of the aperture opening.



.. py:class:: LineBeamStop(height: float = 3.0, color=GREY_D, stroke_width: float = 6, **kwargs)

   Bases: :py:obj:`BeamStop`


   Vertical line that stops rays.

   Useful for modeling:
   - Screens
   - Detectors
   - Hard aperture edges


   .. py:attribute:: stop_height
      :value: 3.0



   .. py:attribute:: color


   .. py:attribute:: stroke_width
      :value: 6



   .. py:method:: intersect(ray_start: numpy.ndarray, ray_direction: numpy.ndarray) -> tuple

      Check if ray intersects the vertical line.

      :param ray_start: Starting point of the ray
      :type ray_start: np.ndarray
      :param ray_direction: Direction vector of the ray
      :type ray_direction: np.ndarray

      :returns: (intersection_point, True) if hit, (None, False) otherwise
      :rtype: tuple



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



.. py:class:: Eye(focal_length: float = 2.0, lens_diameter: float = 1.0, pupil_diameter: float = 0.4, include_pupil: bool = True, focal_delta: float = 0.0, show_focal_point: bool = False, show_cornea: bool = False, cornea_thickness: float = 0.1, lens_color=BLUE_D, pupil_color=BLUE_C, retina_color=WHITE, fill_color=BLUE_D, **kwargs)

   Bases: :py:obj:`manim.VGroup`


   Simplified model of an eye for optical simulations.

   Components:
   - Lens (cornea + crystalline lens simplified as thin lens)
   - Optional CircularAperture (pupil/iris)
   - ArcBeamStop (retina - curved detector)

   All components are positioned relative to the lens center.
   Use get_optical_elements() to get the ordered list for ray tracing.


   .. py:attribute:: focal_length
      :value: 2.0



   .. py:attribute:: lens_diameter
      :value: 1.0



   .. py:attribute:: pupil_diameter
      :value: 0.4



   .. py:attribute:: delta_focal
      :value: 0.0



   .. py:attribute:: show_focal_point
      :value: False



   .. py:attribute:: fill_color


   .. py:attribute:: retina_color


   .. py:attribute:: lens_color


   .. py:attribute:: pupil_color


   .. py:attribute:: fill_opacity
      :value: 0.0



   .. py:attribute:: show_cornea
      :value: False



   .. py:attribute:: cornea_thickness
      :value: 0.1



   .. py:attribute:: lens_entering
      :value: 0.2



   .. py:attribute:: aperture_enterring
      :value: 0.1



   .. py:attribute:: retina_radius
      :value: 1.1111111111111112



   .. py:attribute:: total_aperture_length


   .. py:attribute:: retina_angle


   .. py:attribute:: include_pupil
      :value: True



   .. py:method:: get_optical_elements()

      Get ordered list of optical elements for ray tracing.

      :returns: [lens, pupil (optional), retina] in order of interaction
      :rtype: list



   .. py:method:: set_focal_length(new_focal: float)

      Update the focal length of the eye lens immediately.

      This simulates accommodation (changing focus).

      :param new_focal: New focal length
      :type new_focal: float

      :returns: Self (for chaining)
      :rtype: Eye



   .. py:method:: animate_focal_length(new_focal: float, run_time: float = 2.0, **kwargs)

      Animate a change in focal length (accommodation).

      This simulates the eye's accommodation process where the crystalline
      lens changes shape to focus at different distances.

      :param new_focal: Target focal length
      :type new_focal: float
      :param run_time: Duration of the animation (accommodation time)
      :type run_time: float
      :param \*\*kwargs: Additional arguments for the animation

      :returns: Animation that changes the eye's focal length
      :rtype: Animation

      .. rubric:: Example

      >>> eye = Eye(focal_length=2.0)
      >>> # Animate accommodation to near vision
      >>> scene.play(eye.animate_focal_length(1.5, run_time=1.0))
      >>> # Animate accommodation to far vision
      >>> scene.play(eye.animate_focal_length(2.5, run_time=1.0))



   .. py:method:: set_pupil_diameter(new_diameter: float)

      Update pupil diameter immediately (simulates dilation/constriction).

      :param new_diameter: New pupil diameter
      :type new_diameter: float

      :returns: Self (for chaining)
      :rtype: Eye



   .. py:method:: animate_pupil_diameter(new_diameter: float, run_time: float = 2.0, **kwargs)

      Animate a change in pupil diameter (dilation/constriction).

      This simulates the iris muscles contracting or relaxing to change
      the pupil size in response to light conditions.

      :param new_diameter: Target pupil diameter
      :type new_diameter: float
      :param run_time: Duration of the animation
      :type run_time: float
      :param \*\*kwargs: Additional arguments for the animation

      :returns: Animation that changes the pupil diameter
      :rtype: Animation

      .. rubric:: Example

      >>> eye = Eye(pupil_diameter=0.4)
      >>> # Dilate pupil (dark adaptation)
      >>> scene.play(eye.animate_pupil_diameter(0.8, run_time=1.0))
      >>> # Constrict pupil (bright light)
      >>> scene.play(eye.animate_pupil_diameter(0.3, run_time=0.5))



.. py:class:: ConvergingLens(focal_length: float = 2.0, **kwargs)

   Bases: :py:obj:`ThinLens`


   Converging (convex) lens with positive focal length.


.. py:class:: DivergingLens(focal_length: float = -2.0, **kwargs)

   Bases: :py:obj:`ThinLens`


   Diverging (concave) lens with negative focal length.


.. py:class:: ThinLens(focal_length: float = 2.0, height: float = 3.0, refractive_index_before: float = 1.0, refractive_index_after: float = 1.0, color=BLUE, tip_length: float = 0.3, stroke_width: float = 3, show_focal_points: bool = True, **kwargs)

   Bases: :py:obj:`manim_optics.base.OpticalElement`


   Base class for thin lenses (paraxial approximation).

   In the thin lens approximation:
   - The lens has negligible thickness
   - Small angle approximation: sin(θ) ≈ θ
   - All refraction happens at the principal plane

   The focal length convention:
   - f > 0: converging lens
   - f < 0: diverging lens


   .. py:attribute:: focal_length
      :value: 2.0



   .. py:attribute:: focal_length_tracker


   .. py:attribute:: lens_height
      :value: 3.0



   .. py:attribute:: color


   .. py:attribute:: tip_length
      :value: 0.3



   .. py:attribute:: stroke_width
      :value: 3



   .. py:attribute:: show_focal_points
      :value: True



   .. py:method:: get_optical_plane_position() -> numpy.ndarray

      Get the position of the optical plane (lens line center).

      This returns the position of the lens line itself, not affected by
      the focal points which move during focal length animations.

      :returns: Position of the lens optical plane
      :rtype: np.ndarray



   .. py:method:: create(run_time: float = 1.0) -> manim.AnimationGroup

      Create an animation for the appearance of the lens.

      The arrows grow from the center of the lens outward.

      :param run_time: Duration of the animation
      :type run_time: float

      :returns: Animation showing the lens appearing
      :rtype: AnimationGroup



   .. py:method:: intersect(ray_start: numpy.ndarray, ray_direction: numpy.ndarray) -> tuple

      Calculate intersection with the lens plane.

      For a thin lens, we find where the ray crosses the vertical plane
      at the lens center.



   .. py:method:: animate_focal_length(new_focal_length: float, run_time: float = 2.0, **kwargs)

      Animate a change in focal length.

      :param new_focal_length: Target focal length
      :type new_focal_length: float
      :param run_time: Duration of the animation
      :type run_time: float
      :param \*\*kwargs: Additional arguments for the animation

      :returns: Animation that changes the focal length
      :rtype: Animation

      .. rubric:: Example

      >>> lens = ConvergingLens(focal_length=2.0)
      >>> scene.play(lens.animate_focal_length(3.0, run_time=1.5))



   .. py:method:: set_focal_length(focal_length: float)

      Set focal length immediately without animation.

      :param focal_length: New focal length
      :type focal_length: float

      :returns: Self (for chaining)
      :rtype: ThinLens



   .. py:method:: get_transfer_matrix() -> numpy.ndarray

      Get the ABCD transfer matrix for a thin lens.

      For a thin lens: [[1, 0], [-1/f, 1]]
      where f is the focal length.

      Note: Always reads from focal_length_tracker to ensure we use
      the current animated value during transitions.



   .. py:method:: propagate_ray(ray_start: numpy.ndarray, ray_direction: numpy.ndarray, intersection_point: numpy.ndarray) -> tuple

      Apply thin lens equation using ABCD transfer matrix formalism.

      The ray state is represented as [y, θ] where:
      - y = height relative to optical axis
      - θ = angle of ray (in paraxial approximation: θ ≈ sin(θ) ≈ tan(θ))

      Transfer matrix for thin lens: [[1, 0], [-1/f, 1]]



.. py:class:: Mirror(refractive_index: float = 1.0, **kwargs)

   Bases: :py:obj:`manim_optics.base.OpticalElement`


   Base class for mirrors.

   Implements specular reflection: angle of incidence = angle of reflection

   For mirrors, the refractive index is virtually inverted:
   n_after = -n_before (this models the path reversal)


   .. py:method:: is_mirror() -> bool

      Return True since this is a mirror.



   .. py:method:: get_normal_at(point: numpy.ndarray) -> numpy.ndarray
      :abstractmethod:


      Get the normal vector at a point on the mirror surface.



   .. py:method:: get_transfer_matrix() -> numpy.ndarray

      Get the ABCD transfer matrix for a plane mirror.

      For a plane mirror: [[1, 0], [0, -1]]
      The reflection inverts the angle.



   .. py:method:: propagate_ray(ray_start: numpy.ndarray, ray_direction: numpy.ndarray, intersection_point: numpy.ndarray) -> tuple

      Calculate reflected ray direction using the law of reflection.

      Reflection formula: R = D - 2(D·N)N
      where D is incident direction and N is surface normal



.. py:class:: PlaneMirror(height: float = 3.0, refractive_index: float = 1.0, coating_side: str = 'left', coating_count: int = 5, coating_angle_deg: float = 45.0, coating_length_ratio: float = 0.05, stroke_width: float = 4.0, coating_stroke_width: float | None = None, mirror_color=GREY_A, coating_color=GREY_C, tilt_deg: float = 0.0, **kwargs)

   Bases: :py:obj:`Mirror`


   Plane (flat) mirror.

   A vertical mirror that reflects rays according to the law of reflection.


   .. py:attribute:: mirror_height
      :value: 3.0



   .. py:attribute:: coating_side
      :value: 'left'



   .. py:attribute:: coating_count
      :value: 5



   .. py:attribute:: coating_angle_deg
      :value: 45.0



   .. py:attribute:: coating_length_ratio
      :value: 0.05



   .. py:attribute:: stroke_width
      :value: 4.0



   .. py:attribute:: coating_stroke_width
      :value: 4.0



   .. py:attribute:: mirror_color


   .. py:attribute:: coating_color


   .. py:attribute:: tilt_tracker


   .. py:method:: get_optical_plane_position() -> numpy.ndarray

      Get the position of the optical plane (the mirror line).

      Overrides the base method because the VGroup center can include
      coating indicators, which would give an incorrect position.



   .. py:method:: intersect(ray_start: numpy.ndarray, ray_direction: numpy.ndarray) -> tuple

      Calculate intersection with the (possibly tilted) mirror plane.



   .. py:method:: get_normal_at(point: numpy.ndarray) -> numpy.ndarray

      Normal to the mirror, accounting for tilt.



.. py:class:: SphericalMirror(radius_of_curvature: float = -4.0, height: float = 3.0, refractive_index: float = 1.0, aperture_angle: float = 60 * DEGREES, facing: str = 'left', stroke_width: float = 4.0, mirror_color=GREY_A, coating_color=GREY_C, coating_count: int = 5, tip_length: float = 0.3, show_focal_point: bool = True, tilt_deg: float = 0.0, **kwargs)

   Bases: :py:obj:`Mirror`


   Spherical mirror with a given radius of curvature.

   Uses paraxial approximation and ABCD matrix formalism.

   Convention for radius of curvature R (French algebraic sign convention):
   - R < 0: Concave mirror (converging) — center of curvature on the incident side
   - R > 0: Convex mirror  (diverging)  — center of curvature on the opposite side

   Focal length f = R/2 (signed).  Transfer matrix: [[1, 0], [2/R, 1]]


   .. py:attribute:: radius_of_curvature
      :value: -4.0



   .. py:attribute:: mirror_height
      :value: 3.0



   .. py:attribute:: aperture_angle


   .. py:attribute:: facing
      :value: 'left'



   .. py:attribute:: stroke_width
      :value: 4.0



   .. py:attribute:: mirror_color


   .. py:attribute:: coating_color


   .. py:attribute:: coating_count
      :value: 5



   .. py:attribute:: tip_length
      :value: 0.3



   .. py:attribute:: show_focal_point
      :value: True



   .. py:attribute:: tilt_tracker


   .. py:method:: get_optical_plane_position() -> numpy.ndarray

      Get the position of the optical plane (the mirror line).

      Overrides the base method because the VGroup center includes the focal point,
      which would give an incorrect position.



   .. py:method:: intersect(ray_start: numpy.ndarray, ray_direction: numpy.ndarray) -> tuple

      Calculate intersection with the (possibly tilted) mirror plane.

      In the paraxial approximation, the mirror is treated as a plane.
      The curvature only affects the transfer matrix.



   .. py:method:: get_normal_at(point: numpy.ndarray) -> numpy.ndarray

      Normal points in the facing direction, accounting for tilt.



   .. py:method:: get_transfer_matrix() -> numpy.ndarray

      ABCD transfer matrix: [[1, 0], [2/R, 1]]
      R < 0 (concave/converging): C = 2/R < 0 → focusing
      R > 0 (convex/diverging):   C = 2/R > 0 → defocusing



   .. py:method:: propagate_ray(ray_start: numpy.ndarray, ray_direction: numpy.ndarray, intersection_point: numpy.ndarray) -> tuple

      Calculate reflected ray direction using paraxial ABCD matrix formalism.

      For a tilted mirror the ray is first rotated into the mirror's local frame
      (where the mirror is vertical), the ABCD matrix is applied, then the result
      is rotated back to the world frame.



.. py:class:: CrossGraticule(x_length: float | None = None, y_length: float | None = None, **kwargs)

   Bases: :py:obj:`Graticule`


   Cross graticule - two perpendicular graduated axes.

   Useful for 2D coordinate measurements (like Cartesian axes).


   .. py:attribute:: x_length


   .. py:attribute:: y_length


.. py:class:: Graticule(length: float = 10.0, unit_length: float = 1.0, primary_interval: int = 5, secondary_interval: int = 1, tick_position: Literal['inside', 'outside', 'centered'] = 'centered', primary_tick_length: float = 0.2, secondary_tick_length: float = 0.1, tick_angle: float = 90 * DEGREES, global_angle: float = 0.0, primary_stroke_width: float = 2.5, secondary_stroke_width: float = 1.5, color: str = WHITE, zero_position: float = 0.0, show_main_line: bool = False, show_labels: bool = True, label_offset: float = 0.3, label_font_size: int = 18, label_rotation: float = 0.0, decimal_places: int = 1, **kwargs)

   Bases: :py:obj:`manim.VGroup`


   Base class for graticules (graduated scales/grids).

   A graticule is a graduated reference scale used for measurements.
   This base class provides common functionality for all graticule types.


   .. py:attribute:: length
      :value: 10.0



   .. py:attribute:: unit_length
      :value: 1.0



   .. py:attribute:: primary_interval
      :value: 5



   .. py:attribute:: secondary_interval
      :value: 1



   .. py:attribute:: tick_position
      :value: 'centered'



   .. py:attribute:: primary_tick_length
      :value: 0.2



   .. py:attribute:: secondary_tick_length
      :value: 0.1



   .. py:attribute:: tick_angle


   .. py:attribute:: global_angle
      :value: 0.0



   .. py:attribute:: primary_stroke_width
      :value: 2.5



   .. py:attribute:: secondary_stroke_width
      :value: 1.5



   .. py:attribute:: color


   .. py:attribute:: zero_position
      :value: 0.0



   .. py:attribute:: show_main_line
      :value: False



   .. py:attribute:: show_labels
      :value: True



   .. py:attribute:: label_offset
      :value: 0.3



   .. py:attribute:: label_font_size
      :value: 18



   .. py:attribute:: label_rotation
      :value: 0.0



   .. py:attribute:: decimal_places
      :value: 1



   .. py:attribute:: axis_line
      :value: None



   .. py:attribute:: ticks


   .. py:attribute:: labels


   .. py:method:: highlight_tick(value: float, color: str = YELLOW, scale: float = 1.5)

      Highlight a specific graduation.

      :param value: The value to highlight
      :type value: float
      :param color: Color for highlighting
      :type color: str
      :param scale: Scale factor for the highlighted tick
      :type scale: float

      :returns: Group containing the highlighted elements
      :rtype: VGroup



   .. py:method:: create_animation(run_time: float = 1.0, lag_ratio: float = 0.05) -> manim.Animation

      Create an animation for the graticule appearance.

      :param run_time: Duration of the animation
      :type run_time: float
      :param lag_ratio: Lag between different elements
      :type lag_ratio: float

      :returns: Animation for the graticule
      :rtype: Animation



   .. py:method:: fade_out_animation(run_time: float = 0.5) -> manim.Animation

      Create a fade out animation.

      :param run_time: Duration of the animation
      :type run_time: float

      :returns: Fade out animation
      :rtype: Animation



.. py:class:: GridGraticule(width: float | None = None, height: float | None = None, grid_stroke_width: float = 0.5, show_grid_labels: bool = False, **kwargs)

   Bases: :py:obj:`Graticule`


   Grid graticule - a 2D grid of graduated lines.

   Useful for precise 2D measurements and alignment.


   .. py:attribute:: grid_width


   .. py:attribute:: grid_height


   .. py:attribute:: grid_stroke_width
      :value: 0.5



   .. py:attribute:: show_grid_labels
      :value: False



   .. py:method:: create_animation(run_time: float = 1.0, lag_ratio: float = 0.02) -> manim.Animation

      Create an animation for the grid appearance.

      :param run_time: Duration of the animation
      :type run_time: float
      :param lag_ratio: Lag between different elements
      :type lag_ratio: float

      :returns: Animation for the grid
      :rtype: Animation



.. py:class:: LinearGraticule(direction: numpy.ndarray = RIGHT, skip_zero_label: bool = False, **kwargs)

   Bases: :py:obj:`Graticule`


   Linear graticule - a single graduated line.

   Useful for measuring distances along one axis.


   .. py:attribute:: skip_zero_label
      :value: False



   .. py:attribute:: direction


   .. py:attribute:: perpendicular


.. py:class:: OpticalElement3D(position=ORIGIN, normal_vector=UP, **kwargs)

   Bases: :py:obj:`manim.VGroup`


   Classe de base pour tous les éléments optiques 3D.

   Gère un plan optique dans l'espace 3D avec position et orientation arbitraires.
   Le plan est défini par un point et un vecteur normal.

   :param position: Point de référence sur le plan optique (centre) [x, y, z]
   :type position: np.ndarray
   :param normal_vector: Vecteur normal au plan optique [nx, ny, nz]
                         Par défaut UP = [0, 1, 0] (plan horizontal)
   :type normal_vector: np.ndarray
   :param \*\*kwargs: Arguments supplémentaires pour VGroup


   .. py:attribute:: position


   .. py:attribute:: normal


   .. py:method:: intersect_3d(ray_start, ray_direction)

      Calcule l'intersection entre un rayon et le plan optique.

      Équation du plan : (P - P0) · n = 0
      Équation du rayon : P = R0 + t*d
      Solution : t = (P0 - R0) · n / (d · n)

      :param ray_start: Point de départ du rayon [x, y, z]
      :type ray_start: np.ndarray
      :param ray_direction: Direction du rayon (normalisée) [dx, dy, dz]
      :type ray_direction: np.ndarray

      :returns: Point d'intersection [x, y, z] ou None si pas d'intersection
      :rtype: np.ndarray or None



   .. py:method:: get_optical_plane_position()

      Retourne la position du plan optique (centre).



   .. py:method:: get_normal_vector()

      Retourne le vecteur normal au plan optique.



   .. py:method:: propagate_ray_3d(ray_start, ray_direction, intersection_point)
      :abstractmethod:


      Propage un rayon à travers l'élément optique.
      À redéfinir dans les sous-classes.

      :param ray_start: Point de départ du rayon
      :type ray_start: np.ndarray
      :param ray_direction: Direction du rayon avant interaction
      :type ray_direction: np.ndarray
      :param intersection_point: Point d'intersection avec l'élément
      :type intersection_point: np.ndarray

      :returns: (nouvelle_direction, continue)
                nouvelle_direction : direction après interaction
                continue : True si le rayon continue, False s'il est arrêté
      :rtype: tuple(np.ndarray, bool)



.. py:class:: RayBundle3D(start_points, direction_vector, optical_elements=None, max_length=20.0, color=YELLOW, stroke_width=2, auto_update=True, **kwargs)

   Bases: :py:obj:`manim.VGroup`


   Faisceau de rayons en 3D qui interagissent avec des éléments optiques 3D.

   Trace plusieurs rayons depuis des points de départ différents avec la même
   direction initiale, et les propage à travers une séquence d'éléments optiques.

   :param start_points: Liste des points de départ des rayons [x, y, z]
   :type start_points: list of np.ndarray
   :param direction_vector: Direction initiale commune à tous les rayons [dx, dy, dz]
   :type direction_vector: np.ndarray
   :param optical_elements: Liste des éléments optiques à traverser (dans l'ordre)
   :type optical_elements: list of OpticalElement3D
   :param max_length: Longueur maximale d'un segment de rayon
   :type max_length: float
   :param color: Couleur des rayons
   :type color: Color
   :param stroke_width: Épaisseur des rayons
   :type stroke_width: float
   :param auto_update: Si True, les rayons se recalculent automatiquement à chaque frame
                       quand les éléments optiques bougent (défaut: True)
   :type auto_update: bool
   :param \*\*kwargs: Arguments supplémentaires pour VGroup


   .. py:attribute:: start_points


   .. py:attribute:: direction


   .. py:attribute:: optical_elements
      :value: []



   .. py:attribute:: max_length
      :value: 20.0



   .. py:attribute:: ray_color


   .. py:attribute:: ray_stroke_width
      :value: 2



   .. py:attribute:: auto_update
      :value: True



.. py:class:: ThinLens3D(focal_length=3.0, aperture_radius=2.0, position=ORIGIN, normal_vector=UP, display_mode='simple', thickness=0.2, R1=5.0, R2=5.0, color=BLUE_E, opacity=0.6, show_focal_points=False, **kwargs)

   Bases: :py:obj:`OpticalElement3D`


   Lentille mince en 3D avec support des rotations complètes.

   Implémente l'approximation de la lentille mince en 3D avec deux modes d'affichage :
   - Mode 'simple' : cercle 3D symbolique
   - Mode 'detailed' : surfaces biconvexes réalistes

   :param focal_length: Distance focale de la lentille (positive pour convergente)
   :type focal_length: float
   :param aperture_radius: Rayon d'ouverture de la lentille
   :type aperture_radius: float
   :param position: Position du centre de la lentille [x, y, z]
   :type position: np.ndarray
   :param normal_vector: Vecteur normal au plan de la lentille
   :type normal_vector: np.ndarray
   :param display_mode: 'simple' pour un cercle, 'detailed' pour les surfaces
   :type display_mode: str
   :param thickness: Épaisseur au centre (pour mode detailed)
   :type thickness: float
   :param R1: Rayons de courbure des faces (pour mode detailed)
   :type R1: float
   :param R2: Rayons de courbure des faces (pour mode detailed)
   :type R2: float
   :param color: Couleur de la lentille
   :type color: Color
   :param opacity: Opacité de la lentille
   :type opacity: float
   :param show_focal_points: Afficher les points focaux
   :type show_focal_points: bool
   :param \*\*kwargs: Arguments supplémentaires pour VGroup


   .. py:attribute:: focal_length
      :value: 3.0



   .. py:attribute:: focal_length_tracker


   .. py:attribute:: aperture_radius
      :value: 2.0



   .. py:attribute:: aperture_radius_tracker


   .. py:attribute:: position


   .. py:attribute:: position_x_tracker


   .. py:attribute:: position_y_tracker


   .. py:attribute:: position_z_tracker


   .. py:attribute:: normal


   .. py:attribute:: normal_x_tracker


   .. py:attribute:: normal_y_tracker


   .. py:attribute:: normal_z_tracker


   .. py:attribute:: display_mode
      :value: 'simple'



   .. py:attribute:: thickness
      :value: 0.2



   .. py:attribute:: R1
      :value: 5.0



   .. py:attribute:: R2
      :value: 5.0



   .. py:attribute:: lens_color


   .. py:attribute:: lens_opacity
      :value: 0.6



   .. py:attribute:: show_focal_points
      :value: False



   .. py:method:: animate_focal_length(new_focal_length, run_time=2.0, **kwargs)

      Anime un changement de distance focale.

      :param new_focal_length: Nouvelle distance focale cible
      :type new_focal_length: float
      :param run_time: Durée de l'animation
      :type run_time: float
      :param \*\*kwargs: Arguments supplémentaires pour l'animation

      :returns: Animation qui change la distance focale
      :rtype: Animation



   .. py:method:: set_focal_length(focal_length)

      Définit la distance focale immédiatement sans animation.



   .. py:method:: animate_aperture_radius(new_radius, run_time=2.0, **kwargs)

      Anime un changement de rayon d'ouverture.

      :param new_radius: Nouveau rayon d'ouverture
      :type new_radius: float
      :param run_time: Durée de l'animation
      :type run_time: float
      :param \*\*kwargs: Arguments supplémentaires pour l'animation

      :returns: Animation qui change le rayon d'ouverture
      :rtype: Animation



   .. py:method:: set_aperture_radius(radius)

      Définit le rayon d'ouverture immédiatement sans animation.



   .. py:method:: animate_position(new_position, run_time=2.0, **kwargs)

      Anime un changement de position 3D.

      :param new_position: Nouvelle position [x, y, z]
      :type new_position: np.ndarray
      :param run_time: Durée de l'animation
      :type run_time: float
      :param \*\*kwargs: Arguments supplémentaires pour l'animation

      :returns: Groupe d'animations pour x, y et z
      :rtype: AnimationGroup



   .. py:method:: set_position_3d(position)

      Définit la position 3D immédiatement sans animation.



   .. py:method:: animate_normal_vector(new_normal, run_time=2.0, **kwargs)

      Anime un changement d'orientation (vecteur normal).

      :param new_normal: Nouveau vecteur normal [nx, ny, nz]
      :type new_normal: np.ndarray
      :param run_time: Durée de l'animation
      :type run_time: float
      :param \*\*kwargs: Arguments supplémentaires pour l'animation

      :returns: Groupe d'animations pour les composantes du vecteur normal
      :rtype: AnimationGroup



   .. py:method:: set_normal_vector(normal)

      Définit le vecteur normal immédiatement sans animation.



   .. py:method:: propagate_ray_3d(ray_start, ray_direction, intersection_point)

      Propage un rayon à travers la lentille mince en 3D.

      Utilise la formule de la lentille mince en décomposant le rayon
      dans le repère local de la lentille.

      :param ray_start: Point de départ du rayon
      :type ray_start: np.ndarray
      :param ray_direction: Direction du rayon avant la lentille
      :type ray_direction: np.ndarray
      :param intersection_point: Point d'intersection avec la lentille
      :type intersection_point: np.ndarray

      :returns: (nouvelle_direction, True) - le rayon continue toujours
      :rtype: tuple(np.ndarray, bool)



.. py:class:: DynamicRay(start_point: numpy.typing.NDArray[numpy.floating] | manim.Mobject, direction: numpy.typing.NDArray[numpy.floating] | collections.abc.Callable[[], numpy.typing.NDArray[numpy.floating]], optical_elements: list[manim_optics.base.OpticalElement] | None = None, max_segments: int = 10, ray_length: float = 100.0, color: str = YELLOW, stroke_width: float = 2, opacity: float = 1.0, **kwargs)

   Bases: :py:obj:`manim.VMobject`


   A ray that automatically recalculates its path when optical elements move.

   The ray uses Manim's updater system to recompute its trajectory at every
   frame, enabling dynamic and interactive optical simulations.

   Key features:
   - Automatic path recalculation
   - Supports multiple optical elements
   - Handles reflections and refractions
   - Maximum ray segments to prevent infinite loops


   .. py:attribute:: start_point_source


   .. py:attribute:: direction_source


   .. py:attribute:: optical_elements
      :value: []



   .. py:attribute:: max_segments
      :value: 10



   .. py:attribute:: ray_length
      :value: 100.0



   .. py:attribute:: opacity
      :value: 1.0



   .. py:method:: set_optical_elements(optical_elements: list[manim_optics.base.OpticalElement]) -> None

      Update the list of optical elements and recalculate the ray path.

      :param optical_elements: New list of optical elements
      :type optical_elements: List[OpticalElement]



   .. py:method:: add_optical_element(element: manim_optics.base.OpticalElement) -> None

      Add an optical element to the ray's interaction list.

      :param element: Element to add
      :type element: OpticalElement



   .. py:method:: remove_optical_element(element: manim_optics.base.OpticalElement) -> None

      Remove an optical element from the ray's interaction list.

      :param element: Element to remove
      :type element: OpticalElement



   .. py:method:: stop_updating() -> None

      Remove the updater to freeze the ray.



   .. py:method:: resume_updating(recursive: bool = True) -> None

      Re-add the updater to make the ray dynamic again.



   .. py:method:: animate_propagation(run_time: float = 2.0, rate_func=linear) -> manim.Animation

      Animate the ray propagating along its path with fade-in effect.

      The animation shows the ray appearing gradually while maintaining
      its correct trajectory throughout.

      :param run_time: Duration of the animation
      :type run_time: float
      :param rate_func: Rate function for the animation (default: linear)
      :type rate_func: function

      :returns: Animation that reveals the ray
      :rtype: Animation



   .. py:method:: get_vertex_index_from_pos(pos: numpy.typing.NDArray[numpy.floating]) -> numpy.typing.NDArray

      Given an x-coordinate, return the next vertex point of the ray.



.. py:class:: ImageFormation(ray_bundle: RayBundle, optical_element_index: int = 0, extension_length: float = 5.0, show_extensions: bool = True, show_focal_point: bool = False, show_image_arrow: bool = True, optical_axis_y: float = 0.0, focal_point_color: str = BLUE, image_arrow_color: str = BLUE, extension_color: str | None = None, **kwargs)

   Bases: :py:obj:`manim.VGroup`


   Analyzes and visualizes image formation from a RayBundle.

   Automatically calculates the focal point where rays converge (or are closest)
   after propagating through an optical element. Provides visual components:
   - Extended rays (dashed lines)
   - Focal point marker
   - Image arrow from optical axis to focal point

   All components update automatically when the bundle changes.

   .. attribute:: focal_point_dot

      Marker at the calculated focal point

      :type: Dot

   .. attribute:: image_arrow

      Arrow from optical axis to image position

      :type: Arrow

   .. attribute:: extended_rays

      Dashed ray extensions for visualization

      :type: VGroup


   .. py:attribute:: ray_bundle


   .. py:attribute:: optical_element_index
      :value: 0



   .. py:attribute:: extension_length
      :value: 5.0



   .. py:attribute:: optical_axis_y
      :value: 0.0



   .. py:attribute:: x_pos_image


   .. py:attribute:: extended_rays


   .. py:attribute:: focal_point_dot


   .. py:attribute:: image_arrow


   .. py:method:: get_image_position() -> numpy.typing.NDArray[numpy.floating] | None

      Get the current calculated image position.



.. py:class:: ImageMarker(ray1: DynamicRay, ray2: DynamicRay, segment1: int = -1, segment2: int = -1, optical_axis_y: float = 0.0, color: str = GREEN, show_label: bool = True, **kwargs)

   Bases: :py:obj:`manim.VGroup`


   A dynamic arrow that marks the image position formed by ray intersection.

   The arrow starts from the optical axis and points to the image position.
   Automatically updates position when rays move.


   .. py:attribute:: ray1


   .. py:attribute:: ray2


   .. py:attribute:: segment1
      :value: -1



   .. py:attribute:: segment2
      :value: -1



   .. py:attribute:: optical_axis_y
      :value: 0.0



   .. py:attribute:: marker_color


   .. py:attribute:: show_label
      :value: True



   .. py:attribute:: arrow


.. py:class:: PrincipalRays(object_point: numpy.typing.NDArray[numpy.floating] | manim.Mobject, lens: manim_optics.lenses.ThinLens, **kwargs)

   Bases: :py:obj:`manim.VGroup`


   The three principal rays for a thin lens:
   1. Parallel ray (passes through far focal point after lens)
   2. Central ray (passes through lens center unchanged)
   3. Focal ray (passes through near focal point, exits parallel)

   These rays are essential for geometric optics constructions.


   .. py:attribute:: object_point_source


   .. py:attribute:: lens


   .. py:attribute:: parallel_ray


   .. py:attribute:: center_ray


   .. py:attribute:: focal_ray


.. py:class:: RayBundle(start_points: numpy.typing.NDArray[numpy.floating] | manim.Mobject | list[numpy.typing.NDArray[numpy.floating] | manim.Mobject] | None = None, directions: numpy.typing.NDArray[numpy.floating] | list[numpy.typing.NDArray[numpy.floating]] | None = None, direction_vector: numpy.typing.NDArray[numpy.floating] | list[numpy.typing.NDArray[numpy.floating]] | None = None, direction_angle_rad: float | list[float] | None = None, direction_angle_deg: float | list[float] | None = None, num_rays: int | None = None, optical_elements: list[manim_optics.base.OpticalElement] | None = None, **ray_kwargs)

   Bases: :py:obj:`manim.VGroup`


   A collection of rays with flexible start points and directions.

   Supports three modes:
   1. Same start point, different directions (diverging from a point)
   2. Different start points, same direction (parallel rays)
   3. Different start points AND different directions (custom bundle)


   .. py:attribute:: angle_offset_tracker


   .. py:attribute:: y_offset_tracker


   .. py:attribute:: rays
      :value: []



   .. py:method:: set_optical_elements(optical_elements: list[manim_optics.base.OpticalElement]) -> None

      Update the list of optical elements for all rays in the bundle.

      :param optical_elements: New list of optical elements
      :type optical_elements: List[OpticalElement]



   .. py:method:: add_optical_element(element: manim_optics.base.OpticalElement) -> None

      Add an optical element to all rays in the bundle.

      :param element: Element to add
      :type element: OpticalElement



   .. py:method:: add_optical_elements(elements: list[manim_optics.base.OpticalElement]) -> None

      Add multiple optical elements to all rays in the bundle.

      :param elements: Elements to add
      :type elements: List[OpticalElement]



   .. py:method:: remove_optical_element(element: manim_optics.base.OpticalElement) -> None

      Remove an optical element from all rays in the bundle.

      :param element: Element to remove
      :type element: OpticalElement



   .. py:method:: remove_optical_elements(elements: list[manim_optics.base.OpticalElement]) -> None

      Remove multiple optical elements from all rays in the bundle.

      :param elements: Elements to remove
      :type elements: List[OpticalElement]



   .. py:method:: stop_updating() -> None

      Stop all rays from updating.



   .. py:method:: resume_updating(recursive: bool = True) -> None

      Resume updating for all rays.



   .. py:method:: set_opacity(opacity: float, family: bool = True) -> RayBundle

      Set the opacity of all rays in the bundle.

      :param opacity: Opacity value (0 = transparent, 1 = opaque)
      :type opacity: float
      :param family: If True, applies to all submobjects (default: True)
      :type family: bool

      :returns: Self (for chaining)
      :rtype: RayBundle



   .. py:method:: set_stroke(color=None, width=None, opacity=None, **kwargs) -> RayBundle

      Set stroke properties for all rays in the bundle.

      :param color: Color of the rays
      :type color: str, optional
      :param width: Stroke width of the rays
      :type width: float, optional
      :param opacity: Opacity of the rays
      :type opacity: float, optional
      :param \*\*kwargs: Additional stroke properties

      :returns: Self (for chaining)
      :rtype: RayBundle



   .. py:method:: animate_propagation(run_time: float = 2.0, lag_ratio: float = 0.04, rate_func=linear) -> manim.AnimationGroup

      Animate all rays appearing with a fade-in effect.

      This animation preserves updaters and ensures rays have correct
      trajectories throughout the animation.

      :param run_time: Duration of the animation for each ray
      :type run_time: float
      :param lag_ratio: Delay between starting each ray's animation (0 = all together, 1 = sequential)
      :type lag_ratio: float
      :param rate_func: Rate function for the animation
      :type rate_func: function

      :returns: Group of animations for all rays
      :rtype: AnimationGroup



   .. py:method:: animate_create(run_time: float = 2.0, lag_ratio: float = 0.04, rate_func=linear) -> manim.AnimationGroup

      Animate rays appearing from right to left (following propagation direction).

      Creates a 'wave' effect where rays appear to propagate through the system.
      All rays appear simultaneously but with a sequential reveal along their paths.

      :param run_time: Duration of the animation
      :type run_time: float
      :param lag_ratio: Delay between starting each ray's animation
      :type lag_ratio: float
      :param rate_func: Rate function for the animation
      :type rate_func: function

      :returns: Group of Create animations for all rays
      :rtype: AnimationGroup

      .. rubric:: Example

      >>> rays = RayBundle(...)
      >>> scene.play(rays.animate_create(run_time=2))



   .. py:method:: animate_fade_in(run_time: float = 1.0, lag_ratio: float = 0.0) -> manim.AnimationGroup

      Animate rays fading in with correct trajectories.

      Simple fade-in animation where all rays appear gradually.
      More subtle than animate_propagation.

      :param run_time: Duration of the fade-in
      :type run_time: float
      :param lag_ratio: Delay between starting each ray's fade (usually 0 for simultaneous)
      :type lag_ratio: float

      :returns: Group of FadeIn animations
      :rtype: AnimationGroup

      .. rubric:: Example

      >>> rays = RayBundle(...)
      >>> scene.play(rays.animate_fade_in(run_time=1))



   .. py:method:: animate_uncreate(run_time: float = 1.0, lag_ratio: float = 0.0) -> manim.AnimationGroup

      Animate rays disappearing (reverse of animate_create).

      :param run_time: Duration of the animation
      :type run_time: float
      :param lag_ratio: Delay between starting each ray's animation
      :type lag_ratio: float

      :returns: Group of Uncreate animations
      :rtype: AnimationGroup

      .. rubric:: Example

      >>> scene.play(rays.animate_uncreate(run_time=1))



   .. py:method:: get_image_formation(optical_element_index: int = 0, **kwargs) -> ImageFormation

      Create an ImageFormation object to analyze and visualize image formation.

      This is a convenience method that creates an ImageFormation instance
      for this ray bundle.

      :param optical_element_index: Index of optical element after which to analyze
      :type optical_element_index: int
      :param \*\*kwargs: Additional arguments passed to ImageFormation

      :returns: Object containing image analysis and visualization
      :rtype: ImageFormation

      .. rubric:: Example

      >>> bundle = RayBundle(...)
      >>> image = bundle.get_image_formation(optical_element_index=0)
      >>> scene.add(image)
      >>> # Image position updates automatically
      >>> print(image.get_image_position())



   .. py:method:: get_optical_elements_positions(index=None) -> list[numpy.ndarray] | numpy.ndarray

      Get the positions of the optical elements in the ray bundle.

      :param index: If provided, returns the position of the optical element at this index.
      :type index: int, optional

      :returns: List of positions of all optical elements, or position of specified element.
      :rtype: List[np.ndarray] or np.ndarray



.. py:class:: RayExtension(ray: DynamicRay, element_idx: numpy.typing.NDArray[numpy.floating] = None, ray_bundle: RayBundle = None, image_pos: manim.ValueTracker = None, color: str | None = None, overshoot: float = 1.1, **kwargs)

   Bases: :py:obj:`manim.VMobject`


   Extension of a ray shown as a dashed line.

   Useful for showing virtual images or where rays would continue
   between optical elements.


   .. py:attribute:: ray


   .. py:attribute:: element_idx
      :value: None



   .. py:attribute:: ray_bundle
      :value: None



   .. py:attribute:: image_pos
      :value: None



   .. py:attribute:: overshoot
      :value: 1.1



.. py:function:: create_diverging_bundle(source_point: numpy.typing.NDArray[numpy.floating] | manim.Mobject, angle_range_deg: tuple[float, float] = (-30, 30), num_rays: int = 5, optical_elements: list[manim_optics.base.OpticalElement] | None = None, **ray_kwargs) -> RayBundle

   Helper function to create rays diverging from a point.

   :param source_point: Point from which all rays emanate
   :type source_point: np.ndarray or Mobject
   :param angle_range_deg: (min_angle, max_angle) in degrees
   :type angle_range_deg: tuple
   :param num_rays: Number of rays
   :type num_rays: int
   :param optical_elements: Optical elements to interact with
   :type optical_elements: List[OpticalElement]
   :param \*\*ray_kwargs: Additional arguments for DynamicRay

   :returns: A bundle of diverging rays
   :rtype: RayBundle


.. py:function:: create_parallel_bundle(num_rays: int = 5, spacing: float = 0.5, start_x: float = -5.0, direction: numpy.typing.NDArray[numpy.floating] = RIGHT, optical_elements: list[manim_optics.base.OpticalElement] | None = None, **ray_kwargs) -> RayBundle

   Helper function to create a bundle of evenly-spaced parallel rays.

   :param num_rays: Number of rays in the bundle
   :type num_rays: int
   :param spacing: Vertical spacing between rays
   :type spacing: float
   :param start_x: X-coordinate where rays start
   :type start_x: float
   :param direction: Direction of all rays
   :type direction: np.ndarray
   :param optical_elements: Optical elements to interact with
   :type optical_elements: List[OpticalElement]
   :param \*\*ray_kwargs: Additional arguments for DynamicRay

   :returns: A bundle of parallel rays
   :rtype: RayBundle


.. py:function:: find_focal_point_from_rays(ray_bundle: RayBundle, element_index: int = -1) -> numpy.typing.NDArray[numpy.floating] | None

   Find the focal point from multiple rays using least squares optimization.

   For ideal systems (2 rays), returns exact intersection.
   For non-ideal systems (N rays), finds the point minimizing distance to all rays.

   :param rays: List of rays to analyze
   :type rays: List[DynamicRay]
   :param segment_index: Which segment to analyze (-1 for last segment)
   :type segment_index: int

   :returns: Focal point position, or None if calculation fails
   :rtype: np.ndarray or None


.. py:function:: find_ray_intersection(ray1: DynamicRay, ray2: DynamicRay, segment1: int = -1, segment2: int = -1, max_distance: float = 100.0) -> numpy.typing.NDArray[numpy.floating] | None

   Find the intersection point of two rays.

   This calculates where two ray segments would intersect if extended.
   Useful for finding image positions.

   :param ray1: The two rays to intersect
   :type ray1: DynamicRay
   :param ray2: The two rays to intersect
   :type ray2: DynamicRay
   :param segment1: Which segments to use (-1 for last segment)
   :type segment1: int
   :param segment2: Which segments to use (-1 for last segment)
   :type segment2: int
   :param max_distance: Maximum distance to search for intersection
   :type max_distance: float

   :returns: Intersection point, or None if rays are parallel
   :rtype: np.ndarray or None


.. py:class:: OpticalScene(renderer: manim.renderer.cairo_renderer.CairoRenderer | manim.renderer.opengl_renderer.OpenGLRenderer | None = None, camera_class: type[manim.camera.camera.Camera] = Camera, always_update_mobjects: bool = False, random_seed: int | None = None, skip_animations: bool = False)

   Bases: :py:obj:`manim.Scene`


   Extension of Manim's Scene class with utilities for optical simulations.

   Provides convenient methods for setting up optical experiments and
   managing optical elements and rays.


   .. py:method:: set_theme(theme: str = 'light')

      Set the color theme for the scene.

      :param theme: Theme name ("light" or "dark")
      :type theme: str



   .. py:method:: add_debugging_grid(spacing: float = 1.0, color: str = GREY_D)

      Add a debugging grid to the scene for alignment purposes.

      :param spacing: Spacing between grid lines
      :type spacing: float
      :param color: Color of the grid lines
      :type color: str



   .. py:method:: get_optical_axis_animation(length: float = 12.0, color: str = GREY_C, y_position: float = 0.0, stroke_width: float = 2) -> manim.Animation

      Create an animation to add a horizontal optical axis to the scene.
      :param length: Length of the axis
      :type length: float
      :param color: Color of the axis
      :type color: str
      :param animate: If True, animate the axis growing from center
      :type animate: bool
      :param y_position: Vertical position of the axis
      :type y_position: float

      :returns: Animation to add the optical axis
      :rtype: Animation



   .. py:method:: setup_optical_axis(length: float = 12.0, color: str = GREY_C, animate: bool = False, y_position: float = 0.0, stroke_width: float = 2)

      Add a horizontal optical axis to the scene.

      :param length: Length of the axis
      :type length: float
      :param color: Color of the axis
      :type color: str
      :param animate: If True, animate the axis growing from center
      :type animate: bool
      :param y_position: Vertical position of the axis
      :type y_position: float



   .. py:method:: add_focal_length_labels(lens, font_size: int = 24, animate: bool = False, run_time: float = 1.0)

      Add labels showing the focal length of a lens.

      :param lens: The lens to label
      :type lens: ThinLens
      :param font_size: Size of the label text
      :type font_size: int



   .. py:method:: add_distance_marker(start_point: numpy.ndarray, end_point: numpy.ndarray, label: str, direction: numpy.ndarray = DOWN, font_size: int = 20)

      Add a distance measurement marker with label.

      :param start_point: Start of the distance
      :type start_point: np.ndarray
      :param end_point: End of the distance
      :type end_point: np.ndarray
      :param label: Text label for the distance
      :type label: str
      :param direction: Direction to offset the marker
      :type direction: np.ndarray
      :param font_size: Size of label text
      :type font_size: int



   .. py:method:: add_label_to_object(obj: manim.Mobject, label: str, font_size: int = 24, direction: numpy.ndarray = DOWN, buff: float = 0.2, color: str = WHITE, latex: bool = False, animate: bool = False, run_time: float = 1.0)

      Add a text label to an optical object.

      :param obj: The object to label
      :type obj: Mobject
      :param label: The text of the label
      :type label: str
      :param font_size: Size of the label text
      :type font_size: int
      :param direction: Direction to offset the label from the object
      :type direction: np.ndarray
      :param buff: Buffer distance between object and label
      :type buff: float
      :param color: Color of the label text
      :type color: str



.. py:function:: calculate_image_position(object_distance: float, focal_length: float) -> tuple

   Calculate image position using thin lens equation.

   1/f = 1/p + 1/p'

   :param object_distance: Distance from object to lens (positive)
   :type object_distance: float
   :param focal_length: Focal length of lens
   :type focal_length: float

   :returns: (image_distance, magnification, is_real)
             - image_distance: float (positive for real image on opposite side)
             - magnification: float (negative for inverted)
             - is_real: bool (True for real image, False for virtual)
   :rtype: tuple


.. py:function:: create_image_arrow(position: numpy.ndarray, height: float = 1.0, color: str = BLUE_C, label: str = 'Image', inverted: bool = False) -> manim.VGroup

   Create a standard image arrow for optics diagrams.

   :param position: Position of the arrow base
   :type position: np.ndarray
   :param height: Height of the arrow (negative for inverted image)
   :type height: float
   :param color: Color of the arrow
   :type color: str
   :param label: Label text
   :type label: str
   :param inverted: Whether the image is inverted
   :type inverted: bool

   :returns: Group containing arrow and label
   :rtype: VGroup


.. py:function:: create_object_arrow(position: numpy.ndarray, height: float = 1.0, color: str = WHITE, label: str = 'Object') -> manim.VGroup

   Create a standard object arrow for optics diagrams.

   :param position: Position of the arrow base
   :type position: np.ndarray
   :param height: Height of the arrow
   :type height: float
   :param color: Color of the arrow
   :type color: str
   :param label: Label text
   :type label: str

   :returns: Group containing arrow and label
   :rtype: VGroup


