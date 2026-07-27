# One-command Layer B pilot (Windows / PowerShell).
# Prereq: Docker Desktop running; weights downloaded (via Git Bash: bash download_weights.sh).
$ErrorActionPreference = "Stop"
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Repo = Join-Path $Here "VFSS_analysis"
$Img  = "vfss-pilot:cpu"

Write-Host "== [1/4] Build best-effort CPU image =="
docker build -f "$Here\Dockerfile" -t $Img "$Here"

Write-Host "== [2/4] Check model weights =="
if (-not (Get-ChildItem -Path "$Repo\models" -Recurse -Directory -Filter "Task010_VFSS" -ErrorAction SilentlyContinue)) {
  Write-Host "!! Weights not found under $Repo\models. Run first (Git Bash):  bash download_weights.sh"
  exit 1
}

Write-Host "== [3/4] Run inference on healthy_001 (CPU - may be slow) =="
docker run --rm `
  -v "${Repo}:/work/repo" -w /work/repo `
  -e CUDA_VISIBLE_DEVICES="" `
  -e RESULTS_FOLDER=/work/repo/models `
  -e nnUNet_raw_data_base=/tmp/nnraw -e nnUNet_preprocessed=/tmp/nnprep `
  -e MKL_SERVICE_FORCE_INTEL=1 `
  $Img python run.py 2>&1 | Tee-Object "$Here\rerun.log"

Write-Host "== [4/4] Compare regenerated vs reference =="
docker run --rm `
  -v "${Repo}:/work/repo" -v "${Here}:/out" -w /work `
  $Img python /out/compare.py `
    --ref /out/reference_outputs/test/healthy_001/t0 `
    --new /work/repo/data/output_data/test/healthy_001/t0 `
  2>&1 | Tee-Object "$Here\compare.log"

Write-Host "== done. Logs: rerun.log, compare.log =="
