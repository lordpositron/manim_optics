manim_optics.eye
================

.. py:module:: manim_optics.eye

.. autoapi-nested-parse::

   Eye - Composite optical system modeling the human eye
   =====================================================

   This module provides the Eye class for optical simulations.



Classes
-------

.. autoapisummary::

   manim_optics.eye.Eye


Module Contents
---------------

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



