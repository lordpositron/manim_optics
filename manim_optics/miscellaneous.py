"""
Miscellaneous - Utility classes for optical simulations
=======================================================

This module provides utility classes like graticules for measurements and references.
"""

import numpy as np
from manim import *
from typing import Optional, Literal


class Graticule(VGroup):
    """
    Base class for graticules (graduated scales/grids).

    A graticule is a graduated reference scale used for measurements.
    This base class provides common functionality for all graticule types.
    """

    def __init__(
        self,
        length: float = 10.0,
        unit_length: float = 1.0,
        primary_interval: int = 5,
        secondary_interval: int = 1,
        tick_position: Literal["inside", "outside", "centered"] = "centered",
        primary_tick_length: float = 0.2,
        secondary_tick_length: float = 0.1,
        tick_angle: float = 90 * DEGREES,
        global_angle: float = 0.0,
        primary_stroke_width: float = 2.5,
        secondary_stroke_width: float = 1.5,
        color: str = WHITE,
        zero_position: float = 0.0,
        show_main_line: bool = False,
        show_labels: bool = True,
        label_offset: float = 0.3,
        label_font_size: int = 18,
        label_rotation: float = 0.0,
        decimal_places: int = 1,
        **kwargs,
    ):
        """
        Initialize a graticule.

        Parameters
        ----------
        length : float
            Total length of the graticule
        unit_length : float
            Length corresponding to 1 unit in the graduation
        primary_interval : int
            Interval between primary graduations (in units)
        secondary_interval : int
            Interval between secondary graduations (in units)
        tick_position : str
            Position of ticks: "inside", "outside", or "centered"
        primary_tick_length : float
            Length of primary tick marks
        secondary_tick_length : float
            Length of secondary tick marks
        tick_angle : float
            Angle of tick marks relative to the graticule axis (in radians)
        global_angle : float
            Global rotation angle of the entire graticule (in radians)
        primary_stroke_width : float
            Stroke width for primary ticks and axis
        secondary_stroke_width : float
            Stroke width for secondary ticks
        color : str
            Color of the graticule
        zero_position : float
            Position of zero along the graticule (-0.5 to 0.5, 0 is center)
        show_main_line : bool
            Whether to display the main axis line (default: False, only graduations shown)
        show_labels : bool
            Whether to display numerical labels
        label_offset : float
            Distance of labels from the tick marks
        label_font_size : int
            Font size for labels
        label_rotation : float
            Rotation of label text (in radians)
        decimal_places : int
            Number of decimal places for labels
        """
        super().__init__(**kwargs)

        # Store parameters
        self.length = length
        self.unit_length = unit_length
        self.primary_interval = primary_interval
        self.secondary_interval = secondary_interval
        self.tick_position = tick_position
        self.primary_tick_length = primary_tick_length
        self.secondary_tick_length = secondary_tick_length
        self.tick_angle = tick_angle
        self.global_angle = global_angle
        self.primary_stroke_width = primary_stroke_width
        self.secondary_stroke_width = secondary_stroke_width
        self.color = color
        self.zero_position = zero_position
        self.show_main_line = show_main_line
        self.show_labels = show_labels
        self.label_offset = label_offset
        self.label_font_size = label_font_size
        self.label_rotation = label_rotation
        self.decimal_places = decimal_places

        # Will be populated by subclasses
        self.axis_line = None
        self.ticks = VGroup()
        self.labels = VGroup()

    def _get_tick_direction(self, perpendicular_dir: np.ndarray) -> tuple:
        """
        Calculate tick start and end based on position setting.

        Parameters
        ----------
        perpendicular_dir : np.ndarray
            Direction perpendicular to the axis

        Returns
        -------
        tuple
            (start_multiplier, end_multiplier) for tick positioning
        """
        if self.tick_position == "inside":
            return (0, -1)
        elif self.tick_position == "outside":
            return (0, 1)
        else:  # centered
            return (-0.5, 0.5)

    def _create_tick(
        self,
        position: np.ndarray,
        perpendicular_dir: np.ndarray,
        tick_length: float,
        stroke_width: float,
    ) -> Line:
        """
        Create a single tick mark.

        Parameters
        ----------
        position : np.ndarray
            Position along the axis
        perpendicular_dir : np.ndarray
            Direction perpendicular to the axis
        tick_length : float
            Length of the tick
        stroke_width : float
            Stroke width

        Returns
        -------
        Line
            The tick mark
        """
        start_mult, end_mult = self._get_tick_direction(perpendicular_dir)

        # Rotate perpendicular direction by tick_angle
        cos_a = np.cos(self.tick_angle - PI / 2)
        sin_a = np.sin(self.tick_angle - PI / 2)

        # Apply rotation in 2D (xy plane)
        perp_x, perp_y = perpendicular_dir[0], perpendicular_dir[1]
        rotated_perp = np.array(
            [perp_x * cos_a - perp_y * sin_a, perp_x * sin_a + perp_y * cos_a, 0]
        )

        start = position + rotated_perp * tick_length * start_mult
        end = position + rotated_perp * tick_length * end_mult

        return Line(start, end, stroke_width=stroke_width, color=self.color)

    def _create_label(
        self, value: float, position: np.ndarray, perpendicular_dir: np.ndarray
    ) -> Text:
        """
        Create a numerical label.

        Parameters
        ----------
        value : float
            The numerical value
        position : np.ndarray
            Position along the axis
        perpendicular_dir : np.ndarray
            Direction perpendicular to the axis

        Returns
        -------
        Text
            The label
        """
        # Format the value
        if self.decimal_places == 0:
            text = str(int(value))
        else:
            text = f"{value:.{self.decimal_places}f}"

        label = Text(text, font_size=self.label_font_size, color=self.color)

        # Position the label
        _, end_mult = self._get_tick_direction(perpendicular_dir)
        offset_dir = perpendicular_dir if end_mult > 0 else -perpendicular_dir

        label.move_to(position + offset_dir * self.label_offset)

        # Apply rotation
        if self.label_rotation != 0:
            label.rotate(self.label_rotation)

        return label

    def highlight_tick(self, value: float, color: str = YELLOW, scale: float = 1.5):
        """
        Highlight a specific graduation.

        Parameters
        ----------
        value : float
            The value to highlight
        color : str
            Color for highlighting
        scale : float
            Scale factor for the highlighted tick

        Returns
        -------
        VGroup
            Group containing the highlighted elements
        """
        # To be implemented by subclasses based on their structure
        pass

    def create_animation(
        self, run_time: float = 1.0, lag_ratio: float = 0.05
    ) -> Animation:
        """
        Create an animation for the graticule appearance.

        Parameters
        ----------
        run_time : float
            Duration of the animation
        lag_ratio : float
            Lag between different elements

        Returns
        -------
        Animation
            Animation for the graticule
        """
        animations = []

        if self.axis_line is not None:
            animations.append(Create(self.axis_line))

        animations.append(Create(self.ticks))

        if self.show_labels and len(self.labels) > 0:
            animations.append(FadeIn(self.labels))

        return AnimationGroup(*animations, lag_ratio=lag_ratio, run_time=run_time)

    def fade_out_animation(self, run_time: float = 0.5) -> Animation:
        """
        Create a fade out animation.

        Parameters
        ----------
        run_time : float
            Duration of the animation

        Returns
        -------
        Animation
            Fade out animation
        """
        return FadeOut(self, run_time=run_time)


