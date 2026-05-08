# Example GIF Generation

This directory contains the script to render all README examples as animated GIFs.

## Quick Start

Make the script executable and run it:

```bash
cd example_gif
chmod +x render_examples.sh
bash render_examples.sh
```

The script will:
1. Render each of the 7 README example scenes from `test/test_readme_examples.py`
2. Convert the MP4 videos to animated GIFs
3. Save them in this directory as `example1.gif`, `example2.gif`, etc.

## Requirements

- **Manim** (already installed as part of this project)
- **ffmpeg** (for MP4 → GIF conversion)

Install ffmpeg on macOS:
```bash
brew install ffmpeg
```

Or on Linux:
```bash
sudo apt-get install ffmpeg
```

## GIF Files

After running the script, you'll have:

- `example1.gif` - Parallel bundle through a converging lens
- `example2.gif` - Animated focal length with live ray updates
- `example3.gif` - Eye accommodation
- `example4.gif` - Principal planes with CenteredSystem
- `example5.gif` - Real and virtual image formation
- `example6.gif` - Graticule overlay for optical measurements
- `example7.gif` - 3D focusing

These are referenced in the main `README.md`.

## Rendering Speed

Each scene is rendered with low quality settings (`-ql`) for fast turnaround:
- ~30-60 seconds per scene on a typical machine
- Total runtime: ~5-10 minutes for all 7 scenes

To render with higher quality (slower), replace `-ql` with `-qm` or `-qk` in the script.

## Troubleshooting

**"Error: ffmpeg is not installed"**
- Install ffmpeg (see Requirements above)

**"Error: Video directory not found"**
- The script was interrupted or Manim render failed
- Check the terminal output for Manim errors
- Run individual scenes manually to debug:
  ```bash
  cd ..
  manim test/test_readme_examples.py Example1_LensBundle -ql
  ```

**GIFs are too large**
- Adjust the `scale` parameter in the ffmpeg commands (currently `800:-1`)
- Change `800:-1` to `640:-1` for smaller files or `1024:-1` for larger
