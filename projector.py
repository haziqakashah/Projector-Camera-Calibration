import cv2 as cv
import numpy as np
import pickle

# Load camera calibration parameters
with open("calibration.pkl", "rb") as f:
    cameraMatrix, dist = pickle.load(f)

# Initialize video capture from the camera
cap = cv.VideoCapture(0)

# Define chessboard size
chessboardSize = (9, 7)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break
    
    # Undistort the frame
    undistorted_frame = cv.undistort(frame, cameraMatrix, dist)
    
    # Convert to grayscale
    gray = cv.cvtColor(undistorted_frame, cv.COLOR_BGR2GRAY)
    
    # Find chessboard corners
    ret, corners = cv.findChessboardCorners(gray, chessboardSize, None)
    
    if ret:
        # Project corners to projector space
        # Here you would calculate the corresponding points in the projector space
        
        # For demonstration, let's just draw circles on detected corners
        for corner in corners:
            x, y = corner.ravel()
            cv.circle(frame, (x, y), 5, (0, 0, 255), -1)
        
        # Display the frame with detected corners
        cv.imshow('Projector Output', frame)
    
    # Exit on ESC key press
    if cv.waitKey(1) == 27:
        break

# Release video capture and close windows
cap.release()
cv.destroyAllWindows()
