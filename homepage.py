#HOMEPAGE.PY
import tkinter as tk
from tkinter import messagebox

def open_login():
    import login  # Ensure login.py contains open_login_window()
    login.open_login_window()

def show_homepage():
    root = tk.Tk()
    root.title("🏠 Hostel Management System")
    root.geometry("800x600")
    root.config(bg="#e6f2ff")

    # --- Navbar ---
    navbar = tk.Frame(root, bg="#ccddff", pady=10)
    navbar.pack(fill='x')

    tk.Label(navbar, text="🏠 Hostel Management System", font=("Arial", 16, "bold"), bg="#ccddff").pack(side="left", padx=20)

    nav_buttons = [
        ("Home", lambda: messagebox.showinfo("Home", "You are on the Home page.")),
        ("Features", lambda: messagebox.showinfo("Features", "See the features below.")),
        ("Copy Right", lambda: messagebox.showinfo("Copy Right", "GD 2025."))
    ]

    for text, cmd in nav_buttons:
        tk.Button(navbar, text=text, command=cmd, bg="white", font=("Arial", 12)).pack(side="right", padx=10)

    # --- Hero Section ---
    tk.Label(root, text="Welcome to Hostel Management System", font=("Arial", 20, "bold"), bg="#e6f2ff").pack(pady=30)
    tk.Label(root, text="Efficiently manage hostelers, attendance, and more.", font=("Arial", 14), bg="#e6f2ff").pack(pady=10)
    tk.Button(root, text="Get Started", command=open_login, font=("Arial", 12), bg="#3399ff", fg="white", padx=20, pady=5).pack(pady=10)

    # --- Features Section ---
    tk.Label(root, text="Our Features", font=("Arial", 16, "bold"), bg="#e6f2ff").pack(pady=20)

    features = ["Attendance Tracking", "Out Pass Management", "Warden Notifications", "Birthday Alerts"]
    for feat in features:
        tk.Label(root, text=feat, font=("Arial", 12), bg="#f0f8ff", width=40, relief="groove", pady=5).pack(pady=5)

    # --- Footer ---
    tk.Label(root, text="© 2025 | GD | Hostel Management System | All Rights Reserved", bg="#ccddff", font=("Arial", 10)).pack(side="bottom", fill="x", pady=10)

    root.mainloop()

# Only run if this is the main file
if __name__ == "__main__":
    show_homepage()
