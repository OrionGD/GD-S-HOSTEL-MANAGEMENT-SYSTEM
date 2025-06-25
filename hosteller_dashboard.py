# hosteller_dashboard.py
import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import calendar
from tkcalendar import DateEntry


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gd_hms"
    )


# --- Hosteller Functions ---
def view_hosteller_info(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT first_name, last_name, email, phone_number, year_of_study, department, hostel_name, room_number 
        FROM users WHERE username = %s AND role = 'hosteller'
    """, (username,))
    result = cursor.fetchone()

    if not result:
        messagebox.showerror("Error", "Hosteller data not found.")
        return

    info_win = tk.Toplevel()
    info_win.title("Your Information")
    info_win.geometry("400x400")
    info_win.config(bg="#E0FFF0")

    labels = [
        "First Name", "Last Name", "Email", "Phone Number",
        "Year of Study", "Department", "Hostel Name", "Room Number"
    ]

    for label, value in zip(labels, result):
        tk.Label(info_win, text=f"{label}:", font=("Arial", 10, "bold"), bg="#E0FFF0").pack(pady=2, anchor="w", padx=20)
        tk.Label(info_win, text=value, font=("Arial", 10), bg="#E0FFF0").pack(pady=1, anchor="w", padx=40)

    tk.Button(info_win, text="Close", command=info_win.destroy).pack(pady=20)

def manage_attendance(username):
    from tkcalendar import Calendar
    import tkinter as tk
    from tkinter import ttk

    def mark_attendance(status):
        selected_date = cal.get_date()
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO attendance (username, date, status)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE status = VALUES(status)
            """, (username, selected_date, status))
            conn.commit()
            messagebox.showinfo("Success", f"Marked {status} for {selected_date}")
            load_attendance()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def load_attendance():
        for item in tree.get_children():
            tree.delete(item)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT date, status FROM attendance
            WHERE username = %s ORDER BY date DESC
        """, (username,))
        for date, status in cursor.fetchall():
            tree.insert('', 'end', values=(date, status))
        conn.close()

    att_win = tk.Toplevel()
    att_win.title("Manage Attendance")
    att_win.geometry("500x500")
    att_win.config(bg="#F0FFF0")

    tk.Label(att_win, text="Select a date and mark your attendance:", font=("Arial", 12, "bold"), bg="#F0FFF0").pack(pady=10)
    
    cal = Calendar(att_win, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.pack(pady=10)

    btn_frame = tk.Frame(att_win, bg="#F0FFF0")
    btn_frame.pack(pady=10)
    for label, status in [("Present", "P"), ("Absent", "A"), ("Leave", "L")]:
        tk.Button(btn_frame, text=label, width=10, command=lambda s=status: mark_attendance(s)).pack(side="left", padx=5)

    tree = ttk.Treeview(att_win, columns=("Date", "Status"), show="headings")
    tree.heading("Date", text="Date")
    tree.heading("Status", text="Status")
    tree.pack(pady=20, fill="both", expand=True)

    load_attendance()

    tk.Button(att_win, text="Close", command=att_win.destroy).pack(pady=10)

def request_outpass(username):
    def submit_request():
        start_date = start_cal.get_date()
        end_date = end_cal.get_date()
        reason = reason_text.get("1.0", tk.END).strip()

        if start_date > end_date:
            messagebox.showerror("Invalid Dates", "Start date cannot be after end date.")
            return
        if not reason:
            messagebox.showwarning("Missing Reason", "Please enter a reason for your outpass request.")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
        # Get user_id from username
            cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("User Error", "User not found in the database.")
                return

            user_id = result[0]

        # Insert into outpass_requests with user_id and request_date as NOW()
            cursor.execute("""
                INSERT INTO outpass_requests (user_id, start_date, end_date, reason, status, request_date)
                VALUES (%s, %s, %s, %s, %s, NOW())
            """, (user_id, start_date, end_date, reason, 'Pending'))
    
            conn.commit()
            messagebox.showinfo("Request Submitted", "Your outpass request has been submitted.")
            outpass_win.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()



    # Create popup window
    outpass_win = tk.Toplevel()
    outpass_win.title("Request Outpass")
    outpass_win.geometry("450x400")
    outpass_win.config(bg="#F5F5DC")

    # Start Date (Dropdown calendar)
    tk.Label(outpass_win, text="Select Start Date:", bg="#F5F5DC", font=("Arial", 12)).pack(pady=5)
    start_cal = DateEntry(outpass_win, date_pattern='yyyy-mm-dd', width=15)
    start_cal.pack(pady=5)

    # End Date (Dropdown calendar)
    tk.Label(outpass_win, text="Select End Date:", bg="#F5F5DC", font=("Arial", 12)).pack(pady=5)
    end_cal = DateEntry(outpass_win, date_pattern='yyyy-mm-dd', width=15)
    end_cal.pack(pady=5)

    # Reason Text Field
    tk.Label(outpass_win, text="Reason for Outpass:", bg="#F5F5DC", font=("Arial", 12)).pack(pady=10)
    reason_text = tk.Text(outpass_win, height=5, width=45, wrap="word", font=("Arial", 10))
    reason_text.pack(pady=5)

    # Buttons
    tk.Button(outpass_win, text="Submit Request", command=submit_request, bg="#4CAF50", fg="white", width=20).pack(pady=15)
    tk.Button(outpass_win, text="Cancel", command=outpass_win.destroy, width=20).pack()


def view_outpass_history(username):
    import tkinter as tk
    from tkinter import ttk, messagebox

    def load_outpass_history():
        for item in tree.get_children():
            tree.delete(item)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Step 1: Get user_id from username
            cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()

            if not result:
                messagebox.showerror("Error", "User not found in the database.")
                return

            user_id = result[0]

            # Step 2: Fetch outpass history using user_id
            cursor.execute("""
                SELECT start_date, end_date, reason, status 
                FROM outpass_requests
                WHERE user_id = %s
                ORDER BY request_date DESC
            """, (user_id,))
            rows = cursor.fetchall()

            if not rows:
                messagebox.showinfo("No History", "No outpass requests found.")
                return

            for row in rows:
                tree.insert('', 'end', values=row)

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    # Create a new window for outpass history
    history_win = tk.Toplevel()
    history_win.title("Outpass History")
    history_win.geometry("600x400")
    history_win.config(bg="#FFF8DC")

    # Heading
    tk.Label(history_win, text="Your Outpass Request History", font=("Arial", 14, "bold"), bg="#FFF8DC").pack(pady=10)

    # Treeview to display the outpass history
    tree = ttk.Treeview(history_win, columns=("Start Date", "End Date", "Reason", "Status"), show="headings")
    tree.heading("Start Date", text="Start Date")
    tree.heading("End Date", text="End Date")
    tree.heading("Reason", text="Reason")
    tree.heading("Status", text="Status")
    tree.pack(pady=10, fill="both", expand=True)

    # Load data
    load_outpass_history()

    # Close button
    tk.Button(history_win, text="Close", command=history_win.destroy).pack(pady=10)

# --- Hosteller Dashboard ---
def open_hosteller_dashboard(hosteller_username):
    win = tk.Tk()
    win.title("Hosteller Dashboard")
    win.geometry("600x500")
    win.config(bg="#98FB98")

    # Use the passed username instead of 'hosteller_name'
    greeting = f"Welcome, {hosteller_username}!" if hosteller_username else "Welcome, Hosteller!"
    tk.Label(win, text=greeting, font=("Arial", 16, "bold"), bg="#98FB98").pack(pady=20)
    tk.Label(win, text=calendar.month_name[datetime.now().month], font=("Arial", 14), bg="#98FB98").pack()

    btns = [
        ("📋 View Personal Info", lambda: view_hosteller_info(hosteller_username)),
        ("📅 Manage Attendance", lambda: manage_attendance(hosteller_username)),
        ("📤 Request Out Pass", lambda: request_outpass(hosteller_username)),
        ("🔍 View Out Pass History", lambda: view_outpass_history(hosteller_username)),
        ("🚪 Logout", win.destroy)
    ]
    for text, cmd in btns:
        tk.Button(win, text=text, font=("Arial", 12), bg="lightgreen", width=30, command=cmd).pack(pady=8)

    win.mainloop()
# --- Only run if executed directly ---
if __name__ == "__main__":
    open_hosteller_dashboard()
