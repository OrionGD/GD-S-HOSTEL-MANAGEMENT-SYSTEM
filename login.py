#login.py
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from hosteller_dashboard import open_hosteller_dashboard
from warden_dashboard import open_warden_dashboard
from register import open_extended_registration

# --- Database Connection ---
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gd_hms"
    )
    cursor = db.cursor()
    print("Database connection successful.")
except mysql.connector.Error as err:
    print(f"Database connection failed: {err}")
    exit()

# --- Theme Colors ---
theme_colors = {
    "light": {"bg": "#eafaf1", "fg": "#2c3e50"},
    "dark": {"bg": "#0f2027", "fg": "#7fffd4"}
}
current_theme = "light"

# --- Toggle Theme ---
def toggle_theme(root):
    global current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    root.configure(bg=theme_colors[current_theme]["bg"])
    for widget in root.winfo_children():
        try:
            widget.configure(bg=theme_colors[current_theme]["bg"])
            if "fg" in widget.configure():
                widget.configure(fg=theme_colors[current_theme]["fg"])
        except tk.TclError:
            pass

# --- Register User ---
def register_user(username, password):
    if not username or not password:
        messagebox.showwarning("⚠️ Incomplete", "Please fill out both fields.")
        return
    try:
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, 'hosteller')",
            (username, password)
        )
        db.commit()
        messagebox.showinfo("🎉 Success", "User registered successfully!")
    except mysql.connector.IntegrityError:
        messagebox.showerror("❌ Error", "Username already exists.")

# --- Login User ---
def login_user(username, password, win):

    cursor.execute("SELECT user_id, role FROM users WHERE username=%s AND password=%s", (username, password))
    result = cursor.fetchone()
    if result:
        user_id, role = result
        print(f"User logged in: {username} | Role: {role}")
        win.destroy()
        if role == "warden":
            open_warden_dashboard(username)
        elif role == "hosteller":
            open_hosteller_dashboard(username)
        else:
            messagebox.showerror("Login Error", f"Unknown role: {role}")
    else:
        messagebox.showerror("❌ Login Failed", "Invalid credentials.")

# --- Login Window ---
def main_login():
    login_win = tk.Tk()
    login_win.title("🔐 Secure Login")
    login_win.geometry("400x370")
    login_win.configure(bg=theme_colors[current_theme]["bg"])

    tk.Label(login_win, text="👤 User Access", font=("Helvetica", 18, "bold"),
             bg=theme_colors[current_theme]["bg"], fg=theme_colors[current_theme]["fg"]).pack(pady=20)

    tk.Label(login_win, text="🧑‍💻 Username:", bg=theme_colors[current_theme]["bg"],
             fg=theme_colors[current_theme]["fg"]).pack(pady=5)
    username_entry = tk.Entry(login_win, width=30)
    username_entry.pack(pady=5)

    tk.Label(login_win, text="🔑 Password:", bg=theme_colors[current_theme]["bg"],
             fg=theme_colors[current_theme]["fg"]).pack(pady=5)
    password_entry = tk.Entry(login_win, show="*", width=30)
    password_entry.pack(pady=5)

    button_frame = tk.Frame(login_win, bg=theme_colors[current_theme]["bg"])
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="✅ Login", width=14, font=("Helvetica", 12, "bold"),
              bg="#66bb6a", fg="white",
              command=lambda: login_user(username_entry.get(), password_entry.get(), login_win)).grid(row=0, column=0, padx=10)

    tk.Button(button_frame, text="📝 Register", width=14, font=("Helvetica", 12, "bold"),
              bg="#42a5f5", fg="white",
              command=open_extended_registration).grid(row=0, column=1, padx=10)

    tk.Button(login_win, text="🎨 Switch Theme", font=("Helvetica", 12), relief="flat",
              bg=theme_colors[current_theme]["bg"], fg=theme_colors[current_theme]["fg"],
              command=lambda: toggle_theme(login_win)).pack(pady=10)

    login_win.mainloop()

# --- Launch Login ---
main_login()
