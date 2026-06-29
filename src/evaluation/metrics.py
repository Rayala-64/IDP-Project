import numpy as np

# Driving-relevant COCO class IDs
DRIVING_CLASSES = {0, 1, 2, 3, 5, 6, 7, 9, 11}
# person, bicycle, car, motorcycle, bus, train, truck, traffic light, stop sign


def compute_metrics(results):
    """
    Extract essential detection metrics from YOLO results.

    Returns:
        count          : total number of detections
        avg_conf       : mean confidence score (0 if no detections)
        driving_count  : number of detections relevant to driving safety
    """

    boxes = results[0].boxes
    count = len(boxes)

    # No detections case
    if count == 0:
        return {
            "count": 0,
            "avg_conf": 0.0,
            "driving_count": 0,
        }

    # Extract confidence and class IDs
    conf = boxes.conf.cpu().numpy()
    cls  = boxes.cls.cpu().numpy().astype(int)

    # Compute metrics
    avg_conf = float(np.mean(conf))
    driving_count = int(np.sum(np.isin(cls, list(DRIVING_CLASSES))))

    return {
        "count": count,
        "avg_conf": avg_conf,
        "driving_count": driving_count,
    }