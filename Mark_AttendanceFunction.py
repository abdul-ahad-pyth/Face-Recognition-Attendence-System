import csv
import os
from datetime import datetime, date

def mark_attendance(roll_no, name, csv_file="attendance.csv"):
    today = date.today().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")

    if os.path.exists(csv_file):
        with open(csv_file, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] == today and row[1] == roll_no:
                    print(f" {name} already marked present today!")
                    return False

    file_exists = os.path.exists(csv_file) and os.path.getsize(csv_file) > 0

    with open(csv_file, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Date", "Roll No", "Name", "Time", "Status"])
        writer.writerow([today, roll_no, name, current_time, "Present"])

    print(f" Attendance marked: {roll_no} - {name} at {current_time}")
    return True


# ✅ NEW FUNCTION — manually mark a student absent
def mark_absent(roll_no, name, csv_file="attendance.csv"):
    today = date.today().strftime("%Y-%m-%d")

    # Check if already marked today (present or absent) — skip if so
    if os.path.exists(csv_file):
        with open(csv_file, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] == today and row[1] == roll_no:
                    print(f" {name} already recorded today (skipping absent mark).")
                    return False

    file_exists = os.path.exists(csv_file) and os.path.getsize(csv_file) > 0

    with open(csv_file, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Date", "Roll No", "Name", "Time", "Status"])
        # Time is empty for absent — they weren't there
        writer.writerow([today, roll_no, name, "", "Absent"])

    print(f" Marked ABSENT: {roll_no} - {name}")
    return True


# ✅ NEW FUNCTION — auto-mark all undetected students as absent
def mark_remaining_absent(student_info, marked_today_set, csv_file="attendance.csv"):
    print("\n--- Auto-marking absent students ---")
    absent_count = 0
    for roll, name in student_info:
        if roll not in marked_today_set:
            mark_absent(roll, name, csv_file)
            absent_count += 1
    print(f" Total absent: {absent_count}\n")