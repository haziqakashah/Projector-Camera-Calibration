import cv2
import numpy as np

# Load the camera-projector calibration parameters from the XML file
calibration_data = cv2.FileStorage("calibration_result.xml", cv2.FILE_STORAGE_READ)

# Read camera intrinsic matrix and distortion coefficients
cam_int = calibration_data.getNode("cam_int").mat()
cam_dist = calibration_data.getNode("cam_dist").mat()

# Read projector intrinsic matrix and distortion coefficients
proj_int = calibration_data.getNode("proj_int").mat()
proj_dist = calibration_data.getNode("proj_dist").mat()

# Read rotation matrix and translation vector
rotation = calibration_data.getNode("rotation").mat()
translation = calibration_data.getNode("translation").mat()

# Release the file storage
calibration_data.release()

# Load the image you want to project
image_to_project = cv2.imread('test.jpg')

# Undistort the image using camera calibration parameters
undistorted_image = cv2.undistort(image_to_project, cam_int, cam_dist)

# Project the image using the projector calibration parameters and transformation
# Apply the rotation and translation from camera to projector
# For simplicity, you can directly warp the undistorted image using warpPerspective
h, w = undistorted_image.shape[:2]
new_camera_matrix, _ = cv2.getOptimalNewCameraMatrix(cam_int, cam_dist, (w, h), 1, (w, h))
map1, map2 = cv2.initUndistortRectifyMap(cam_int, cam_dist, None, new_camera_matrix, (w, h), cv2.CV_32FC1)
undistorted_image = cv2.remap(undistorted_image, map1, map2, interpolation=cv2.INTER_LINEAR)

# Create the projection matrix (3x3) by using proj_int directly
projection_matrix = proj_int

# Project the undistorted image using the projection matrix
projected_image = cv2.warpPerspective(undistorted_image, projection_matrix, (w, h))

# Display the projected image using a projector library or hardware
# Example: Using OpenCV to display on screen (not suitable for projecting on physical surfaces)
cv2.imshow('Projected Image', projected_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
