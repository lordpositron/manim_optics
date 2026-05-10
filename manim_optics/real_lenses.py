"""
Real Spherical Lenses - Thick lens with exact Snell-Descartes refraction
=========================================================================

Lenses defined by two spherical surfaces with true vectorial refraction.
No paraxial approximation in the ray tracing.

Sign convention (same as SphericalMirror, French algebraic):
    R > 0  →  center of curvature to the RIGHT of the surface vertex
    R < 0  →  center of curvature to the LEFT  of the surface vertex

For a standard biconvex (converging) lens:   R1 > 0, R2 < 0
For a standard biconcave (diverging) lens:   R1 < 0, R2 > 0
"""

from __future__ import annotations

import numpy as np
from manim import BLUE, DEGREES, ValueTracker, VMobject, VectorizedPoint

from .base import OpticalElement

_FLAT_R_THRESHOLD = 1e7  # treat |R| > this as a flat surface


class SphericalLens(OpticalElement):
    """
    Thick spherical lens defined by two refracting surfaces.

    Ray tracing uses the exact vectorial Snell-Descartes law at each surface.
    The lens handles both surfaces internally in ``propagate_ray``, returning
    a teleport exit point on the second surface so DynamicRay continuity is
    preserved correctly.

    Parameters
    ----------
    R1 : float
        Radius of curvature of the front surface.
        R1 > 0 → convex front (biconvex-type),  R1 < 0 → concave front.
    R2 : float
        Radius of curvature of the back surface.
        R2 < 0 → convex back  (biconvex-type),  R2 > 0 → concave back.
    thickness : float
        Center thickness of the lens (along the optical axis).
    n : float
        Refractive index of the glass.
    diameter : float
        Clear aperture diameter.
    n_outside : float
        Refractive index of the surrounding medium (default 1.0 = air).
    fill_color : color
        Fill color of the lens body.
    fill_opacity : float
        Opacity of the lens fill (0–1).
    stroke_width : float
        Stroke width of the lens outline.
    offset : np.ndarray
        Initial decentering (x, y) shift relative to where the lens is placed.
    tilt_deg : float
        Initial tilt angle in degrees around the lens center.
    birefringence : float
        Placeholder — not yet used in ray tracing.
    """

    def __init__(
        self,
        R1: float = 4.0,
        R2: float = -4.0,
        thickness: float = 0.5,
        n: float = 1.5,
        diameter: float = 3.0,
        n_outside: float = 1.0,
        fill_color=BLUE,
        fill_opacity: float = 0.25,
        stroke_width: float = 2.0,
        offset: np.ndarray | None = None,
        tilt_deg: float = 0.0,
        birefringence: float = 0.0,
        **kwargs,
    ):
        super().__init__(
            refractive_index_before=n_outside,
            refractive_index_after=n_outside,
            **kwargs,
        )

        # --- ValueTrackers (all physical parameters are animatable) ---
        self.R1_tracker = ValueTracker(R1)
        self.R2_tracker = ValueTracker(R2)
        self.thickness_tracker = ValueTracker(thickness)
        self.n_tracker = ValueTracker(n)
        self.diameter_tracker = ValueTracker(diameter)
        self.n_outside_tracker = ValueTracker(n_outside)
        self.tilt_tracker = ValueTracker(tilt_deg)
        self.birefringence_tracker = ValueTracker(birefringence)

        _offset = np.zeros(3)
        if offset is not None:
            arr = np.asarray(offset, dtype=float)
            _offset[: len(arr)] = arr[:3]
        self.offset_x_tracker = ValueTracker(_offset[0])
        self.offset_y_tracker = ValueTracker(_offset[1])

        # Style
        self._fill_color = fill_color
        self._fill_opacity = fill_opacity
        self._stroke_width = stroke_width

        # Invisible reference point kept at the optical center.
        # After any shift/rotate applied to the VGroup it tracks the true world
        # center, which is needed to rebuild the body in world coordinates.
        self._center_ref = VectorizedPoint(np.zeros(3))
        self.add(self._center_ref)

        # Build initial visual
        self._create_lens_visual()

        # Shadow values for change detection
        self._prev_R1 = R1
        self._prev_R2 = R2
        self._prev_d = thickness
        self._prev_diam = diameter

        # Apply initial transforms
        self._prev_tilt = tilt_deg
        self._prev_offset = _offset.copy()
        if tilt_deg != 0.0:
            self.rotate(np.deg2rad(tilt_deg))
        if not np.allclose(_offset, 0):
            self.shift(_offset)

        # Updater handles animated tilt / offset / shape changes
        self.add_updater(self._update_transforms)

    # ------------------------------------------------------------------
    # Visual
    # ------------------------------------------------------------------

    def _create_lens_visual(self) -> None:
        """Build the filled lens shape from current tracker values."""
        R1 = self.R1_tracker.get_value()
        R2 = self.R2_tracker.get_value()
        d = self.thickness_tracker.get_value()
        h = self.diameter_tracker.get_value() / 2

        front_x = -d / 2
        back_x = d / 2

        n_pts = 48
        arc1 = _arc_points(R1, front_x, h, n_pts)  # front: top → bottom
        arc2 = _arc_points(R2, back_x, h, n_pts)  # back:  top → bottom

        # Outline: front arc (top→bottom), then back arc reversed (bottom→top)
        outline = np.vstack([arc1, arc2[::-1]])

        body = VMobject()
        # Close the path by appending the first point at the end
        body.set_points_as_corners([*outline, outline[0]])
        body.set_fill(color=self._fill_color, opacity=self._fill_opacity)
        body.set_stroke(color=self._fill_color, width=self._stroke_width)

        if hasattr(self, "_lens_body"):
            self.remove(self._lens_body)
        self._lens_body = body
        self.add(body)

    def rebuild(self) -> None:
        """Recreate the lens visual — kept for backward compatibility."""
        self._rebuild_body_in_place()

    def _rebuild_body_in_place(self) -> None:
        """
        Recompute the lens outline and update ``_lens_body`` in-place.

        Works in world coordinates: local outline points are rotated by the
        current tilt and translated to ``_center_ref`` (which tracks the true
        optical center after any shift/rotate applied to the VGroup).
        """
        R1 = self.R1_tracker.get_value()
        R2 = self.R2_tracker.get_value()
        d = self.thickness_tracker.get_value()
        h = self.diameter_tracker.get_value() / 2

        n_pts = 48
        arc1 = _arc_points(R1, -d / 2, h, n_pts)
        arc2 = _arc_points(R2, d / 2, h, n_pts)
        outline = np.vstack([arc1, arc2[::-1]])

        # Rotate local points by current tilt
        tilt_rad = np.deg2rad(self.tilt_tracker.get_value())
        c, s = np.cos(tilt_rad), np.sin(tilt_rad)
        rotated = np.column_stack(
            [
                outline[:, 0] * c - outline[:, 1] * s,
                outline[:, 0] * s + outline[:, 1] * c,
                outline[:, 2],
            ]
        )

        # Translate to current world center
        world_pts = rotated + self._center_ref.get_center()

        new_body = VMobject()
        new_body.set_points_as_corners([*world_pts, world_pts[0]])
        new_body.set_fill(color=self._fill_color, opacity=self._fill_opacity)
        new_body.set_stroke(color=self._fill_color, width=self._stroke_width)

        self._lens_body.become(new_body)

    # ------------------------------------------------------------------
    # Updater
    # ------------------------------------------------------------------

    def _update_transforms(self, _mob) -> None:
        """Delta-based updater: tilt, offset, and shape parameters."""
        # --- Tilt ---
        tilt = self.tilt_tracker.get_value()
        delta_tilt = tilt - self._prev_tilt
        if abs(delta_tilt) > 1e-9:
            self.rotate(np.deg2rad(delta_tilt))
            self._prev_tilt = tilt
            # rotate() already moves all submobjects — no rebuild needed for tilt alone

        # --- Offset ---
        ox = self.offset_x_tracker.get_value()
        oy = self.offset_y_tracker.get_value()
        new_offset = np.array([ox, oy, 0.0])
        delta = new_offset - self._prev_offset
        if np.linalg.norm(delta) > 1e-9:
            self.shift(delta)
            self._prev_offset = new_offset.copy()

        # --- Shape parameters (R1, R2, thickness, diameter) ---
        R1 = self.R1_tracker.get_value()
        R2 = self.R2_tracker.get_value()
        d = self.thickness_tracker.get_value()
        diam = self.diameter_tracker.get_value()
        if (
            abs(R1 - self._prev_R1) > 1e-9
            or abs(R2 - self._prev_R2) > 1e-9
            or abs(d - self._prev_d) > 1e-9
            or abs(diam - self._prev_diam) > 1e-9
        ):
            self._prev_R1 = R1
            self._prev_R2 = R2
            self._prev_d = d
            self._prev_diam = diam
            self._rebuild_body_in_place()

    # ------------------------------------------------------------------
    # Coordinate transforms
    # ------------------------------------------------------------------

    def _optical_center(self) -> np.ndarray:
        """True world position of the optical center (immune to body-shape drift)."""
        return self._center_ref.get_center()

    def _ray_to_local(
        self, ray_start: np.ndarray, ray_dir: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray]:
        """World → local (un-rotate by tilt, translate to optical center)."""
        tilt_rad = np.deg2rad(self.tilt_tracker.get_value())
        center = self._optical_center()
        c, s = np.cos(tilt_rad), np.sin(tilt_rad)

        def unrot(v: np.ndarray) -> np.ndarray:
            return np.array([v[0] * c + v[1] * s, -v[0] * s + v[1] * c, v[2]])

        return unrot(ray_start - center), unrot(ray_dir)

    def _to_world_point(self, local_pt: np.ndarray) -> np.ndarray:
        tilt_rad = np.deg2rad(self.tilt_tracker.get_value())
        c, s = np.cos(tilt_rad), np.sin(tilt_rad)
        rotated = np.array(
            [
                local_pt[0] * c - local_pt[1] * s,
                local_pt[0] * s + local_pt[1] * c,
                local_pt[2],
            ]
        )
        return rotated + self._optical_center()

    def _to_world_dir(self, local_dir: np.ndarray) -> np.ndarray:
        tilt_rad = np.deg2rad(self.tilt_tracker.get_value())
        c, s = np.cos(tilt_rad), np.sin(tilt_rad)
        return np.array(
            [
                local_dir[0] * c - local_dir[1] * s,
                local_dir[0] * s + local_dir[1] * c,
                local_dir[2],
            ]
        )

    # ------------------------------------------------------------------
    # Geometry helpers (all in local frame)
    # ------------------------------------------------------------------

    @staticmethod
    def _intersect_surface(
        ray_start: np.ndarray,
        ray_dir: np.ndarray,
        R: float,
        vertex_x: float,
        half_diam: float,
    ) -> tuple[np.ndarray | None, float]:
        """
        Intersect a ray with a spherical (or flat) surface in local frame.

        Returns (intersection_point, t) or (None, inf).
        Convention: we return the intersection on the VERTEX side of the sphere.
        """
        h = half_diam

        # Flat surface
        if abs(R) < 1e-10 or abs(R) > _FLAT_R_THRESHOLD:
            if abs(ray_dir[0]) < 1e-10:
                return None, float("inf")
            t = (vertex_x - ray_start[0]) / ray_dir[0]
            if t < 1e-6:
                return None, float("inf")
            p = ray_start + t * ray_dir
            if abs(p[1]) > h:
                return None, float("inf")
            return p, t

        # Spherical surface
        # Center of sphere at (vertex_x + R, 0, 0)
        cx = vertex_x + R
        ox = ray_start[0] - cx
        oy = ray_start[1]
        dx = ray_dir[0]
        dy = ray_dir[1]

        a = dx * dx + dy * dy
        b = 2.0 * (ox * dx + oy * dy)
        c_coef = ox * ox + oy * oy - R * R

        disc = b * b - 4.0 * a * c_coef
        if disc < 0.0:
            return None, float("inf")

        sqrt_disc = np.sqrt(disc)
        t1 = (-b - sqrt_disc) / (2.0 * a)
        t2 = (-b + sqrt_disc) / (2.0 * a)

        best_t = float("inf")
        best_p = None

        for t in (t1, t2):
            if t < 1e-6:
                continue
            p = ray_start + t * ray_dir
            if abs(p[1]) > h:
                continue
            # Keep only the vertex-side intersection
            # R > 0: vertex is left of center → p[0] < cx
            # R < 0: vertex is right of center → p[0] > cx
            on_vertex_side = (R > 0 and p[0] <= cx + 1e-9) or (
                R < 0 and p[0] >= cx - 1e-9
            )
            if not on_vertex_side:
                continue
            if t < best_t:
                best_t = t
                best_p = p

        return best_p, best_t

    @staticmethod
    def _normal_at(point: np.ndarray, R: float, vertex_x: float) -> np.ndarray:
        """
        Outward normal at *point* on the spherical surface (local frame).

        'Outward' = away from the center of curvature.
        For a flat surface, returns (+x, 0, 0).
        """
        if abs(R) < 1e-10 or abs(R) > _FLAT_R_THRESHOLD:
            return np.array([1.0, 0.0, 0.0])
        cx = vertex_x + R
        center = np.array([cx, 0.0, 0.0])
        n = point - center
        norm = np.linalg.norm(n)
        if norm < 1e-10:
            return np.array([1.0, 0.0, 0.0])
        return n / norm

    @staticmethod
    def _snell(
        ray_dir: np.ndarray, normal: np.ndarray, n1: float, n2: float
    ) -> np.ndarray | None:
        """
        Vectorial Snell-Descartes law.

        Parameters
        ----------
        ray_dir : np.ndarray
            Unit incident direction.
        normal : np.ndarray
            Surface normal (outward, pointing into the incident medium).
            Automatically flipped if it points the wrong way.
        n1, n2 : float
            Refractive indices (incident, refracted).

        Returns
        -------
        np.ndarray or None
            Refracted unit direction, or None on total internal reflection.
        """
        # Normal must point into the incident medium (oppose the ray)
        if np.dot(ray_dir, normal) > 0:
            normal = -normal

        cos_i = -np.dot(ray_dir, normal)
        eta = n1 / n2
        sin2_t = eta**2 * (1.0 - cos_i**2)

        if sin2_t > 1.0:
            return None  # Total internal reflection

        cos_t = np.sqrt(1.0 - sin2_t)
        refracted = eta * ray_dir + (eta * cos_i - cos_t) * normal
        norm = np.linalg.norm(refracted)
        if norm < 1e-10:
            return None
        return refracted / norm

    # ------------------------------------------------------------------
    # OpticalElement interface
    # ------------------------------------------------------------------

    def get_optical_plane_position(self) -> np.ndarray:
        return self._optical_center()

    def intersect(
        self, ray_start: np.ndarray, ray_direction: np.ndarray
    ) -> tuple[np.ndarray | None, bool]:
        """Return the first surface (front or back) hit by the ray."""
        local_start, local_dir = self._ray_to_local(ray_start, ray_direction)

        R1 = self.R1_tracker.get_value()
        R2 = self.R2_tracker.get_value()
        d = self.thickness_tracker.get_value()
        h = self.diameter_tracker.get_value() / 2

        p1, t1 = self._intersect_surface(local_start, local_dir, R1, -d / 2, h)
        p2, t2 = self._intersect_surface(local_start, local_dir, R2, d / 2, h)

        if p1 is not None and t1 <= t2:
            return self._to_world_point(p1), True
        if p2 is not None:
            return self._to_world_point(p2), True
        return None, False

    def propagate_ray(
        self,
        ray_start: np.ndarray,
        ray_direction: np.ndarray,
        intersection_point: np.ndarray,
    ) -> tuple:
        """
        Refract through both surfaces using vectorial Snell-Descartes.

        Returns
        -------
        (new_direction, True, exit_point)
            exit_point is the world-space point on the second surface, used by
            DynamicRay as a teleport so the ray continues from there.
        (ray_direction, False)
            If the ray is blocked (TIR, misses inner surface, outside aperture).
        """
        local_start, local_dir = self._ray_to_local(ray_start, ray_direction)

        R1 = self.R1_tracker.get_value()
        R2 = self.R2_tracker.get_value()
        d = self.thickness_tracker.get_value()
        h = self.diameter_tracker.get_value() / 2
        n_lens = self.n_tracker.get_value()
        n_out = self.n_outside_tracker.get_value()

        front_x = -d / 2
        back_x = d / 2

        p1, t1 = self._intersect_surface(local_start, local_dir, R1, front_x, h)
        p2, t2 = self._intersect_surface(local_start, local_dir, R2, back_x, h)

        # Determine which surface is hit first and set up the refraction chain
        if p1 is not None and t1 <= t2:
            # Front → back  (left-to-right ray)
            entry_pt, entry_R, entry_x = p1, R1, front_x
            exit_R, exit_x = R2, back_x
            n_entry_out, n_entry_in = n_out, n_lens
            n_exit_in, n_exit_out = n_lens, n_out
        elif p2 is not None:
            # Back → front  (right-to-left ray, e.g. after a mirror)
            entry_pt, entry_R, entry_x = p2, R2, back_x
            exit_R, exit_x = R1, front_x
            n_entry_out, n_entry_in = n_out, n_lens
            n_exit_in, n_exit_out = n_lens, n_out
        else:
            return ray_direction, False

        # --- Refraction at entry surface ---
        n_entry = self._normal_at(entry_pt, entry_R, entry_x)
        dir_inside = self._snell(local_dir, n_entry, n_entry_out, n_entry_in)
        if dir_inside is None:
            return ray_direction, False

        # --- Trace internally to exit surface ---
        exit_pt, _ = self._intersect_surface(entry_pt, dir_inside, exit_R, exit_x, h)
        if exit_pt is None:
            return ray_direction, False

        # --- Refraction at exit surface ---
        n_exit = self._normal_at(exit_pt, exit_R, exit_x)
        dir_out = self._snell(dir_inside, n_exit, n_exit_in, n_exit_out)
        if dir_out is None:
            return ray_direction, False

        world_dir = self._to_world_dir(dir_out)
        world_exit = self._to_world_point(exit_pt)
        return world_dir, True, world_exit

    def get_transfer_matrix(self) -> np.ndarray:
        """
        Paraxial ABCD matrix (for reference only; ray tracing uses exact Snell).

        System matrix = M_refr2 @ M_prop @ M_refr1
        Convention: state vector [y, θ] with θ the geometric ray angle.
        """
        R1 = self.R1_tracker.get_value()
        R2 = self.R2_tracker.get_value()
        d = self.thickness_tracker.get_value()
        n = self.n_tracker.get_value()
        no = self.n_outside_tracker.get_value()

        def refr_matrix(n1, n2, R):
            if abs(R) < 1e-10 or abs(R) > _FLAT_R_THRESHOLD:
                return np.array([[1.0, 0.0], [0.0, n1 / n2]])
            P = (n2 - n1) / R
            return np.array([[1.0, 0.0], [-P / n2, n1 / n2]])

        M1 = refr_matrix(no, n, R1)
        M_prop = np.array([[1.0, d], [0.0, 1.0]])
        M2 = refr_matrix(n, no, R2)
        return M2 @ M_prop @ M1


