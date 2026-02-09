import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext, filedialog
import tkinter.font
import os
try:
    from markdown_preview import open_markdown_preview
except ImportError:
    open_markdown_preview = None

try:
    from emoji_picker import open_emoji_picker
except ImportError:
    open_emoji_picker = None

try:
    from tag_manager import TagManager, TagWidget
except ImportError:
    TagManager = None
    TagWidget = None

root = tk.Tk()


text_font = tkinter.font.Font(family="Arial", size=10, weight="normal")
root.option_add("*Font", text_font)

root.title("Notepad V0.21")
root.geometry("415x50")
root.configure(bg="darkgrey")


try:
    icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
    root.iconbitmap(icon_path)
except Exception as e:
    print(f"Icon load failed: {e}")

frm = ttk.Frame(root, padding=10)
frm.grid()

current_filename = None
tag_manager = TagManager() if TagManager else None  

def close_app():
    if messagebox.askokcancel("Notepad V0.211: Quit", "Do you want to quit?"):
        root.destroy()

def delete_current_file():
    """Delete the current file and remove its tags"""
    global current_filename
    
    if not current_filename:
        messagebox.showerror("Delete File: Error", "No file is currently open.")
        return
    
    # Confirm deletion
    if not messagebox.askyesno(
        "Delete File: Confirmation",
        f"Are you sure you want to delete '{current_filename}'?\n\nThis will also remove all associated tags.\n\nThis action cannot be undone!"
    ):
        return
    
    # Try to find and delete the file
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    possible_paths = [
        os.path.join(desktop_path, f"{current_filename}.txt"),
        os.path.join(desktop_path, f"{current_filename}.md"),
        os.path.join(desktop_path, current_filename)
    ]
    
    file_deleted = False
    for file_path in possible_paths:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                file_deleted = True
                break
            except Exception as e:
                messagebox.showerror("Delete File: Error", f"Failed to delete file:\n{e}")
                return
    
    # Remove tags for this file
    if tag_manager:
        tag_manager.remove_file(current_filename)
    
    if file_deleted:
        messagebox.showinfo("Delete File: Success", f"File '{current_filename}' and its tags have been deleted.")
    else:
        # Even if file wasn't found, still remove tags
        messagebox.showinfo("Delete Tags: Success", f"Tags removed for '{current_filename}'.\n\nNote: File was not found on Desktop.")
    
    # Close the editor
    close_app()

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

def open_notepad(initial_content=""):
    root.geometry("950x750")
    root.title(f"Notepad V0.211 - {current_filename}.txt*")
    
    notepad_frame = ttk.Frame(root, padding=10)
    notepad_frame.grid()
    
    # Add tag widget if available
    if TagWidget and tag_manager and current_filename:
        tag_widget = TagWidget(notepad_frame, current_filename, tag_manager)
        tag_widget.get_frame().grid(column=0, row=0, columnspan=4, sticky="ew", pady=(0, 5))

    text_widget = scrolledtext.ScrolledText(notepad_frame, wrap=tk.WORD, width=110, height=32)
    text_widget.grid(column=0, row=1, columnspan=5)
    
    if initial_content:
        text_widget.insert("1.0", initial_content)

     
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
    save_btn.grid(column=0, row=2, sticky="w", padx=5, pady=5)
    
    
    if open_markdown_preview:
        preview_btn = tk.Button(
            notepad_frame,
            text="Preview Markdown",
            font=("Helvetica", 10, "italic"),
            bg="white",
            fg="black",
            activebackground="darkgrey",
            activeforeground="black",
            bd=3,
            relief="sunken",
            padx=6,
            pady=4,
            command=lambda: open_markdown_preview(root, text_widget.get("1.0", tk.END))
        )
        preview_btn.grid(column=1, row=2, padx=5, pady=5)
    
    # Emoji Picker button
    if open_emoji_picker:
        emoji_btn = tk.Button(
            notepad_frame,
            text="😀 Emojis",
            font=("Helvetica", 10, "italic"),
            bg="white",
            fg="black",
            activebackground="darkgrey",
            activeforeground="black",
            bd=3,
            relief="sunken",
            padx=6,
            pady=4,
            command=lambda: open_emoji_picker(root, text_widget)
        )
        emoji_btn.grid(column=2, row=2, padx=5, pady=5)
    
    # Delete File button
    delete_btn = tk.Button(
        notepad_frame,
        text="🗑️ Delete File",
        font=("Helvetica", 10, "italic"),
        bg="#f44336",
        fg="white",
        activebackground="#d32f2f",
        activeforeground="white",
        bd=3,
        relief="sunken",
        padx=6,
        pady=4,
        command=lambda: delete_current_file()
    )
    delete_btn.grid(column=3, row=2, padx=5, pady=5)

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
    close_btn.grid(column=4, row=2, sticky="e", padx=5, pady=5)

def load_file():
    global current_filename

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    file_path = filedialog.askopenfilename(
        initialdir=desktop_path,
        title="Select a file to open",
        filetypes=[("Text Files", "*.txt"), ("Markdown Files", "*.md"), ("Python Files", "*.py"), ("All Files", "*.*")]
    )
    
    if not file_path:
        return
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        
        current_filename = os.path.splitext(os.path.basename(file_path))[0]
        open_notepad(initial_content=content)
        messagebox.showinfo("Load File: Success", f"File loaded successfully:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Load File: Error", f"Failed to load file:\n{e}")

def start():
    global current_filename
    if messagebox.askyesno("Notepad V0.21: Confirmation", "Do you want to proceed?"):
        filename = simpledialog.askstring("Notepad V0.21: File Name", "Enter the file name (without extension):")
        if filename:
            current_filename = filename.strip()
            open_notepad()
        else:
            messagebox.showwarning("Notepad V0.21: File Name", "No file name provided!")
    else:
        messagebox.showinfo("Notepad V0.21: Output", "Returning to the main menu.")

# GUI setup
ttk.Label(frm, text="Notepad V0.21").grid(column=0, row=0)

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

# Open File button
open_btn = tk.Button(
    frm,
    text="Open File",
    font=("Helvetica", 10, "italic"),
    bg="white",
    fg="black",
    activebackground="darkgrey",
    activeforeground="black",
    bd=3,
    relief="sunken",
    padx=6,
    pady=4,
    command=load_file
)
open_btn.grid(column=2, row=0, padx=5)

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
stop_btn.grid(column=3, row=0, padx=5)

root.mainloop()
