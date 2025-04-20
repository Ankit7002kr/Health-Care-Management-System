import os,sys
import tkinter as tk
from tkinter import ttk, messagebox
import firebase_admin
from firebase_admin import credentials, db
from PIL import Image, ImageTk  # For background image
import threading
def go_back():
    root.destroy()
    os.system("python home.py")
def get_firebase_data():
    threading.Thread(target=load_medicines, daemon=True).start()
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

ref = db.reference("medicines")

# Initialize Tkinter
root = tk.Tk()
root.title("Storage Management - Medicines")
root.geometry('1440x750+50+50')

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

image_path = resource_path("medicine.jpg")
bg_image = Image.open(image_path)
 # Replace with your image path
bg_image = bg_image.resize((1440, 450), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a Canvas for Background
canvas = tk.Canvas(root, width=1440, height=750)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Title Label
title_label = tk.Label(root, text="Medicine Storage Management", font=("Helvetica", 18, "bold"), bg="white")
title_label.place(x=500, y=20)

# Frame for Input Fields
form_frame = tk.Frame(root, bg="white", bd=2, relief="groove")
form_frame.place(x=50, y=80, width=450, height=180)

# Labels & Entry Fields
tk.Label(form_frame, text="Medicine Name:", font=("Helvetica", 12), bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
medicine_name_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=25)
medicine_name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Quantity:", font=("Helvetica", 12), bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
quantity_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=25)
quantity_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Price:", font=("Helvetica", 12), bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
price_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=25)
price_entry.grid(row=2, column=1, padx=10, pady=5)

# Buttons Frame
button_frame = tk.Frame(root, bg="white")
button_frame.place(x=50, y=280)

# Buttons
tk.Button(button_frame, text="Add Medicine", font=("Helvetica", 12), bg="#2c3e50", fg="white", width=15, command=lambda: add_medicine()).grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Update Medicine", font=("Helvetica", 12), bg="#2980b9", fg="white", width=15, command=lambda: update_medicine()).grid(row=0, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Delete Medicine", font=("Helvetica", 12), bg="#c0392b", fg="white", width=15, command=lambda: delete_medicine()).grid(row=0, column=2, padx=5, pady=5)
tk.Button(button_frame, text="Back", font=("Helvetica", 12), bg="#e67e22", fg="white", width=15, command=go_back).grid(row=0, column=3, padx=5, pady=5)  # Back Button

# Treeview Frame
tree_frame = tk.Frame(root, bg="white", bd=2, relief="groove")
tree_frame.place(x=50, y=350, width=1340, height=350)

# Scrollbars
scroll_y = ttk.Scrollbar(tree_frame, orient="vertical")
scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal")

# Treeview to display medicines
columns = ("ID", "Name", "Quantity", "Price")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

# Configure scrollbars
scroll_y.config(command=tree.yview)
scroll_x.config(command=tree.xview)

scroll_y.pack(side="right", fill="y")
scroll_x.pack(side="bottom", fill="x")

# Define column headings
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=300)

tree.pack(fill="both", expand=True)

# Functions to interact with Firebase
def load_medicines():
    tree.delete(*tree.get_children())  # Clear existing data
    medicines = ref.get()
    if medicines:
        for key, data in medicines.items():
            tree.insert("", "end", values=(key, data["name"], data["quantity"], data["price"]))

def add_medicine():
    name = medicine_name_entry.get()
    quantity = quantity_entry.get()
    price = price_entry.get()
    if name and quantity and price:
        ref.push({"name": name, "quantity": quantity, "price": price})
        messagebox.showinfo("Success", "Medicine added successfully!")
        clear_entries()
        get_firebase_data()
    else:
        messagebox.showerror("Error", "Please fill all fields")

def update_medicine():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a medicine to update")
        return
    item = tree.item(selected_item)
    medicine_id = item["values"][0]
    new_data = {"name": medicine_name_entry.get(), "quantity": quantity_entry.get(), "price": price_entry.get()}
    ref.child(medicine_id).update(new_data)
    messagebox.showinfo("Success", "Medicine updated successfully!")
    clear_entries()
    get_firebase_data()

def delete_medicine():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a medicine to delete")
        return
    item = tree.item(selected_item)
    medicine_id = item["values"][0]
    ref.child(medicine_id).delete()
    messagebox.showinfo("Success", "Medicine deleted successfully!")
    clear_entries()
    get_firebase_data()

def clear_entries():
    medicine_name_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)


# Load initial data
get_firebase_data()

# Run Tkinter
root.mainloop()
