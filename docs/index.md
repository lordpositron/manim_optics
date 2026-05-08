# manim-optics

**Dynamic optics for Manim** — build scenes where light behaves like a living part of the
animation rather than a static overlay.

`manim-optics` provides thin lenses, mirrors, apertures, beam stops, composite optical
systems, 3D optics, and reactive rays that recompute their trajectories automatically
while your scene is in motion.

---

## Why it feels different

- **Rays are live objects.** `DynamicRay` and `RayBundle` recalculate their path at every
  frame — move a lens, change a focal length, or insert a new element and the light follows immediately.
- **Trackers drive optics.** Focal length, pupil diameter, tilt angle, aperture radius —
  all animatable via `ValueTracker` while ray tracing stays coherent.
- **Classroom-ready visuals.** Converging/diverging arrow tips on lenses and mirrors, hatching
  conventions, focal-point dots, principal-plane labels — everything matches standard optics diagrams.
- **Stays close to Manim.** Optical elements are `VGroup` subclasses; scenes stay short and Manim-idiomatic.

---

## Contents

```{toctree}
:maxdepth: 2
:caption: Getting Started

installation
quickstart
concepts
```

```{toctree}
:maxdepth: 2
:caption: API Reference

api/index
```

```{toctree}
:maxdepth: 1
:caption: Project

changelog
GitHub <https://github.com/lordpositron/manim_optics>
```

---

## Feature table

| Category | Classes |
|---|---|
| Thin lenses | `ThinLens`, `ConvergingLens`, `DivergingLens` |
| Mirrors | `PlaneMirror`, `SphericalMirror` |
| Stops & apertures | `LineBeamStop`, `CircularAperture`, `ArcBeamStop` |
| Reactive rays | `DynamicRay`, `RayBundle`, `PrincipalRays` |
| Composite systems | `Eye`, `CenteredSystem` |
| 3D optics | `OpticalElement3D`, `ThinLens3D`, `RayBundle3D` |
| Measurement overlays | `LinearGraticule`, `CrossGraticule`, `GridGraticule` |
| Image analysis | `ImageFormation`, `ImageMarker`, `RayExtension`, `find_focal_point_from_rays` |
