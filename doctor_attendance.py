import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import firebase_admin
from firebase_admin import credentials, db
import os
import sys
import threading
import subprocess

def get_firebase_data():
    threading.Thread(target=load_doctors, daemon=True).start()
# Firebase Initialization


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):  # When bundled by PyInstaller
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

cred_path = resource_path("healthcare-management-sy-7134e-firebase-adminsdk-fbsvc-177d58ab4d.json")

if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://healthcare-management-sy-7134e-default-rtdb.firebaseio.com/"
        })
    except Exception as e:
        print("Firebase init error:", e)
        messagebox.showerror("Firebase Error", f"Failed to initialize Firebase:\n{e}")
        sys.exit()
def go_back():
    root.destroy()
    subprocess.run(["python", "home.py"])

# GUI Setup
root = tk.Tk()
root.title("Doctor Attendance")
root.geometry('1440x750+50+50')
root.configure(bg="#f0f0f0")

tk.Label(root, text="Doctor Attendance", font=("Helvetica", 24, "bold"), bg="#2c3e50", fg="white").pack(fill="x", pady=10)

# Date Picker
date_frame = tk.Frame(root, bg="#f0f0f0")
date_frame.pack(pady=20)

tk.Label(date_frame, text="Select Date:", font=("Helvetica", 14), bg="#f0f0f0").pack(side="left", padx=10)
date_entry = DateEntry(date_frame, font=("Helvetica", 14), date_pattern='yyyy-mm-dd')
date_entry.pack(side="left")

# Scrollable Frame for Doctor List
checkbox_frame = tk.Frame(root, bg="#f0f0f0")
checkbox_frame.pack(pady=20, fill="both", expand=True)

canvas = tk.Canvas(checkbox_frame, bg="#f0f0f0", highlightthickness=0)
scrollbar = tk.Scrollbar(checkbox_frame, orient="vertical", command=canvas.yview)
scrollable = tk.Frame(canvas, bg="#f0f0f0")

scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Checkbox storage
doctor_checkboxes = []

def load_doctors():
    doctor_checkboxes.clear()
    for widget in scrollable.winfo_children():
        widget.destroy()

    try:
        ref = db.reference("doctors")
        doctors = ref.get()
        if not doctors:
            tk.Label(scrollable, text="No doctor records found.", bg="#f0f0f0", font=("Helvetica", 12)).pack()
            return

        for doctor in doctors.values():
            name = doctor.get("name", "")
            if name:
                var = tk.BooleanVar()
                cb = tk.Checkbutton(scrollable, text=name, variable=var, font=("Helvetica", 12), bg="#f0f0f0")
                cb.pack(anchor="w", padx=20, pady=5)
                doctor_checkboxes.append((name, var))
    except Exception as e:
        print("Error loading doctors:", e)
        messagebox.showerror("Error", f"Failed to load doctor list:\n{e}")

# Save attendance to Firebase
def submit_attendance():
    selected_date = date_entry.get()
    if not selected_date:
        status_label.config(text="Please select a date", fg="red")
        return

    data = {}
    for name, var in doctor_checkboxes:
        data[name] = "Present" if var.get() else "Absent"

    try:
        ref = db.reference(f"attendance/{selected_date}")
        ref.set(data)
        status_label.config(text="Attendance saved successfully!", fg="green")
        print(f"Saved to Firebase: attendance/{selected_date}")
        print(data)
    except Exception as e:
        print("Error submitting attendance:", e)
        status_label.config(text="Failed to save attendance", fg="red")
        messagebox.showerror("Error", f"Could not submit attendance:\n{e}")

def select_all():
    for _, var in doctor_checkboxes:
        var.set(True)

def clear_all():
    for _, var in doctor_checkboxes:
        var.set(False)

btn_frame = tk.Frame(root, bg="#f0f0f0")
btn_frame.pack()

tk.Button(btn_frame, text="Select All", command=select_all, bg="#5cb85c", fg="white",
          font=("Helvetica", 12), padx=10).pack(side="left", padx=10)
tk.Button(btn_frame, text="Clear All", command=clear_all, bg="#d9534f", fg="white",
          font=("Helvetica", 12), padx=10).pack(side="left", padx=10)
# Submit button
submit_btn = tk.Button(root, text="Submit", font=("Helvetica", 14), bg="#2c3e50", fg="white", padx=20, pady=10,
                       command=submit_attendance)
submit_btn.pack(pady=10)

status_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#f0f0f0")
status_label.pack()

back_btn = tk.Button(root, text="Back", command=go_back,
                     font=("Helvetica", 14, "bold"),
                     bg='#d9534f', fg='white',
                     activebackground='#c9302c',
                     relief=tk.FLAT, padx=15, pady=5)
back_btn.place(x=10, y=10)


# Load doctor list
get_firebase_data()
root.mainloop()
