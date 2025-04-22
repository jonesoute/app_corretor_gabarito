import cv2
import numpy as np

def detect_and_align(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Load the predefined dictionary
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
    parameters = cv2.aruco.DetectorParameters_create()

    # Detect the markers in the image
    corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if ids is None or len(ids) < 4:
        raise ValueError("Não foi possível detectar os 4 marcadores ArUco.")

    # Assume that the markers with IDs 0 to 3 are at the corners
    # Map them to top-left, top-right, bottom-right, bottom-left
    marker_positions = {}
    for corner, id in zip(corners, ids.flatten()):
        marker_positions[id] = corner[0][0]  # Use the first corner point

    if not all(i in marker_positions for i in range(4)):
        raise ValueError("Marcadores ArUco com IDs 0 a 3 são necessários.")

    # Define the destination points for perspective transform
    width, height = 600, 800  # Adjust as needed
    dst_pts = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]
    ], dtype="float32")

    # Order the source points according to destination
    src_pts = np.array([
        marker_positions[0],
        marker_positions[1],
        marker_positions[2],
        marker_positions[3]
    ], dtype="float32")

    # Compute the perspective transform matrix and apply it
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)
    aligned = cv2.warpPerspective(image, M, (width, height))

    return aligned
