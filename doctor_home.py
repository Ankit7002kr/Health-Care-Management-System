import sys


import os
import firebase_admin
from firebase_admin import credentials, db
import tkinter as tk
from tkinter import font as tkfont, ttk, messagebox
import subprocess
import threading

from openpyxl import Workbook
from tkinter import filedialog

def load_firebase_data():

    threading.Thread(target=load_leaves, daemon=True).start()
    threading.Thread(target=load_history, daemon=True).start()
    threading.Thread(target=load_appointments, daemon=True).start()
    threading.Thread(target=load_attendance, daemon=True).start()

def export_to_excel():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")],
        title="Save Attendance As"
    )

    if not file_path:
        return  # User canceled save dialog

    try:
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Attendance Records"

        # Write headers
        headers = [attendance_tree.heading(col)["text"] for col in attendance_tree["columns"]]
        sheet.append(headers)

        # Write data rows
        for row_id in attendance_tree.get_children():
            row = attendance_tree.item(row_id)['values']
            sheet.append(row)

        workbook.save(file_path)
        tk.messagebox.showinfo("Success", f"Data exported to:\n{file_path}")
    except Exception as e:
        tk.messagebox.showerror("Error", f"Failed to export data:\n{e}")
# Firebase Configuration
def open_patients():
    root.destroy()
    subprocess.run([sys.executable, "patients.py"])
def go_back():
    root.destroy()
    subprocess.run([sys.executable, "login.py"])
# Load Data Functions
def load_appointments():
    appointment_tree.delete(*appointment_tree.get_children())

    ref = db.reference("appointments")
    appointments = ref.get()
    if appointments:
        for key, appointment in appointments.items():
            if appointment.get("status", "Pending") == "Pending":
                appointment_tree.insert("", "end", values=(
                    key, appointment.get("patient_name", ""), appointment.get("date", ""), appointment.get("time", ""),
                    "Pending"))

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):  # When bundled by PyInstaller
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

cred_path = resource_path("healthcare-management-sy-7134e-firebase-adminsdk-fbsvc-177d58ab4d.json")

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://healthcare-management-sy-7134e-default-rtdb.firebaseio.com/"
    })

def load_attendance():
    attendance_tree.delete(*attendance_tree.get_children())  # Clear table

    ref = db.reference("attendance")
    attendance_data = ref.get()

    if attendance_data:
        for date, doctors in attendance_data.items():
            for doctor_name, status in doctors.items():
                attendance_tree.insert("", "end", values=(doctor_name, date, status))



def load_leaves():
    leave_tree.delete(*leave_tree.get_children())  # Clear table before loading new data

    ref = db.reference("leaves")
    leave_data = ref.get()

    if leave_data:
        for key, entry in leave_data.items():
            leave_tree.insert("", "end", values=(
                entry.get("doctor_name", ""),
                entry.get("date", ""),
                entry.get("reason", "")
            ))

# Function to submit leave request
def submit_leave():
    doctor_name = doctor_name_entry.get().strip()
    leave_date = leave_date_entry.get().strip()
    reason = reason_entry.get("1.0", tk.END).strip()

    if not doctor_name or not leave_date or not reason:
        messagebox.showwarning("Error", "All fields are required!")
        return

    try:
        ref = db.reference("leaves")
        ref.push({
            "doctor_name": doctor_name,
            "date": leave_date,
            "reason": reason
        })
        messagebox.showinfo("Success", "Leave request submitted successfully!")

        # Clear fields after submission
        doctor_name_entry.delete(0, tk.END)
        leave_date_entry.delete(0, tk.END)
        reason_entry.delete("1.0", tk.END)

        # Refresh leave history
        load_firebase_data()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to submit leave: {str(e)}")

# Function to switch frames
def show_frame(frame):
    attendance_frame.pack_forget()
    appointment_frame.pack_forget()
    leave_frame.pack_forget()
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
def load_history():
    history_tree.delete(*history_tree.get_children())

    ref = db.reference("appointments")
    appointments = ref.get()
    if appointments:
        for key, appointment in appointments.items():
            if appointment.get("status", "") != "Pending":
                history_tree.insert("", "end", values=(
                    appointment.get("patient_name", ""),
                    appointment.get("date", ""),
                    appointment.get("time", ""),
                    appointment.get("status", ""),
                    appointment.get("doctor_comment", "")
                ))

# Create main window
root = tk.Tk()
root.geometry('1440x750+50+50')
root.title('Doctor Dashboard')
root.configure(bg='#f0f0f0')

# Title Bar
title_bar = tk.Frame(root, bg='#2c3e50', height=50)
title_bar.pack(fill=tk.X)
title_font = tkfont.Font(family="Helvetica", size=26, weight="bold")
tk.Label(title_bar, text="Doctor Dashboard", font=title_font, bg='#2c3e50', fg="white").pack(pady=5)

# Frames
attendance_frame = tk.Frame(root, bg='#f0f0f0')
leave_frame = tk.Frame(root, bg='#f0f0f0')
appointment_frame = tk.Frame(root, bg='#f0f0f0')

# Buttons Frame
button_frame = tk.Frame(root, bg='#f0f0f0')
button_frame.pack(anchor="nw", padx=10, pady=5)

