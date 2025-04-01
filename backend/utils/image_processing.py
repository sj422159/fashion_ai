import cv2
import numpy as np
import mediapipe as mp
from PIL import Image

def validate_and_save_image(file, save_path):
    """
    Validates the uploaded image file format and saves it to the specified path.
    
    Args:
        file (werkzeug.FileStorage): The uploaded image file.
        save_path (str): The path to save the validated image.
        
    Returns:
        str: The path of the saved image.
    """
    allowed_extensions = {'jpeg', 'jpg', 'png'}
    if not (file.filename.lower().endswith(tuple(allowed_extensions))):
        raise ValueError("Invalid file format. Only JPEG and PNG are allowed.")

    # Save the file using PIL
    image = Image.open(file)
    image = image.convert("RGB")  # Ensure the image is in RGB format
    image.save(save_path)
    return save_path


def process_user_image(image_path):
    """
    Processes the uploaded image and creates a 3D model based on the user's body dimensions and posture.
    
    Args:
        image_path (str): Path to the uploaded image.
        
    Returns:
        dict: A dictionary containing user body dimensions and posture data.
    """
    mp_pose = mp.solutions.pose
    body_dimensions = {}

    # Load the image
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Initialize Mediapipe Pose
    with mp_pose.Pose(static_image_mode=True, model_complexity=2, enable_segmentation=True) as pose:
        results = pose.process(image_rgb)
        if not results.pose_landmarks:
            raise ValueError("Unable to detect body landmarks. Please upload a clear full-body image.")

        # Extract key body landmarks and dimensions
        landmarks = results.pose_landmarks.landmark
        body_dimensions = {
            'shoulder_width': calculate_distance(landmarks, mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.RIGHT_SHOULDER),
            'waist_width': calculate_distance(landmarks, mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.RIGHT_HIP),
            'height': calculate_height(landmarks),
        }

        # Return pose visualization (optional)
        annotated_image = image.copy()
        mp.solutions.drawing_utils.draw_landmarks(
            annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        cv2.imwrite("static/annotated_image.jpg", annotated_image)  # Save the annotated image for feedback

    return body_dimensions


def calculate_distance(landmarks, point1, point2):
    """
    Calculates the Euclidean distance between two body landmarks.
    
    Args:
        landmarks (list): List of body landmarks from Mediapipe Pose.
        point1 (int): Index of the first landmark.
        point2 (int): Index of the second landmark.
        
    Returns:
        float: The distance between the two landmarks.
    """
    x1, y1, z1 = landmarks[point1].x, landmarks[point1].y, landmarks[point1].z
    x2, y2, z2 = landmarks[point2].x, landmarks[point2].y, landmarks[point2].z
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)


def calculate_height(landmarks):
    """
    Estimates the user's height based on body landmarks.
    
    Args:
        landmarks (list): List of body landmarks from Mediapipe Pose.
        
    Returns:
        float: Estimated height of the user.
    """
    # Approximation: Use the distance between the head and feet landmarks
    head_to_feet = calculate_distance(landmarks, mp.solutions.pose.PoseLandmark.NOSE, mp.solutions.pose.PoseLandmark.LEFT_ANKLE)
    return head_to_feet * 170  # Assume a scaling factor (e.g., 170 cm for normalization)
