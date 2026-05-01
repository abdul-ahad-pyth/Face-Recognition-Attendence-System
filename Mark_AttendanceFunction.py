import csv
import os  # 'os' import karna zaroori hai
from datetime import datetime, date  # 'date' bhi datetime se hi nikalta hai

def mark_attendance(roll_no, name, csv_file="attendance.csv"):
    today = date.today().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")

    # Check if already marked today
    if os.path.exists(csv_file):
        with open(csv_file, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                # 'today' pehli column mein hai aur 'roll_no' doosri mein
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