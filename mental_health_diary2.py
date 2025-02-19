import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import datetime

# Initialize database
conn = sqlite3.connect("diary.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        mood TEXT,
        content TEXT
    )
""")
conn.commit()
conn.close()

# Function to save diary entry
def save_entry():
    mood = mood_var.get()
    content = entry_text.get("1.0", tk.END).strip()

    if not content:
        messagebox.showwarning("Empty Entry", "Please write something before saving!")
        return

    date = str(datetime.date.today())

    conn = sqlite3.connect("diary.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO entries (date, mood, content) VALUES (?, ?, ?)", (date, mood, content))
    conn.commit()
    conn.close()

    suggestion_label.config(text=f"💡 Suggestion: {suggestions.get(mood, 'Take care!')}")
    entry_text.delete("1.0", tk.END)
    messagebox.showinfo("Saved", "Your diary entry has been saved!")

# Function to view past entries
def view_entries():
    conn = sqlite3.connect("diary.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM entries ORDER BY id DESC")
    records = cursor.fetchall()
    conn.close()

    if not records:
        messagebox.showinfo("No Entries", "No past entries found.")
        return

    entries_window = tk.Toplevel(root)
    entries_window.title("Past Entries")
    entries_window.geometry("450x400")
    entries_window.configure(bg="#F5F5F5")  # macOS-like light gray

    text_area = tk.Text(entries_window, wrap=tk.WORD, font=("SF Pro Text", 12))
    text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    for record in records:
        text_area.insert(tk.END, f"📅 {record[1]} | Mood: {record[2]}\n{record[3]}\n{'-'*40}\n")

    text_area.config(state=tk.DISABLED)

# Mood suggestions
suggestions = {
    "Happy": "Keep spreading positivity! Maybe journal about what made you happy.",
    "Sad": "Try listening to music, talking to a friend, or taking a walk.",
    "Anxious": "Breathe deeply, meditate, or write about your feelings.",
    "Stressed": "Take a break, go for a walk, or do something creative."
}

# macOS GUI Setup
root = tk.Tk()
root.title("Mental Health Diary 📝")
root.geometry("500x550")
root.configure(bg="#ECECEC")  # macOS-like background

# Use native macOS theme
style = ttk.Style()
style.theme_use("aqua")  # macOS default theme

# Title Label
ttk.Label(root, text="Mental Health Diary", font=("SF Pro Display", 18, "bold"), background="#ECECEC").pack(pady=10)

# Mood Selection
ttk.Label(root, text="How are you feeling today?", font=("SF Pro Text", 12), background="#ECECEC").pack()
mood_var = tk.StringVar(value="Happy")
mood_menu = ttk.Combobox(root, textvariable=mood_var, values=list(suggestions.keys()), state="readonly", font=("SF Pro Text", 12))
mood_menu.pack(pady=5)

# Text Entry Box
entry_text = tk.Text(root, height=8, width=50, font=("SF Pro Text", 12), relief="flat", wrap=tk.WORD, padx=10, pady=10)
entry_text.pack(pady=10)

# Buttons with macOS Styling
button_frame = tk.Frame(root, bg="#ECECEC")
button_frame.pack()

save_button = ttk.Button(button_frame, text="💾 Save Entry", command=save_entry)
save_button.grid(row=0, column=0, padx=5, pady=5)

view_button = ttk.Button(button_frame, text="📖 View Past Entries", command=view_entries)
view_button.grid(row=0, column=1, padx=5, pady=5)

# Suggestion Label
suggestion_label = ttk.Label(root, text="💡 Suggestions will appear here", font=("SF Pro Text", 11, "italic"), foreground="gray", background="#ECECEC")
suggestion_label.pack(pady=10)

root.mainloop()
