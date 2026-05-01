import cv2
import face_recognition
import pickle
import numpy as np
from datetime import date
import os

from Mark_AttendanceFunction import mark_attendance 


with open("encodings.pkl", "rb") as f:
    data = pickle.load(f)

known_encodings = data["encodings"]
student_info = data["student_info"] 


known_names = [info[1] for info in student_info]
known_rolls = [info[0] for info in student_info]

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print(" Attendance system started. Press 'q' to quit.")
marked_today = set() 

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.5, fy=0.5)

    face_locations = face_recognition.face_locations(small_frame)
    face_encodings = face_recognition.face_encodings(small_frame, face_locations)

    for (top, right, bottom, left), face_enc in zip(face_locations, face_encodings):
        
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        matches = face_recognition.compare_faces(known_encodings, face_enc, tolerance=0.55)
        distances = face_recognition.face_distance(known_encodings, face_enc)

        name = "Unknown"
        roll = "N/A"

        if len(distances) > 0:
            best_match_index = np.argmin(distances)
            if matches[best_match_index]:
                name = known_names[best_match_index]
                roll = known_rolls[best_match_index]

                
                if roll not in marked_today:
                    mark_attendance(roll, name)
                    marked_today.add(roll)

        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, f"{roll} - {name}", (left, top-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.imshow("Student Attendance System - Press Q to Quit", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print(" Attendance session ended.")