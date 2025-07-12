from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import cv2
import base64
import numpy as np
from datetime import datetime
import os
from face_recognition_module import FaceRecognitionSystem
from database_mongo import Database

app = Flask(__name__)
CORS(app)

# Initialize components
face_system = FaceRecognitionSystem()
db = Database()

# Video capture for live feed
camera = None

@app.route('/')
def index():
    return jsonify({"status": "Face Recognition Attendance System API Running"})

@app.route('/api/register', methods=['POST'])
def register_face():
    """Register a new face in the system"""
    try:
        data = request.json
        name = data.get('name')
        student_id = data.get('student_id')
        image_data = data.get('image')
        
        # Decode base64 image
        image_bytes = base64.b64decode(image_data.split(',')[1])
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Register face
        success, message = face_system.register_face(image, name, student_id)
        
        if success:
            # Save to database
            db.add_user(student_id, name)
            return jsonify({"success": True, "message": message})
        else:
            return jsonify({"success": False, "message": message}), 400
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/recognize', methods=['POST'])
def recognize_face():
    """Recognize face and mark attendance"""
    try:
        data = request.json
        image_data = data.get('image')
        
        # Decode base64 image
        image_bytes = base64.b64decode(image_data.split(',')[1])
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Recognize face
        result = face_system.recognize_face(image)
        
        if result['success']:
            # Mark attendance
            attendance_id = db.mark_attendance(result['student_id'])
            result['attendance_id'] = attendance_id
            result['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/attendance/today')
def get_today_attendance():
    """Get today's attendance records"""
    try:
        records = db.get_today_attendance()
        return jsonify({"success": True, "records": records})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/attendance/report')
def get_attendance_report():
    """Get attendance report for date range"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        records = db.get_attendance_report(start_date, end_date)
        return jsonify({"success": True, "records": records})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

def generate_frames():
    """Generate frames for video streaming"""
    global camera
    camera = cv2.VideoCapture(0)
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Detect and mark faces
            marked_frame = face_system.mark_faces_in_frame(frame)
            
            ret, buffer = cv2.imencode('.jpg', marked_frame)
            frame = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/api/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, port=5000)