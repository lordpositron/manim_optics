# Core Concepts

## ABCD transfer matrices

Every `OpticalElement` exposes `get_transfer_matrix() → np.ndarray (2×2)`.
The ray state is `[y, θ]` (height above axis, paraxial angle).

| Element | Matrix |
|---|---|
| Thin lens (focal length *f*) | `[[1, 0], [-1/f, 1]]` |
| Plane mirror | `[[1, 0], [0, -1]]` |
| Spherical mirror (radius *R*) | `[[1, 0], [2/R, 1]]` |
| Free propagation (distance *d*) | `[[1, d], [0, 1]]` |

## Sign convention for `SphericalMirror`

`manim-optics` uses the French algebraic sign convention:

| R | Mirror type | Visual |
|---|---|---|
| R < 0 | Concave (converging) | Half-arrows point **left** |
| R > 0 | Convex (diverging) | Half-arrows point **right** |

The `facing` parameter only controls hatching placement
(`facing="left"` → hatching to the right of the mirror line).

## Reactive ray tracing

`DynamicRay` and `RayBundle` use Manim updaters — every frame recomputes the full
ray path by iterating over the `optical_elements` list in order.
Move an element, change a tracker, or swap the element list and the scene stays live.

```{note}
`DynamicRay.get_points()` returns `[]` outside an active `Scene` because the geometry
lives in sub-mobjects via `self.become(...)`.
```

## Optical plane vs. VGroup centre

`get_optical_plane_position()` returns the true optical reference of an element
(the lens or mirror line), not the bounding-box centre, which can be offset by
focal-point dots or hatching geometry.

## `ValueTracker` pattern

All animatable parameters are `ValueTracker` instances stored as attributes:

| Class | Tracker | Default |
|---|---|---|
| `ThinLens` | `focal_length_tracker` | constructor value |
| `PlaneMirror` | `tilt_tracker` | `0.0` deg |
| `SphericalMirror` | `tilt_tracker` | `0.0` deg |
| `CircularAperture` | `radius_tracker` | constructor value |
| `Eye` | `focal_length_tracker`, `pupil_diameter_tracker` | constructor values |

Always read `tracker.get_value()` inside computations — not the plain attribute —
so animated values are captured each frame.
