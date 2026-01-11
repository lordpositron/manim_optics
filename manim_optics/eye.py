"""
Eye - Composite optical system modeling the human eye
=====================================================

This module provides the Eye class for optical simulations.
"""

import numpy as np
from manim import *
from .lenses import ConvergingLens
from .beam_stops import CircularAperture, ArcBeamStop


class Eye(VGroup):
    """
    Simplified model of an eye for optical simulations.

    Components:
    - Lens (cornea + crystalline lens simplified as thin lens)
    - Optional CircularAperture (pupil/iris)
    - ArcBeamStop (retina - curved detector)

    All components are positioned relative to the lens center.
    Use get_optical_elements() to get the ordered list for ray tracing.
    """

    def __init__(
        self,
        focal_length: float = 2.0,
        lens_diameter: float = 1.0,
        pupil_diameter: float = 0.4,
        include_pupil: bool = True,
        focal_delta: float = 0.0,
        show_focal_point: bool = False,
        show_cornea: bool = False,
        cornea_thickness: float = 0.1,
        lens_color=BLUE_D,
        pupil_color=BLUE_C,
        retina_color=WHITE,
        fill_color=BLUE_D,
        **kwargs
    ):
        """
        Initialize an eye model.

        Parameters
        ----------
        focal_length : float
            Focal length of the eye lens (cornea + crystalline)
        lens_diameter : float
            Diameter (height) of the lens
        pupil_diameter : float
            Diameter of the pupil aperture
        include_pupil : bool
            Whether to include a pupil aperture
        lens_color : str
            Color of the lens
        pupil_color : str
            Color of the pupil
        retina_color : str
            Color of the retina

        Notes
        -----
        The retina radius and angle are calculated automatically from the focal length
        using geometric relationships defined by lens_entering and aperture_entering parameters.
        """
        super().__init__(**kwargs)

        self.focal_length = focal_length
        self.lens_diameter = lens_diameter
        self.pupil_diameter = pupil_diameter
        self.delta_focal = focal_delta
        self.show_focal_point = show_focal_point
        self.fill_color = fill_color
        self.retina_color = retina_color
        self.lens_color = lens_color
        self.pupil_color = pupil_color
        self.fill_opacity = 0.0
        if self.fill_color is not None:
            self.fill_opacity = 0.2

        self.show_cornea = show_cornea
        self.cornea_thickness = cornea_thickness

        self.lens_entering = 0.2
        self.aperture_enterring = 0.1

        self.retina_radius = (focal_length - focal_delta) / (2 - self.lens_entering)

        self.total_aperture_length = (
            2
            * self.retina_radius
            * np.sqrt(self.aperture_enterring * (2 - self.aperture_enterring))
        )

        self.retina_angle = 2 * np.pi - 2 * np.arctan(
            self.total_aperture_length
            / (2 * self.retina_radius * (1 - self.aperture_enterring))
        )

        self.include_pupil = include_pupil

        # Create components
        self._create_eye_components()

    def _create_eye_components(self):
        """Create and position all eye components."""

        # 1. Lens (at origin, center of reference)
        self.lens = ConvergingLens(
            focal_length=self.focal_length,
            height=self.lens_diameter,
            color=self.lens_color,
            tip_length=0.1,
            show_focal_points=self.show_focal_point,
        )
        self.lens.move_to(ORIGIN)
        self.add(self.lens)

        # 2. Optional pupil (just after lens)
        if self.include_pupil:
            # Pupil opening is the actual pupil diameter
            self.pupil = CircularAperture(
                radius=self.pupil_diameter / 2,
                total_length=self.total_aperture_length,
                line_color=self.pupil_color,
                line_stroke_width=4,
            )

            self.pupil.shift(
                RIGHT
                * self.retina_radius
                * (self.aperture_enterring - self.lens_entering)
            )
            self.add(self.pupil)
            if self.show_cornea:
                self.cornea = ArcBetweenPoints(
                    self.pupil.get_top_coordinates(),
                    self.pupil.get_bottom_coordinates(),
                    radius=self.total_aperture_length / 1.5,
                    stroke_width=0,
                    fill_color=self.fill_color,
                    fill_opacity=self.fill_opacity,
                )
                self.cornea.next_to(self.pupil, LEFT, buff=0)
                self.add(self.cornea)
        else:
            self.pupil = None

        # 3. Retina (curved detector at back of eye)
        # Position it so the light focuses on it
        # For a simple model: retina is approximately at focal length from lens

        self.retina = ArcBeamStop(
            radius=self.retina_radius,
            arc_angle=self.retina_angle,
            fill_color=self.fill_color,
            fill_opacity=self.fill_opacity,
            stroke_color=self.retina_color,
        )

        self.retina.shift(RIGHT * self.retina_radius * (1 - self.lens_entering))
        self.add(self.retina)

    def get_optical_elements(self):
        """
        Get ordered list of optical elements for ray tracing.

        Returns
        -------
        list
            [lens, pupil (optional), retina] in order of interaction
        """
        elements = [self.lens]

        if self.pupil is not None:
            elements.append(self.pupil)

        elements.append(self.retina)

        return elements

    def set_focal_length(self, new_focal: float):
        """
        Update the focal length of the eye lens.

        This simulates accommodation (changing focus).

        Parameters
        ----------
        new_focal : float
            New focal length
        """
        self.focal_length = new_focal
        self.lens.focal_length = new_focal
        return self

    def set_pupil_diameter(self, new_diameter: float):
        """
        Update pupil diameter (simulates dilation/constriction).

        Parameters
        ----------
        new_diameter : float
            New pupil diameter
        """
        if self.pupil is not None:
            self.pupil_diameter = new_diameter
            self.pupil.aperture_radius = new_diameter / 2
            # Recreate visual
            self.pupil.remove(*self.pupil.submobjects)
            self.pupil._create_visual()
        return self

    def shift(self, *vectors):
        """Override shift to update retina curvature center."""
        # Apply shift to VGroup (which shifts all submobjects)
        super().shift(*vectors)

        # Manually update retina's curvature center
        for vector in vectors:
            self.retina._curvature_center += vector

        return self

    def move_to(self, point_or_mobject, aligned_edge=ORIGIN, clobber_submobjects=False):
        """Override move_to to update retina curvature center."""
        # Get displacement
        old_center = self.get_center()

        # Apply move_to to VGroup
        super().move_to(point_or_mobject, aligned_edge, clobber_submobjects)

        # Calculate displacement and update retina's curvature center
        new_center = self.get_center()
        displacement = new_center - old_center
        self.retina._curvature_center += displacement

        return self
