import cv2

# Initialize the webcam
cap = cv2.VideoCapture(1)

# Define the actual width of the object (in inches or any other unit)
actual_width = 5.0  # For example, if the object is 6 inches wide

# Define the focal length of the camera (in pixels)
focal_length = 1000.0  # This value depends on your camera and setup, you may need to calibrate it

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform edge detection, contour detection, and size estimation
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Approximate the largest contour as a polygon
    approx = cv2.approxPolyDP(largest_contour, 0.02 * cv2.arcLength(largest_contour, True), True)
    
    # Calculate the width of the bounding box of the largest contour
    x, y, w, h = cv2.boundingRect(approx)
    
    # Estimate the distance based on the size of the largest contour
    distance = (actual_width * focal_length) / w
    
    # Display the distance on the frame
    cv2.putText(frame, f"Distance: {distance:.2f} inches", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Frame', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam
cap.release()
cv2.destroyAllWindows()
