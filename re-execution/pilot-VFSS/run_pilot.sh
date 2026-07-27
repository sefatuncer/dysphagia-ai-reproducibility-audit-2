#!/usr/bin/env bash
# One-command Layer B pilot: build -> run.py (CPU) -> compare vs reference.
# Prereq: Docker running; weights already downloaded (bash download_weights.sh).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$HERE/VFSS_analysis"
IMG="vfss-pilot:cpu"

echo "== [1/4] Build best-effort CPU image =="
docker build -f "$HERE/Dockerfile" -t "$IMG" "$HERE"

echo "== [2/4] Check model weights =="
if ! find "$REPO/models" -type d -name 'Task010_VFSS' 2>/dev/null | grep -q .; then
  echo "!! Weights not found under $REPO/models. Run first:  bash \"$HERE/download_weights.sh\""
  exit 1
fi

echo "== [3/4] Run inference on healthy_001 (CPU — may be slow) =="
docker run --rm \
  -v "$REPO":/work/repo -w /work/repo \
  -e CUDA_VISIBLE_DEVICES="" \
  -e RESULTS_FOLDER=/work/repo/models \
  -e nnUNet_raw_data_base=/tmp/nnraw -e nnUNet_preprocessed=/tmp/nnprep \
  -e MKL_SERVICE_FORCE_INTEL=1 \
  "$IMG" python run.py 2>&1 | tee "$HERE/rerun.log"

echo "== [4/4] Compare regenerated vs reference (Layer B verdict) =="
docker run --rm \
  -v "$REPO":/work/repo -v "$HERE":/out -w /work \
  "$IMG" python /out/compare.py \
    --ref /out/reference_outputs/test/healthy_001/t0 \
    --new /work/repo/data/output_data/test/healthy_001/t0 \
  2>&1 | tee "$HERE/compare.log"

echo "== done. Logs: rerun.log, compare.log =="
