# Impact of Dehazing on Object Detection in Foggy Driving Environments

---

# 1. Project Overview

## Problem Statement

Fog significantly reduces visibility in driving environments, making object detection systems less reliable. In autonomous driving and Advanced Driver Assistance Systems (ADAS), reduced visibility can lead to:

* Missed object detections
* Lower confidence scores
* Reduced situational awareness
* Increased driving risk

This project analyzes how image dehazing techniques influence object detection performance under different fog densities.

The project compares:

1. Detection directly on foggy images
2. Detection after simplified DCP dehazing
3. Detection after full DCP dehazing

The evaluation is performed across three fog density levels:

* No Fog
* Medium Fog
* Dense Fog

---

# 2. Objective

The primary objective of this project is:

> To analyze whether image dehazing improves object detection performance under foggy driving conditions.

The project focuses on:

* Visibility enhancement
* Detection consistency
* Detection robustness under increasing fog density
* Comparative evaluation of dehazing approaches

---

# 3. Key Contributions

## Contributions of the Project

### 1. Comparative Fog Analysis

The system evaluates object detection under multiple fog densities:

* No Fog
* Medium Fog
* Dense Fog

### 2. Dehazing Comparison

The project compares:

* Raw foggy images
* Simplified DCP
* Full DCP

### 3. Pipeline-Based Evaluation

An end-to-end pipeline was built integrating:

* Dehazing
* Object detection
* Evaluation
* Metric generation
* Visualization

### 4. Practical Proxy Metrics

Instead of computationally expensive benchmark metrics such as:

* mAP
* Recall
* Precision
* False Positives
* False Negatives

The project uses practical proxy metrics suitable for comparative analysis.

### 5. Realistic Driving Context

The project specifically focuses on driving-related object detection performance.

---

# 4. Dataset Description

## Dataset Structure

The dataset contains approximately:

* 600 images total
* 200 images per fog density category

### Fog Categories

| Fog Density | Number of Images |
| ----------- | ---------------- |
| No_Fog      | ~200             |
| Medium_Fog  | ~200             |
| Dense_Fog   | ~200             |

---

## Dataset Purpose

The dataset is used to:

* Simulate varying driving visibility conditions
* Analyze object detection degradation
* Measure effectiveness of dehazing methods

---

# 5. Technologies and Libraries Used

| Component             | Technology              |
| --------------------- | ----------------------- |
| Programming Language  | Python                  |
| Image Processing      | OpenCV                  |
| Numerical Computation | NumPy                   |
| Visualization         | Matplotlib              |
| Data Handling         | Pandas                  |
| Object Detection      | YOLO                    |
| Evaluation            | Custom Metrics Pipeline |

---

# 6. Project Architecture

## High-Level Pipeline

```text
Input Images
      ↓
Fog Density Selection
      ↓
Dehazing Stage
  ├── No Dehazing
  ├── Simplified DCP
  └── Full DCP
      ↓
YOLO Object Detection
      ↓
Metrics Extraction
      ↓
CSV Generation
      ↓
Visualization and Analysis
```

---

# 7. Folder Structure

```text
IDP Project/
│
├── dataset/
│   ├── No_Fog/
│   ├── Medium_Fog/
│   └── Dense_Fog/
│
├── results/
│   ├── No_Fog/
│   │   ├── images/
│   │   └── metrics/
│   │
│   ├── Medium_Fog/
│   │   ├── images/
│   │   └── metrics/
│   │
│   ├── Dense_Fog/
│   │   ├── images/
│   │   └── metrics/
│   │
│   └── plots/
│
├── src/
│   ├── dehazing/
│   │   ├── classical.py
│   │   └── dcp_dehaze.py
│   │
│   ├── detection/
│   │   └── yolo_detect.py
│   │
│   ├── evaluation/
│   │   ├── analysis.py
│   │   └── metrics.py
│   │
│   ├── pipeline/
│   │   └── main_pipeline.py
│   │
│   └── safety/
│       └── stopping_distance.py
│── app.py
├── requirements.txt
└── README.txt
```

---

# 8. Core Modules Explanation

## 8.1 Dehazing Module

### Purpose

The dehazing module improves image visibility before object detection.

---

## 8.1.1 Simplified DCP

### Idea

A lightweight version of Dark Channel Prior (DCP).

### Characteristics

* Faster execution
* Lower computational complexity
* Moderate enhancement quality
* Suitable for resource-constrained environments

### Advantages

* Faster processing
* Lower resource usage
* Easier implementation

### Limitations

* Lower restoration quality
* Less accurate atmospheric estimation

