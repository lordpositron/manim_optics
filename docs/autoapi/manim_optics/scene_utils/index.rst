manim_optics.scene_utils
========================

.. py:module:: manim_optics.scene_utils

.. autoapi-nested-parse::

   Optical Scene Utilities
   =======================

   Helper functions and classes for creating optical scenes.



Classes
-------

.. autoapisummary::

   manim_optics.scene_utils.OpticalScene


Functions
---------

.. autoapisummary::

   manim_optics.scene_utils.create_object_arrow
   manim_optics.scene_utils.create_image_arrow
   manim_optics.scene_utils.calculate_image_position


Module Contents
---------------

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


