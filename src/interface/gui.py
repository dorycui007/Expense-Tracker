import tkinter as tk
from tkinter import messagebox
from src.storage.database import add_expense_db

def create_gui():
    """
    Creates a Tkinter GUI for entering expense data with a styled design.

    Displays input fields for date, amount, category, description, and payment method,
    with a light purple background, white rounded container, and a centered dark purple submit button with black text.

    Returns:
        None
    """
    window = tk.Tk()
    window.title("Expense Tracker")
    window.geometry("400x500")
    window.configure(bg="#E6E6FA")  # Light purple background

    # Main frame with white background and rounded corners
    frame = tk.Frame(window, bg="white", bd=0)
    frame.place(relx=0.5, rely=0.5, anchor="center", width=300, height=400)
    # Simulate rounded corners with a canvas
    canvas = tk.Canvas(frame, bg="white", bd=0, highlightthickness=0, width=300, height=400)
    canvas.pack()
    canvas.create_oval(0, 0, 40, 40, fill="white", outline="white")  # Top-left corner
    canvas.create_oval(260, 0, 300, 40, fill="white", outline="white")  # Top-right corner
    canvas.create_oval(0, 360, 40, 400, fill="white", outline="white")  # Bottom-left corner
    canvas.create_oval(260, 360, 300, 400, fill="white", outline="white")  # Bottom-right corner
    canvas.create_rectangle(20, 0, 280, 400, fill="white", outline="white")  # Middle fill
    canvas.create_rectangle(0, 20, 300, 380, fill="white", outline="white")  # Middle fill

    # Title
    tk.Label(frame, text="Expense Tracker", font=("Arial", 14, "bold"), bg="white").place(x=10, y=20)

    # Date field
    tk.Label(frame, text="Date (YYYY-MM-DD)", font=("Arial", 10), bg="white", fg="#555555").place(x=10, y=50)
    date_entry = tk.Entry(frame, width=30, bd=1, relief="solid", bg="#F5F5F5", fg="#999999")
    date_entry.place(x=10, y=70)

    # Amount field
    tk.Label(frame, text="Amount", font=("Arial", 10), bg="white", fg="#555555").place(x=10, y=100)
    amount_entry = tk.Entry(frame, width=30, bd=1, relief="solid", bg="#F5F5F5", fg="#999999")
    amount_entry.place(x=10, y=120)

    # Category field
    tk.Label(frame, text="Category", font=("Arial", 10), bg="white", fg="#555555").place(x=10, y=150)
    category_entry = tk.Entry(frame, width=30, bd=1, relief="solid", bg="#F5F5F5", fg="#999999")
    category_entry.place(x=10, y=170)

    # Description field
    tk.Label(frame, text="Description", font=("Arial", 10), bg="white", fg="#555555").place(x=10, y=200)
    desc_entry = tk.Entry(frame, width=30, bd=1, relief="solid", bg="#F5F5F5", fg="#999999")
    desc_entry.place(x=10, y=220)

    # Payment Method field
    tk.Label(frame, text="Payment Method", font=("Arial", 10), bg="white", fg="#555555").place(x=10, y=250)
    payment_entry = tk.Entry(frame, width=30, bd=1, relief="solid", bg="#F5F5F5", fg="#999999")
    payment_entry.place(x=10, y=270)

    # Submit button
    def submit():
        date = date_entry.get()
        amount = amount_entry.get()
        category = category_entry.get()
        desc = desc_entry.get()
        payment = payment_entry.get()

        if not date or not amount or not category or not desc or not payment:
            messagebox.showerror("Error", "Please fill in all fields.")
        else:
            try:
                add_expense_db(date, float(amount), category, desc, payment)
                messagebox.showinfo("Success", "Expense added successfully!")
                window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Amount must be a number.")

    tk.Button(frame, text="Submit", command=submit, font=("Arial", 10), bg="#3A0061", fg="black", width=20, height=1, bd=0).place(relx=0.5, rely=0.85, anchor="center")

    window.mainloop()

if __name__ == "__main__":
    create_gui()