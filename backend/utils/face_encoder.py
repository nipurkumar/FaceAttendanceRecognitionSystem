import face_recognition
import numpy as np
import cv2
from typing import Optional, Tuple, List

class FaceEncoder:
    """Utility class for face encoding operations"""
    
    @staticmethod
    def extract_face_encoding(image: np.ndarray, face_location: Optional[Tuple] = None) -> Optional[np.ndarray]:
        """
        Extract face encoding from an image
        
        Args:
            image: Input image as numpy array
            face_location: Optional face location tuple
            
        Returns:
            Face encoding as numpy array or None if no face found
        """
        try:
            if face_location:
                face_encodings = face_recognition.face_encodings(image, [face_location])
            else:
                face_locations = face_recognition.face_locations(image)
                if not face_locations:
                    return None
                face_encodings = face_recognition.face_encodings(image, face_locations)
            
            if face_encodings:
                return face_encodings[0]
            return None
            
        except Exception as e:
            print(f"Error extracting face encoding: {e}")
            return None
    
    @staticmethod
    def compare_faces(known_encodings: List[np.ndarray], 
                     face_encoding: np.ndarray, 
                     tolerance: float = 0.6) -> Tuple[List[bool], List[float]]:
        """
        Compare a face encoding against a list of known encodings
        
        Args:
            known_encodings: List of known face encodings
            face_encoding: Face encoding to compare
            tolerance: Distance tolerance for matching
            
        Returns:
            Tuple of (matches list, distances list)
        """
        if not known_encodings:
            return [], []
            
        matches = face_recognition.compare_faces(
            known_encodings, face_encoding, tolerance=tolerance
        )
        distances = face_recognition.face_distance(known_encodings, face_encoding)
        
        return matches, distances.tolist()
    
    @staticmethod
    def get_face_landmarks(image: np.ndarray, face_location: Optional[Tuple] = None) -> Optional[dict]:
        """
        Get facial landmarks for a face in the image
        
        Args:
            image: Input image
            face_location: Optional face location
            
        Returns:
            Dictionary of facial landmarks or None
        """
        try:
            if face_location:
                landmarks = face_recognition.face_landmarks(image, [face_location])
            else:
                landmarks = face_recognition.face_landmarks(image)
            
            if landmarks:
                return landmarks[0]
            return None
            
        except Exception as e:
            print(f"Error getting face landmarks: {e}")
            return None
    
    @staticmethod
    def validate_face_quality(image: np.ndarray, face_location: Tuple) -> Tuple[bool, str]:
        """
        Validate face quality for registration
        
        Args:
            image: Input image
            face_location: Face location tuple
            
        Returns:
            Tuple of (is_valid, message)
        """
        top, right, bottom, left = face_location
        face_width = right - left
        face_height = bottom - top
        
        # Check face size
        if face_width < 100 or face_height < 100:
            return False, "Face too small. Please move closer to camera."
        
        # Check if face is too close to edges
        height, width = image.shape[:2]
        margin = 50
        if left < margin or top < margin or right > width - margin or bottom > height - margin:
            return False, "Face too close to edge. Please center your face."
        
        # Check face aspect ratio
        aspect_ratio = face_width / face_height
        if aspect_ratio < 0.7 or aspect_ratio > 1.3:
            return False, "Please face the camera directly."
        
        # Check image brightness
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_region = gray[top:bottom, left:right]
        mean_brightness = np.mean(face_region)
        
        if mean_brightness < 50:
            return False, "Image too dark. Please improve lighting."
        elif mean_brightness > 200:
            return False, "Image too bright. Please reduce lighting."
        
        return True, "Face quality acceptable."