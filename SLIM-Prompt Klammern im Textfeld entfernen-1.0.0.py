# Datum: 31.03.2025
# Versionsnummer
version = "1.0.0"
# Zusammenfassung: Dieses Skript erstellt ein GUI zur Entfernung spezifischer Zeichen aus Text (Zahlen, Punkte, Doppelpunkte vor Klammern und Klammern selbst).
# Es unterstützt Clipboard-Operationen, Transparenzanpassung, "Always on Top"-Funktion und Drag-and-Drop. Neu in v1.0.0: Start mit 100% Transparenz,
# Fenster um 20% verkleinert, "?"-Button neben "Always on Top", Versionsnummer im GUI, Farbdesign angepasst.

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pyperclip
import re

class CharacterRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Character Remover")

        # Transparenz auf 100% setzen (1.0 = vollständig sichtbar)
        self.root.attributes("-alpha", 1.0)

        # Farbdesign aus den Anforderungen
        self.root.configure(bg="#1F1F1F")  # Hintergrundfarbe des Formulars

        # Fenstergröße um 20% verkleinern (Basisgröße dynamisch berechnet)
        self.root.update_idletasks()  # Widget-Größen aktualisieren
        base_width, base_height = self.root.winfo_reqwidth(), self.root.winfo_reqheight()
        new_width, new_height = int(base_width * 0.8), int(base_height * 0.8)

        # Variables for dragging
        self.drag_start_x = None
        self.drag_start_y = None

        # Create widgets
        self.create_widgets()

        # Initialize the "Always on Top" status (Default: False wie gefordert)
        self.keep_on_top_var = tk.BooleanVar(value=False)
        self.toggle_keep_on_top()

        # Bind mouse events for dragging
        self.root.bind("<Button-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.do_drag)

        # Fenstergröße anpassen (nach Widget-Erstellung)
        self.adjust_window_size()

    def create_widgets(self):
        # Frame für Buttons und Kontrollkästchen
        self.top_frame = tk.Frame(self.root, bg="#1F1F1F")
        self.top_frame.pack(pady=5)

        # "Always on Top" Kontrollkästchen
        self.keep_on_top_check = ttk.Checkbutton(self.top_frame, text="Always on Top", variable=self.keep_on_top_var,
                                                 command=self.toggle_keep_on_top, style="TCheckbutton")
        self.keep_on_top_check.grid(row=0, column=0, padx=(5, 0), pady=2)

        # "?" Button direkt neben "Always on Top"
        self.help_button = tk.Button(self.top_frame, text="?", command=self.show_instructions, bg="#FFA500", fg="#000000",
                                     height=1, width=2)
        self.help_button.grid(row=0, column=1, padx=5, pady=2)

        # Frame für den "Remove Characters" Button
        self.button_frame = tk.Frame(self.root, bg="#1F1F1F")
        self.button_frame.pack(pady=5)

        # Button zum Entfernen von Zeichen
        self.remove_button = tk.Button(self.button_frame, text="Remove Characters", command=self.remove_and_copy_text,
                                       bg="#FFA500", fg="#000000", height=3, width=20)
        self.remove_button.pack(padx=5, pady=5)

        # Slider für Transparenz
        self.transparency_label = tk.Label(self.root, text="Transparency:", bg="#1F1F1F", fg="#FFA500")
        self.transparency_label.pack(pady=2)
        self.transparency_slider = tk.Scale(self.root, from_=0, to_=100, orient=tk.HORIZONTAL, command=self.adjust_transparency,
                                            length=150, bg="#1F1F1F", fg="#FFA500", troughcolor="#000000", sliderlength=20)
        self.transparency_slider.set(100)  # Start bei 100% Transparenz
        self.transparency_slider.pack(pady=2)

        # Versionsnummer dezent anzeigen
        self.version_label = tk.Label(self.root, text=f"v{version}", bg="#1F1F1F", fg="#FFA500", font=("Arial", 8))
        self.version_label.pack(side=tk.BOTTOM, pady=2)

        # Style für Checkbutton
        style = ttk.Style()
        style.configure("TCheckbutton", background="#1F1F1F", foreground="#FFA500")

    def remove_and_copy_text(self):
        try:
            # Text aus der Zwischenablage holen
            clipboard_content = pyperclip.paste()
            # Text verarbeiten
            processed_text = self.process_text(clipboard_content)
            # Verarbeiteten Text in die Zwischenablage kopieren
            pyperclip.copy(processed_text)
        except Exception as e:
            print(f"Error processing text: {e}")

    def process_text(self, text):
        # Zahlen, Punkte und Doppelpunkte vor einer schließenden Klammer entfernen
        text = re.sub(r'[0-9:.]+(?=\))', '', text)
        # Klammern entfernen
        text = text.replace('(', '').replace(')', '')
        # Doppelpunkte entfernen (optional auskommentiert im Original)
        # text = text.replace(':', '')
        return text

    def toggle_keep_on_top(self):
        self.root.attributes('-topmost', self.keep_on_top_var.get())

    def adjust_transparency(self, value):
        alpha = float(value) / 100
        self.root.attributes('-alpha', alpha)

    def adjust_window_size(self):
        # Fenstergröße basierend auf Widgets berechnen
        self.root.update_idletasks()
        button_width = self.remove_button.winfo_reqwidth() + 20
        transparency_slider_length = self.transparency_slider.winfo_reqwidth() + 40
        window_width = max(button_width, transparency_slider_length)
        window_height = (self.remove_button.winfo_reqheight() + self.keep_on_top_check.winfo_reqheight() +
                         self.transparency_slider.winfo_reqheight() + self.version_label.winfo_reqheight() + 50)
        # Fenster um 20% verkleinern
        new_width, new_height = int(window_width * 0.8), int(window_height * 0.8)
        self.root.geometry(f"{new_width}x{new_height}")

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
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def do_drag(self, event):
        x = self.root.winfo_x() + (event.x - self.drag_start_x)
        y = self.root.winfo_y() + (event.y - self.drag_start_y)
        self.root.geometry(f'+{x}+{y}')

if __name__ == "__main__":
    root = tk.Tk()
    app = CharacterRemoverApp(root)
    root.mainloop()