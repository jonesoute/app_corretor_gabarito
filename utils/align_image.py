import cv2
import numpy as np

def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]      # top-left
    rect[2] = pts[np.argmax(s)]      # bottom-right

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]   # top-right
    rect[3] = pts[np.argmax(diff)]   # bottom-left

    return rect

def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    widthA = np.hypot(br[0] - bl[0], br[1] - bl[1])
    widthB = np.hypot(tr[0] - tl[0], tr[1] - tl[1])
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.hypot(tr[0] - br[0], tr[1] - br[1])
    heightB = np.hypot(tl[0] - bl[0], tl[1] - bl[1])
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped

def detect_and_align(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    square_contours = []

    for c in contours:
        approx = cv2.approxPolyDP(c, 0.02 * cv2.arcLength(c, True), True)
        area = cv2.contourArea(c)
        if len(approx) == 4 and area > 1000:
            square_contours.append(approx.reshape(4, 2))

    if len(square_contours) < 4:
        raise ValueError("Não foi possível detectar os 4 quadrados pretos nas bordas.")

    # Pega os 4 quadrados com maior área
    square_contours = sorted(square_contours, key=cv2.contourArea, reverse=True)[:4]

    # Concatena os centros de cada quadrado
    centers = []
    for sq in square_contours:
        M = cv2.moments(sq)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        centers.append([cX, cY])

    return four_point_transform(image, np.array(centers, dtype="float32"))

