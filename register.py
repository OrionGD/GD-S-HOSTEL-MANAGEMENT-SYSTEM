import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import mysql.connector

# --- Database Connection ---
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gd_hms"
    )
    cursor = db.cursor()
except mysql.connector.Error as err:
    print(f"Database connection failed: {err}")
    exit()

# --- Register Hosteller ---
def register_hosteller(data):
    try:
        query = """
        INSERT INTO users (
            username, password, role, first_name, last_name, email, phone_number,
            year_of_study, department, hostel_name, room_number, DOB
        )
        VALUES (%s, %s, 'hosteller', %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, data)
        db.commit()
        messagebox.showinfo("Success", "Hosteller registered successfully!")
    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "Username or Email already exists.")
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# --- Registration Form GUI ---
def open_extended_registration():
    reg_win = tk.Tk()
    reg_win.title("Extended Hosteller Registration")
    reg_win.geometry("400x650")
    reg_win.config(bg="white")

    fields = {}

    def add_field(label, show=None):
        tk.Label(reg_win, text=label, bg="white").pack(pady=2)
        entry = tk.Entry(reg_win, show=show) if not label.startswith("DOB") else DateEntry(reg_win, date_pattern='yyyy-mm-dd')
        entry.pack(pady=2)
        fields[label] = entry

    labels = [
        "Username", "Password", "First Name", "Last Name", "Email",
        "Phone Number", "Year of Study", "Department", "Hostel Name",
        "Room Number", "DOB"
    ]

    for lbl in labels:
        add_field(lbl, show="*" if lbl == "Password" else None)

    def on_submit():
        values = [fields[label].get() for label in labels]
        if all(values):
            register_hosteller(tuple(values))
        else:
            messagebox.showwarning("Missing Fields", "Please fill in all fields.")

    tk.Button(reg_win, text="Register", bg="skyblue", command=on_submit).pack(pady=20)
    reg_win.mainloop()

# Run
if __name__ == "__main__":
    open_extended_registration()
