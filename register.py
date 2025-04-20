import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
import firebase_admin
from firebase_admin import credentials, db
import os
import sys
import subprocess

# Initialize Firebase
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

# Constants for UI
BG_COLOR = "#f0f0f0"
PRIMARY_COLOR = "#2c3e50"
SECONDARY_COLOR = "#3498db"
BUTTON_COLOR = "#2980b9"
TEXT_COLOR = "#ffffff"
FONT_FAMILY = "Helvetica"
TITLE_FONT_SIZE = 26
BUTTON_FONT_SIZE = 14

# Save data to Firebase
def save_data():
    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    password = password_entry.get()

    if name and email and phone and password:
        ref = db.reference("patients")
        new_patient_ref = ref.push()
        new_patient_ref.set({
            "name": name,
            "email": email,
            "phone": phone,
            "password": password  # In a real-world app, store a hashed password
        })
        status_label.config(text="Registration Successful!", fg="green")
        clear_entries()
    else:
        status_label.config(text="All fields are required!", fg="red")

# Clear input fields
def clear_entries():
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

# Back button function
def go_back():
    root.destroy()
    subprocess.run(["python", "login.py"])  # Open login.py when back is clicked

# Create main window
root = tk.Tk()
root.geometry('1440x750+50+50')
root.title('Hospital Management System - Registration')

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

image_path = resource_path("patient.jpg")
background_image = Image.open(image_path)

background_image = background_image.resize((720, 750), Image.Resampling.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

canvas = tk.Canvas(root, width=720, height=750)
canvas.place(x=0, y=0)
canvas.create_image(0, 0, image=background_photo, anchor="nw")

# Title Bar
title_bar = tk.Frame(root, bg=PRIMARY_COLOR, relief='raised', bd=0, height=50)
title_bar.place(x=720, y=0, width=720, height=50)

title_font = tkfont.Font(family=FONT_FAMILY, size=TITLE_FONT_SIZE, weight="bold")
tk.Label(title_bar, text="Patient Registration", font=title_font, bg=PRIMARY_COLOR, fg=TEXT_COLOR).place(x=200, y=5)

# Registration Frame
register_frame = tk.Frame(root, bg="#e6f3ff")
register_frame.place(x=720, y=50, width=720, height=700)

# Labels and Entry Fields
fields = [("Full Name", ""), ("Email", ""), ("Phone", ""), ("Password", "*")]
y_offset = 100
entries = {}

for field, show in fields:
    tk.Label(register_frame, text=field, font=(FONT_FAMILY, 14), bg=BG_COLOR).place(x=50, y=y_offset)
    entry = tk.Entry(register_frame, font=(FONT_FAMILY, 14), width=30, show=show)
    entry.place(x=200, y=y_offset)
    entries[field] = entry
    y_offset += 50

name_entry = entries["Full Name"]
email_entry = entries["Email"]
phone_entry = entries["Phone"]
password_entry = entries["Password"]

# Register Button
register_btn = tk.Button(
    register_frame, text="Register", font=(FONT_FAMILY, 14, "bold"), width=15, height=2,
    bg=BUTTON_COLOR, fg=TEXT_COLOR, activebackground=SECONDARY_COLOR, relief=tk.FLAT, command=save_data
)
register_btn.place(x=250, y=y_offset + 20)

# Back Button
back_btn = tk.Button(
    register_frame, text="Back", font=(FONT_FAMILY, 12, "bold"), width=10, height=2,
    bg=PRIMARY_COLOR, fg=TEXT_COLOR, activebackground=SECONDARY_COLOR, relief=tk.FLAT, command=go_back
)
back_btn.place(x=50, y=y_offset + 20)

# Status Label
status_label = tk.Label(register_frame, text="", font=(FONT_FAMILY, 14), bg=BG_COLOR)
status_label.place(x=200, y=y_offset + 70)

# Run application
root.mainloop()
