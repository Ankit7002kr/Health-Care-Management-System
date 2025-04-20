import sys
import os
import firebase_admin
from firebase_admin import credentials, db
import tkinter as tk
from tkinter import font as tkfont, ttk
import subprocess
import threading

def get_firebase_data():
    threading.Thread(target=load_data, daemon=True).start()

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

cred_path = resource_path("healthcare-management-sy-7134e-firebase-adminsdk-fbsvc-177d58ab4d.json")

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://healthcare-management-sy-7134e-default-rtdb.firebaseio.com/"
    })

selected_doctor_key = None

def save_data(name, specialization, phone, email, address, experience, department, availability):
    ref = db.reference("doctors")
    new_doctor_ref = ref.push()
    doctor_data = {
        "name": name,
        "specialization": specialization,
        "phone": phone,
        "email": email,
        "address": address,
        "experience": experience,
        "department": department,
        "availability": availability
    }
    new_doctor_ref.set(doctor_data)
    status_label.config(text="Doctor's details saved!", fg="green")
    clear_entries()
    get_firebase_data()

def submit_data():
    name = name_entry.get()
    specialization = specialization_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get()
    experience = experience_entry.get()
    department = department_entry.get()
    availability = availability_entry.get()

    if all([name, specialization, phone, email, address, experience, department, availability]):
        save_data(name, specialization, phone, email, address, experience, department, availability)
    else:
        status_label.config(text="Please fill all the details", fg="red")

def clear_entries():
    global selected_doctor_key
    selected_doctor_key = None
    for entry in entries:
        entry.delete(0, tk.END)
    status_label.config(text="")

def load_data():
    global key_map
    key_map = {}  # Mapping TreeView item ID to Firebase key
    for item in tree.get_children():
        tree.delete(item)

    ref = db.reference("doctors")
    doctors = ref.get()
    if doctors:
        for key, doctor in doctors.items():
            item_id = tree.insert("", "end", values=(
                doctor.get("name", ""),
                doctor.get("specialization", ""),
                doctor.get("phone", ""),
                doctor.get("email", ""),
                doctor.get("address", ""),
                doctor.get("experience", ""),
                doctor.get("department", ""),
                doctor.get("availability", "")
            ))
            key_map[item_id] = key

def on_tree_select(event):
    global selected_doctor_key
    selected_item = tree.focus()
    if not selected_item:
        return
    values = tree.item(selected_item, 'values')
    selected_doctor_key = key_map.get(selected_item)

    for entry, value in zip(entries, values):
        entry.delete(0, tk.END)
        entry.insert(0, value)

def update_doctor():
    global selected_doctor_key
    if not selected_doctor_key:
        status_label.config(text="Select a doctor to update.", fg="red")
        return

    updated_data = {
        "name": name_entry.get(),
        "specialization": specialization_entry.get(),
        "phone": phone_entry.get(),
        "email": email_entry.get(),
        "address": address_entry.get(),
        "experience": experience_entry.get(),
        "department": department_entry.get(),
        "availability": availability_entry.get()
    }

    if all(updated_data.values()):
        db.reference(f"doctors/{selected_doctor_key}").update(updated_data)
        status_label.config(text="Doctor's details updated!", fg="green")
        clear_entries()
        get_firebase_data()
    else:
        status_label.config(text="Please fill all the details.", fg="red")

def delete_doctor():
    global selected_doctor_key
    if not selected_doctor_key:
        status_label.config(text="Select a doctor to delete.", fg="red")
        return

    db.reference(f"doctors/{selected_doctor_key}").delete()
    status_label.config(text="Doctor deleted!", fg="green")
    clear_entries()
    get_firebase_data()

def go_back():
    root.destroy()
    subprocess.run(["python", "home.py"])

# Create main window
root = tk.Tk()
root.geometry('1440x750+50+50')
root.title('Hospital Management System')
root.configure(bg='#f0f0f0')

# Title Bar
title_bar = tk.Frame(root, bg='#2c3e50', relief='raised', bd=0, height=50)
title_bar.pack(fill=tk.X)
title_font = tkfont.Font(family="Helvetica", size=26, weight="bold")
tk.Label(title_bar, text="Doctor Management", font=title_font, bg='#2c3e50', fg="white").pack(pady=5)

# Back Button
back_btn = tk.Button(root, text="Back", command=go_back, font=("Helvetica", 14, "bold"), bg='#d9534f', fg='white',
                     activebackground='#c9302c', relief=tk.FLAT, padx=15, pady=5)
back_btn.pack(pady=10, padx=10, anchor="nw")

# Main Frame
main_frame = tk.Frame(root, bg='#f0f0f0')
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Form Section
form_frame = tk.Frame(main_frame, bg='#f0f0f0', padx=20, pady=20)
form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=10)

# Table Section
table_frame = tk.Frame(main_frame, bg='#f0f0f0', padx=20, pady=20)
table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=10)

labels = ["Doctor's Name", "Specialization", "Phone", "Email", "Address", "Years of Experience", "Department", "Availability"]
entries = []

for i, label_text in enumerate(labels):
    tk.Label(form_frame, text=label_text, font=("Helvetica", 14), bg='#f0f0f0', anchor="w").grid(
        row=i, column=0, padx=10, pady=10, sticky="w")
    entry = tk.Entry(form_frame, font=("Helvetica", 14), width=40)
    entry.grid(row=i, column=1, padx=10, pady=10, sticky="w")
    entries.append(entry)

(name_entry, specialization_entry, phone_entry, email_entry, address_entry,
 experience_entry, department_entry, availability_entry) = entries

# Submit / Update / Delete Buttons
btn_frame = tk.Frame(form_frame, bg='#f0f0f0')
btn_frame.grid(row=len(labels), column=0, columnspan=2, pady=20)

submit_btn = tk.Button(btn_frame, text="Submit", command=submit_data, bg='#2c3e50', fg='white', font=("Helvetica", 14),
                       padx=15, pady=10)
submit_btn.grid(row=0, column=0, padx=5)

update_btn = tk.Button(btn_frame, text="Update", command=update_doctor, bg='#0275d8', fg='white', font=("Helvetica", 14),
                       padx=15, pady=10)
update_btn.grid(row=0, column=1, padx=5)

delete_btn = tk.Button(btn_frame, text="Delete", command=delete_doctor, bg='#d9534f', fg='white', font=("Helvetica", 14),
                       padx=15, pady=10)
delete_btn.grid(row=0, column=2, padx=5)

# Status Label
status_label = tk.Label(form_frame, text="", font=("Helvetica", 14), bg='#f0f0f0')
status_label.grid(row=len(labels)+1, column=0, columnspan=2)

# TreeView Table
columns = ("Name", "Specialization", "Phone", "Email", "Address", "Experience", "Department", "Availability")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=150)

scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
scroll_y.pack(side=tk.RIGHT, fill="y")
tree.configure(yscrollcommand=scroll_y.set)
tree.pack(fill=tk.BOTH, expand=True)

# Bind selection event
tree.bind("<<TreeviewSelect>>", on_tree_select)

# Load Firebase data
get_firebase_data()

root.mainloop()
