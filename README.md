# manim_optics

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Dynamic optics for Manim — build scenes where light behaves like a living part of the animation rather than a static overlay.

`manim_optics` provides thin lenses, mirrors, apertures, beam stops, composite optical systems, 3D optics, and reactive rays that recompute their trajectories automatically while your scene is in motion.

---

## Why it feels different

- **Rays are live objects.** `DynamicRay` and `RayBundle` recalculate their path at every frame — move a lens, change a focal length, or insert a new element and the light follows immediately.
- **Trackers drive optics.** Focal length, pupil diameter, tilt angle, aperture radius — all animatable via `ValueTracker` while ray tracing stays coherent.
- **Classroom-ready visuals.** Converging/diverging arrow tips on lenses and mirrors, hatching conventions, focal point dots, principal plane labels — everything matches standard optics diagrams.
- **Stays close to Manim.** Optical elements are `VGroup` subclasses; scenes stay short and Manim-idiomatic.

---

## Feature Highlights

| Category | Classes |
| --- | --- |
| Thin lenses | `ThinLens`, `ConvergingLens`, `DivergingLens` |
| Real lenses | `SphericalLens`|
| Mirrors | `PlaneMirror`, `SphericalMirror` |
| Stops & apertures | `LineBeamStop`, `CircularAperture`, `ArcBeamStop` |
| Reactive rays | `DynamicRay`, `RayBundle`, `PrincipalRays` |
| Composite systems | `Eye`, `CenteredSystem` |
| 3D optics | `OpticalElement3D`, `ThinLens3D`, `RayBundle3D` |
| Measurement overlays | `LinearGraticule`, `CrossGraticule`, `GridGraticule` |
| Image analysis | `ImageFormation`, `ImageMarker`, `RayExtension`, `find_focal_point_from_rays` |

---

## Installation

