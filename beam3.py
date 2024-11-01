import cv2

def project_image_to_second_screen(image_path, screen_index=1):
    # Load the image
    image = cv2.imread(image_path)
    
    # Check if the image was loaded successfully
    if image is None:
        print(f"Error: Unable to load image from {image_path}")
        return
    
    # Get screen resolution
    screen_width, screen_height = 1920, 1080  # Default resolution, you might need to change this
    
    # Create a window on the second screen
    cv2.namedWindow("Second Screen", cv2.WINDOW_NORMAL)
    cv2.moveWindow("Second Screen", screen_width, 0)
    cv2.setWindowProperty("Second Screen", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Show the image on the second screen
    cv2.imshow("Second Screen", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# # Example usage
# project_image_to_second_screen("exp_11.jpg", screen_index=1)

# for main screen
# def project_image_to_main_screen(image_path):
#     # Load the image
#     image = cv2.imread(image_path)
    
#     # Check if the image was loaded successfully
#     if image is None:
#         print(f"Error: Unable to load image from {image_path}")
#         return
    
#     # Create a window on the main screen
#     cv2.namedWindow("Main Screen", cv2.WINDOW_NORMAL)
#     cv2.setWindowProperty("Main Screen", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

#     # Show the image on the main screen
#     cv2.imshow("Main Screen", image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# # Example usage
# project_image_to_main_screen("exp_11.jpg")
