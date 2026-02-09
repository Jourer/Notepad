import tkinter as tk
from tkinter import scrolledtext, messagebox
import re


class MarkdownPreview:
    """Markdown preview window with live rendering"""
    
    def __init__(self, parent, content=""):
        self.window = tk.Toplevel(parent)
        self.window.title("Markdown Preview")
        self.window.geometry("800x600")
        self.preview_widget = scrolledtext.ScrolledText(
            self.window, 
            wrap=tk.WORD, 
            width=100, 
            height=35,
            font=("Arial", 11),
            bg="white",
            padx=10,
            pady=10
        )
        self.preview_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self._configure_tags()
        if content:
            self.update_preview(content)
    
    def _configure_tags(self):
        """Configure text tags for markdown styling"""

        self.preview_widget.tag_config("h1", font=("Arial", 24, "bold"), spacing3=10)
        self.preview_widget.tag_config("h2", font=("Arial", 20, "bold"), spacing3=8)
        self.preview_widget.tag_config("h3", font=("Arial", 16, "bold"), spacing3=6)
        self.preview_widget.tag_config("h4", font=("Arial", 14, "bold"), spacing3=5)
        self.preview_widget.tag_config("h5", font=("Arial", 12, "bold"), spacing3=4)
        self.preview_widget.tag_config("h6", font=("Arial", 11, "bold"), spacing3=3)
        self.preview_widget.tag_config("bold", font=("Arial", 11, "bold"))
        self.preview_widget.tag_config("italic", font=("Arial", 11, "italic"))
        self.preview_widget.tag_config("code", font=("Courier New", 10), background="#f0f0f0")
        self.preview_widget.tag_config("code_block", font=("Courier New", 10), background="#f5f5f5", spacing1=5, spacing3=5)
        self.preview_widget.tag_config("link", foreground="blue", underline=True)
        self.preview_widget.tag_config("list", lmargin1=20, lmargin2=40)
        self.preview_widget.tag_config("quote", lmargin1=20, lmargin2=20, background="#f9f9f9", foreground="#666")
        self.preview_widget.tag_config("hr", foreground="#ccc")
    
    def update_preview(self, markdown_text):
        """Update the preview with new markdown content"""
        self.preview_widget.delete("1.0", tk.END)
        self._render_markdown(markdown_text)
    
    def _render_markdown(self, text):
        """Parse and render markdown text"""
        lines = text.split('\n')
        in_code_block = False
        code_block_content = []
        
        for line in lines:
            if line.strip().startswith('```'):
                if in_code_block:
                    self.preview_widget.insert(tk.END, '\n'.join(code_block_content) + '\n', "code_block")
                    code_block_content = []
                    in_code_block = False
                else:
                    in_code_block = True
                continue
            if in_code_block:
                code_block_content.append(line)
                continue

            if line.startswith('# '):
                self._insert_formatted_line(line[2:], "h1")
            elif line.startswith('## '):
                self._insert_formatted_line(line[3:], "h2")
            elif line.startswith('### '):
                self._insert_formatted_line(line[4:], "h3")
            elif line.startswith('#### '):
                self._insert_formatted_line(line[5:], "h4")
            elif line.startswith('##### '):
                self._insert_formatted_line(line[6:], "h5")
            elif line.startswith('###### '):
                self._insert_formatted_line(line[7:], "h6")
            
            elif line.strip() in ['---', '***', '___']:
                self.preview_widget.insert(tk.END, '—' * 50 + '\n', "hr")
            
            elif line.startswith('> '):
                self._insert_formatted_line(line[2:], "quote")
            
            elif line.strip().startswith('- ') or line.strip().startswith('* '):
                content = line.strip()[2:]
                self.preview_widget.insert(tk.END, '• ', "list")
                self._insert_formatted_line(content, "list", add_newline=True)
            
            elif re.match(r'^\d+\.\s', line.strip()):
                content = re.sub(r'^\d+\.\s', '', line.strip())
                num = re.match(r'^(\d+)\.', line.strip()).group(1)
                self.preview_widget.insert(tk.END, f'{num}. ', "list")
                self._insert_formatted_line(content, "list", add_newline=True)
            
            else:
                self._insert_formatted_line(line)
    
    def _insert_formatted_line(self, text, base_tag=None, add_newline=True):
        """Insert a line with inline formatting applied"""
        if not text.strip():
            self.preview_widget.insert(tk.END, '\n')
            return
        
        pos = 0

        pattern = r'(\*\*\*(.+?)\*\*\*|___(.+?)___|' \
                  r'\*\*(.+?)\*\*|__(.+?)__|' \
                  r'\*(.+?)\*|_(.+?)_|' \
                  r'`(.+?)`|' \
                  r'\[(.+?)\]\((.+?)\))'
        
        for match in re.finditer(pattern, text):
            if match.start() > pos:
                tags = (base_tag,) if base_tag else ()
                self.preview_widget.insert(tk.END, text[pos:match.start()], tags)
            
            if match.group(2) or match.group(3):  # ***text*** or ___text___
                content = match.group(2) or match.group(3)
                tags = ("bold_italic",) if not base_tag else (base_tag, "bold_italic")
                self.preview_widget.insert(tk.END, content, tags)
            elif match.group(4) or match.group(5):  # **text** or __text__
                content = match.group(4) or match.group(5)
                tags = ("bold",) if not base_tag else (base_tag, "bold")
                self.preview_widget.insert(tk.END, content, tags)
            elif match.group(6) or match.group(7):  # *text* or _text_
                content = match.group(6) or match.group(7)
                tags = ("italic",) if not base_tag else (base_tag, "italic")
                self.preview_widget.insert(tk.END, content, tags)
            elif match.group(8):  # `code`
                tags = ("code",) if not base_tag else (base_tag, "code")
                self.preview_widget.insert(tk.END, match.group(8), tags)
            elif match.group(9) and match.group(10):  # [text](url)
                tags = ("link",) if not base_tag else (base_tag, "link")
                self.preview_widget.insert(tk.END, match.group(9), tags)
            
            pos = match.end()
        if pos < len(text):
            tags = (base_tag,) if base_tag else ()
            self.preview_widget.insert(tk.END, text[pos:], tags)
        
        if add_newline:
            self.preview_widget.insert(tk.END, '\n')


