from pymongo import MongoClient
from datetime import datetime, date
import os
from bson import ObjectId

class Database:
    def __init__(self):
        # MongoDB connection
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['face_recognition_attendance']
        self.users = self.db['users']
        self.attendance = self.db['attendance']
        
        # Create indexes
        self.users.create_index("student_id", unique=True)
        self.attendance.create_index([("student_id", 1), ("date", -1)])
    
    def add_user(self, student_id, name, email=None, department=None):
        """Add new user to database"""
        try:
            user_doc = {
                "student_id": student_id,
                "name": name,
                "email": email,
                "department": department,
                "registered_date": datetime.utcnow(),
                "face_encodings": [],
                "profile_images": []
            }
            
            result = self.users.insert_one(user_doc)
            return str(result.inserted_id)
        except Exception as e:
            if "duplicate key error" in str(e):
                return None
            raise e
    
    def get_user(self, student_id):
        """Get user by student ID"""
        return self.users.find_one({"student_id": student_id})
    
    def update_user_face_encoding(self, student_id, encoding, image_path):
        """Update user's face encoding"""
        self.users.update_one(
            {"student_id": student_id},
            {
                "$push": {
                    "face_encodings": encoding.tolist(),
                    "profile_images": image_path
                }
            }
        )
    
    def get_all_users(self):
        """Get all registered users"""
        return list(self.users.find({}, {"_id": 0, "face_encodings": 0}))
    
    def mark_attendance(self, student_id, confidence=0.0, location="Main Campus"):
        """Mark attendance for a student"""
        today = datetime.now().date()
        
        # Check if already marked today
        existing = self.attendance.find_one({
            "student_id": student_id,
            "date": today.isoformat()
        })
        
        if existing:
            return None  # Already marked
        
        # Mark attendance
        attendance_doc = {
            "student_id": student_id,
            "timestamp": datetime.utcnow(),
            "date": today.isoformat(),
            "confidence": confidence,
            "location": location,
            "check_in_time": datetime.now().strftime("%H:%M:%S"),
            "status": "present"
        }
        
        result = self.attendance.insert_one(attendance_doc)
        
        # Update user's last seen
        self.users.update_one(
            {"student_id": student_id},
            {"$set": {"last_seen": datetime.utcnow()}}
        )
        
        return str(result.inserted_id)
    
    def get_today_attendance(self):
        """Get today's attendance records"""
        today = date.today().isoformat()
        
        pipeline = [
            {"$match": {"date": today}},
            {"$lookup": {
                "from": "users",
                "localField": "student_id",
                "foreignField": "student_id",
                "as": "user_info"
            }},
            {"$unwind": "$user_info"},
            {"$project": {
                "student_id": 1,
                "name": "$user_info.name",
                "timestamp": 1,
                "check_in_time": 1,
                "confidence": 1,
                "location": 1
            }},
            {"$sort": {"timestamp": -1}}
        ]
        
        records = list(self.attendance.aggregate(pipeline))
        
        # Convert ObjectId to string
        for record in records:
            record['_id'] = str(record['_id'])
        
        return records
    
    def get_attendance_report(self, start_date, end_date):
        """Get attendance report for date range"""
        pipeline = [
            {"$match": {
                "date": {
                    "$gte": start_date,
                    "$lte": end_date
                }
            }},
            {"$group": {
                "_id": "$student_id",
                "days_present": {"$sum": 1},
                "attendance_dates": {"$push": "$date"}
            }},
            {"$lookup": {
                "from": "users",
                "localField": "_id",
                "foreignField": "student_id",
                "as": "user_info"
            }},
            {"$unwind": "$user_info"},
            {"$project": {
                "student_id": "$_id",
                "name": "$user_info.name",
                "days_present": 1,
                "attendance_dates": 1
            }},
            {"$sort": {"name": 1}}
        ]
        
        return list(self.attendance.aggregate(pipeline))
    
    def get_user_attendance_history(self, student_id, limit=30):
        """Get attendance history for a specific user"""
        records = self.attendance.find(
            {"student_id": student_id},
            {"_id": 0}
        ).sort("date", -1).limit(limit)
        
        return list(records)
    
    def get_attendance_statistics(self):
        """Get overall attendance statistics"""
        today = date.today().isoformat()
        
        # Total registered users
        total_users = self.users.count_documents({})
        
        # Present today
        present_today = self.attendance.count_documents({"date": today})
        
        # Average attendance this month
        month_start = date.today().replace(day=1).isoformat()
        
        pipeline = [
            {"$match": {"date": {"$gte": month_start}}},
            {"$group": {
                "_id": "$date",
                "count": {"$sum": 1}
            }},
            {"$group": {
                "_id": None,
                "avg_attendance": {"$avg": "$count"}
            }}
        ]
        
        result = list(self.attendance.aggregate(pipeline))
        avg_attendance = result[0]['avg_attendance'] if result else 0
        
        return {
            "total_users": total_users,
            "present_today": present_today,
            "absent_today": total_users - present_today,
            "average_attendance": round(avg_attendance, 2),
            "attendance_rate": round((present_today / total_users * 100) if total_users > 0 else 0, 2)
        }