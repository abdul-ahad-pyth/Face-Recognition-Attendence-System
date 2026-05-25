import cv2
import face_recognition
import pickle
import numpy as np
from datetime import datetime
import os

from Mark_AttendanceFunction import mark_attendance, mark_absent, mark_remaining_absent

with open("encodings.pkl", "rb") as f:
    data = pickle.load(f)

known_encodings = data["encodings"]
student_info = data["student_info"]   # list of (roll, name) tuples

known_names = [info[1] for info in student_info]
known_rolls = [info[0] for info in student_info]

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print(" Attendance system started.")
print(" Controls: Q = Quit | S = Screenshot | M = Manual absent entry")
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
        top *= 2; right *= 2; bottom *= 2; left *= 2

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
        cv2.putText(frame, f"{roll} - {name}", (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    # Show present count on screen
    cv2.putText(frame, f"Present: {len(marked_today)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Student Attendance System", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        # ✅ On quit — auto-mark everyone not detected as absent
        mark_remaining_absent(student_info, marked_today)
        break

    elif key == ord('s'):
        filename = f"screenshot_{datetime.now().strftime('%H%M%S')}.jpg"
        cv2.imwrite(filename, frame)
        print(f" Saved: {filename}")

    elif key == ord('m'):
        # ✅ Manual absent entry — pause camera, take input in terminal
        print("\n--- MANUAL ABSENT ENTRY ---")
        print("Registered students:")
        for i, (roll, name) in enumerate(student_info):
            status = "✓ Present" if roll in marked_today else "  ---"
            print(f"  {i+1}. {roll} - {name}  [{status}]")

        entry = input("Enter Roll No to mark ABSENT (or press Enter to cancel): ").strip()
        if entry:
            # Find the student by roll number
            match = next(((r, n) for r, n in student_info if r == entry), None)
            if match:
                mark_absent(match[0], match[1])
                # Remove from present set if they were wrongly detected
                marked_today.discard(match[0])
            else:
                print(f" Roll No '{entry}' not found in registered students.")

cap.release()
cv2.destroyAllWindows()
print(" Attendance session ended.")