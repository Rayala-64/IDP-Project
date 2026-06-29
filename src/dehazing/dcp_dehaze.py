# pyrefly: ignore [missing-import]
import cv2
import numpy as np


# -------------------------
# Dark Channel
# -------------------------
def get_dark_channel(img, patch_size=15):
    min_channel = np.min(img, axis=2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (patch_size, patch_size))
    dark = cv2.erode(min_channel, kernel)
    return dark


# -------------------------
# Atmospheric Light
# -------------------------
def estimate_atmospheric_light(img, dark):
    h, w = dark.shape
    num_pixels = int(max(h * w * 0.001, 1))  # top 0.1%

    dark_vec = dark.reshape(h * w)
    img_vec = img.reshape(h * w, 3)

    indices = dark_vec.argsort()[-num_pixels:]  # brightest in dark channel

    A = np.mean(img_vec[indices], axis=0)
    return A


# -------------------------
# Transmission Map
# -------------------------
def estimate_transmission(img, A, patch_size=15, omega=0.95):
    norm_img = img / A
    dark_norm = get_dark_channel(norm_img, patch_size)
    t = 1 - omega * dark_norm
    return t


# -------------------------
# Recover Image
# -------------------------
def recover_image(img, t, A, t0=0.1):
    t = np.clip(t, t0, 1)

    J = np.empty_like(img)
    for i in range(3):
        J[:, :, i] = (img[:, :, i] - A[i]) / t + A[i]

    J = np.clip(J, 0, 1)
    return J


# -------------------------
# Main Function
# -------------------------
def dehaze_dcp(img):
    img = img.astype(np.float32) / 255.0

    dark = get_dark_channel(img)
    A = estimate_atmospheric_light(img, dark)
    t = estimate_transmission(img, A)
    J = recover_image(img, t, A)

    return (J * 255).astype(np.uint8)


