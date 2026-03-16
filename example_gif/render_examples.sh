#!/bin/bash

# Render all README example scenes to MP4, then convert to GIF
# Usage:
#   cd example_gif && bash render_examples.sh
#   cd example_gif && bash render_examples.sh --convert-only

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_DIR="$SCRIPT_DIR"

SCENES=(
    "Example1_LensBundle"
    "Example2_AnimatedFocalLength"
    "Example3_EyeAccommodation"
    "Example4_PrincipalPlanes"
    "Example5_RealVsVirtual"
    "Example6_MeasuredFocus"
    "Example7_Focal3D"
)

if [ "${1:-}" != "--convert-only" ]; then
    echo "Rendering manim_optics README examples..."
    cd "$ROOT_DIR" || exit 1

    echo "Rendering Example 1: Lens Bundle..."
    manim test/test_readme_examples.py Example1_LensBundle -ql 2>&1 | grep -v "Clip" | tail -5

    echo "Rendering Example 2: Animated Focal Length..."
    manim test/test_readme_examples.py Example2_AnimatedFocalLength -ql 2>&1 | grep -v "Clip" | tail -5

    echo "Rendering Example 3: Eye Accommodation..."
    manim test/test_readme_examples.py Example3_EyeAccommodation -ql 2>&1 | grep -v "Clip" | tail -5

    echo "Rendering Example 4: Principal Planes..."
    manim test/test_readme_examples.py Example4_PrincipalPlanes -ql 2>&1 | grep -v "Clip" | tail -5

    echo "Rendering Example 5: Real vs Virtual..."
    manim test/test_readme_examples.py Example5_RealVsVirtual -ql 2>&1 | grep -v "Clip" | tail -5

    echo "Rendering Example 6: Measured Focus..."
    manim test/test_readme_examples.py Example6_MeasuredFocus -ql 2>&1 | grep -v "Clip" | tail -5

    echo "Rendering Example 7: Focal 3D..."
    manim test/test_readme_examples.py Example7_Focal3D -ql 2>&1 | grep -v "Clip" | tail -5
fi

echo ""
echo "Converting MP4s to GIF..."

if ! command -v ffmpeg >/dev/null 2>&1; then
    echo "Error: ffmpeg is not installed. Install it with: brew install ffmpeg"
    exit 1
fi

find_scene_mp4() {
    local scene_name="$1"
    find "$ROOT_DIR/media/videos" -type f -name "${scene_name}.mp4" | grep "test_readme_examples" | head -1
}

converted=0
index=1
for scene in "${SCENES[@]}"; do
    mp4_path="$(find_scene_mp4 "$scene")"
    gif_path="$OUTPUT_DIR/example${index}.gif"

    if [ -z "$mp4_path" ]; then
        echo "Warning: MP4 not found for $scene (skipping)"
        index=$((index + 1))
        continue
    fi

    ffmpeg -y -i "$mp4_path" -vf "fps=15,scale=800:-1:flags=lanczos" -loop 0 "$gif_path" >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "OK example${index}.gif <- $scene"
        converted=$((converted + 1))
    else
        echo "Error: conversion failed for $scene"
    fi

    index=$((index + 1))
done

echo ""
echo "Done: $converted GIF(s) written to $OUTPUT_DIR"
ls -1 "$OUTPUT_DIR"/example*.gif 2>/dev/null || true
