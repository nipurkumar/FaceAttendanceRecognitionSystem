import cv2
import numpy as np
from PIL import Image
import io
import base64
from typing import Tuple, Optional

class ImageProcessor:
    """Utility class for image processing operations"""
    
    @staticmethod
    def resize_image(image: np.ndarray, max_width: int = 800) -> np.ndarray:
        """Resize image while maintaining aspect ratio"""
        height, width = image.shape[:2]
        
        if width > max_width:
            scale = max_width / width
            new_width = int(width * scale)
            new_height = int(height * scale)
            return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        return image
    
    @staticmethod
    def enhance_image(image: np.ndarray) -> np.ndarray:
        """Enhance image quality for better face recognition"""
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Merge channels
        enhanced = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        
        # Denoise
        enhanced = cv2.fastNlMeansDenoisingColored(enhanced, None, 10, 10, 7, 21)
        
        return enhanced
    
    @staticmethod
    def detect_blur(image: np.ndarray) -> Tuple[bool, float]:
        """
        Detect if image is blurry
        
        Returns:
            Tuple of (is_blurry, variance)
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        variance = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Threshold for blur detection
        threshold = 100.0
        is_blurry = variance < threshold
        
        return is_blurry, variance
    
    @staticmethod
    def crop_face(image: np.ndarray, face_location: Tuple, padding: float = 0.2) -> np.ndarray:
        """
        Crop face from image with padding
        
        Args:
            image: Input image
            face_location: Face location (top, right, bottom, left)
            padding: Padding percentage
            
        Returns:
            Cropped face image
        """
        top, right, bottom, left = face_location
        height, width = image.shape[:2]
        
        # Add padding
        pad_width = int((right - left) * padding)
        pad_height = int((bottom - top) * padding)
        
        # Calculate new boundaries with padding
        new_top = max(0, top - pad_height)
        new_bottom = min(height, bottom + pad_height)
        new_left = max(0, left - pad_width)
        new_right = min(width, right + pad_width)
        
        return image[new_top:new_bottom, new_left:new_right]
    
    @staticmethod
    def draw_face_box(image: np.ndarray, face_location: Tuple, name: str, 
                     color: Tuple[int, int, int] = (0, 255, 0)) -> np.ndarray:
        """Draw bounding box and name on face"""
        top, right, bottom, left = face_location
        
        # Draw rectangle
        cv2.rectangle(image, (left, top), (right, bottom), color, 2)
        
        # Draw name background
        cv2.rectangle(image, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
        
        # Draw name
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(image, name, (left + 6, bottom - 6), font, 0.6, (255, 255, 255), 1)
        
        return image
    
    @staticmethod
    def base64_to_image(base64_string: str) -> Optional[np.ndarray]:
        """Convert base64 string to numpy array image"""
        try:
            # Remove data URL prefix if present
            if ',' in base64_string:
                base64_string = base64_string.split(',')[1]
            
            # Decode base64
            image_bytes = base64.b64decode(base64_string)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to numpy array
            return np.array(image)
            
        except Exception as e:
            print(f"Error converting base64 to image: {e}")
            return None
    
    @staticmethod
    def image_to_base64(image: np.ndarray) -> str:
        """Convert numpy array image to base64 string"""
        try:
            _, buffer = cv2.imencode('.jpg', image)
            image_base64 = base64.b64encode(buffer).decode('utf-8')
            return f"data:image/jpeg;base64,{image_base64}"
        except Exception as e:
            print(f"Error converting image to base64: {e}")
            return ""
    
    @staticmethod
    def apply_face_alignment(image: np.ndarray, face_landmarks: dict) -> np.ndarray:
        """Align face based on eye positions"""
        try:
            left_eye = np.mean(face_landmarks['left_eye'], axis=0)
            right_eye = np.mean(face_landmarks['right_eye'], axis=0)
            
            dY = right_eye[1] - left_eye[1]
            dX = right_eye[0] - left_eye[0]
            angle = np.degrees(np.arctan2(dY, dX))
            
            eyes_center = ((left_eye[0] + right_eye[0]) // 2,
                          (left_eye[1] + right_eye[1]) // 2)
            
            M = cv2.getRotationMatrix2D(eyes_center, angle, 1.0)
            aligned = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]),
                                   flags=cv2.INTER_CUBIC)
            
            return aligned
        except Exception as e:
            print(f"Error aligning face: {e}")
            return image