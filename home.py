"""install the library for firebase pillow, openpyxl, threading
pip install firebase_admin
pip install pillow
pip install openpyxl
pip install threading
"""
import sys
import tkinter as tk

from tkinter import font as tkfont
from PIL import Image, ImageTk
import os
import subprocess
def open_doctor_attendance():
    root.destroy()
    os.system("python doctor_attendance.py")
def open_doctor_section():
    root.destroy()
    os.system("python doctor_management.py")

def open_patient_section():
    root.destroy()
    os.system("python patient_records.py")

def open_staff_section():
    root.destroy()
    os.system("python bed_management.py")

def open_storage_section():
    root.destroy()
    os.system("python Storage_management.py")
def go_back():
    root.destroy()
    subprocess.run(["python", "login.py"])  # Change to previous page file

# Create the main window
root = tk.Tk()
root.geometry('1440x750+50+50')
root.title('Hospital Management System')
root.configure(bg='#f0f0f0')

# Load the background image
def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

image_path = resource_path("hospital building.jpg")
background_image = Image.open(image_path)
background_image = background_image.resize((1440, 750), Image.Resampling.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

# Create a canvas to place the background image
canvas = tk.Canvas(root, width=1440, height=750)
canvas.place(x=0, y=0)  # Changed from pack to place
canvas.create_image(0, 0, image=background_photo, anchor="nw")
PRIMARY_COLOR = "#2c3e50"
TEXT_COLOR = "#ffffff"
FONT_FAMILY = "Helvetica"
BUTTON_FONT_SIZE = 14
# Custom title bar
title_bar = tk.Frame(root, bg='#2c3e50', relief='raised', bd=0, height=50)
title_bar.place(x=0, y=0, width=1440, height=50)  # Changed from pack to place
back_btn = tk.Button(
    title_bar, text="Back", font=(FONT_FAMILY, BUTTON_FONT_SIZE, "bold"), width=10,
    bg=PRIMARY_COLOR, fg=TEXT_COLOR, activebackground=PRIMARY_COLOR, relief=tk.FLAT, command=go_back
)
back_btn.pack(side="left",pady=10)


# Main content frame (for buttons)
content_frame = tk.Frame(root, bg='#f0f0f0')
content_frame.place(x=450, y=100, width=600, height=550)  # Changed from pack to place

# Buttons for different sections
btn_font = ("Helvetica", 16)
button_width = 20
button_height = 2

buttons = [
    ("Doctor Management", open_doctor_section),
    ("Doctor Attendance", open_doctor_attendance),
    ("Patient Records", open_patient_section),
    ("Bed Management", open_staff_section),
    ("Storage Management", open_storage_section)
]

y_offset = 50
for text, command in buttons:
    btn = tk.Button(content_frame, text=text, font=btn_font, width=button_width, height=button_height, bg='#2c3e50', fg='white', command=command)
    btn.place(x=150, y=y_offset)  # Changed from pack to place
    y_offset += 100

root.mainloop()
