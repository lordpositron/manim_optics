manim_optics.beam_stops
=======================

.. py:module:: manim_optics.beam_stops

.. autoapi-nested-parse::

   Beam Stops - Elements that block/absorb light
   =============================================

   This module provides beam stop implementations for optical simulations.



Classes
-------

.. autoapisummary::

   manim_optics.beam_stops.BeamStop
   manim_optics.beam_stops.LineBeamStop
   manim_optics.beam_stops.CircularAperture
   manim_optics.beam_stops.ArcBeamStop


Module Contents
---------------

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