---

## 8.1.2 Full DCP

### Idea

Full implementation of Dark Channel Prior image dehazing.

### Characteristics

* Better visibility restoration
* Stronger contrast enhancement
* Improved feature recovery

### Advantages

* Better object visibility
* More stable detections
* Stronger performance under dense fog

### Limitations

* Higher computational cost
* Slower than simplified version

---

# 9. Object Detection Module

## YOLO-Based Detection

### Purpose

YOLO is used to detect objects in:

* Raw foggy images
* Simplified DCP outputs
* Full DCP outputs

---

## Why YOLO?

YOLO was selected because:

* Real-time capable
* Fast inference
* Good general object detection performance
* Widely used in driving perception tasks

---

# 10. Evaluation Methodology

## Why Proxy Metrics Were Used

Traditional metrics such as:

* mAP
* Recall
* Precision
* F1-score

require:

* Ground truth annotations
* Bounding box labeling
* Complex benchmarking pipeline

Since this project focuses on comparative analysis and pipeline behavior, proxy metrics were used instead.

---

# 11. Proxy Metrics Used

## 11.1 Average Detections

### Definition

Average number of objects detected per image.

### Purpose

Measures overall detection capability.

### Interpretation

Higher value indicates:

* Better visibility
* Better feature recovery
* Better detection consistency

---

## 11.2 Average Confidence

### Definition

Average confidence score of detected objects.

### Purpose

Measures detector certainty.

### Interpretation

Higher confidence indicates:

* Clearer object visibility
* Better object recognition
* Stronger detector confidence

---
## 11.3 Proposed Perception Recovery Index (PRI)

### Purpose

Detection Count alone ignores certainty.

Average Confidence alone ignores detection yield.

PRI combines both.

### Formula

PRI =
(Detection Count × Average Confidence)_Dehazed

/

(Detection Count × Average Confidence)_Foggy

### Interpretation

| PRI Range       | Meaning                |
| --------------- | ---------------------- |
| PRI < 1.0       | Perception Degradation |
| 1.0 ≤ PRI < 1.5 | Minimal Recovery       |
| 1.5 ≤ PRI < 3.0 | Moderate Recovery      |
| PRI ≥ 3.0       | Strong Recovery        |

### Note

PRI is a project-specific composite metric proposed for comparative perception analysis.
---

# 12. Pipeline Execution Flow

## Step-by-Step Execution

### Step 1 — Load Dataset

Images are loaded based on fog density category.

---

### Step 2 — Apply Dehazing

Each image is processed using:

* No dehazing
* Simplified DCP
* Full DCP

---

### Step 3 — Perform Detection

YOLO performs object detection on each output.

---

### Step 4 — Extract Metrics

Metrics are calculated for:

* Detection count
* Confidence
* Driving-related detections

---

### Step 5 — Save Results

Results are saved as:

* CSV files
* Output images
* Metric summaries

---

### Step 6 — Generate Plots

Visualization graphs are generated for comparison.

---

# 13. Execution Command

## Running the Pipeline

```bash
python -m src.pipeline.main_pipeline
```

---

# 14. Experimental Results

# 14.1 No Fog Results

| Metric              | Fog   | Simple DCP | Full DCP |
| ------------------- | ----- | ---------- | -------- |
| Avg detections      | 8.157 | 7.379      | 8.116    |
| Avg confidence      | 0.554 | 0.546      | 0.527    |
| Avg PRI             | 1     | 0.892      | 0.946    | 

---

# 14.2 Medium Fog Results

| Metric              | Fog   | Simple DCP | Full DCP |
| ------------------- | ----- | ---------- | -------- |
| Avg detections      | 7.732 | 5.934      | 8.227    |
| Avg confidence      | 0.556 | 0.555      | 0.523    |
| Avg PRI             | 1     | 0.765      | 1.000    | 

---

# 14.3 Dense Fog Results

| Metric              | Fog   | Simple DCP | Full DCP |
| ------------------- | ----- | ---------- | -------- |
| Avg detections      | 6.884 | 4.242      | 8.222    |
| Avg confidence      | 0.567 | 0.518      | 0.531    |
| Avg PRI             | 1     | 0.562      | 1.117    | 

---

# 15. Result Analysis

## Observation 1 — Detection Drops with Fog

Without dehazing:

* Detection count decreases as fog density increases.
* PRI decreases as fog density increases.
* Confidence remains relatively stable.

This demonstrates:

* visibility degradation
* feature suppression
* detection instability under dense fog

---

## Observation 2 — Simplified DCP Performance

Simplified DCP:

