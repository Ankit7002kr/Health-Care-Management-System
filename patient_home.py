import sys
import os
import firebase_admin
from firebase_admin import credentials, db
import tkinter as tk
from tkinter import ttk, messagebox
import threading

def load_firebase_data():
    """Load Firebase data asynchronously."""
    threading.Thread(target=load_doctors, daemon=True).start()
    threading.Thread(target=load_appointments, daemon=True).start()
    threading.Thread(target=load_medical_resources, daemon=True).start()
def go_back():
    root.destroy()  # Close the current window
    os.system("python login.py")  # Run the login script


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

# Retrieve user email
if len(sys.argv) >= 2:
    user_email = sys.argv[1]
else:
    messagebox.showerror("Error", "No user details provided.")
    sys.exit()


def load_doctors():
    doctor_tree.delete(*doctor_tree.get_children())  # Clear existing data

    ref = db.reference("doctors")
    doctors = ref.get()

    if doctors:
        for key, doctor in doctors.items():
            doctor_tree.insert("", "end", values=(
                doctor.get("name", "N/A"),
                doctor.get("availability", "N/A"),
                doctor.get("specialization", "N/A")
            ))


def book_appointment():
    patient_name = name_entry.get()
    patient_age = age_entry.get()
    issue = issue_entry.get()

    selected_item = doctor_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a doctor.")
        return

    doctor_data = doctor_tree.item(selected_item[0], "values")
    doctor_name = doctor_data[0]
    doctor_availability = doctor_data[1]

    if not all([patient_name, patient_age, issue]):
        messagebox.showerror("Error", "Please fill in all details")
        return

    ref = db.reference("appointments")
    new_appointment_ref = ref.push()
    appointment_data = {
        "patient_email": user_email,
        "patient_name": patient_name,
        "patient_age": patient_age,
        "issue": issue,
        "doctor_name": doctor_name,
        "date": doctor_availability,
        "status": "Pending"
    }
    new_appointment_ref.set(appointment_data)
    messagebox.showinfo("Notice", "Your appointment request has been received. Kindly visit the hospital for your treatment.")
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    issue_entry.delete(0, tk.END)

    load_firebase_data()

# Load Appointments from Firebase
def load_appointments():
    appointment_tree.delete(*appointment_tree.get_children())

    ref = db.reference("appointments")
    appointments = ref.get()

    if appointments:
        for key, appointment in appointments.items():
            if appointment.get("patient_email", "").lower() == user_email.lower():
                appointment_tree.insert("", "end", values=(
                    appointment.get("patient_name", "N/A"),
                    appointment.get("date", "N/A"),
                    appointment.get("issue", "N/A"),
                    appointment.get("patient_age", "N/A"),
                    appointment.get("doctor_name", "N/A"),
                    appointment.get("status", "N/A")
                ))

# Load Medical Resources
def load_medical_resources():
    medicine_tree.delete(*medicine_tree.get_children())

    ref = db.reference("medicines")
    medicines = ref.get()

    if medicines:
        for key, medicine in medicines.items():
            medicine_tree.insert("", "end", values=(
                medicine.get("name", "N/A"),
                medicine.get("price", "N/A"),
                medicine.get("quantity", "N/A")
            ))

# Request Ambulance
def request_ambulance():
    location = location_entry.get()
    if location:
        messagebox.showinfo("Initiated", f"Ambulance requested for {location}!")
    else:
        messagebox.showerror("Error", "Please enter a location.")

# Function to switch between sections
def show_section(section):
    for widget in main_frame.winfo_children():
        widget.pack_forget()

    if section == "Appointments":
        appointment_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        booking_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        doctor_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Ensuring Doctor Table is shown

        load_firebase_data()
    elif section == "Medical Resources":
        medical_resources_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        load_firebase_data()
    elif section=="Back":
        go_back()
    elif section == "Ambulance Helpline":
        ambulance_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create main window
root = tk.Tk()
root.geometry('1440x750+50+50')
root.title('Patient Dashboard')
root.configure(bg='#f0f0f0')

