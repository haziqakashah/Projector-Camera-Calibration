import cv2
import os
import time

TARGETDIR = './graycode_pattern'
CAPTUREDDIR = './captured_images'

def project_image_to_second_screen(image, screen_index=1):
    # Get screen resolution (you might need to change this)
    screen_width, screen_height = 1280, 720
    
    # Create a window on the second screen
    cv2.namedWindow("Second Screen", cv2.WINDOW_NORMAL)
    cv2.moveWindow("Second Screen", screen_width, 0)
    cv2.setWindowProperty("Second Screen", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    # Show the image on the second screen
    cv2.imshow("Second Screen", image)
    cv2.waitKey(1)  # Display the image for at least 1 ms

def capture_image_from_camera(cam_index=0):
    cap = cv2.VideoCapture(cam_index)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None
    ret, frame = cap.read()
    cap.release()
    if not ret:
        print("Error: Failed to capture image.")
        return None
    return frame

def main():
    if not os.path.exists(CAPTUREDDIR):
        os.makedirs(CAPTUREDDIR)
    
    pattern_files = sorted([f for f in os.listdir(TARGETDIR) if f.endswith('.png')])
    
    for i, pattern_file in enumerate(pattern_files):
        image_path = os.path.join(TARGETDIR, pattern_file)
        image = cv2.imread(image_path)
        
        if image is None:
            print(f"Error: Unable to load image from {image_path}")
            continue
        
        # Project the image to the second screen
        project_image_to_second_screen(image)
        
        # Allow some time for the camera to adjust to the projected image
        time.sleep(1)  # Adjust this delay as needed
        
        # Capture the image from the camera
        captured_image = capture_image_from_camera()
        
        if captured_image is not None:
            # Save the captured image
            capture_path = os.path.join(CAPTUREDDIR, f'graycode_{str(i).zfill(2)}.png')
            cv2.imwrite(capture_path, captured_image)
            print(f"Captured image saved to {capture_path}")
        
        # Close the projection window
        cv2.destroyWindow("Second Screen")
        
        # Short delay to avoid any issues with window management
        time.sleep(0.5)

if __name__ == '__main__':
    main()