`manim_optics` builds on [Manim Community](https://github.com/ManimCommunity/manim) (`manim >= 0.20.0`). Install Manim first following the [official guide](https://docs.manim.community/en/stable/installation.html), then:

```bash
git clone https://github.com/<your-account>/manim_optics.git
cd manim_optics
pip install -e .
```

---

## Quick Start

```python
import numpy as np
from manim import *
from manim_optics import OpticalScene, ConvergingLens, create_parallel_bundle


class QuickStart(OpticalScene):
    def construct(self):
        self.play(self.get_optical_axis_animation())

        lens = ConvergingLens(focal_length=2.0, height=3.0)

        rays = create_parallel_bundle(
            num_rays=7,
            spacing=0.4,
            start_x=-5.0,
            optical_elements=[lens],
            color=YELLOW,
            stroke_width=2,
        )

        self.play(Create(lens))
        self.play(rays.animate_propagation(run_time=1.6))
        self.wait()
```

---

## Example Gallery

### Ray Bundles

Parallel and diverging bundles with `y_offset_tracker` and `angle_offset_tracker`, plus a Mobject-tracked source.

![Ray Bundles](examples/example_gif/scene_01_ray_bundles.gif)

<!-- ```python
bundle = RayBundle(
    start_points=[np.array([-6, y, 0]) for y in np.linspace(-1.5, 1.5, 7)],
    direction_angle_deg=0,
    optical_elements=[],
    color=YELLOW_E,
    stroke_width=2,
)
self.play(bundle.animate_propagation())
self.play(bundle.y_offset_tracker.animate.set_value(1.3))
self.play(bundle.angle_offset_tracker.animate.set_value(15))
``` -->

---

### Thin Lenses

`ConvergingLens` and `DivergingLens` with animated focal length and moving image formation.

![Thin Lenses](examples/example_gif/scene_02_lenses.gif)

<!-- ```python
lens = ConvergingLens(focal_length=2.5, height=3.5)
bundle = RayBundle(
    start_points=[np.array([-6, y, 0]) for y in np.linspace(-1.4, 1.4, 7)],
    direction_angle_deg=0,
    optical_elements=[lens],
    color=YELLOW_E,
    stroke_width=2,
)
self.play(Create(lens))
self.play(bundle.animate_propagation())
self.play(lens.focal_length_tracker.animate.set_value(4.5))
``` -->

---

### Real Lenses

`SphericalLens` with animated radii of curvature, thickness, refractive index...

![Thin Lenses](examples/example_gif/scene_07_real_lenses.gif)

---

### Beam Stops & Apertures

`LineBeamStop`, `CircularAperture`, and `ArcBeamStop` with animated position and radius.

![Beam Stops](examples/example_gif/scene_03_beam_stops.gif)

<!-- ```python
stop = LineBeamStop(height=1.5)
aperture = CircularAperture(radius=0.8)
arc_stop = ArcBeamStop(inner_radius=0.5, outer_radius=1.5)
# stops block rays that fall outside the aperture
``` -->

---

### Mirrors

`PlaneMirror` with `tilt_tracker` animation and `SphericalMirror` (concave, R < 0) converging a parallel bundle.

![Mirrors](examples/example_gif/scene_04_mirrors.gif)

<!-- ```python
mirror = PlaneMirror(height=4.0)
mirror.shift(RIGHT * 2.5)
# animate tilt
self.play(mirror.tilt_tracker.animate.set_value(30))
self.play(mirror.tilt_tracker.animate.set_value(-30))

# concave spherical mirror (R < 0 = converging)
sph = SphericalMirror(radius_of_curvature=-6.0, height=3.5, facing="right")
``` -->

---

### Eye Model

`Eye` with accommodation (`animate_focal_length`) and pupil diameter animation.

![Eye Model](examples/example_gif/scene_05_eye.gif)

<!-- ```python
eye = Eye(
    focal_length=2.2,
    pupil_diameter=0.8,
    lens_diameter=1.8,
    show_cornea=True,
)
bundle = RayBundle(
    start_points=[np.array([-6, y, 0]) for y in np.linspace(-0.7, 0.7, 7)],
    direction_angle_deg=0,
    optical_elements=eye.get_optical_elements(),
)
self.play(eye.animate_focal_length(1.8))
self.play(eye.animate_pupil_diameter(0.4))
``` -->

---

### 06 — Graticules

`LinearGraticule`, `CrossGraticule`, and `GridGraticule` as measurement overlays.

![Graticules](examples/example_gif/scene_06_graticules.gif)

<!-- ```python
linear = LinearGraticule(length=8, unit_length=1, primary_interval=1,
                          secondary_interval=0.2, show_labels=True)

cross = CrossGraticule(length=8, unit_length=1, primary_interval=1,
                        secondary_interval=0.5, show_labels=True)

grid = GridGraticule(length=6, unit_length=1, primary_interval=1,
                      secondary_interval=0.1, color=GREY_B, show_labels=False)
``` -->

---

## Core Concepts

### Sign convention for `SphericalMirror`

`manim_optics` uses the French algebraic sign convention:

| R | Mirror type | Visual |
| --- | --- | --- |
| R < 0 | Concave (converging) | Half-arrows point **left** |
| R > 0 | Convex (diverging) | Half-arrows point **right** |

The `facing` parameter only controls hatching placement (`facing="left"` → hatching to the right).

### Reactive ray tracing

`DynamicRay` and `RayBundle` use Manim updaters — every frame recomputes the full ray path. Move an element, change a tracker, or swap a list of optical elements and the scene stays live.

### Optical plane vs. VGroup centre

`get_optical_plane_position()` returns the true optical reference of an element (the lens or mirror line), not the bounding-box centre, which can be offset by focal-point dots or hatching geometry.

---

## API Reference

### Optical elements

```python
from manim_optics import (
    ThinLens, ConvergingLens, DivergingLens,
    Mirror, PlaneMirror, SphericalMirror,
    BeamStop, LineBeamStop, CircularAperture, ArcBeamStop, SphericalLens
)
```

### Rays

```python
from manim_optics import (
    DynamicRay, RayBundle, PrincipalRays, RayExtension,
    create_parallel_bundle, create_diverging_bundle,
    find_ray_intersection, find_focal_point_from_rays,
    ImageMarker, ImageFormation,
)
```

### Systems and 3D

```python
from manim_optics import (
    Eye, CenteredSystem,
    OpticalElement3D, ThinLens3D, RayBundle3D,
)
```

### Scene helpers and measurement

```python
from manim_optics import (
    OpticalScene, create_object_arrow, create_image_arrow, calculate_image_position,
    Graticule, LinearGraticule, CrossGraticule, GridGraticule,
)
```

---

## Running the Examples

```bash
# render one sub-scene
manim -pql examples/all_2d_gallery.py GalleryRay
```
Avaliable scenes are : `GalleryRay`, `GalleryLens`, `GalleryBeamStop`, `GalleryMirror`, `GalleryEyeModel`, `GalleryGraticules`, `GalleryRealLenses`

---

## Project Structure

```text
manim_optics/          ← source package
  base.py              ← OpticalElement ABC
  lenses.py            ← ThinLens, ConvergingLens, DivergingLens
  mirrors.py           ← PlaneMirror, SphericalMirror
  beam_stops.py        ← LineBeamStop, CircularAperture, ArcBeamStop
  rays.py              ← DynamicRay, RayBundle, PrincipalRays…
  real_lenses.py       ← SphericalLens, BiconvexLens…
  centered_system.py   ← CenteredSystem
  eye.py               ← Eye
  optics_3d.py         ← OpticalElement3D, ThinLens3D, RayBundle3D
  scene_utils.py       ← OpticalScene, helpers
  miscellaneous.py     ← Graticule variants
examples/
  all_2d_gallery.py    ← all 2D scenes (Ray, Lens, BeamStop, Mirror, EyeModel, Graticules)
  example_gif/         ← rendered GIFs + render_gallery.sh
tests/                 ← 176 pytest tests
```