# 🧠 Face Recognition Attendance System (FRAS)

A smart, modular, and full-stack web-based _Face Recognition Attendance System_ built using _Python (Flask)_ for the backend and _MongoDB_ for database management. It leverages _facial recognition_ to automate attendance tracking securely and efficiently.

---

## 📁 Project Structure

FRAS/
├── backend/
│ ├── utils/ # Facial encoding and processing
│ ├── models/ # MongoDB models/schemas (if using ODM like MongoEngine)
│ ├── app.py # Flask app entry point
│ ├── database.py # MongoDB connection logic
│ ├── requirements.txt # Python dependencies
│ └── init.py
├── data/
│ ├── attendance_logs/ # Exported attendance files (CSV or JSON)
│ ├── database/ # MongoDB (for local dev) or configs
│ ├── registered_faces/ # Saved face images
│ └── init.py
├── frontend/
│ ├── assets/ # Images, videos, logos
│ ├── css/ # Stylesheets
│ ├── js/ # Frontend JavaScript
│ ├── index.html # Landing page
│ └── README.md # UI-specific documentation
├── venv/ # Python virtual environment

---

## 🚀 Features

- 🔍 Face detection using face_recognition and OpenCV
- 📸 User registration via webcam
- ✅ Real-time attendance logging
- 📅 Export attendance to CSV
- 🧠 MongoDB for storing:
  - User profiles
  - Attendance history
  - Face encodings (optionally as binary/BSON or cloud links)
- 💻 Responsive frontend with smooth UI/UX
- 📦 Modular code structure for scalability

---

## 🛠 Tech Stack

| Component        | Technology                         |
| ---------------- | ---------------------------------- |
| Backend          | Python, Flask                      |
| Database         | MongoDB (via pymongo)              |
| Face Recognition | OpenCV, face_recognition           |
| Frontend         | HTML, CSS, JavaScript              |
| UI Effects       | Lottie, animations, video BGs      |
| Storage          | MongoDB GridFS or local filesystem |
| Styling          | Bootstrap / Custom CSS             |

---

## ⚙ Setup Instructions

### 🔧 Prerequisites

- Python 3.8+
- MongoDB (local or Atlas URI)
- Node.js (optional, for advanced JS features)

### 📥 Clone Repository

```bash
git clone https://github.com/nipurkumar/FaceAttendanceRecognitionSystem.git
cd FRAS

📦 Install Python Dependencies

cd backend
pip install -r requirements.txt

🔌 Configure MongoDB

In backend/database.py, set your MongoDB URI:

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")  # or use Atlas URI
db = client["attendance_system"]

OR store credentials securely using .env:

MONGODB_URI=mongodb+srv://<user>:<pass>@cluster.mongodb.net/attendance

🚀 Run Flask Server

cd backend
python app.py

🌐 Open the Frontend

Open frontend/index.html in your browser or host using Flask routes.

⸻

🧪 Functional Flow
	1.	User Registration
	•	Capture name + face via webcam
	•	Save image + generate face encoding
	•	Store in MongoDB (User collection)
	2.	Mark Attendance
	•	Detect face via webcam
	•	Compare with database
	•	On match → mark present (timestamp, date)
	3.	View Attendance
	•	Admin dashboard loads attendance logs from MongoDB
	•	Option to export to CSV

⸻

💾 MongoDB Collections Example

👤 users

{
  "_id": ObjectId,
  "name": "John Doe",
  "face_encoding": [0.123, 0.456, ...],
  "registered_at": ISODate("2025-07-12T08:00:00Z")
}

🗓 attendance_logs

{
  "_id": ObjectId,
  "user_id": ObjectId,
  "name": "John Doe",
  "timestamp": ISODate("2025-07-12T09:30:00Z"),
  "status": "Present"
}


⸻

📊 Optional Features (Extendable)
	•	🎥 Live video attendance mode
	•	🔐 Admin login panel
	•	📈 Attendance analytics charts
	•	📤 Cloud sync (Firebase, Google Drive, Sheets)
	•	🧪 Liveness detection (anti-spoofing)
	•	📲 Progressive Web App (PWA) for mobile use

⸻

📦 Requirements

Flask
face_recognition
opencv-python
pymongo
dnspython
python-dotenv
numpy


⸻

📜 License

This project is licensed under the MIT License.

⸻

🙌 Credits
	•	face_recognition by @ageitgey
	•	MongoDB for flexible data storage
	•	Bootstrap & Pexels for UI inspiration
	•	OpenCV & Dlib for face detection

⸻

📫 Contact

Developer: Nipur Kumar
📧 nipurkumar84@gmail.com
🔗 GitHub | LinkedIn

---
```
