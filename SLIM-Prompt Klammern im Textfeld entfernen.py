import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pyperclip
import re

# Header
"""
This script provides a GUI for removing specific characters from text. 
The text is processed according to the following rules:
- Remove all parentheses `(` and `)` after processing the rest of the text.
- Remove all digits, periods `.` and colons `:` that are immediately before a closing parenthesis `)`.
- Remove all colons `:`.

Modules Required:
- tkinter: For creating the GUI.
- pyperclip: For clipboard operations.
- re: For regular expression operations.

To install the required modules, you can use pip:
pip install pyperclip
"""

class CharacterRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Character Remover")

        # Set the background color of the window
        self.root.configure(bg='black')

        # Variables for dragging
        self.drag_start_x = None
        self.drag_start_y = None

        # Create widgets
        self.create_widgets()

        # Initialize the "Keep on Top" status
        self.keep_on_top = True
        self.toggle_keep_on_top()

        # Adjust the window size to fit the content
        self.root.update_idletasks()  # Necessary to calculate widget sizes
        self.adjust_window_size()

        # Bind mouse events for dragging
        self.root.bind("<Button-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.do_drag)

    def create_widgets(self):
        # Frame for the buttons
        self.button_frame = tk.Frame(self.root, bg='black')
        self.button_frame.pack(pady=0)

        # Button to remove characters
        self.remove_button = tk.Button(self.button_frame, text="Remove Characters", command=self.remove_and_copy_text, bg="darkorange", fg="black", height=3, width=20)
        self.remove_button.grid(row=0, column=0, padx=5, pady=5)

        # Small button for instructions
        self.help_button = tk.Button(self.button_frame, text="?", command=self.show_instructions, bg="black", fg="orange", height=1, width=2)
        self.help_button.grid(row=0, column=1, padx=5, pady=5)

        # Toggle switch for "Keep on Top" mode
        self.keep_on_top_var = tk.BooleanVar(value=True)
        self.keep_on_top_check = ttk.Checkbutton(self.root, text="Keep on Top", variable=self.keep_on_top_var, command=self.toggle_keep_on_top, style="TCheckbutton")
        self.keep_on_top_check.pack(pady=2)

        # Style for the Checkbutton
        style = ttk.Style()
        style.configure("TCheckbutton", background="black", foreground="orange")

        # Slider for transparency
        self.transparency_label = tk.Label(self.root, text="Transparency:", bg='black', fg='orange')
        self.transparency_label.pack(pady=2)
        self.transparency_slider = tk.Scale(self.root, from_=0, to_=100, orient=tk.HORIZONTAL, command=self.adjust_transparency, length=150, bg='black', fg='orange', troughcolor='orange', sliderlength=20)
        self.transparency_slider.set(50)  # Set the default transparency to 50%
        self.transparency_slider.pack(pady=2)

    def remove_and_copy_text(self):
        try:
            # Get the text from the clipboard
            clipboard_content = pyperclip.paste()
            # Process the text
            processed_text = self.process_text(clipboard_content)
            # Set the processed text back to the clipboard
            pyperclip.copy(processed_text)
        except Exception as e:
            print(f"Error processing text: {e}")

    def process_text(self, text):
        # Remove digits, periods, and colons before a closing parenthesis
        text = re.sub(r'[0-9:.]+(?=\))', '', text)

        # Remove parentheses
        text = text.replace('(', '')  # Remove opening parentheses
        text = text.replace(')', '')  # Remove closing parentheses

        # Remove colons
       # text = text.replace(':', '')  # Remove colons

        return text

    def toggle_keep_on_top(self):
        self.keep_on_top = self.keep_on_top_var.get()
        self.root.attributes('-topmost', self.keep_on_top)

    def adjust_transparency(self, value):
        alpha = float(value) / 100
        self.root.attributes('-alpha', alpha)

    def adjust_window_size(self):
        # Calculate the window size based on the widgets
        button_width = self.remove_button.winfo_reqwidth() + 20  # +20 for padding
        button_height = self.remove_button.winfo_reqheight() + 20  # +20 for padding
        transparency_slider_length = self.transparency_slider.winfo_reqwidth() + 40  # +40 for padding

        # Calculate the window size based on the maximum dimensions
        window_width = max(button_width, transparency_slider_length)
        window_height = button_height + self.keep_on_top_check.winfo_reqheight() + self.transparency_slider.winfo_reqheight() + 40  # +40 for padding

        # Set the window size
        self.root.geometry(f"{window_width}x{window_height}")

    def show_instructions(self):
        instructions = (
            "Instructions:\n"
            "1. Copy the desired text from the prompt to the clipboard.\n"
            "2. Click on the Remove Characters button.\n"
            "3. The characters `(:0-9)` from the clipboard are removed and the edited text is pasted back into the clipboard.\n"
            "4. Replace the previously copied text with the text from the clipboard.\n"
            "\nA project by LordKa Photography"
        )
        messagebox.showinfo("Instructions", instructions)

    def start_drag(self, event):
        # Record the starting position for dragging
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def do_drag(self, event):
        # Calculate the distance moved and update the window position
        x = self.root.winfo_x() + (event.x - self.drag_start_x)
        y = self.root.winfo_y() + (event.y - self.drag_start_y)
        self.root.geometry(f'+{x}+{y}')

if __name__ == "__main__":
    root = tk.Tk()
    app = CharacterRemoverApp(root)
    root.mainloop()
