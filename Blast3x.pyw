import pymem
import customtkinter
import win32con  # For PROCESS_ALL_ACCESS

customtkinter.set_appearance_mode("dark")  # Set dark theme for better visibility

app = customtkinter.CTk()
app.geometry("700x300")
app.title("Memory Editor | GITHUB.COM/BLAST3X")

# Label
label = customtkinter.CTkLabel(master=app, text="MADE BY GITHUB.COM/BLAST3X", text_color="#FF0000", font=("Arial", 16))
label.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)

# Entry for process name
entry = customtkinter.CTkEntry(master=app, placeholder_text="Process name (e.g., notepad.exe)", width=200, height=30, border_width=2, corner_radius=10)
entry.place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)

# Entry for memory address
entry1 = customtkinter.CTkEntry(master=app, placeholder_text="Memory address (hex, e.g., 0x12345678)", width=200, height=30, border_width=2, corner_radius=10)
entry1.place(relx=0.5, rely=0.45, anchor=customtkinter.CENTER)

# Entry for length
entry2 = customtkinter.CTkEntry(master=app, placeholder_text="Length (bytes)", width=200, height=30, border_width=2, corner_radius=10)
entry2.place(relx=0.5, rely=0.6, anchor=customtkinter.CENTER)

# Label for status messages
status_label = customtkinter.CTkLabel(master=app, text="", text_color="#FFFFFF", font=("Arial", 12))
status_label.place(relx=0.5, rely=0.75, anchor=customtkinter.CENTER)

def button_event():
    try:
        # Get user inputs
        proc_name = entry.get().strip()
        address_str = entry1.get().strip()
        length_str = entry2.get().strip()

        # Input validation
        if not proc_name or not address_str or not length_str:
            status_label.configure(text="Error: All fields are required!", text_color="#FF0000")
            return

        try:
            address = int(address_str, 16)  # Convert hex string to integer
            length = int(length_str)  # Convert length to integer
            if length <= 0:
                raise ValueError("Length must be positive")
        except ValueError as e:
            status_label.configure(text=f"Error: Invalid address or length ({str(e)})", text_color="#FF0000")
            return

        # Open process by name
        pm = pymem.Pymem(proc_name)
        handle = pm.process_handle

        # Read the current string at the address
        current_string = pymem.memory.read_string(pm.process_handle, address, length)
        status_label.configure(text=f"Read string: {current_string}", text_color="#00FF00")

        # Create a string of dots to write
        value = b'.' * length  # Use bytes for memory writing

        # Write the string of dots to the memory address
        pymem.memory.write_bytes(pm.process_handle, address, value, length)
        status_label.configure(text=f"Successfully wrote {length} bytes to {hex(address)}", text_color="#00FF00")

        # Close the process handle
        pm.close_process()

    except pymem.exception.PymemError as e:
        status_label.configure(text=f"Error: {str(e)}", text_color="#FF0000")
    except Exception as e:
        status_label.configure(text=f"Unexpected error: {str(e)}", text_color="#FF0000")

# Button to trigger memory operation
button = customtkinter.CTkButton(master=app,
                                 width=120,
                                 height=32,
                                 border_width=0,
                                 corner_radius=8,
                                 fg_color="#FF0000",
                                 hover_color="#6A6767",
                                 text="Replace String",
                                 command=button_event)
button.place(relx=0.5, rely=0.9, anchor=customtkinter.CENTER)

app.mainloop()