def open_markdown_preview(parent, content):
    """Open a markdown preview window"""
    try:
        preview = MarkdownPreview(parent, content)
    except Exception as e:
        messagebox.showerror("Markdown Preview Error", f"Failed to open preview:\n{e}")


def render_markdown_to_html(markdown_text):
    """Convert markdown to basic HTML (for future HTML viewer integration)"""
    html = "<html><head><style>"
    html += "body { font-family: Arial, sans-serif; padding: 20px; }"
    html += "h1 { font-size: 24px; }"
    html += "h2 { font-size: 20px; }"
    html += "code { background: #f0f0f0; padding: 2px 4px; font-family: 'Courier New'; }"
    html += "pre { background: #f5f5f5; padding: 10px; }"
    html += "blockquote { background: #f9f9f9; border-left: 3px solid #ccc; padding: 10px; }"
    html += "</style></head><body>"
    
    lines = markdown_text.split('\n')
    in_code_block = False
    
    for line in lines:
        if line.strip().startswith('```'):
            if in_code_block:
                html += "</pre>"
                in_code_block = False
            else:
                html += "<pre>"
                in_code_block = True
            continue
        
        if in_code_block:
            html += line + '\n'
            continue
        
        # Headers
        for i in range(6, 0, -1):
            prefix = '#' * i + ' '
            if line.startswith(prefix):
                html += f"<h{i}>{line[len(prefix):]}</h{i}>"
                break
        else:
            
            line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
            line = re.sub(r'\*(.+?)\*', r'<em>\1</em>', line)
            line = re.sub(r'`(.+?)`', r'<code>\1</code>', line)
            line = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', line)
            
            if line.startswith('> '):
                html += f"<blockquote>{line[2:]}</blockquote>"
            elif line.strip():
                html += f"<p>{line}</p>"
            else:
                html += "<br>"
    
    html += "</body></html>"
    return html