# ---------------------------------------------------------------------------
# Convenience subclasses
# ---------------------------------------------------------------------------


class BiconvexLens(SphericalLens):
    """
    Symmetric biconvex lens (R1 = |R|, R2 = -|R|).

    Parameters
    ----------
    R : float
        Absolute value of the radius of curvature for both surfaces (R > 0).
    """

    def __init__(self, R: float = 4.0, **kwargs):
        if R <= 0:
            raise ValueError("BiconvexLens: R must be positive")
        super().__init__(R1=R, R2=-R, **kwargs)


class BiconcaveLens(SphericalLens):
    """
    Symmetric biconcave lens (R1 = -|R|, R2 = |R|).

    Parameters
    ----------
    R : float
        Absolute value of the radius of curvature for both surfaces (R > 0).
    """

    def __init__(self, R: float = 4.0, **kwargs):
        if R <= 0:
            raise ValueError("BiconcaveLens: R must be positive")
        super().__init__(R1=-R, R2=R, **kwargs)


class PlanoConvexLens(SphericalLens):
    """
    Plano-convex lens: flat front, convex back (or vice-versa).

    Parameters
    ----------
    R : float
        Radius of curvature of the curved surface (R > 0 → back surface convex).
    flat_front : bool
        If True (default), front surface is flat; if False, back is flat.
    """

    def __init__(self, R: float = 4.0, flat_front: bool = True, **kwargs):
        if R <= 0:
            raise ValueError("PlanoConvexLens: R must be positive")
        if flat_front:
            super().__init__(R1=_FLAT_R_THRESHOLD, R2=-R, **kwargs)
        else:
            super().__init__(R1=R, R2=_FLAT_R_THRESHOLD, **kwargs)


