# pyrefly: ignore [missing-import]
import cv2
import numpy as np

def dehaze(img):
    """
    Simple Dark Channel Prior (approximation)
    Input: BGR image (uint8)
    Output: Dehazed BGR image (uint8)
    """

    if img is None:
        raise ValueError("Input image is None")

    img = img.astype(np.float32) / 255.0

    # Dark channel
    dark = np.min(img, axis=2)

    # Transmission map
    t = 1 - 0.95 * dark
    t = np.clip(t, 0.1, 1)   # avoid division issues

    # Recover image
    J = img / t[:, :, None]
    J = np.clip(J, 0, 1)

    return (J * 255).astype(np.uint8)


# Optional testing block
if __name__ == "__main__":
    img = cv2.imread("dataset/raw/Medium_Fog/020.png")

    output = dehaze(img)

    cv2.imshow("Original", img)
    cv2.imshow("Dehazed", output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()