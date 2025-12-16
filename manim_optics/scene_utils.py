"""
Optical Scene Utilities
=======================

Helper functions and classes for creating optical scenes.
"""

import numpy as np
from manim import *
from typing import List


class OpticalScene(Scene):
    """
    Extension of Manim's Scene class with utilities for optical simulations.

    Provides convenient methods for setting up optical experiments and
    managing optical elements and rays.
    """

    def set_theme(self, theme: str = "light"):
        """
        Set the color theme for the scene.

        Parameters
        ----------
        theme : str
            Theme name ("light" or "dark")
        """
        if theme == "light":
            self.camera.background_color = WHITE
        elif theme == "dark":
            self.camera.background_color = BLACK
        else:
            raise ValueError("Theme must be 'light' or 'dark'.")

    def add_debugging_grid(self, spacing: float = 1.0, color: str = GREY_D):
        """
        Add a debugging grid to the scene for alignment purposes.

        Parameters
        ----------
        spacing : float
            Spacing between grid lines
        color : str
            Color of the grid lines
        """
        grid = NumberPlane().add_coordinates()
        self.add(grid)
        return grid

    def get_optical_axis_animation(
        self,
        length: float = 12.0,
        color: str = GREY_C,
        y_position: float = 0.0,
        stroke_width: float = 2,
    ) -> Animation:
        """
        Create an animation to add a horizontal optical axis to the scene.
        Parameters
        ----------
        length : float
            Length of the axis
        color : str
            Color of the axis
        animate : bool
            If True, animate the axis growing from center
        y_position : float
            Vertical position of the axis
        Returns
        -------
        Animation
            Animation to add the optical axis
        """

        # Start with a point at center
        self.optical_axis = Line(
            ORIGIN + UP * y_position,
            ORIGIN + UP * y_position,
            color=color,
            stroke_width=stroke_width,
        )
        self.add(self.optical_axis)

        return self.optical_axis.animate.put_start_and_end_on(
            LEFT * length / 2 + UP * y_position,
            RIGHT * length / 2 + UP * y_position,
        )

    def setup_optical_axis(
        self,
        length: float = 12.0,
        color: str = GREY_C,
        animate: bool = False,
        y_position: float = 0.0,
        stroke_width: float = 2,
    ):
        """
        Add a horizontal optical axis to the scene.

        Parameters
        ----------
        length : float
            Length of the axis
        color : str
            Color of the axis
        animate : bool
            If True, animate the axis growing from center
        y_position : float
            Vertical position of the axis
        """
        if animate:
            animation = self.get_optical_axis_animation(
                length=length,
                color=color,
                y_position=y_position,
                stroke_width=stroke_width,
            )
            # Animate it growing to full length
            self.play(
                animation,
                run_time=1.5,
            )
        else:
            self.optical_axis = Line(
                LEFT * length / 2 + UP * y_position,
                RIGHT * length / 2 + UP * y_position,
                color=color,
                stroke_width=stroke_width,
            )
            self.add(self.optical_axis)

        return self.optical_axis

    def add_focal_length_labels(
        self, lens, font_size: int = 24, animate: bool = False, run_time: float = 1.0
    ):
        """
        Add labels showing the focal length of a lens.

        Parameters
        ----------
        lens : ThinLens
            The lens to label
        font_size : int
            Size of the label text
        """
        f_text = MathTex(
            f"f'= {lens.focal_length*10:.1f}\\text{{mm}}", font_size=font_size
        )
        f_text.next_to(lens, DOWN, buff=0.5)
        if animate:
            self.play(Write(f_text), run_time=run_time)
        else:
            self.add(f_text)
        return f_text

    def add_distance_marker(
        self,
        start_point: np.ndarray,
        end_point: np.ndarray,
        label: str,
        direction: np.ndarray = DOWN,
        font_size: int = 20,
    ):
        """
        Add a distance measurement marker with label.

        Parameters
        ----------
        start_point : np.ndarray
            Start of the distance
        end_point : np.ndarray
            End of the distance
        label : str
            Text label for the distance
        direction : np.ndarray
            Direction to offset the marker
        font_size : int
            Size of label text
        """
        # Create double-headed arrow
        distance_line = DoubleArrow(
            start_point,
            end_point,
            buff=0,
            color=GREY_B,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.1,
        )

        # Create label
        distance_label = Text(label, font_size=font_size, color=GREY_B)
        center = (start_point + end_point) / 2
        distance_label.next_to(center, direction, buff=0.2)

        marker = VGroup(distance_line, distance_label)
        self.add(marker)
        return marker

    def add_label_to_object(
        self,
        obj: Mobject,
        label: str,
        font_size: int = 24,
        direction: np.ndarray = DOWN,
        buff: float = 0.2,
        color: str = WHITE,
        latex: bool = False,
        animate: bool = False,
        run_time: float = 1.0,
    ):
        """
        Add a text label to an optical object.

        Parameters
        ----------
        obj : Mobject
            The object to label
        label : str
            The text of the label
        font_size : int
            Size of the label text
        direction : np.ndarray
            Direction to offset the label from the object
        buff : float
            Buffer distance between object and label
        color : str
            Color of the label text
        """
        if latex:
            label_text = MathTex(label, font_size=font_size, color=color)
        else:
            label_text = Tex(label, font_size=font_size, color=color)
        label_text.next_to(obj, direction, buff=buff)

        if animate:
            self.play(Write(label_text), run_time=run_time)
        else:
            self.add(label_text)
        return label_text


