import cv2
import numpy as np
from PIL import Image
def perform_dress_fitting(user_image_path, dress_image_path):
    """
    Simulates the fitting of a dress onto a user's 3D model.
    
    Args:
        user_image_path (str): Path to the user's uploaded image.
        dress_image_path (str): Path to the extracted dress image.
        
    Returns:
        dict: A dictionary containing the fitting results.
    """
    try:
        # Load user image
        user_image = cv2.imread(user_image_path, cv2.IMREAD_UNCHANGED)
        if user_image is None:
            raise ValueError("User image could not be loaded.")
        
        # Load dress image
        dress_image = cv2.imread(dress_image_path, cv2.IMREAD_UNCHANGED)
        if dress_image is None:
            raise ValueError("Dress image could not be loaded.")
        
        # Resize dress image to fit user image dimensions
        dress_resized = cv2.resize(dress_image, (user_image.shape[1], user_image.shape[0]), interpolation=cv2.INTER_AREA)
        
        # Overlay the dress on the user image
        result = overlay_images(user_image, dress_resized)
        
        # Save the final fitted image
        fitted_image_path = "static/fitted_image.jpg"
        cv2.imwrite(fitted_image_path, result)
        
        return {'fitted_image': fitted_image_path}
    
    except Exception as e:
        raise RuntimeError(f"Error during dress fitting simulation: {e}")

def overlay_dress(user_image_path, dress_image_path, body_dimensions):
    """
    Overlays the extracted dress image onto the user's 3D model.
    
    Args:
        user_image_path (str): Path to the user's uploaded image.
        dress_image_path (str): Path to the extracted dress image.
        body_dimensions (dict): User's body dimensions, including shoulder width and waist width.
        
    Returns:
        str: Path to the final fitted image.
    """
    try:
        # Load user image
        user_image = cv2.imread(user_image_path, cv2.IMREAD_UNCHANGED)
        if user_image is None:
            raise ValueError("User image could not be loaded.")

        # Load dress image
        dress_image = cv2.imread(dress_image_path, cv2.IMREAD_UNCHANGED)
        if dress_image is None:
            raise ValueError("Dress image could not be loaded.")

        # Resize dress image to fit user's body dimensions
        dress_width = int(body_dimensions['shoulder_width'] * user_image.shape[1])  # Scale based on shoulder width
        dress_height = int(body_dimensions['height'] * user_image.shape[0])  # Scale based on height

        dress_resized = cv2.resize(dress_image, (dress_width, dress_height), interpolation=cv2.INTER_AREA)

        # Calculate position to overlay the dress (aligned to shoulders)
        user_height, user_width = user_image.shape[:2]
        x_offset = (user_width - dress_width) // 2
        y_offset = int(user_height * 0.3)  # Assume the dress starts near the top 30% of the image

        # Overlay the dress on the user image
        result = overlay_images(user_image, dress_resized, x_offset, y_offset)

        # Save the final fitted image
        fitted_image_path = "static/fitted_image.jpg"
        cv2.imwrite(fitted_image_path, result)
        return fitted_image_path

    except Exception as e:
        raise RuntimeError(f"Error during dress fitting simulation: {e}")


def overlay_images(base_image, overlay_image, x_offset, y_offset):
    """
    Overlays one image onto another at a specific position, handling transparency.
    
    Args:
        base_image (numpy.ndarray): The base image.
        overlay_image (numpy.ndarray): The image to overlay.
        x_offset (int): The x-coordinate for overlay positioning.
        y_offset (int): The y-coordinate for overlay positioning.
        
    Returns:
        numpy.ndarray: The resulting image with the overlay.
    """
    # Ensure the overlay image has an alpha channel for transparency
    if overlay_image.shape[2] < 4:
        overlay_image = cv2.cvtColor(overlay_image, cv2.COLOR_BGR2BGRA)

    # Overlay bounds
    y1, y2 = y_offset, y_offset + overlay_image.shape[0]
    x1, x2 = x_offset, x_offset + overlay_image.shape[1]

    # Ensure overlay dimensions do not exceed base image dimensions
    y2 = min(y2, base_image.shape[0])
    x2 = min(x2, base_image.shape[1])

    # Overlay transparency handling
    alpha_overlay = overlay_image[:, :, 3] / 255.0
    alpha_base = 1.0 - alpha_overlay

    for c in range(0, 3):  # Loop over color channels
        base_image[y1:y2, x1:x2, c] = (
            alpha_overlay * overlay_image[:, :, c] +
            alpha_base * base_image[y1:y2, x1:x2, c]
        )

    return base_image


if __name__ == "__main__":
    # Example usage
    try:
        # Sample user image and dress image paths
        user_image_path = "uploads/sample_user_image.jpg"
        dress_image_path = "static/extracted_dress_image.png"

        # Example body dimensions (assume values are normalized)
        body_dimensions = {
            'shoulder_width': 0.4,  # 40% of image width
            'waist_width': 0.3,     # 30% of image width
            'height': 0.6           # 60% of image height
        }

        # Simulate dress fitting
        fitted_image = overlay_dress(user_image_path, dress_image_path, body_dimensions)
        print(f"Fitted image saved at: {fitted_image}")

    except Exception as e:
        print(f"Error: {e}")
