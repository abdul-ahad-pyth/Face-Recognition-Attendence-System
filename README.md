# 🚀 Smart Face Recognition Attendance System

A professional real-time attendance system built with Python, OpenCV, and Face Recognition library. This project automatically detects faces, matches them with a pre-encoded database, and marks attendance in a CSV file.

## ✨ Key Features
- **Real-time Recognition:** High-speed face detection using dlib and OpenCV.
- **Smart Attendance:** Logic to prevent duplicate entries in a single session.
- **Auto-CSV Generation:** Creates and updates `attendance.csv` with timestamps automatically.
- **Optimized Performance:** Uses frame resizing for smoother video processing.

## 🛠️ Installation & Setup

1. **Clone the Project:**
   ```bash
   git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
   cd your-repo-name
2. Setup Virtual Environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
3. Install Dependencies:
   ```bash
   pip install -r requirements.txt
4. How to Use

   Step 1: Prepare Database
   Place student photos in the student_photos/ folder.

   Format the file name as: RollNo_Name.jpg (e.g., 101_Ali.jpg).

   Step 2: Generate Encodings
   Run the following command to process photos and create the encodings.pkl file:
   python student_database.py


   Step 3: Run Attendance System
   Start the camera and mark attendance:
   python main_attendance.py
   Press 'q' to quit the session.


5. Project Structure
   student_database.py: Scripts to encode faces and save data.

   main_attendance.py: Main script for camera and recognition logic.

   attendance.csv: Records marked with Date, Roll No, Name, and Time.

   requirements.txt: List of all necessary Python libraries.

6. 📝 Requirements
   Python 3.10+

   OpenCV

   Face-Recognition Library

   Numpy

Developed with  by []





   