* performs worse under medium and dense fog
* reduces detections significantly
* lowers PRI
* lowers confidence

Possible reasons:

* incomplete haze removal
* information distortion
* insufficient contrast recovery

---

## Observation 3 — Full DCP Performance

Full DCP consistently:

* maintains stable detections
* improves PRI under dense fog
* performs strongly under dense fog

Key insight:

> Full DCP significantly improves robustness of object detection under foggy conditions.

---

## Observation 4 — Confidence Trends

Confidence scores remain relatively stable.

This indicates:

* YOLO still detects objects confidently
* but the number of detectable objects changes significantly

Thus:

* detection count becomes a more informative indicator than confidence alone.

---

# 16. Visualization Insights

## Detection vs Fog Density

Observation:

* Fog detections decrease with density
* Simplified DCP drops sharply
* Full DCP remains stable

Interpretation:

Full DCP improves detection robustness.

---

## PRI vs Fog Density

Observation:

* PRI decreases in fog
* Full DCP maintains nearly constant PRI levels

Interpretation:

Full DCP preserves critical driving scene information.

---

## Confidence vs Fog Density

Observation:

* Confidence changes are relatively small
* Detection count variation is more significant

Interpretation:

Visibility primarily affects object discoverability rather than detector certainty.

---

# 17. Why mAP Was Not Used

## Reasons

### 1. Annotation Requirement

mAP requires:

* labeled bounding boxes
* ground truth annotations

for every image.

---

### 2. Project Scope

The project focuses on:

* comparative analysis
* pipeline behavior
* visibility enhancement effects

rather than benchmark competition evaluation.

---

### 3. Computational Simplicity

Proxy metrics:

* are simpler
* faster to compute
* easier to interpret
* sufficient for trend analysis

---

# 18. Advantages of the Project

## Technical Advantages

* Modular pipeline design
* End-to-end automation
* Comparative evaluation framework
* Multi-density analysis
* Realistic driving context

---

## Research Advantages

* Demonstrates fog impact on perception
* Shows importance of visibility enhancement
* Highlights robustness differences between dehazing methods

---

# 19. Limitations

## Current Limitations

### 1. Proxy Metrics

The project does not use:

* mAP
* precision
* recall
* IoU benchmarking

---

### 2. Limited Dehazing Methods

Only:

* Simplified DCP
* Full DCP

are evaluated.

---

### 3. Static Dataset

The project uses image-based evaluation instead of:

* video sequences
* temporal tracking
* real-time driving streams

---

### 4. No Real-Time Optimization

The pipeline prioritizes analysis rather than deployment efficiency.

---

# 20. Future Enhancements

## Possible Extensions

### 1. Deep Learning Dehazing

Integrate:

* AOD-Net
* DehazeNet
* GAN-based dehazing

---

### 2. Standard Evaluation Metrics

Add:

* mAP
* Recall
* Precision
* IoU
* False Positive Rate

---

### 3. Video-Based Processing

Extend the pipeline for:

* dashcam videos
* traffic surveillance
* real-time perception

---

### 4. Real-Time Edge Optimization

Optimize for:

* embedded systems
* autonomous vehicles
* edge AI hardware

---

### 5. Big Data Extension

Possible future extension:

* YouTube API integration
* large-scale fog analysis
* traffic/weather correlation studies
* streaming analytics

---

# 21. Conclusion

This project demonstrates the influence of fog density on object detection performance and evaluates how dehazing techniques improve visibility and detection robustness.

Key findings include:

* Detection performance degrades with increasing fog density.
* Simplified DCP is insufficient under dense fog conditions.
* Full DCP maintains stable object detection performance.
* Proxy metrics effectively reveal visibility-related detection trends.

The project successfully builds a modular end-to-end perception analysis pipeline integrating:

* image enhancement
* object detection
* evaluation
* visualization

The work highlights the importance of visibility restoration for intelligent driving perception systems operating under adverse weather conditions.

---

# 22. Sample README / Execution Guide

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run Pipeline

```bash
python -m src.pipeline.main_pipeline
```

---

## Outputs

Generated outputs are stored inside:

```text
results/
```

Including:

* processed images
* CSV files
* plots
* metric summaries

---

# 23. Expected Outputs

The pipeline generates:

* Detection result images
* Metric CSV files
* Fog-density comparison plots
* Detection statistics
* PRI statistics

---

# 24. Final Summary

This project provides a complete comparative analysis framework for studying:

* fog impact on driving perception
* dehazing effectiveness
* detection robustness
* visibility enhancement techniques

using a modular, automated, and extensible pipeline.