class PlanoConcaveLens(SphericalLens):
    """
    Plano-concave lens: flat front, concave back (or vice-versa).

    Parameters
    ----------
    R : float
        Radius of curvature of the curved surface (R > 0).
    flat_front : bool
        If True (default), front surface is flat; if False, back is flat.
    """

    def __init__(self, R: float = 4.0, flat_front: bool = True, **kwargs):
        if R <= 0:
            raise ValueError("PlanoConcaveLens: R must be positive")
        if flat_front:
            super().__init__(R1=_FLAT_R_THRESHOLD, R2=R, **kwargs)
        else:
            super().__init__(R1=-R, R2=_FLAT_R_THRESHOLD, **kwargs)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _arc_points(
    R: float, vertex_x: float, half_diam: float, n_pts: int = 48
) -> np.ndarray:
    """
    Sample points along a spherical surface arc, from top (+h) to bottom (-h).

    Uses the sign convention: x = vertex_x + R - sign(R)*sqrt(R²-y²)
    """
    h = half_diam
    ys = np.linspace(h, -h, n_pts)

    if abs(R) < 1e-10 or abs(R) > _FLAT_R_THRESHOLD:
        xs = np.full(n_pts, vertex_x)
    else:
        # Clamp to avoid sqrt of negative (when |R| is only slightly > h)
        xs = vertex_x + R - np.sign(R) * np.sqrt(np.maximum(R**2 - ys**2, 0.0))

    return np.column_stack([xs, ys, np.zeros(n_pts)])
