import tkinter as tk
import os
import firebase_admin
from firebase_admin import credentials, db
from tkinter import font as tkfont, messagebox
from PIL import Image, ImageTk
import sys
root = tk.Tk()
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

# Colors & Fonts
BG_COLOR = "#f0f0f0"
PRIMARY_COLOR = "#2c3e50"
SECONDARY_COLOR = "#3498db"
BUTTON_COLOR = "#2980b9"
TEXT_COLOR = "#ffffff"
FONT_FAMILY = "Helvetica"
TITLE_FONT_SIZE = 26
BUTTON_FONT_SIZE = 14

# Default Credentials for Admin & Doctor
CREDENTIALS = {
    "Admin": {"email": "admin", "password": "123"},
    "Doctor": {"email": "doctor", "password": "123"}
}

# Initialize Tkinter Window

root.geometry('1440x750+50+50')
root.title('Hospital Management System')

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

image_path = resource_path("hospital building.jpg")
background_image = Image.open(image_path)

background_image = background_image.resize((1440, 750), Image.Resampling.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

# Create a Canvas for Background
canvas = tk.Canvas(root, width=1440, height=750)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_photo, anchor="nw")

# Title Bar
title_bar = tk.Frame(root, bg=PRIMARY_COLOR, height=50)
title_bar.place(x=0, y=0, width=1440, height=50)

title_font = tkfont.Font(family=FONT_FAMILY, size=TITLE_FONT_SIZE, weight="bold")
tk.Label(title_bar, text="Welcome to Hospital Management System", font=title_font, bg=PRIMARY_COLOR,
         fg=TEXT_COLOR).place(x=350, y=5)


# Function to Show Welcome Page
def show_welcome():
    hide_frames()
    welcome_frame.place(x=400, y=150, width=690, height=350)


# Function to Show Login Page
def show_login(user_type):
    hide_frames()
    login_frame.place(x=450, y=200, width=550, height=300)

    # Update Login Title
    login_label.config(text=f"{user_type} Login")

    # Change Button Command
    login_btn.config(command=lambda: login_action(user_type))


# Function to Hide All Frames
def hide_frames():
    welcome_frame.place_forget()
    login_frame.place_forget()


# Function to Open Register Page
def open_register():
    root.destroy()
    os.system("python register.py")


# Function for Login Action
def login_action(user_type):
    email = email_entry.get().strip()
    password = password_entry.get().strip()

    # Admin & Doctor Login
    if user_type in CREDENTIALS:
        if email == CREDENTIALS[user_type]["email"] and password == CREDENTIALS[user_type]["password"]:
            messagebox.showinfo("Login Successful", f"Welcome, {user_type}!")
            root.destroy()  # Destroy the main window before opening a new one
            if user_type == "Admin":
                os.system("python home.py")
                root.destroy()

            else:

                os.system("python doctor_home.py")

            return
        else:
            messagebox.showerror("Login Failed", "Invalid Email or Password")
            return

    # Patient Login - Check Firebase
    ref = db.reference("patients")
    patients = ref.get()

    if patients:
        for key, patient in patients.items():
            if patient.get("email") == email and patient.get("password") == password:
                messagebox.showinfo("Login Successful", f"Welcome, {patient.get('name', 'Patient')}!")
                root.destroy()  # Destroy the main window before opening a new one
                os.system(f'python patient_home.py "{email}"')
                return

    messagebox.showerror("Login Failed", "Invalid Email or Password")


# Welcome Page
welcome_frame = tk.Frame(root, bg="#e6f3ff")
welcome_frame.place(x=400, y=150, width=690, height=350)

tk.Label(welcome_frame, text="Log in as", foreground="blue", font=(FONT_FAMILY, 18), bg=BG_COLOR).place(x=290, y=50)

btn_font = tkfont.Font(family=FONT_FAMILY, size=BUTTON_FONT_SIZE, weight="bold")

# Buttons for Login Types
login_buttons = [
    ("Admin", "Admin"),
    ("Doctor", "Doctor"),
    ("Patient", "Patient")
]

x_offset = 50
for text, user_type in login_buttons:
    tk.Button(
        welcome_frame,
        text=text,
        font=btn_font,
        width=15,
        height=2,
        bg=BUTTON_COLOR,
        fg=TEXT_COLOR,
        activebackground=SECONDARY_COLOR,
        activeforeground=TEXT_COLOR,
        relief=tk.FLAT,
        command=lambda u=user_type: show_login(u)
    ).place(x=x_offset, y=150)
    x_offset += 200

# "or" Label
tk.Label(welcome_frame, text="or", font=(FONT_FAMILY, 14), bg=BG_COLOR).place(x=290, y=250)

# "Register" Label (Clickable)
register_label = tk.Label(welcome_frame, text="Register", font=(FONT_FAMILY, 16, "underline"), fg="blue", bg=BG_COLOR,
                          cursor="hand2")
register_label.place(x=290, y=300)
register_label.bind("<Button-1>", lambda e: open_register())

# Login Page
login_frame = tk.Frame(root, bg="#e6f3ff")

# Login Title
login_label = tk.Label(login_frame, text="Login", font=(FONT_FAMILY, 20, "bold"), bg="#e6f3ff")
login_label.place(x=220, y=20)

# Email & Password Fields
tk.Label(login_frame, text="Email:", font=(FONT_FAMILY, 14), bg="#e6f3ff").place(x=100, y=80)
email_entry = tk.Entry(login_frame, font=(FONT_FAMILY, 14), width=30)
email_entry.place(x=200, y=80)

tk.Label(login_frame, text="Password:", font=(FONT_FAMILY, 14), bg="#e6f3ff").place(x=100, y=130)
password_entry = tk.Entry(login_frame, font=(FONT_FAMILY, 14), width=30, show="*")
password_entry.place(x=200, y=130)

# Login Button
login_btn = tk.Button(login_frame, text="Login", font=btn_font, width=12, height=1, bg=BUTTON_COLOR, fg=TEXT_COLOR,
                      relief=tk.FLAT)
login_btn.place(x=220, y=180)

# Back Button
tk.Button(login_frame, text="Back", font=btn_font, width=12, height=1, bg=SECONDARY_COLOR, fg=TEXT_COLOR,
          relief=tk.FLAT, command=show_welcome).place(x=220, y=230)

# Show Welcome Page Initially
show_welcome()

# Run the application
root.mainloop()