tk.Button(button_frame, text="Attendance", command=lambda: show_frame(attendance_frame), font=("Helvetica", 12),
          bg="#3498db", fg="white").pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Appointments", command=lambda: show_frame(appointment_frame), font=("Helvetica", 12),
          bg="#2ecc71", fg="white").pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Leaves", command=lambda: show_frame(leave_frame), font=("Helvetica", 12), bg="#e67e22",
          fg="white").pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Back", command=go_back, font=("Helvetica", 12), bg="#e67e22",
          fg="white").pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Patient History", command=open_patients, font=("Helvetica", 12), bg="#e67e22",
          fg="white").pack(side=tk.LEFT, padx=5)
def search_attendance(doctor_query):
    attendance_tree.delete(*attendance_tree.get_children())  # Clear table

    ref = db.reference("attendance")
    attendance_data = ref.get()

    if attendance_data:
        for date, daily_attendance in attendance_data.items():
            for doctor, status in daily_attendance.items():
                if doctor_query.lower() in doctor.lower():
                    attendance_tree.insert("", "end", values=(doctor, date, status))

# Attendance Section
search_attendance_frame = tk.Frame(attendance_frame, bg="#f0f0f0")
search_attendance_frame.pack(pady=10)
tk.Label(search_attendance_frame, text="Search Doctor:", font=("Helvetica", 12), bg="#f0f0f0").pack(side="left", padx=5)

search_attendance_entry = tk.Entry(search_attendance_frame, font=("Helvetica", 12), width=30)
search_attendance_entry.pack(side="left", padx=5)

search_attendance_button = tk.Button(
    search_attendance_frame, text="Search", font=("Helvetica", 12), bg="#2c3e50", fg="white",
    command=lambda: search_attendance(search_attendance_entry.get())
)
search_attendance_button.pack(side="left", padx=5)

export_data = tk.Button(search_attendance_frame, text="Export", font=("Helvetica", 12), bg="#2c3e50", fg="white",
                      command=export_to_excel)
export_data.pack(side="left",padx=(0, 30))
attendance_columns = ("Doctor Name", "Date", "Status")

attendance_tree = ttk.Treeview(attendance_frame, columns=attendance_columns, show="headings", height=10)

# Define column headings
for col in attendance_columns:
    attendance_tree.heading(col, text=col)
    attendance_tree.column(col, anchor="center", width=150)

attendance_tree.pack(fill=tk.BOTH, expand=True)

# Function to Load Attendance Data


# Call function to load attendance on startup



# **Appointment Section**
appointment_columns = ("ID", "Patient Name", "Date", "Time", "Status")
appointment_tree = ttk.Treeview(appointment_frame, columns=appointment_columns, show="headings", height=10)

for col in appointment_columns:
    appointment_tree.heading(col, text=col)
    appointment_tree.column(col, anchor="center", width=150)

appointment_tree.pack(fill=tk.BOTH, expand=True)

appointment_status_vars = {}
doctor_comments = {}

status_frame = tk.Frame(appointment_frame, bg="#f0f0f0")
status_frame.pack(fill=tk.X, pady=5)

tk.Label(status_frame, text="Select Status:", font=("Helvetica", 12), bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
status_dropdown = ttk.Combobox(status_frame, values=["Success", "Not Available"], font=("Helvetica", 12))
status_dropdown.pack(side=tk.LEFT, padx=5)

tk.Label(status_frame, text="Doctor Comment:", font=("Helvetica", 12), bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
comment_box = tk.Text(status_frame, height=2, width=30)
comment_box.pack(side=tk.LEFT, padx=5)


def update_selected_status():
    selected_item = appointment_tree.selection()
    if not selected_item:
        messagebox.showwarning("Error", "Please select an appointment!")
        return

    appointment_id = appointment_tree.item(selected_item[0], "values")[0]
    status = status_dropdown.get()
    comment = comment_box.get("1.0", tk.END).strip()

    if status:
        ref = db.reference("appointments").child(appointment_id)
        ref.update({"status": status, "doctor_comment": comment})

        messagebox.showinfo("Success", "Appointment updated successfully!")

        load_firebase_data()


tk.Button(status_frame, text="Update Status", command=update_selected_status, font=("Helvetica", 12),
          bg="#e74c3c", fg="white").pack(side=tk.LEFT, padx=5)

# **Patient History Table**
history_columns = ("Patient Name", "Date", "Time", "Status", "Doctor Comment")
history_tree = ttk.Treeview(appointment_frame, columns=history_columns, show="headings", height=10)
for col in history_columns:
    history_tree.heading(col, text=col)
    history_tree.column(col, anchor="center", width=150)
history_tree.pack(fill=tk.BOTH, expand=True)

# **Leave Section**
tk.Label(leave_frame, text="Doctor Name:", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=2)
doctor_name_entry = tk.Entry(leave_frame, font=("Helvetica", 12))
doctor_name_entry.pack(pady=5)

tk.Label(leave_frame, text="Leave Date:", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=2)
leave_date_entry = tk.Entry(leave_frame, font=("Helvetica", 12))
leave_date_entry.pack(pady=5)

tk.Label(leave_frame, text="Reason:", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=2)
reason_entry = tk.Text(leave_frame, height=4, width=50)
reason_entry.pack(pady=5)

leave_tree = ttk.Treeview(leave_frame, columns=("Doctor Name", "Date", "Reason"), show="headings", height=10)
for col in ("Doctor Name", "Date", "Reason"):
    leave_tree.heading(col, text=col)
    leave_tree.column(col, anchor="center", width=150)
leave_tree.pack(fill=tk.BOTH, expand=True)
load_firebase_data()
tk.Button(leave_frame, text="Submit Leave",
          command=submit_leave,
          font=("Helvetica", 12), bg="#e74c3c", fg="white").pack(pady=5)


show_frame(appointment_frame)
root.mainloop()
