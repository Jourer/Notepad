import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


class TagManager:
    """Manage tags/labels for notes"""
    
    def __init__(self, tags_file=None):
        self.tags_file = tags_file or os.path.join(
            os.path.dirname(__file__), "note_tags.json"
        )
        self.tags_data = self._load_tags()
    
    def _load_tags(self):
        """Load tags from JSON file"""
        if os.path.exists(self.tags_file):
            try:
                with open(self.tags_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading tags: {e}")
                return {}
        return {}
    
    def _save_tags(self):
        """Save tags to JSON file"""
        try:
            with open(self.tags_file, 'w', encoding='utf-8') as f:
                json.dump(self.tags_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving tags: {e}")
    
    def add_tag(self, filename, tag):
        """Add a tag to a file"""
        tag = tag.strip().lower()
        if not tag:
            return False
        
        if filename not in self.tags_data:
            self.tags_data[filename] = []
        
        if tag not in self.tags_data[filename]:
            self.tags_data[filename].append(tag)
            self._save_tags()
            return True
        return False
    
    def remove_tag(self, filename, tag):
        """Remove a tag from a file"""
        tag = tag.strip().lower()
        if filename in self.tags_data and tag in self.tags_data[filename]:
            self.tags_data[filename].remove(tag)
            if not self.tags_data[filename]:
                del self.tags_data[filename]
            self._save_tags()
            return True
        return False
    
    def get_tags(self, filename):
        """Get all tags for a file"""
        return self.tags_data.get(filename, [])
    
    def get_all_tags(self):
        """Get all unique tags across all files"""
        all_tags = set()
        for tags in self.tags_data.values():
            all_tags.update(tags)
        return sorted(list(all_tags))
    
    def get_files_by_tag(self, tag):
        """Get all files with a specific tag"""
        tag = tag.strip().lower()
        files = []
        for filename, tags in self.tags_data.items():
            if tag in tags:
                files.append(filename)
        return files
    
    def remove_file(self, filename):
        """Remove all tags for a file (e.g., when file is deleted)"""
        if filename in self.tags_data:
            del self.tags_data[filename]
            self._save_tags()
            return True
        return False


class TagWidget:
    """Widget for displaying and managing tags in the notepad"""
    
    def __init__(self, parent, filename, tag_manager):
        self.parent = parent
        self.filename = filename
        self.tag_manager = tag_manager
        self.tag_buttons = []
        
        # Create frame for tags
        self.frame = tk.Frame(parent, bg="#f0f0f0", pady=5)
        
        # Label
        label = tk.Label(
            self.frame,
            text="Tags:",
            font=("Arial", 9, "bold"),
            bg="#f0f0f0",
            fg="#333"
        )
        label.pack(side="left", padx=5)
        
        # Tags container
        self.tags_container = tk.Frame(self.frame, bg="#f0f0f0")
        self.tags_container.pack(side="left", fill="x", expand=True)
        
        # Add tag button
        add_btn = tk.Button(
            self.frame,
            text="+ Add Tag",
            font=("Arial", 9),
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            cursor="hand2",
            relief="flat",
            padx=8,
            pady=2,
            command=self.add_tag_dialog
        )
        add_btn.pack(side="right", padx=5)
        
        # Browse tags button
        browse_btn = tk.Button(
            self.frame,
            text="📋 Browse",
            font=("Arial", 9),
            bg="#2196F3",
            fg="white",
            activebackground="#0b7dda",
            cursor="hand2",
            relief="flat",
            padx=8,
            pady=2,
            command=self.browse_tags
        )
        browse_btn.pack(side="right", padx=2)
        
        # Load and display tags
        self.refresh_tags()
    
    def refresh_tags(self):
        """Refresh the display of tags"""
        # Clear existing tag buttons
        for widget in self.tags_container.winfo_children():
            widget.destroy()
        self.tag_buttons.clear()
        
        # Get tags for current file
        tags = self.tag_manager.get_tags(self.filename)
        
        if not tags:
            no_tags_label = tk.Label(
                self.tags_container,
                text="No tags yet",
                font=("Arial", 9, "italic"),
                fg="#999",
                bg="#f0f0f0"
            )
            no_tags_label.pack(side="left", padx=5)
        else:
            for tag in tags:
                self._create_tag_button(tag)
    
    def _create_tag_button(self, tag):
        """Create a tag button with remove option"""
        tag_frame = tk.Frame(self.tags_container, bg="#e3f2fd", relief="raised", bd=1)
        tag_frame.pack(side="left", padx=2, pady=2)
        
        # Tag label
        tag_label = tk.Label(
            tag_frame,
            text=f"#{tag}",
            font=("Arial", 9),
            bg="#e3f2fd",
            fg="#1976D2",
            padx=5,
            pady=2
        )
        tag_label.pack(side="left")
        
        # Remove button
        remove_btn = tk.Label(
            tag_frame,
            text="✕",
            font=("Arial", 8, "bold"),
            bg="#e3f2fd",
            fg="#d32f2f",
            cursor="hand2",
            padx=3
        )
        remove_btn.pack(side="left")
        remove_btn.bind("<Button-1>", lambda e, t=tag: self.remove_tag(t))
        
        # Hover effects
        for widget in [tag_label, remove_btn]:
            widget.bind("<Enter>", lambda e, f=tag_frame: f.configure(bg="#bbdefb"))
            widget.bind("<Leave>", lambda e, f=tag_frame: f.configure(bg="#e3f2fd"))
        
        self.tag_buttons.append(tag_frame)
    
    def add_tag_dialog(self):
        """Show dialog to add a new tag"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add Tag")
        dialog.geometry("300x120")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Center the dialog
        dialog.transient(self.parent)
        
        # Input frame
        input_frame = tk.Frame(dialog, padx=20, pady=20)
        input_frame.pack(fill="both", expand=True)
        
        label = tk.Label(input_frame, text="Enter tag name:", font=("Arial", 10))
        label.pack(anchor="w")
        
        entry = tk.Entry(input_frame, font=("Arial", 11), width=25)
        entry.pack(pady=5, fill="x")
        entry.focus()
        
        # Suggestion label
        suggestion = tk.Label(
            input_frame,
            text="Tip: Use short, descriptive tags (e.g., work, ideas, todo)",
            font=("Arial", 8),
            fg="#666"
        )
        suggestion.pack(anchor="w")
        
        def add_tag():
            tag = entry.get().strip()
            if tag:
                if self.tag_manager.add_tag(self.filename, tag):
                    self.refresh_tags()
                    dialog.destroy()
                else:
                    messagebox.showinfo("Info", f"Tag '{tag}' already exists for this note.")
            else:
                messagebox.showwarning("Warning", "Please enter a tag name.")
        
        # Buttons
        btn_frame = tk.Frame(input_frame)
        btn_frame.pack(pady=10, fill="x")
        
        add_btn = tk.Button(
            btn_frame,
            text="Add",
            command=add_tag,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 9),
            cursor="hand2",
            padx=15
        )
        add_btn.pack(side="left", padx=5)
        
        cancel_btn = tk.Button(
            btn_frame,
            text="Cancel",
            command=dialog.destroy,
            bg="#f44336",
            fg="white",
            font=("Arial", 9),
            cursor="hand2",
            padx=15
        )
        cancel_btn.pack(side="left")
        
        # Bind Enter key
        entry.bind("<Return>", lambda e: add_tag())
    
    def remove_tag(self, tag):
        """Remove a tag from the current file"""
        if messagebox.askyesno("Remove Tag", f"Remove tag '#{tag}'?"):
            if self.tag_manager.remove_tag(self.filename, tag):
                self.refresh_tags()
    
    def browse_tags(self):
        """Show tag browser window"""
        TagBrowserWindow(self.parent, self.tag_manager)
    
    def get_frame(self):
        """Get the tag widget frame"""
        return self.frame


class TagBrowserWindow:
    """Window for browsing all tags and files"""
    
    def __init__(self, parent, tag_manager):
        self.parent = parent
        self.tag_manager = tag_manager
        
        self.window = tk.Toplevel(parent)
        self.window.title("Tag Browser")
        self.window.geometry("600x400")
        
        # Title
        title_frame = tk.Frame(self.window, bg="#2196F3", pady=10)
        title_frame.pack(fill="x")
        
        title_label = tk.Label(
            title_frame,
            text="📋 Browse Tags",
            font=("Arial", 14, "bold"),
            bg="#2196F3",
            fg="white"
        )
        title_label.pack()
        
        # Content frame with two columns
        content = tk.Frame(self.window, padx=10, pady=10)
        content.pack(fill="both", expand=True)
        
        # Left: Tags list
        left_frame = tk.Frame(content)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        tk.Label(
            left_frame,
            text="All Tags:",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=5)
        
        # Scrollable tags list
        tags_scroll = tk.Scrollbar(left_frame)
        tags_scroll.pack(side="right", fill="y")
        
        self.tags_listbox = tk.Listbox(
            left_frame,
            font=("Arial", 10),
            yscrollcommand=tags_scroll.set,
            selectmode="single",
            bg="#f5f5f5"
        )
        self.tags_listbox.pack(side="left", fill="both", expand=True)
        tags_scroll.config(command=self.tags_listbox.yview)
        
        # Right: Files with selected tag
        right_frame = tk.Frame(content)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        self.files_label = tk.Label(
            right_frame,
            text="Select a tag to see files",
            font=("Arial", 11, "bold")
        )
        self.files_label.pack(anchor="w", pady=5)
        
        files_scroll = tk.Scrollbar(right_frame)
        files_scroll.pack(side="right", fill="y")
        
        self.files_listbox = tk.Listbox(
            right_frame,
            font=("Arial", 10),
            yscrollcommand=files_scroll.set,
            bg="#f5f5f5"
        )
        self.files_listbox.pack(side="left", fill="both", expand=True)
        files_scroll.config(command=self.files_listbox.yview)
        
        # Populate tags
        self._populate_tags()
        
        # Bind selection
        self.tags_listbox.bind("<<ListboxSelect>>", self._on_tag_select)
    
    def _populate_tags(self):
        """Populate the tags listbox"""
        all_tags = self.tag_manager.get_all_tags()
        
        if not all_tags:
            self.tags_listbox.insert(tk.END, "No tags yet")
        else:
            for tag in all_tags:
                # Count files with this tag
                count = len(self.tag_manager.get_files_by_tag(tag))
                self.tags_listbox.insert(tk.END, f"#{tag} ({count})")
    
    def _on_tag_select(self, event):
        """Handle tag selection"""
        selection = self.tags_listbox.curselection()
        if not selection:
            return
        
        # Get selected tag
        selected_text = self.tags_listbox.get(selection[0])
        if selected_text == "No tags yet":
            return
        
        # Extract tag name (remove # and count)
        tag = selected_text.split(" (")[0][1:]  # Remove # prefix
        
        # Update label
        self.files_label.config(text=f"Files tagged with #{tag}:")
        
        # Clear and populate files list
        self.files_listbox.delete(0, tk.END)
        files = self.tag_manager.get_files_by_tag(tag)
        
        if not files:
            self.files_listbox.insert(tk.END, "No files found")
        else:
            for filename in files:
                self.files_listbox.insert(tk.END, filename)
