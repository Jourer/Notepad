import tkinter as tk
from tkinter import ttk
import os


class EmojiPicker:
    """Emoji picker window with categorized emoji selection"""
    
    EMOJI_COLLECTION = {
        "Smileys": [
            "😀", "😃", "😄", "😁", "😆", "😅", "🤣", "😂",
            "🙂", "🙃", "😉", "😊", "😇", "🥰", "😍", "🤩",
            "😘", "😗", "😚", "😙", "😋", "😛", "😜", "🤪",
            "😝", "🤑", "🤗", "🤭", "🤫", "🤔", "🤐", "🤨"
        ],
        "Emotions": [
            "😐", "😑", "😶", "😏", "😒", "🙄", "😬", "🤥",
            "😌", "😔", "😪", "🤤", "😴", "😷", "🤒", "🤕",
            "🤢", "🤮", "🤧", "🥵", "🥶", "😵", "🤯", "🤠",
            "🥳", "😎", "🤓", "🧐", "😕", "😟", "🙁", "☹️"
        ],
        "Hearts": [
            "❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍",
            "🤎", "💔", "❣️", "💕", "💞", "💓", "💗", "💖",
            "💘", "💝", "💟", "♥️", "💌", "💋", "💏", "💑"
        ],
        "Hands": [
            "👍", "👎", "👊", "✊", "🤛", "🤜", "🤞", "✌️",
            "🤟", "🤘", "👌", "🤏", "👈", "👉", "👆", "👇",
            "☝️", "✋", "🤚", "🖐️", "🖖", "👋", "🤙", "💪",
            "🙏", "✍️", "👏", "🙌", "👐", "🤲", "🤝", "🙏"
        ],
        "Animals": [
            "🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼",
            "🐨", "🐯", "🦁", "🐮", "🐷", "🐸", "🐵", "🐔",
            "🐧", "🐦", "🐤", "🦆", "🦅", "🦉", "🦇", "🐺",
            "🐗", "🐴", "🦄", "🐝", "🐛", "🦋", "🐌", "🐞"
        ],
        "Food": [
            "🍎", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🍈",
            "🍒", "🍑", "🥭", "🍍", "🥥", "🥝", "🍅", "🍆",
            "🥑", "🥦", "🥬", "🌶️", "🌽", "🥕", "🥒", "🥔",
            "🍞", "🥐", "🥖", "🥨", "🧀", "🥚", "🍳", "🥓"
        ],
        "Symbols": [
            "❤️", "💔", "💯", "✨", "⭐", "🌟", "💫", "🔥",
            "💧", "💦", "⚡", "☀️", "🌙", "⛅", "🌈", "☁️",
            "✅", "❌", "⭕", "🔴", "🟠", "🟡", "🟢", "🔵",
            "🟣", "⚫", "⚪", "🟤", "♻️", "⚠️", "☢️", "☣️"
        ],
        "Objects": [
            "💻", "⌨️", "🖱️", "🖨️", "💾", "💿", "📱", "☎️",
            "📞", "📟", "📠", "📺", "📻", "🎙️", "🎚️", "🎛️",
            "⏰", "⏱️", "⏲️", "⌚", "📡", "🔋", "🔌", "💡",
            "🔦", "🕯️", "🗑️", "🛒", "💰", "💵", "💴", "💶"
        ],
        "Decor": [
            "🎀", "🎁", "🎈", "🎉", "🎊", "🎋", "🎍", "🎎",
            "🎏", "🎐", "🎑", "🧧", "🎗️", "🎟️", "🎫", "🏮",
            "🌸", "🌺", "🌻", "🌷", "🌹", "🥀", "💐", "🏵️",
            "🌼", "🪴", "🎨", "🖼️", "✨", "💫", "⭐", "🌟"
        ]
    }
    
    def __init__(self, parent, text_widget):
        self.parent = parent
        self.text_widget = text_widget
        self.window = None
        
    def show(self):
        """Display the emoji picker window"""
        if self.window and self.window.winfo_exists():
            self.window.focus()
            return
            
        self.window = tk.Toplevel(self.parent)
        self.window.title("Emoji Picker")
        self.window.geometry("500x450")
        self.window.resizable(False, False)
        
        
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        
        for category, emojis in self.EMOJI_COLLECTION.items():
            frame = tk.Frame(notebook, bg="white")
            notebook.add(frame, text=category)
            
            
            canvas = tk.Canvas(frame, bg="white", highlightthickness=0)
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="white")
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e, c=canvas: c.configure(scrollregion=c.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            row, col = 0, 0
            for emoji in emojis:
                btn = tk.Button(
                    scrollable_frame,
                    text=emoji,
                    font=("Segoe UI Emoji", 20),
                    width=2,
                    height=1,
                    relief="flat",
                    bg="white",
                    activebackground="#e6f2ff",
                    cursor="hand2",
                    command=lambda e=emoji: self.insert_emoji(e)
                )
                btn.grid(row=row, column=col, padx=2, pady=2)
                
                
                btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#f0f8ff"))
                btn.bind("<Leave>", lambda e, b=btn: b.configure(bg="white"))
                
                col += 1
                if col >= 8:  
                    col = 0
                    row += 1
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
        
        
        info_frame = tk.Frame(self.window, bg="#f0f0f0", padx=10, pady=5)
        info_frame.pack(fill="x", side="bottom")
        
        info_label = tk.Label(
            info_frame,
            text="💡 Tip: Add custom emoji images to the 'resources' folder!",
            bg="#f0f0f0",
            font=("Arial", 9),
            fg="#666"
        )
        info_label.pack()
        
    def insert_emoji(self, emoji):
        """Insert selected emoji at cursor position"""
        try:
            cursor_pos = self.text_widget.index(tk.INSERT)
            self.text_widget.insert(cursor_pos, emoji)
            self.text_widget.focus()
        except:
            self.text_widget.insert(tk.END, emoji)
            self.text_widget.focus()


class CustomImageEmojiPicker(EmojiPicker):
    """Extended emoji picker that loads custom images from resources folder"""
    
    def __init__(self, parent, text_widget, resources_path=None):
        super().__init__(parent, text_widget)
        self.resources_path = resources_path or os.path.join(
            os.path.dirname(__file__), "resources"
        )
        self.custom_emojis = self._load_custom_emojis()
    
    def _load_custom_emojis(self):
        """Load custom emoji images from resources folder"""
        custom = {}
        if not os.path.exists(self.resources_path):
            return custom
        
        try:
            # Look for image files
            for filename in os.listdir(self.resources_path):
                if filename.lower().endswith(('.png', '.gif', '.ico')):
                    filepath = os.path.join(self.resources_path, filename)
                    emoji_name = os.path.splitext(filename)[0]
                    custom[emoji_name] = filepath
        except Exception as e:
            print(f"Error loading custom emojis: {e}")
        
        return custom
    
    def show(self):
        """Display emoji picker with custom images tab if available"""
        super().show()
        
        # Add custom emojis tab if any exist
        if self.custom_emojis:
            # Find the notebook widget
            for child in self.window.winfo_children():
                if isinstance(child, ttk.Notebook):
                    self._add_custom_tab(child)
                    break
    
    def _add_custom_tab(self, notebook):
        """Add a tab for custom emoji images"""
        frame = tk.Frame(notebook, bg="white")
        notebook.add(frame, text="Custom")
        
        canvas = tk.Canvas(frame, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add custom emoji buttons
        row, col = 0, 0
        for name, filepath in self.custom_emojis.items():
            try:
                # Try to load the image
                img = tk.PhotoImage(file=filepath)
                # Store reference to prevent garbage collection
                if not hasattr(self, '_images'):
                    self._images = []
                self._images.append(img)
                
                btn = tk.Button(
                    scrollable_frame,
                    image=img,
                    relief="flat",
                    bg="white",
                    activebackground="#e6f2ff",
                    cursor="hand2",
                    command=lambda n=name: self.insert_custom_emoji(n)
                )
                btn.image = img  # Keep a reference
                btn.grid(row=row, column=col, padx=2, pady=2)
                
                # Add tooltip
                self._create_tooltip(btn, name)
                
                # Hover effects
                btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#f0f8ff"))
                btn.bind("<Leave>", lambda e, b=btn: b.configure(bg="white"))
                
                col += 1
                if col >= 8:
                    col = 0
                    row += 1
            except Exception as e:
                print(f"Error loading emoji {name}: {e}")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_tooltip(self, widget, text):
        """Create a simple tooltip for emoji name"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = tk.Label(tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1)
            label.pack()
            widget._tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, '_tooltip'):
                widget._tooltip.destroy()
                del widget._tooltip
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def insert_custom_emoji(self, name):
        """Insert custom emoji image into the text widget"""
        if name not in self.custom_emojis:
            return
        
        filepath = self.custom_emojis[name]
        
        try:
            # Load the image
            original_img = tk.PhotoImage(file=filepath)
            
            # Resize image to match emoji size (approximately 16-20 pixels)
            # Get original dimensions
            width = original_img.width()
            height = original_img.height()
            
            # Calculate subsample factor to get ~18px size
            target_size = 18
            subsample_factor = max(width, height) // target_size
            if subsample_factor < 1:
                subsample_factor = 1
            
            # Create resized image
            img = original_img.subsample(subsample_factor, subsample_factor)
            
            # Store reference to prevent garbage collection
            if not hasattr(self.text_widget, '_emoji_images'):
                self.text_widget._emoji_images = []
            self.text_widget._emoji_images.append(img)
            
            # Get cursor position
            try:
                cursor_pos = self.text_widget.index(tk.INSERT)
            except:
                cursor_pos = tk.END
            
            # Insert the image at cursor position
            self.text_widget.image_create(cursor_pos, image=img)
            
            # Add a space after the emoji for better formatting
            self.text_widget.insert(cursor_pos + "+1c", " ")
            
            # Focus back to text widget
            self.text_widget.focus()
            
        except Exception as e:
            print(f"Error inserting custom emoji {name}: {e}")
            # Fallback to text representation if image fails
            self.insert_emoji(f"[{name}]")


def open_emoji_picker(parent, text_widget, use_custom=True):
    """Open emoji picker window"""
    if use_custom:
        picker = CustomImageEmojiPicker(parent, text_widget)
    else:
        picker = EmojiPicker(parent, text_widget)
    picker.show()
