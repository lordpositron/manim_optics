manim_optics.mirrors
====================

.. py:module:: manim_optics.mirrors

.. autoapi-nested-parse::

   Mirrors - Mirror implementations
   =================================

   This module provides mirror classes for optical simulations.



Classes
-------

.. autoapisummary::

   manim_optics.mirrors.Mirror
   manim_optics.mirrors.PlaneMirror
   manim_optics.mirrors.SphericalMirror


Module Contents
---------------

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



