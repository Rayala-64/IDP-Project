# Impact of Dehazing on Object Detection in Foggy Driving Environments

## Project Overview

### Problem Statement

Fog significantly reduces visibility in driving environments, making object detection systems less reliable. In autonomous driving and Advanced Driver Assistance Systems (ADAS), reduced visibility can lead to:

* Missed object detections
* Lower confidence scores
* Reduced situational awareness
* Increased driving risk

This project analyzes how image dehazing techniques influence object detection performance under different fog densities.

The project compares:

* Detection directly on foggy images
* Detection after Simplified DCP dehazing
* Detection after Full DCP dehazing

Evaluation is performed across:

* No Fog
* Medium Fog
* Dense Fog

---

## Objective

To analyze whether image dehazing improves object detection performance under foggy driving conditions.

Focus areas:

* Visibility enhancement
* Detection consistency
* Detection robustness
* Comparative evaluation of dehazing approaches

---

## Key Contributions

### Comparative Fog Analysis

Evaluation across:

* No Fog
* Medium Fog
* Dense Fog

### Dehazing Comparison

Comparison of:

* Raw Foggy Images
* Simplified DCP
* Full DCP

### Pipeline-Based Evaluation

Integrated pipeline consisting of:

* Dehazing
* Object Detection
* Evaluation
* Metric Generation
* Visualization

### Practical Proxy Metrics

Instead of annotation-heavy metrics such as:

* mAP
* Precision
* Recall
* F1-score

The project uses lightweight proxy metrics for comparative evaluation.

---

## Dataset

Approximately:

* 600 Images Total
* 200 Images per Fog Density

| Fog Density | Images |
| ----------- | ------ |
| No_Fog      | ~200   |
| Medium_Fog  | ~200   |
| Dense_Fog   | ~200   |

---

## Technologies

| Component           | Technology              |
| ------------------- | ----------------------- |
| Language            | Python                  |
| Image Processing    | OpenCV                  |
| Numerical Computing | NumPy                   |
| Data Handling       | Pandas                  |
| Visualization       | Matplotlib              |
| Object Detection    | YOLO                    |
| Evaluation          | Custom Metrics Pipeline |

---

## Architecture

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
Metrics Extraction
↓
CSV Generation
↓
Visualization & Analysis

---

## Proxy Metrics

### Average Detection Count

Average number of detected objects per image.

### Average Confidence

Average confidence score of detected objects.

---

## Conclusion

The project evaluates how dehazing affects object detection performance under varying fog densities and compares the effectiveness of Simplified DCP and Full DCP approaches.