# Top Menu Bar
menu_bar = tk.Frame(root, bg='#2c3e50', height=50)
menu_bar.pack(fill=tk.X)

for text in ["Appointments", "Medical Resources", "Ambulance Helpline","Back"]:
    tk.Button(menu_bar, text=text, command=lambda t=text: show_section(t), font=("Helvetica", 14),
              bg='#2c3e50', fg='white', relief=tk.FLAT, padx=10, pady=5).pack(side=tk.LEFT, padx=10)

# Main Frame
main_frame = tk.Frame(root, bg='#f0f0f0')
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Appointment Section UI
booking_frame = tk.LabelFrame(main_frame, text="Book an Appointment", font=("Helvetica", 16, "bold"), bg='#f0f0f0')
labels = ["Patient Name", "Patient's Age", "Issue"]
entries = []
for i, label_text in enumerate(labels):
    tk.Label(booking_frame, text=label_text, font=("Helvetica", 14), bg='#f0f0f0').grid(row=i, column=0, padx=10,
                                                                                        pady=10, sticky="w")
    entry = tk.Entry(booking_frame, font=("Helvetica", 14), width=30)
    entry.grid(row=i, column=1, padx=10, pady=10, sticky="w")
    entries.append(entry)
name_entry, age_entry, issue_entry = entries

tk.Button(booking_frame, text="Book Appointment", command=book_appointment, bg='#2c3e50', fg='white',
          font=("Helvetica", 14, "bold"), padx=20, pady=10).grid(row=len(labels), column=0, columnspan=2, pady=20)
# Medical Resources Section UI
medical_resources_frame = tk.LabelFrame(main_frame, text="Medical Resources", font=("Helvetica", 16, "bold"), bg='#f0f0f0')

medicine_columns = ("Medicine Name", "Price", "Quantity")
medicine_tree = ttk.Treeview(medical_resources_frame, columns=medicine_columns, show="headings", height=10)

for col in medicine_columns:
    medicine_tree.heading(col, text=col)
    medicine_tree.column(col, anchor="center", width=150)

medicine_tree.pack(fill=tk.BOTH, expand=True)

# Doctor Selection Table
doctor_frame = tk.LabelFrame(main_frame, text="Available Doctors", font=("Helvetica", 16, "bold"), bg='#f0f0f0')
doctor_columns = ("Name", "Availability", "Specialization")
doctor_tree = ttk.Treeview(doctor_frame, columns=doctor_columns, show="headings", height=10)

for col in doctor_columns:
    doctor_tree.heading(col, text=col)
    doctor_tree.column(col, anchor="center", width=150)
doctor_tree.pack(fill=tk.BOTH, expand=True)
# Ambulance Helpline Section UI
ambulance_frame = tk.LabelFrame(main_frame, text="Ambulance Helpline", font=("Helvetica", 16, "bold"), bg='#f0f0f0')

tk.Label(ambulance_frame, text="Enter Location:", font=("Helvetica", 14), bg='#f0f0f0').pack(pady=10)
location_entry = tk.Entry(ambulance_frame, font=("Helvetica", 14), width=30)
location_entry.pack(pady=10)

tk.Button(ambulance_frame, text="Request Ambulance", command=request_ambulance, bg='#c0392b', fg='white',
          font=("Helvetica", 14, "bold"), padx=20, pady=10).pack(pady=20)

# Updated Appointment Table
appointment_frame = tk.LabelFrame(main_frame, text="Your Appointments", font=("Helvetica", 16, "bold"), bg='#f0f0f0')
appointment_columns = ("Patient Name", "Date", "Issue", "Age", "Doctor", "Status")
appointment_tree = ttk.Treeview(appointment_frame, columns=appointment_columns, show="headings", height=10)

for col in appointment_columns:
    appointment_tree.heading(col, text=col)
    appointment_tree.column(col, anchor="center", width=150)
appointment_tree.pack(fill=tk.BOTH, expand=True)

show_section("Appointments")
root.mainloop()