class LinearGraticule(Graticule):
    """
    Linear graticule - a single graduated line.

    Useful for measuring distances along one axis.
    """

    def __init__(self, direction: np.ndarray = RIGHT, **kwargs):
        """
        Initialize a linear graticule.

        Parameters
        ----------
        direction : np.ndarray
            Direction of the graticule axis (will be normalized)
        **kwargs
            Additional arguments passed to Graticule
        """
        super().__init__(**kwargs)

        # Normalize direction
        self.direction = direction / np.linalg.norm(direction)
        self.perpendicular = np.array([-self.direction[1], self.direction[0], 0])

        # Create the graticule
        self._create_graticule()

        # Apply global rotation
        if self.global_angle != 0:
            self.rotate(self.global_angle)

    def _create_graticule(self):
        """Create the visual representation of the linear graticule."""
        # Calculate start and end positions accounting for zero_position
        # zero_position: -0.5 = left, 0 = center, 0.5 = right
        offset = self.zero_position * self.length
        start_pos = -self.length / 2 * self.direction - offset * self.direction
        end_pos = self.length / 2 * self.direction - offset * self.direction

        # Create main axis line only if requested
        if self.show_main_line:
            self.axis_line = Line(
                start_pos,
                end_pos,
                stroke_width=self.primary_stroke_width,
                color=self.color,
            )
            self.add(self.axis_line)
        else:
            self.axis_line = None

        # Calculate number of units
        num_units = self.length / self.unit_length

        # Determine range based on zero position
        min_value = -num_units / 2 - self.zero_position * num_units
        max_value = num_units / 2 - self.zero_position * num_units

        # Create ticks and labels
        for i in range(
            int(min_value / self.secondary_interval),
            int(max_value / self.secondary_interval) + 1,
        ):
            value = i * self.secondary_interval

            # Position along the axis
            pos = (
                (value + self.zero_position * num_units)
                * self.unit_length
                * self.direction
            )

            # Determine if primary or secondary tick
            is_primary = (i * self.secondary_interval) % self.primary_interval == 0

            if is_primary:
                tick = self._create_tick(
                    pos,
                    self.perpendicular,
                    self.primary_tick_length,
                    self.primary_stroke_width,
                )

                # Add label for primary ticks
                if self.show_labels:
                    label = self._create_label(value, pos, self.perpendicular)
                    self.labels.add(label)
            else:
                tick = self._create_tick(
                    pos,
                    self.perpendicular,
                    self.secondary_tick_length,
                    self.secondary_stroke_width,
                )

            self.ticks.add(tick)

        self.add(self.ticks)

        if self.show_labels:
            self.add(self.labels)


