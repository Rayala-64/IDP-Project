"""
main_pipeline.py
----------------
Runs the full fog → detection comparison pipeline across all three fog densities.

Pipeline per image:
  1. Foggy image        → YOLOv8 detect
  2. Simple dehaze      → YOLOv8 detect
  3. Full DCP dehaze    → YOLOv8 detect

Output folder structure:
  results/
  ├── No_Fog/
  │    ├── images/
  │    │    ├── foggy_outputs/
  │    │    ├── simple_dehazed_outputs/
  │    │    └── dcp_outputs/
  │    └── metrics/
  │         └── results.csv
  ├── Medium_Fog/
  │    └── ...
  └── Dense_Fog/
       └── ...
"""

import os
# pyrefly: ignore [missing-import]
import cv2
import json
import pandas as pd

from src.detection.yolo_detect import detect
from src.dehazing.classical import dehaze
from src.dehazing.dcp_dehaze import dehaze_dcp
from src.evaluation.metrics import compute_metrics


# ── Configuration ──────────────────────────────────────────────────────────────

DATASET_BASE  = "dataset/sampled"  # Base folder for input images, organized by density level
RESULTS_BASE  = "results"

FOG_DENSITIES = ["No_Fog", "Medium_Fog", "Dense_Fog"]

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}


# ── Folder Setup ───────────────────────────────────────────────────────────────

def get_density_paths(density: str) -> dict:
    """
    Returns all relevant paths for a given density, fully self-contained.

    Example for density="Medium_Fog":
      {
        "dataset" : "dataset/sampled/Medium_Fog",
        "images"  : "results/Medium_Fog/images",
        "metrics" : "results/Medium_Fog/metrics",
        "foggy"   : "results/Medium_Fog/images/foggy_outputs",
        "simple"  : "results/Medium_Fog/images/simple_dehazed_outputs",
        "dcp"     : "results/Medium_Fog/images/dcp_outputs",
        "csv"     : "results/Medium_Fog/metrics/results.csv",
      }
    """
    base         = os.path.join(RESULTS_BASE, density)
    images_base  = os.path.join(base, "images")
    metrics_base = os.path.join(base, "metrics")

    return {
        "dataset" : os.path.join(DATASET_BASE, density),
        "images"  : images_base,
        "metrics" : metrics_base,
        "foggy"   : os.path.join(images_base, "foggy_outputs"),
        "simple"  : os.path.join(images_base, "simple_dehazed_outputs"),
        "dcp"     : os.path.join(images_base, "dcp_outputs"),
        "csv"     : os.path.join(metrics_base, "results.csv"),
    }


def create_output_dirs(paths: dict):
    """Create all output directories for one density level."""
    for key in ("foggy", "simple", "dcp", "metrics"):
        os.makedirs(paths[key], exist_ok=True)


# ── Single Image Processing ────────────────────────────────────────────────────

def process_image(img_path: str, paths: dict, density: str) -> dict | None:
    """
    Runs all three pipelines on one image and returns a flat result dict.

    Args:
        img_path : full path to the foggy input image
        paths    : dict returned by get_density_paths()
        density  : density label used for tagging rows in the CSV

    Returns:
        Flat dict of all metrics, or None if the image fails to load.
    """
    img_name = os.path.basename(img_path)
    img = cv2.imread(img_path)

    if img is None:
        print(f"  [SKIP] Cannot load: {img_path}")
        return None

    result = {"image": img_name, "density": density}

    # (tag, processed_image, save_directory)
    pipeline_inputs = [
        ("fog",    img,                paths["foggy"]),
        ("simple", dehaze(img),        paths["simple"]),
        ("dcp",    dehaze_dcp(img),    paths["dcp"]),
    ]

    for tag, processed_img, save_dir in pipeline_inputs:

        try:
            det_results = detect(processed_img)
        except Exception as e:
            print(f"  [ERROR] Detection failed ({tag}): {img_name} → {e}")
            return None

        m = compute_metrics(det_results)

        result[f"{tag}_count"] = m["count"]
        result[f"{tag}_avg_conf"] = round(m["avg_conf"], 4)
        result[f"{tag}_driving_count"] = m["driving_count"]

        det_results[0].save(filename=os.path.join(save_dir, img_name))

    # Signed delta vs raw fog — positive = dehazing helped, negative = hurt
    for tag in ("simple", "dcp"):
        result[f"{tag}_det_delta"]     = result[f"{tag}_count"]          - result["fog_count"]
        result[f"{tag}_conf_delta"]    = round(result[f"{tag}_avg_conf"] - result["fog_avg_conf"], 4)
        result[f"{tag}_driving_delta"] = result[f"{tag}_driving_count"]  - result["fog_driving_count"]

    return result


# ── Console Summary ────────────────────────────────────────────────────────────

def print_summary(density: str, df: pd.DataFrame):
    print(f"\n  {'Metric':<28} {'Fog':>8} {'Simple':>8} {'DCP':>8}")
    print(f"  {'─' * 54}")
    for col_base, label in [
        ("count",         "Avg detections"),
        ("avg_conf",      "Avg confidence"),
        ("driving_count", "Avg driving objects"),
    ]:
        fog_v    = df[f"fog_{col_base}"].mean()
        simple_v = df[f"simple_{col_base}"].mean()
        dcp_v    = df[f"dcp_{col_base}"].mean()
        print(f"  {label:<28} {fog_v:>8.3f} {simple_v:>8.3f} {dcp_v:>8.3f}")


# ── Main Pipeline ──────────────────────────────────────────────────────────────

def run_pipeline():
    print("\n" + "=" * 60)
    print("  IMAGE DEHAZING & OBJECT DETECTION PIPELINE")
    print("=" * 60)

    for density in FOG_DENSITIES:
        paths = get_density_paths(density)

        if not os.path.isdir(paths["dataset"]):
            print(f"\n[WARN] Dataset folder not found, skipping: {paths['dataset']}")
            continue

        create_output_dirs(paths)

        image_files = sorted([
            f for f in os.listdir(paths["dataset"])
            if os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS
        ])

        print(f"\n{'─' * 60}")
        print(f"  Density : {density}")
        print(f"  Images  : {len(image_files)}")
        print(f"  Output  : results/{density}/")
        print(f"{'─' * 60}")

        density_results = []

        for img_name in image_files:
            img_path = os.path.join(paths["dataset"], img_name)
            if len(density_results) > 0 and len(density_results) % 10 == 0:
                print(f"  Processed {len(density_results)} / {len(image_files)} images")

            result = process_image(img_path, paths, density)
            if result:
                density_results.append(result)

        # Save per-density CSV
        if density_results:
            df = pd.DataFrame(density_results)
            df.to_csv(paths["csv"], index=False)
            print(f"\n  ✅ Saved: {paths['csv']}  ({len(df)} images)")
            print_summary(density, df)
        else:
            print(f"\n  [WARN] No results produced for {density}.")

    print("\n" + "=" * 60)
    print("  Pipeline complete.")
    print("=" * 60 + "\n")


# ── Entry Point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_pipeline()