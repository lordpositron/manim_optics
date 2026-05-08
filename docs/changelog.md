# Changelog

## 0.1.0 — Alpha (2024)

Initial public release.

- Thin lenses: `ThinLens`, `ConvergingLens`, `DivergingLens`
- Mirrors: `PlaneMirror` (with `tilt_tracker`), `SphericalMirror` (French sign convention, `tilt_tracker`)
- Beam stops & apertures: `LineBeamStop`, `CircularAperture`, `ArcBeamStop`
- Reactive rays: `DynamicRay`, `RayBundle`, `PrincipalRays`, `RayExtension`
- Image analysis: `ImageFormation`, `ImageMarker`, `find_focal_point_from_rays`, `find_ray_intersection`
- Composite systems: `Eye`, `CenteredSystem`
- 3D optics: `OpticalElement3D`, `ThinLens3D`, `RayBundle3D`
- Measurement overlays: `Graticule`, `LinearGraticule`, `CrossGraticule`, `GridGraticule`
- Scene helpers: `OpticalScene`, `create_object_arrow`, `create_image_arrow`, `calculate_image_position`