class CrossGraticule(Graticule):
    """
    Cross graticule - two perpendicular graduated axes.

    Useful for 2D coordinate measurements (like Cartesian axes).
    """

    def __init__(
        self,
        x_length: Optional[float] = None,
        y_length: Optional[float] = None,
        **kwargs,
    ):
        """
        Initialize a cross graticule.

        Parameters
        ----------
        x_length : float, optional
            Length of horizontal axis (if None, uses length parameter)
        y_length : float, optional
            Length of vertical axis (if None, uses length parameter)
        **kwargs
            Additional arguments passed to Graticule
        """
        super().__init__(**kwargs)

        # Use provided lengths or default to the base length
        self.x_length = x_length if x_length is not None else self.length
        self.y_length = y_length if y_length is not None else self.length

        # Create the cross graticule
        self._create_graticule()

        # Apply global rotation
        if self.global_angle != 0:
            self.rotate(self.global_angle)

    def _create_graticule(self):
        """Create the visual representation of the cross graticule."""
        # Create horizontal axis (X)
        self.x_axis = LinearGraticule(
            direction=RIGHT,
            length=self.x_length,
            unit_length=self.unit_length,
            primary_interval=self.primary_interval,
            secondary_interval=self.secondary_interval,
            tick_position=self.tick_position,
            primary_tick_length=self.primary_tick_length,
            secondary_tick_length=self.secondary_tick_length,
            tick_angle=self.tick_angle,
            primary_stroke_width=self.primary_stroke_width,
            secondary_stroke_width=self.secondary_stroke_width,
            color=self.color,
            zero_position=self.zero_position,
            show_main_line=self.show_main_line,
            show_labels=self.show_labels,
            label_offset=self.label_offset,
            label_font_size=self.label_font_size,
            label_rotation=self.label_rotation,
            decimal_places=self.decimal_places,
        )

        # Create vertical axis (Y)
        self.y_axis = LinearGraticule(
            direction=UP,
            length=self.y_length,
            unit_length=self.unit_length,
            primary_interval=self.primary_interval,
            secondary_interval=self.secondary_interval,
            tick_position=self.tick_position,
            primary_tick_length=self.primary_tick_length,
            secondary_tick_length=self.secondary_tick_length,
            tick_angle=self.tick_angle,
            primary_stroke_width=self.primary_stroke_width,
            secondary_stroke_width=self.secondary_stroke_width,
            color=self.color,
            zero_position=self.zero_position,
            show_main_line=self.show_main_line,
            show_labels=self.show_labels,
            label_offset=self.label_offset,
            label_font_size=self.label_font_size,
            label_rotation=self.label_rotation,
            decimal_places=self.decimal_places,
        )

        self.add(self.x_axis, self.y_axis)

        # Collect ticks and labels for animation purposes
        self.ticks.add(self.x_axis.ticks, self.y_axis.ticks)
        self.labels.add(self.x_axis.labels, self.y_axis.labels)


