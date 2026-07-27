#!/usr/bin/env bash
# Download the CC-BY-4.0 model weights (~6.1 GB) from Zenodo and unpack into the repo's models/ folder.
# Usage:  bash download_weights.sh [path-to-VFSS_analysis]
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="${1:-$HERE/VFSS_analysis}"
DEST="$REPO/models"
URL="https://zenodo.org/records/17191973/files/models_VFSS.zip?download=1"

mkdir -p "$DEST"
echo ">> Downloading models_VFSS.zip (~6.1 GB, CC-BY-4.0) ..."
wget -c -O "$DEST/models_VFSS.zip" "$URL"
echo ">> SHA256 (record this in analiz/ as provenance):"
sha256sum "$DEST/models_VFSS.zip" | tee "$DEST/models_VFSS.zip.sha256"
echo ">> Unzipping ..."
unzip -o "$DEST/models_VFSS.zip" -d "$DEST"
echo ">> Directory layout under models/ (RESULTS_FOLDER=models expects an nnUNet/... tree with Task010_VFSS):"
find "$DEST" -maxdepth 3 -type d | head -30
echo ">> If Task010_VFSS is nested differently, move it so nnU-Net v1 finds it under RESULTS_FOLDER, or adjust run_pilot.sh."