def create_object_arrow(
    position: np.ndarray, height: float = 1.0, color: str = WHITE, label: str = "Object"
) -> VGroup:
    """
    Create a standard object arrow for optics diagrams.

    Parameters
    ----------
    position : np.ndarray
        Position of the arrow base
    height : float
        Height of the arrow
    color : str
        Color of the arrow
    label : str
        Label text

    Returns
    -------
    VGroup
        Group containing arrow and label
    """
    arrow = Arrow(position, position + UP * height, buff=0, color=color, stroke_width=4)

    label_text = Text(label, font_size=20, color=color)
    label_text.next_to(arrow, LEFT, buff=0.2)

    return VGroup(arrow, label_text)


def create_image_arrow(
    position: np.ndarray,
    height: float = 1.0,
    color: str = BLUE_C,
    label: str = "Image",
    inverted: bool = False,
) -> VGroup:
    """
    Create a standard image arrow for optics diagrams.

    Parameters
    ----------
    position : np.ndarray
        Position of the arrow base
    height : float
        Height of the arrow (negative for inverted image)
    color : str
        Color of the arrow
    label : str
        Label text
    inverted : bool
        Whether the image is inverted

    Returns
    -------
    VGroup
        Group containing arrow and label
    """
    if inverted:
        height = -abs(height)

    arrow = Arrow(position, position + UP * height, buff=0, color=color, stroke_width=4)

    label_text = Text(label, font_size=20, color=color)
    if inverted:
        label_text.next_to(arrow, LEFT, buff=0.2, aligned_edge=DOWN)
    else:
        label_text.next_to(arrow, LEFT, buff=0.2, aligned_edge=UP)

    return VGroup(arrow, label_text)


def calculate_image_position(object_distance: float, focal_length: float) -> tuple:
    """
    Calculate image position using thin lens equation.

    1/f = 1/p + 1/p'

    Parameters
    ----------
    object_distance : float
        Distance from object to lens (positive)
    focal_length : float
        Focal length of lens

    Returns
    -------
    tuple
        (image_distance, magnification, is_real)
        - image_distance: float (positive for real image on opposite side)
        - magnification: float (negative for inverted)
        - is_real: bool (True for real image, False for virtual)
    """
    if abs(object_distance) < 1e-6:
        return float("inf"), float("inf"), True

    # Thin lens equation: 1/f = 1/p + 1/p'
    # Solve for p': p' = 1 / (1/f - 1/p)

    try:
        image_distance = 1 / (1 / focal_length - 1 / object_distance)
    except ZeroDivisionError:
        return float("inf"), float("inf"), True

    # Magnification: m = -p'/p
    magnification = -image_distance / object_distance

    # Real image if on opposite side of lens from object
    is_real = image_distance > 0

    return image_distance, magnification, is_real
