import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
import tkinter.font
import os

root = tk.Tk()

# Set global font
text_font = tkinter.font.Font(family="Arial", size=12, weight="bold")
root.option_add("*Font", text_font)

root.title("Notepad V0.1")
root.geometry("300x200")
root.configure(bg="darkgrey")

# Use iconbitmap for .ico files
try:
    root.iconbitmap("icon.ico")
except Exception as e:
    print(f"Icon load failed: {e}")

frm = ttk.Frame(root, padding=10)
frm.grid()

current_filename = None  # Global file name

def close_app():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

def save_file(text_widget):
    global current_filename
    content = text_widget.get("1.0", tk.END).strip()
    if not content:
        messagebox.showwarning("Save File", "No content to save!")
        return
    
    if not current_filename:
        messagebox.showerror("Error", "Filename not set.")
        return

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    file_path = os.path.join(desktop_path, f"{current_filename}.txt")

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        messagebox.showinfo("Save File", f"File saved successfully to:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file:\n{e}")

def open_notepad():
    root.geometry("800x1000")
    root.title(f"Notepad V0.1 - {current_filename}.txt")
    
    notepad_frame = ttk.Frame(root, padding=10)
    notepad_frame.grid()

    text_widget = scrolledtext.ScrolledText(notepad_frame, wrap=tk.WORD, width=100, height=30)
    text_widget.grid(column=0, row=0, columnspan=2)

    # Create new button instances instead of reusing SpecButton
    save_btn = tk.Button(
        notepad_frame,
        text="Save",
        font=("Helvetica", 9, "bold"),
        bg="white",
        fg="darkgrey",
        activebackground="darkgrey",
        activeforeground="black",
        bd=3,
        relief="sunken",
        padx=6,
        pady=4,
        command=lambda: save_file(text_widget)
    )
    save_btn.grid(column=0, row=1, sticky="w", padx=5, pady=5)

    close_btn = tk.Button(
        notepad_frame,
        text="Close",
        font=("Helvetica", 9, "bold"),
        bg="white",
        fg="darkgrey",
        activebackground="darkgrey",
        activeforeground="black",
        bd=3,
        relief="sunken",
        padx=6,
        pady=4,
        command=close_app
    )
    close_btn.grid(column=1, row=1, sticky="e", padx=5, pady=5)

def start():
    global current_filename
    if messagebox.askyesno("Notepad V0.1 -- Confirmation", "Do you want to proceed?"):
        filename = simpledialog.askstring("File Name", "Enter the file name (without extension):")
        if filename:
            current_filename = filename.strip()
            open_notepad()
        else:
            messagebox.showwarning("File Name", "No file name provided!")
    else:
        messagebox.showinfo("Info", "Returning to the main menu.")

# GUI setup
ttk.Label(frm, text="Notepad V0.1").grid(column=0, row=0)

# Start button
start_btn = tk.Button(
    frm,
    text="Start",
    font=("Helvetica", 9, "bold"),
    bg="white",
    fg="darkgrey",
    activebackground="darkgrey",
    activeforeground="black",
    bd=3,
    relief="sunken",
    padx=6,
    pady=4,
    command=start
)
start_btn.grid(column=1, row=0, padx=5)

# Stop button
stop_btn = tk.Button(
    frm,
    text="Stop",
    font=("Helvetica", 9, "bold"),
    bg="white",
    fg="darkgrey",
    activebackground="darkgrey",
    activeforeground="black",
    bd=3,
    relief="sunken",
    padx=6,
    pady=4,
    command=root.destroy
)
stop_btn.grid(column=2, row=0, padx=5)

root.mainloop()
