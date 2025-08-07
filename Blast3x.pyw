import pymem
import customtkinter
import tkinter
from pymem.process import PROCESS_ALL_ACCESS

# Set dark theme with custom appearance
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# Initialize main window
app = customtkinter.CTk()
app.geometry("800x400")
app.title("Memory Editor | github.com/BLAST3X")
app.resizable(False, False)

# Create frame for better organization
main_frame = customtkinter.CTkFrame(master=app, corner_radius=10)
main_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER, relwidth=0.9, relheight=0.9)

# Title label
title_label = customtkinter.CTkLabel(
    master=main_frame,
    text="Memory Editor by github.com/BLAST3X",
    font=("Arial", 20, "bold"),
    text_color="#FF5555"
)
title_label.pack(pady=20)

# PID Entry
pid_entry = customtkinter.CTkEntry(
    master=main_frame,
    placeholder_text="Enter Process ID (PID)",
    width=300,
    height=35,
    font=("Arial", 14),
    corner_radius=10,
    border_color="#FF5555"
)
pid_entry.pack(pady=10)

# Memory Address Entry
address_entry = customtkinter.CTkEntry(
    master=main_frame,
    placeholder_text="Memory Address (hex)",
    width=300,
    height=35,
    font=("Arial", 14),
    corner_radius=10,
    border_color="#FF5555"
)
address_entry.pack(pady=10)

# Length Entry
length_entry = customtkinter.CTkEntry(
    master=main_frame,
    placeholder_text="Length of bytes",
    width=300,
    height=35,
    font=("Arial", 14),
    corner_radius=10,
    border_color="#FF5555"
)
length_entry.pack(pady=10)

# Status Label
status_label = customtkinter.CTkLabel(
    master=main_frame,
    text="",
    font=("Arial", 12),
    text_color="#55FF55"
)
status_label.pack(pady=10)

def remove_string():
    try:
        # Get input values
        pid = int(pid_entry.get())
        address = int(address_entry.get(), 16)  # Convert hex string to int
        length = int(length_entry.get())

        # Validate inputs
        if length <= 0:
            status_label.configure(text="Error: Length must be positive", text_color="#FF5555")
            return

        # Open process
        pm = pymem.Pymem()
        pm.open_process(pid)

        try:
            # Read original bytes
            original_bytes = pm.read_bytes(address, length)
            original_string = original_bytes.decode('utf-8', errors='ignore')
            
            # Create replacement bytes (dots)
            replacement = b'.' * length
            
            # Write dots to memory
            pm.write_bytes(address, replacement, length)
            
            status_label.configure(
                text=f"Success! Replaced {length} bytes\nOriginal: {original_string}",
                text_color="#55FF55"
            )
            
        finally:
            pm.close_process()
            
    except Exception as e:
        status_label.configure(text=f"Error: {str(e)}", text_color="#FF5555")

# Action Button
action_button = customtkinter.CTkButton(
    master=main_frame,
    text="Remove String",
    width=200,
    height=40,
    font=("Arial", 14, "bold"),
    fg_color="#FF5555",
    hover_color="#CC4444",
    command=remove_string
)
action_button.pack(pady=20)

# Start main loop
app.mainloop()
