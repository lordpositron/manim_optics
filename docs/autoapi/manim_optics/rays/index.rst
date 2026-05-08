manim_optics.rays
=================

.. py:module:: manim_optics.rays

.. autoapi-nested-parse::

   Dynamic Ray System - Automatic ray tracing with updaters
   =========================================================

   This module implements rays that automatically update their paths when
   optical elements move or change.



Classes
-------

.. autoapisummary::

   manim_optics.rays.DynamicRay
   manim_optics.rays.RayBundle
   manim_optics.rays.PrincipalRays
   manim_optics.rays.RayExtension
   manim_optics.rays.ImageMarker
   manim_optics.rays.ImageFormation


Functions
---------

.. autoapisummary::

   manim_optics.rays.create_parallel_bundle
   manim_optics.rays.create_diverging_bundle
   manim_optics.rays.find_ray_intersection
   manim_optics.rays.find_focal_point_from_rays


Module Contents
---------------

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



