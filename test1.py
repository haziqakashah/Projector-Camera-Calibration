import cv2
import numpy as np
import xml.etree.ElementTree as ET
import os

def load_calibration_data(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    def get_matrix(node):
        rows = int(node.find('rows').text)
        cols = int(node.find('cols').text)
        data = list(map(float, node.find('data').text.split()))
        return np.array(data).reshape((rows, cols))

    cam_int = get_matrix(root.find('cam_int'))
    cam_dist = get_matrix(root.find('cam_dist'))
    proj_int = get_matrix(root.find('proj_int'))
    proj_dist = get_matrix(root.find('proj_dist'))
    rotation = get_matrix(root.find('rotation'))
    translation = get_matrix(root.find('translation'))

    return cam_int, cam_dist, proj_int, proj_dist, rotation, translation

def project_and_capture_pattern(camera_id, captured_image_path='captured_image.jpg'):
    cap = cv2.VideoCapture(camera_id)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise Exception("Failed to capture image")
    
    # Save the captured image to a file
    cv2.imwrite(captured_image_path, frame)
    return frame, captured_image_path

def undistort_and_reproject(img, cam_int, cam_dist, proj_int, rotation, translation, pattern_size=(7, 7)):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)
    if ret:
        corners_refined = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), 
                                           (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
        points_camera = cv2.undistortPoints(corners_refined, cam_int, cam_dist)
        # Ensure points_camera is in the correct format for cv2.projectPoints
        points_camera = np.squeeze(points_camera)  # Remove single-dimensional entries
        points_camera = points_camera.astype(np.float32)
        points_projector, _ = cv2.projectPoints(points_camera, rotation, translation, proj_int, None)
        return corners_refined, points_projector
    else:
        cv2.imshow('Failed Detection', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        raise Exception("Pattern not found")

def display_results(img, corners, points_projector):
    for point in points_projector:
        cv2.circle(img, tuple(point[0].astype(int)), 5, (0, 255, 0), -1)
    for corner in corners:
        cv2.circle(img, tuple(corner[0].astype(int)), 5, (255, 0, 0), -1)
    
    cv2.imshow('Calibration Test', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def project_image_to_second_screen(image_path, screen_index=1):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to load image from {image_path}")
        return
    
    screen_width, screen_height = 1920, 1080  # Default resolution, you might need to change this
    
    cv2.namedWindow("Second Screen", cv2.WINDOW_NORMAL)
    cv2.moveWindow("Second Screen", screen_width, 0)
    cv2.setWindowProperty("Second Screen", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cv2.imshow("Second Screen", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    filename = 'calibration_result.xml'
    cam_int, cam_dist, proj_int, proj_dist, rotation, translation = load_calibration_data(filename)
    
    camera_id = 0  # Adjust this as necessary
    captured_image_path = 'captured_image.jpg'  # Path to save the captured image
    img, img_path = project_and_capture_pattern(camera_id, captured_image_path)
    
    try:
        corners, points_projector = undistort_and_reproject(img, cam_int, cam_dist, proj_int, rotation, translation)
        display_results(img, corners, points_projector)
    except Exception as e:
        print(str(e))
    
    # Use the path to the captured image
    project_image_to_second_screen(img_path)

if __name__ == "__main__":
    main()
