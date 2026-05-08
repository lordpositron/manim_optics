manim_optics.lenses
===================

.. py:module:: manim_optics.lenses

.. autoapi-nested-parse::

   Lenses - Thin lens implementations
   ==================================

   This module provides lens classes for optical simulations.



Classes
-------

.. autoapisummary::

   manim_optics.lenses.ThinLens
   manim_optics.lenses.ConvergingLens
   manim_optics.lenses.DivergingLens


Module Contents
---------------

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



.. py:class:: ConvergingLens(focal_length: float = 2.0, **kwargs)

   Bases: :py:obj:`ThinLens`


   Converging (convex) lens with positive focal length.


.. py:class:: DivergingLens(focal_length: float = -2.0, **kwargs)

   Bases: :py:obj:`ThinLens`


   Diverging (concave) lens with negative focal length.


