manim_optics.miscellaneous
==========================

.. py:module:: manim_optics.miscellaneous

.. autoapi-nested-parse::

   Miscellaneous - Utility classes for optical simulations
   =======================================================

   This module provides utility classes like graticules for measurements and references.



Classes
-------

.. autoapisummary::

   manim_optics.miscellaneous.Graticule
   manim_optics.miscellaneous.LinearGraticule
   manim_optics.miscellaneous.CrossGraticule
   manim_optics.miscellaneous.GridGraticule


Module Contents
---------------

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



.. py:class:: LinearGraticule(direction: numpy.ndarray = RIGHT, skip_zero_label: bool = False, **kwargs)

   Bases: :py:obj:`Graticule`


   Linear graticule - a single graduated line.

   Useful for measuring distances along one axis.


   .. py:attribute:: skip_zero_label
      :value: False



   .. py:attribute:: direction


   .. py:attribute:: perpendicular


.. py:class:: CrossGraticule(x_length: float | None = None, y_length: float | None = None, **kwargs)

   Bases: :py:obj:`Graticule`


   Cross graticule - two perpendicular graduated axes.

   Useful for 2D coordinate measurements (like Cartesian axes).


   .. py:attribute:: x_length


   .. py:attribute:: y_length


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



