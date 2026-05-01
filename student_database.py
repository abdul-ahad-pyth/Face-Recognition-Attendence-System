import face_recognition
import pickle
import os
from datetime import date

def create_student_database(photo_folder="student_photos"):
    encodings = []
    student_info = [] 

    
    if not os.path.exists(photo_folder):
        print(f"Error: Folder '{photo_folder}' nahi mila!")
        return

    for filename in os.listdir(photo_folder):
        if filename.lower().endswith((".jpg", ".png", ".jpeg")):
            name_part = os.path.splitext(filename)[0]
            
        
            try:
                roll_no, student_name = name_part.split("_", 1)
            except ValueError:
                print(f"Skipping {filename}: Name format 'RollNo_Name' ")
                continue

            image_path = os.path.join(photo_folder, filename)
            image = face_recognition.load_image_file(image_path)
            enc = face_recognition.face_encodings(image)

            if len(enc) > 0:
                encodings.append(enc[0])
                student_info.append([roll_no, student_name])
                print(f"Encoded: {roll_no} - {student_name}")
            else:
                print(f"No face found in {filename}")

    data = {
        "encodings": encodings,
        "student_info": student_info, 
        "last_updated": str(date.today())
    }

    # Data save karna
    with open("encodings.pkl", "wb") as f:
        pickle.dump(data, f)

    print(f"\nStudent database created with {len(encodings)} students!")
    return data

# Run this once
if __name__ == "__main__":
    create_student_database()