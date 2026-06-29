# Impact of Dehazing on Object Detection in Foggy Driving Environments

## Extended Version: Perception-to-Safety Evaluation Framework

---

## Motivation

Traditional dehazing studies often focus on:

* Visual enhancement
* Contrast improvement
* Image quality restoration

However, improved image appearance does not necessarily imply improved machine perception.

This work investigates:

> How image dehazing influences downstream object detection performance and how perception improvements can be translated into transportation safety insights.

---

## Updated Objective

To evaluate the impact of image dehazing on object detection performance under varying fog densities and translate perception improvements into interpretable transportation safety assessments.

---

## Core Contributions

### 1. Multi-Density Fog Evaluation

Evaluation across:

* No Fog
* Medium Fog
* Dense Fog

### 2. Comparative Dehazing Analysis

Comparison of:

* Raw Foggy Images
* Simplified DCP
* Full DCP

### 3. YOLO-Based Perception Evaluation

Assessment of detection performance after visibility enhancement.

### 4. Proposed Perception Recovery Index (PRI)

A confidence-weighted perception metric combining:

* Detection Count
* Average Confidence

into a single perception effectiveness indicator.

### 5. Transportation Safety Layer

Translation of perception quality into:

* Risk Level
* Recommended Speed
* Estimated Stopping Distance

### 6. Interactive Streamlit Dashboard

Real-time exploration of:

* Fog Densities
* Sample Images
* Dehazing Outputs
* Detection Results
* PRI Analysis
* Safety Assessment

---

## Updated Architecture

Input Images
↓
Fog Density Selection
↓
Dehazing Stage

* No Dehazing
* Simplified DCP
* Full DCP

↓
YOLO Object Detection
↓
Proxy Metrics

* Detection Count
* Average Confidence

↓
Proposed PRI

(Perception Recovery Index)

↓
Transportation Safety Layer

* Risk Assessment
* Speed Recommendation
* Stopping Distance Estimation

↓
Interactive Dashboard

---

## Proposed Perception Recovery Index (PRI)

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

## Transportation Safety Layer

### Purpose

Convert perception quality into understandable driving insights.

### Inputs

* Fog Density
* Detection Count
* Average Confidence
* PRI

### Outputs

#### Risk Level

* HIGH
* MODERATE
* LOW

#### Recommended Speed

| Risk     | Speed   |
| -------- | ------- |
| HIGH     | 20 km/h |
| MODERATE | 40 km/h |
| LOW      | 60 km/h |

#### Stopping Distance

Based on:

* Reaction Distance
* Braking Distance
* Total Stopping Distance

### Important Note

This module is an educational perception-to-safety interpretation framework and is not intended to provide certified driving recommendations.

---

## Interactive Dashboard

### Features

#### Dataset Explorer

* Fog Density Selection
* Sample Image Selection

#### Dehazing Comparison

* Foggy Input
* Simplified DCP
* Full DCP

#### Detection Comparison

* Fog Detection
* Simplified DCP Detection
* Full DCP Detection

#### Quantitative Comparison

* Detection Count
* Average Confidence
* PRI

#### Transportation Safety Assessment

* Risk Level
* Recommended Speed
* Stopping Distance

---

## Novelty

The novelty of this work lies in integrating:

Dehazing
↓
Object Detection
↓
Perception Recovery Analysis
↓
Transportation Safety Interpretation

into a unified perception-to-safety evaluation framework for foggy driving environments.

Unlike traditional dehazing studies that stop at image enhancement or detection evaluation, this project extends the analysis by translating perception quality into interpretable safety insights.

---

## Future Work

* Incorporate annotated driving datasets
* Evaluate using mAP and Recall
* Introduce visibility estimation metrics
* Calibrate safety thresholds using transportation datasets
* Extend to real-time perception systems

---

## Conclusion

This project demonstrates how image dehazing influences downstream object detection performance under foggy driving conditions. The proposed PRI metric and Transportation Safety Layer extend conventional evaluation pipelines by connecting computer vision perception with practical safety-oriented interpretation.
