#!/bin/bash
# Render all Gallery2D sub-scenes to MP4 then convert to GIF.
# Usage: bash render_gallery.sh [--convert-only]

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_DIR="$SCRIPT_DIR"
GALLERY_FILE="$ROOT_DIR/all_2d_gallery.py"

SCENES=(
    "GalleryRay"
    "GalleryLens"
    "GalleryBeamStop"
    "GalleryMirror"
    "GalleryEyeModel"
    "GalleryGraticules"
)

GIF_NAMES=(
    "scene_01_ray_bundles"
    "scene_02_lenses"
    "scene_03_beam_stops"
    "scene_04_mirrors"
    "scene_05_eye"
    "scene_06_graticules"
)

if ! command -v ffmpeg >/dev/null 2>&1; then
    echo "Error: ffmpeg is not installed. Install it with: brew install ffmpeg"
    exit 1
fi

if [ "${1:-}" != "--convert-only" ]; then
    echo "Rendering Gallery2D sub-scenes..."
    cd "$ROOT_DIR" || exit 1

    for scene in "${SCENES[@]}"; do
        echo "Rendering $scene..."
        manim -ql "$GALLERY_FILE" "$scene" 2>&1 | grep -E "Animation|Rendering|Error|Warning|file written" | tail -3
    done
fi

echo ""
echo "Converting MP4s to GIF..."

find_mp4() {
    local scene_name="$1"
    find "$ROOT_DIR/media/videos" -type f -name "${scene_name}.mp4" | head -1
}

converted=0
for i in "${!SCENES[@]}"; do
    scene="${SCENES[$i]}"
    gif_name="${GIF_NAMES[$i]}"
    mp4_path="$(find_mp4 "$scene")"
    gif_path="$OUTPUT_DIR/${gif_name}.gif"

    if [ -z "$mp4_path" ]; then
        echo "Warning: MP4 not found for $scene (skipping)"
        continue
    fi

    ffmpeg -y -i "$mp4_path" \
        -vf "fps=15,scale=800:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer" \
        -loop 0 "$gif_path" >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        size=$(du -sh "$gif_path" | cut -f1)
        echo "OK ${gif_name}.gif ($size) <- $scene"
        converted=$((converted + 1))
    else
        echo "Error: conversion failed for $scene"
    fi
done

echo ""
echo "Done: $converted GIF(s) written to $OUTPUT_DIR"
ls -1 "$OUTPUT_DIR"/*.gif 2>/dev/null || true
