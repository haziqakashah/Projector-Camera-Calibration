import cv2
import numpy as np
import matplotlib.pyplot as plt

# Function to track the dot
def track_dot(frame):
    # Convert the frame to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define the lower and upper bounds for the color (here, red)
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    
    # Threshold the HSV image to get only red colors
    mask = cv2.inRange(hsv_frame, lower_red, upper_red)
    
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # If contours are found
    if contours:
        # Get the largest contour (assuming it's the dot)
        contour = max(contours, key=cv2.contourArea)
        
        # Get the centroid of the contour
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            return cx, cy
    return None, None

# Function to project dot
def project_dot(frame, x, y):
    # Draw a dot on the frame at coordinates (x, y)
    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
    return frame

# Main function
def main():
    # Open camera
    cap = cv2.VideoCapture(0)
    
    # Open projector
    # Initialize projector here
    
    # Loop to capture frames from the camera
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Track the dot
        x, y = track_dot(frame)
        
        # If dot is found, project it
        if x is not None and y is not None:
            # Project dot on screen
            # Use x, y coordinates to adjust the projected dot location
            
            # Display the frame with projected dot
            frame = project_dot(frame, x, y)
        
        # Display the frame
        cv2.imshow('Frame', frame)
        
        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