class GridGraticule(Graticule):
    """
    Grid graticule - a 2D grid of graduated lines.

    Useful for precise 2D measurements and alignment.
    """

    def __init__(
        self,
        width: Optional[float] = None,
        height: Optional[float] = None,
        grid_stroke_width: float = 0.5,
        show_grid_labels: bool = False,
        **kwargs,
    ):
        """
        Initialize a grid graticule.

        Parameters
        ----------
        width : float, optional
            Width of the grid (if None, uses length parameter)
        height : float, optional
            Height of the grid (if None, uses length parameter)
        grid_stroke_width : float
            Stroke width for grid lines (typically thinner than ticks)
        show_grid_labels : bool
            Whether to show labels on the grid lines
        **kwargs
            Additional arguments passed to Graticule
        """
        super().__init__(**kwargs)

        # Use provided dimensions or default to the base length
        self.width = width if width is not None else self.length
        self.height = height if height is not None else self.length
        self.grid_stroke_width = grid_stroke_width
        self.show_grid_labels = show_grid_labels

        # Create the grid graticule
        self._create_graticule()

        # Apply global rotation
        if self.global_angle != 0:
            self.rotate(self.global_angle)

    def _create_graticule(self):
        """Create the visual representation of the grid graticule."""
        # Create border frame only if requested
        if self.show_main_line:
            self.frame = Rectangle(
                width=self.width,
                height=self.height,
                stroke_width=self.primary_stroke_width,
                color=self.color,
                fill_opacity=0,
            )
            self.add(self.frame)
        else:
            self.frame = None

        # Calculate number of units
        num_x_units = self.width / self.unit_length
        num_y_units = self.height / self.unit_length

        # Grid lines
        self.grid_lines = VGroup()

        # Vertical grid lines
        for i in range(
            int(-num_x_units / 2 / self.secondary_interval),
            int(num_x_units / 2 / self.secondary_interval) + 1,
        ):
            value = i * self.secondary_interval
            x_pos = (value + self.zero_position * num_x_units) * self.unit_length

            # Check if within bounds
            if abs(x_pos) <= self.width / 2:
                is_primary = (i * self.secondary_interval) % self.primary_interval == 0

                line = Line(
                    [x_pos, -self.height / 2, 0],
                    [x_pos, self.height / 2, 0],
                    stroke_width=(
                        self.primary_stroke_width
                        if is_primary
                        else self.grid_stroke_width
                    ),
                    color=self.color,
                    stroke_opacity=1.0 if is_primary else 0.5,
                )
                self.grid_lines.add(line)

                # Add labels for primary lines
                if is_primary and self.show_labels and value != 0:
                    label = Text(
                        (
                            f"{value:.{self.decimal_places}f}"
                            if self.decimal_places > 0
                            else str(int(value))
                        ),
                        font_size=self.label_font_size,
                        color=self.color,
                    )
                    label.next_to([x_pos, -self.height / 2, 0], DOWN, buff=0.1)
                    if self.label_rotation != 0:
                        label.rotate(self.label_rotation)
                    self.labels.add(label)

        # Horizontal grid lines
        for i in range(
            int(-num_y_units / 2 / self.secondary_interval),
            int(num_y_units / 2 / self.secondary_interval) + 1,
        ):
            value = i * self.secondary_interval
            y_pos = (value + self.zero_position * num_y_units) * self.unit_length

            # Check if within bounds
            if abs(y_pos) <= self.height / 2:
                is_primary = (i * self.secondary_interval) % self.primary_interval == 0

                line = Line(
                    [-self.width / 2, y_pos, 0],
                    [self.width / 2, y_pos, 0],
                    stroke_width=(
                        self.primary_stroke_width
                        if is_primary
                        else self.grid_stroke_width
                    ),
                    color=self.color,
                    stroke_opacity=1.0 if is_primary else 0.5,
                )
                self.grid_lines.add(line)

                # Add labels for primary lines
                if is_primary and self.show_labels and value != 0:
                    label = Text(
                        (
                            f"{value:.{self.decimal_places}f}"
                            if self.decimal_places > 0
                            else str(int(value))
                        ),
                        font_size=self.label_font_size,
                        color=self.color,
                    )
                    label.next_to([-self.width / 2, y_pos, 0], LEFT, buff=0.1)
                    if self.label_rotation != 0:
                        label.rotate(self.label_rotation)
                    self.labels.add(label)

        self.add(self.grid_lines)

        if self.show_labels:
            self.add(self.labels)

        # Store for animation
        self.ticks = self.grid_lines

    def create_animation(
        self, run_time: float = 1.0, lag_ratio: float = 0.02
    ) -> Animation:
        """
        Create an animation for the grid appearance.

        Parameters
        ----------
        run_time : float
            Duration of the animation
        lag_ratio : float
            Lag between different elements

        Returns
        -------
        Animation
            Animation for the grid
        """
        animations = []

        if self.frame is not None:
            animations.append(Create(self.frame))
        animations.append(Create(self.grid_lines))

        if self.show_labels and len(self.labels) > 0:
            animations.append(FadeIn(self.labels))

        return AnimationGroup(*animations, lag_ratio=lag_ratio, run_time=run_time)
