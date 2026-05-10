manim_optics.real_lenses
========================

.. py:module:: manim_optics.real_lenses

.. autoapi-nested-parse::

   Real Spherical Lenses - Thick lens with exact Snell-Descartes refraction
   =========================================================================

   Lenses defined by two spherical surfaces with true vectorial refraction.
   No paraxial approximation in the ray tracing.

   Sign convention (same as SphericalMirror, French algebraic):
       R > 0  →  center of curvature to the RIGHT of the surface vertex
       R < 0  →  center of curvature to the LEFT  of the surface vertex

   For a standard biconvex (converging) lens:   R1 > 0, R2 < 0
   For a standard biconcave (diverging) lens:   R1 < 0, R2 > 0



Classes
-------

.. autoapisummary::

   manim_optics.real_lenses.SphericalLens
   manim_optics.real_lenses.BiconvexLens
   manim_optics.real_lenses.BiconcaveLens
   manim_optics.real_lenses.PlanoConvexLens
   manim_optics.real_lenses.PlanoConcaveLens


Module Contents
---------------

.. py:class:: SphericalLens(R1: float = 4.0, R2: float = -4.0, thickness: float = 0.5, n: float = 1.5, diameter: float = 3.0, n_outside: float = 1.0, fill_color=BLUE, fill_opacity: float = 0.25, stroke_width: float = 2.0, offset: numpy.ndarray | None = None, tilt_deg: float = 0.0, birefringence: float = 0.0, **kwargs)

   Bases: :py:obj:`manim_optics.base.OpticalElement`


   Thick spherical lens defined by two refracting surfaces.

   Ray tracing uses the exact vectorial Snell-Descartes law at each surface.
   The lens handles both surfaces internally in ``propagate_ray``, returning
   a teleport exit point on the second surface so DynamicRay continuity is
   preserved correctly.

   :param R1: Radius of curvature of the front surface.
              R1 > 0 → convex front (biconvex-type),  R1 < 0 → concave front.
   :type R1: float
   :param R2: Radius of curvature of the back surface.
              R2 < 0 → convex back  (biconvex-type),  R2 > 0 → concave back.
   :type R2: float
   :param thickness: Center thickness of the lens (along the optical axis).
   :type thickness: float
   :param n: Refractive index of the glass.
   :type n: float
   :param diameter: Clear aperture diameter.
   :type diameter: float
   :param n_outside: Refractive index of the surrounding medium (default 1.0 = air).
   :type n_outside: float
   :param fill_color: Fill color of the lens body.
   :type fill_color: color
   :param fill_opacity: Opacity of the lens fill (0–1).
   :type fill_opacity: float
   :param stroke_width: Stroke width of the lens outline.
   :type stroke_width: float
   :param offset: Initial decentering (x, y) shift relative to where the lens is placed.
   :type offset: np.ndarray
   :param tilt_deg: Initial tilt angle in degrees around the lens center.
   :type tilt_deg: float
   :param birefringence: Placeholder — not yet used in ray tracing.
   :type birefringence: float


   .. py:attribute:: R1_tracker


   .. py:attribute:: R2_tracker


   .. py:attribute:: thickness_tracker


   .. py:attribute:: n_tracker


   .. py:attribute:: diameter_tracker


   .. py:attribute:: n_outside_tracker


   .. py:attribute:: tilt_tracker


   .. py:attribute:: birefringence_tracker


   .. py:attribute:: offset_x_tracker


   .. py:attribute:: offset_y_tracker


   .. py:method:: rebuild() -> None

      Recreate the lens visual — kept for backward compatibility.



   .. py:method:: get_optical_plane_position() -> numpy.ndarray

      Get the position of the optical plane (where rays interact).

      For most elements, this is the same as get_center().
      Override this in subclasses if the optical plane differs from the VGroup center.

      :returns: Position of the optical plane
      :rtype: np.ndarray



   .. py:method:: intersect(ray_start: numpy.ndarray, ray_direction: numpy.ndarray) -> tuple[numpy.ndarray | None, bool]

      Return the first surface (front or back) hit by the ray.



   .. py:method:: propagate_ray(ray_start: numpy.ndarray, ray_direction: numpy.ndarray, intersection_point: numpy.ndarray) -> tuple

      Refract through both surfaces using vectorial Snell-Descartes.

      :returns: * *(new_direction, True, exit_point)* -- exit_point is the world-space point on the second surface, used by
                  DynamicRay as a teleport so the ray continues from there.
                * *(ray_direction, False)* -- If the ray is blocked (TIR, misses inner surface, outside aperture).



   .. py:method:: get_transfer_matrix() -> numpy.ndarray

      Paraxial ABCD matrix (for reference only; ray tracing uses exact Snell).

      System matrix = M_refr2 @ M_prop @ M_refr1
      Convention: state vector [y, θ] with θ the geometric ray angle.



.. py:class:: BiconvexLens(R: float = 4.0, **kwargs)

   Bases: :py:obj:`SphericalLens`


   Symmetric biconvex lens (R1 = |R|, R2 = -|R|).

   :param R: Absolute value of the radius of curvature for both surfaces (R > 0).
   :type R: float


.. py:class:: BiconcaveLens(R: float = 4.0, **kwargs)

   Bases: :py:obj:`SphericalLens`


   Symmetric biconcave lens (R1 = -|R|, R2 = |R|).

   :param R: Absolute value of the radius of curvature for both surfaces (R > 0).
   :type R: float


.. py:class:: PlanoConvexLens(R: float = 4.0, flat_front: bool = True, **kwargs)

   Bases: :py:obj:`SphericalLens`


   Plano-convex lens: flat front, convex back (or vice-versa).

   :param R: Radius of curvature of the curved surface (R > 0 → back surface convex).
   :type R: float
   :param flat_front: If True (default), front surface is flat; if False, back is flat.
   :type flat_front: bool


.. py:class:: PlanoConcaveLens(R: float = 4.0, flat_front: bool = True, **kwargs)

   Bases: :py:obj:`SphericalLens`


   Plano-concave lens: flat front, concave back (or vice-versa).

   :param R: Radius of curvature of the curved surface (R > 0).
   :type R: float
   :param flat_front: If True (default), front surface is flat; if False, back is flat.
   :type flat_front: bool


