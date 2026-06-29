# pyrefly: ignore [missing-import]
from ultralytics import YOLO

# Load once globally (efficient)
model = YOLO("models/yolo/yolov8n.pt")


def detect(img):
    """
    Runs YOLO detection on input image
    Returns: YOLO results object
    """
    if img is None:
        raise ValueError("Input image is None")

    results = model(img, verbose=False)  # disable console output

    return results




# pyrefly: ignore [missing-import]
import cv2

img = cv2.imread("dataset/raw/No_Fog/080.png")

results = model(img, verbose=False)

results[0].show()  # display output"""