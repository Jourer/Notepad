import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext, filedialog
import tkinter.font
import os

root = tk.Tk()


text_font = tkinter.font.Font(family="Arial", size=10, weight="normal")
root.option_add("*Font", text_font)

root.title("Notepad V0.2")
root.geometry("350x50")
root.configure(bg="darkgrey")


try:
    icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
    root.iconbitmap(icon_path)
except Exception as e:
    print(f"Icon load failed: {e}")

frm = ttk.Frame(root, padding=10)
frm.grid()

current_filename = None  

def close_app():
    if messagebox.askokcancel("Notepad V0.2: Quit", "Do you want to quit?"):
        root.destroy()

def save_file(text_widget):
    global current_filename
    content = text_widget.get("1.0", tk.END).strip()
    if not content:
        messagebox.showwarning("Save File: Warning", "No content to save!")
        return
    
    if not current_filename:
        messagebox.showerror("Save File: error", "Filename not set.")
        return

    
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    file_path = filedialog.asksaveasfilename(
        initialdir=desktop_path,
        initialfile=f"{current_filename}.txt",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    
    if not file_path:  
        return

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        messagebox.showinfo("Save File: Output", f"File saved successfully to:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Save File: Error", f"Failed to save file:\n{e}")

def open_notepad():
    root.geometry("740x600")
    root.title(f"Notepad V0.2 - {current_filename}.txt*")
    
    notepad_frame = ttk.Frame(root, padding=10)
    notepad_frame.grid()

    text_widget = scrolledtext.ScrolledText(notepad_frame, wrap=tk.WORD, width=100, height=30)
    text_widget.grid(column=0, row=0, columnspan=2)

     
    save_btn = tk.Button(
        notepad_frame,
        text="Save File",
        font=("Helvetica", 10, "italic"),
        bg="white",
        fg="black",
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
        font=("Helvetica", 10, "italic"),
        bg="white",
        fg="black",
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
    if messagebox.askyesno("Notepad V0.2: Confirmation", "Do you want to proceed?"):
        filename = simpledialog.askstring("Notepad V0.2: File Name", "Enter the file name (without extension):")
        if filename:
            current_filename = filename.strip()
            open_notepad()
        else:
            messagebox.showwarning("Notepad V0.2: File Name", "No file name provided!")
    else:
        messagebox.showinfo("Notepad V0.2: Output", "Returning to the main menu.")

# GUI setup
ttk.Label(frm, text="Notepad V0.2").grid(column=0, row=0)

# Start button
start_btn = tk.Button(
    frm,
    text="New Text File",
    font=("Helvetica", 10, "italic"),
    bg="white",
    fg="black",
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
    text="Exit Notepad",
    font=("Helvetica", 10, "italic"),
    bg="white",
    fg="black",
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
