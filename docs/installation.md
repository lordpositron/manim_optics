# Installation

## Prerequisites

`manim-optics` builds on [Manim Community](https://github.com/ManimCommunity/manim)
(`manim >= 0.20.0`). Install Manim first following the
[official guide](https://docs.manim.community/en/stable/installation.html).

Manim itself requires Cairo, FFmpeg, and (optionally) LaTeX — see the Manim docs for
platform-specific instructions.

## From GitHub (current)

```bash
git clone https://github.com/lordpositron/manim_optics.git
cd manim_optics
pip install -e .
```

## From PyPI (upcoming)

```bash
pip install manim-optics
```

## Development install

```bash
git clone https://github.com/lordpositron/manim_optics.git
cd manim_optics
pip install -e ".[dev]"
```

This adds `pytest` and `ruff` for testing and linting.

## Verify

```python
import manim_optics
print(manim_optics.__version__)   # 0.1.0
```
