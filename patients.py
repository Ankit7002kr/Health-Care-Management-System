import tkinter as tk
from tkinter import ttk, font as tkfont
import firebase_admin
from firebase_admin import credentials, db
import os
import sys
import subprocess
import threading
from openpyxl import Workbook
from tkinter import filedialog
import os
def export_to_excel():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")],
        title="Save Patient Records As"
    )

    if not file_path:
        return  # User canceled save dialog

    try:
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Patient Records"

        # Write headers
        headers = [tree.heading(col)["text"] for col in tree["columns"]]
        sheet.append(headers)

        # Write data rows
        for row_id in tree.get_children():
            row = tree.item(row_id)['values']
            sheet.append(row)

        workbook.save(file_path)
        tk.messagebox.showinfo("Success", f"Data exported to:\n{file_path}")
    except Exception as e:
        tk.messagebox.showerror("Error", f"Failed to export data:\n{e}")


def search_patient(name_query):
    ref = db.reference("appointments")
    records = ref.get()

    for item in tree.get_children():
        tree.delete(item)

    if records:
        for key, data in records.items():
            name = data.get("patient_name", "")
            if name_query.lower() in name.lower():
                tree.insert("", "end", values=(
                    data.get("patient_name", ""),
                    data.get("patient_email", ""),
                    data.get("patient_age", ""),
                    data.get("doctor_comment", ""),
                    data.get("status", ""),
                    data.get("issue", "")
                ))


def get_firebase_data():
    threading.Thread(target=fetch_records, daemon=True).start()
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

# Fetch patient records from Firebase
def fetch_records():
    ref = db.reference("appointments")
    records = ref.get()
    if records:
        for item in tree.get_children():
            tree.delete(item)
        for key, data in records.items():
            tree.insert("", "end", values=(
                data.get("patient_name", ""),
                data.get("patient_email", ""),
                data.get("patient_age", ""),
                data.get("doctor_comment", ""),
                data.get("status", ""),
                data.get("issue", "")
            ))

# Go back function
def go_back():
    root.destroy()
    subprocess.run(["python", "doctor_home.py"])  # Change to previous page file

# UI Constants
BG_COLOR = "#f0f0f0"
PRIMARY_COLOR = "#2c3e50"
TEXT_COLOR = "#ffffff"
FONT_FAMILY = "Helvetica"
TITLE_FONT_SIZE = 24
BUTTON_FONT_SIZE = 14

# Create main window
root = tk.Tk()
root.geometry('1440x750+50+50')
root.title('Patient Records')

# Title Label
title_font = tkfont.Font(family=FONT_FAMILY, size=TITLE_FONT_SIZE, weight="bold")
title_label = tk.Label(root, text="Patient Records", font=title_font, bg=PRIMARY_COLOR, fg=TEXT_COLOR, pady=10)
title_label.pack(fill="x")

# Search Frame
search_frame = tk.Frame(root, bg=BG_COLOR)
search_frame.pack(pady=10)

search_label = tk.Label(search_frame, text="Search Name:", font=(FONT_FAMILY, 12), bg=BG_COLOR)
search_label.pack(side="left", padx=(0, 10))

search_entry = tk.Entry(search_frame, font=(FONT_FAMILY, 12), width=30)
search_entry.pack(side="left", padx=(0, 10))

search_btn = tk.Button(search_frame, text="Search", font=(FONT_FAMILY, 12), bg=PRIMARY_COLOR, fg=TEXT_COLOR,
                       activebackground=PRIMARY_COLOR, relief=tk.FLAT, command=lambda: search_patient(search_entry.get()))
search_btn.pack(side="left",padx=(0, 10))
export_data = tk.Button(search_frame, text="Export", font=(FONT_FAMILY, 12), bg=PRIMARY_COLOR, fg=TEXT_COLOR,
                       activebackground=PRIMARY_COLOR, relief=tk.FLAT, command=export_to_excel)
export_data.pack(side="left",padx=(0, 30))



# Treeview Frame
tree_frame = tk.Frame(root, bg=BG_COLOR)
tree_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Create Treeview
columns = ("Full Name", "Email", "Age", "Doctor's Comment", "Status", "Issue")

tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

# Define column headings
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=200, anchor="center")

tree.pack(fill="both", expand=True)

# Fetch data on startup
get_firebase_data()

# Back Button
back_btn = tk.Button(
    root, text="Back", font=(FONT_FAMILY, BUTTON_FONT_SIZE, "bold"), width=10,
    bg=PRIMARY_COLOR, fg=TEXT_COLOR, activebackground=PRIMARY_COLOR, relief=tk.FLAT, command=go_back
)
back_btn.pack(pady=10)

# Run application
root.mainloop()
