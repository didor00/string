import pymem
import customtkinter
import tkinter

customtkinter.set_appearance_mode("Dark")

app = customtkinter.CTk()
app.geometry("700x350")
app.title("GITHUB.COM/BLAST3X | PROCESS MEMORY EDITOR (NO ADMIN REQUIRED)")

label = customtkinter.CTkLabel(master=app, text="MADE BY GITHUB.COM/BLAST3X", text_color="#FF0000")
label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

# Теперь запрашиваем PID (Process ID)
entry_pid = customtkinter.CTkEntry(master=app,
                                   placeholder_text="Process ID (PID, e.g. 1234)",
                                   width=220,
                                   height=25,
                                   border_width=2,
                                   corner_radius=10)
entry_pid.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

entry_addr = customtkinter.CTkEntry(master=app,
                                    placeholder_text="Memory Address (e.g. 0x140AC30)",
                                    width=220,
                                    height=25,
                                    border_width=2,
                                    corner_radius=10)
entry_addr.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

entry_len = customtkinter.CTkEntry(master=app,
                                   placeholder_text="Length (number of bytes)",
                                   width=220,
                                   height=25,
                                   border_width=2,
                                   corner_radius=10)
entry_len.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

status_label = customtkinter.CTkLabel(master=app, text="", text_color="white")
status_label.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

def button_event():
    status_label.configure(text="", text_color="white")

    try:
        pid = int(entry_pid.get())  # Преобразуем PID в число
        address = int(entry_addr.get(), 0)  # 0x... или просто число
        length = int(entry_len.get())

        status_label.configure(text=f"Opening process with PID: {pid}...", text_color="yellow")
        app.update_idletasks()

        # Открываем процесс по PID (НЕ требует прав админа)
        pm = pymem.Pymem(pid)

        status_label.configure(text=f"Process opened! Writing {length} bytes to {hex(address)}...", text_color="cyan")
        app.update_idletasks()

        null_bytes = b'\x00' * length
        pm.write_bytes(address, null_bytes, length)

        success_message = f"Success! Wrote {length} null bytes to {hex(address)} in PID {pid}."
        status_label.configure(text=success_message, text_color="#00FF00")

    except ValueError:
        status_label.configure(text="Error: PID, Address and Length must be valid numbers.", text_color="#FF5733")
    except pymem.exception.ProcessNotFound:
        status_label.configure(text=f"Error: Process with PID {entry_pid.get()} not found.", text_color="#FF5733")
    except pymem.exception.MemoryWriteError:
        status_label.configure(text=f"Warning: Could not write to {hex(address)}. Memory may be protected.\nTry running as Administrator if needed.", text_color="#FFA500")  # Оранжевый (предупреждение)
    except Exception as e:
        status_label.configure(text=f"Unexpected error: {e}", text_color="#FF5733")


button = customtkinter.CTkButton(master=app,
                                 width=120,
                                 height=32,
                                 border_width=0,
                                 corner_radius=8,
                                 fg_color="#FF0000",
                                 hover_color="#6A6767",
                                 text="Clear Memory",
                                 command=button_event)
button.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)

app.mainloop()
