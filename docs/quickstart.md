# Quick Start

## Minimal example — parallel bundle through a converging lens

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

Render with:

```bash
manim -pql quickstart.py QuickStart
```

## Animating a tracker

Every optical parameter is a `ValueTracker`, so you can animate it directly:

```python
self.play(lens.focal_length_tracker.animate.set_value(4.5), run_time=2)
```

## Tilting a mirror

```python
from manim_optics import PlaneMirror

mirror = PlaneMirror(height=4.0)
self.play(mirror.tilt_tracker.animate.set_value(30), run_time=1.5)
self.play(mirror.tilt_tracker.animate.set_value(-30), run_time=1.5)
```

## Live bundle with updaters

`RayBundle` re-traces rays every frame, so any position or tracker change is immediately reflected:

```python
bundle = RayBundle(
    start_points=[np.array([-6, y, 0]) for y in np.linspace(-1.5, 1.5, 7)],
    direction_angle_deg=0,
    optical_elements=[lens],
    color=YELLOW_E,
    stroke_width=2,
)
self.play(bundle.animate_propagation())
# Move the source upward — rays follow automatically
self.play(bundle.y_offset_tracker.animate.set_value(1.3))
```
