import face_recognition
import cv2
import numpy as np
import os
import json
from datetime import datetime
from database_mongo import Database

class FaceRecognitionSystem:
    def __init__(self):
        self.db = Database()
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_face_ids = []
        self.load_registered_faces()
        
    def load_registered_faces(self):
        """Load all registered faces from MongoDB"""
        users = self.db.users.find({"face_encodings": {"$exists": True, "$ne": []}})
        
        for user in users:
            if user.get('face_encodings'):
                # Convert list back to numpy array
                for encoding in user['face_encodings']:
                    self.known_face_encodings.append(np.array(encoding))
                    self.known_face_names.append(user['name'])
                    self.known_face_ids.append(user['student_id'])
    
    def register_face(self, image, name, student_id, email=None, department=None):
        """Register a new face in the system"""
        try:
            # Find face in image
            face_locations = face_recognition.face_locations(image)
            
            if len(face_locations) == 0:
                return False, "No face detected in image"
            
            if len(face_locations) > 1:
                return False, "Multiple faces detected. Please ensure only one face is in the image"
            
            # Get face encoding
            face_encoding = face_recognition.face_encodings(image, face_locations)[0]
            
            # Check if face already exists
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            if True in matches:
                return False, "Face already registered in the system"
            
            # Check if user already exists
            existing_user = self.db.get_user(student_id)
            
            if existing_user:
                # Add new face encoding to existing user
                self.db.update_user_face_encoding(student_id, face_encoding, f"{student_id}_{datetime.now().timestamp()}.jpg")
            else:
                # Create new user
                user_id = self.db.add_user(student_id, name, email, department)
                if user_id:
                    self.db.update_user_face_encoding(student_id, face_encoding, f"{student_id}.jpg")
                else:
                    return False, "User with this ID already exists"
            
            # Save face image
            face_img_path = f"../data/registered_faces/{student_id}_{datetime.now().timestamp()}.jpg"
            os.makedirs(os.path.dirname(face_img_path), exist_ok=True)
            cv2.imwrite(face_img_path, image)
            
            # Update memory
            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(name)
            self.known_face_ids.append(student_id)
            
            return True, "Face registered successfully"
            
        except Exception as e:
            return False, f"Error registering face: {str(e)}"
    
    def recognize_face(self, image):
        """Recognize face in image"""
        try:
            # Find faces in image
            face_locations = face_recognition.face_locations(image)
            
            if len(face_locations) == 0:
                return {'success': False, 'message': 'No face detected'}
            
            # Get face encodings
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            for face_encoding in face_encodings:
                # Compare with known faces
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.6)
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                
                if True in matches:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        student_id = self.known_face_ids[best_match_index]
                        confidence = 1 - face_distances[best_match_index]
                        
                        return {
                            'success': True,
                            'name': name,
                            'student_id': student_id,
                            'confidence': float(confidence)
                        }
            
            return {'success': False, 'message': 'Face not recognized'}
            
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def mark_faces_in_frame(self, frame):
        """Mark recognized faces in video frame"""
        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Find faces
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"
            
            if True in matches:
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
            
            face_names.append(name)
        
        # Draw boxes and labels
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            # Draw box
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            
            # Draw label
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.6, (255, 255, 255), 1)
        
        return frame