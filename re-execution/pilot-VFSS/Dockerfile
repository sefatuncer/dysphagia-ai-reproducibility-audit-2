# Dockerfile — best-effort CPU re-execution of BSEL-UC3M/VFSS_analysis (nnU-Net v1)
# for a computational-reproducibility audit (Layer B, Makale C).
# The repo is BIND-MOUNTED at run time (see run_pilot.sh) — we do NOT copy the
# unlicensed upstream code into the image (repo has no LICENSE → don't redistribute).
#
# DEVIATIONS FROM THE DECLARED ENVIRONMENT (these ARE the reproducibility finding — RECORD THEM):
#   nnU-Net v1.7.1 requires numpy<1.24 (removed aliases np.bool/np.int). BUT the declared env pins
#   THREE packages that require numpy>=1.24 → the declared set is UNSATISFIABLE. Forced downgrades:
#     * numpy         2.1.3  -> 1.23.5
#     * scikit-image  0.25.0 -> 0.19.3   (0.25 needs numpy>=1.24)
#     * MedPy         0.5.2  -> 0.4.0    (0.5.2 needs numpy>=1.24)  [empirically confirmed in build log]
#   Also: torch = CPU wheel (declared env shipped nvidia-cu12; `torch` UNPINNED in setup.py);
#         environment.yml not used (python=3.10 vs python_abi=3.13 inconsistent export).

FROM continuumio/miniconda3:latest

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 ffmpeg unzip wget ca-certificates && rm -rf /var/lib/apt/lists/*

# Base image ships Python 3.14 (numpy 1.23.5 has no cp314 wheel). Create a real py3.10 env on PATH.
RUN conda create -y -n VFSS_env python=3.10 pip && conda clean -afy
ENV PATH=/opt/conda/envs/VFSS_env/bin:$PATH

# CPU-only PyTorch (pinned; py3.10). Installed before the numpy constraint so torch resolves freely.
RUN pip install --no-cache-dir torch==2.0.1 --index-url https://download.pytorch.org/whl/cpu

# Pin numpy<1.24 across the whole resolution; downgrade the numpy>=1.24 offenders.
RUN printf 'numpy==1.23.5\n' > /tmp/constraints.txt
ENV PIP_CONSTRAINT=/tmp/constraints.txt
# batchgenerators left unpinned: nnunet 1.7.1 requires >=0.23; pip picks the newest
# version compatible with numpy==1.23.5 (the PIP_CONSTRAINT above keeps numpy fixed).
RUN pip install --no-cache-dir \
      "numpy==1.23.5" "scikit-image==0.19.3" "MedPy==0.4.0" \
      "SimpleITK==2.4.0" "opencv-python==4.10.0.84" "pandas==1.5.3" "scipy==1.10.1" \
      "scikit-learn==1.3.2" "tifffile==2023.7.10" \
      "spicy==0.16.0" "pydicom" \
      "nnunet==1.7.1"

WORKDIR /work/repo
CMD ["bash"]
