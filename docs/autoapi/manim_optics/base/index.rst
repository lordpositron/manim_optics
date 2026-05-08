manim_optics.base
=================

.. py:module:: manim_optics.base

.. autoapi-nested-parse::

   Base Optical Element - Abstract base class for all optical elements
   ===================================================================

   This module provides the base OpticalElement class and utility functions.



Classes
-------

.. autoapisummary::

   manim_optics.base.OpticalElement


Functions
---------

.. autoapisummary::

   manim_optics.base.rotate_vector_2d


Module Contents
---------------

.. py:function:: rotate_vector_2d(vector: numpy.ndarray, angle: float) -> numpy.ndarray

   Rotate a 2D vector by an angle around the z-axis.

   :param vector: The vector to rotate (3D, but rotation is in xy-plane)
   :type vector: np.ndarray
   :param angle: Angle in radians
   :type angle: float

   :returns: Rotated vector
   :rtype: np.ndarray


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



