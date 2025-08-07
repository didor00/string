import pymem
import pymem.process
import customtkinter
import tkinter

customtkinter.set_appearance_mode("Dark")

app = customtkinter.CTk()
app.geometry("700x350")  # Немного увеличим высоту для статус-бара
app.title("GITHUB.COM/BLAST3X     |     THIS TOOL IS FREE")

label = customtkinter.CTkLabel(master=app, text="MADE BY GITHUB.COM/BLAST3X", text_color="#FF0000")
label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

# Изменили placeholder, чтобы было понятно, что нужно вводить имя процесса
entry = customtkinter.CTkEntry(master=app,
                               placeholder_text="Process Name (e.g. notepad.exe)",
                               width=220,  # Увеличим ширину
                               height=25,
                               border_width=2,
                               corner_radius=10)
entry.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

entry1 = customtkinter.CTkEntry(master=app,
                                placeholder_text="Memory Address (e.g. 0x140AC30)",
                                width=220,
                                height=25,
                                border_width=2,
                                corner_radius=10)
entry1.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

entry2 = customtkinter.CTkEntry(master=app,
                                placeholder_text="Length (number of bytes)",
                                width=220,
                                height=25,
                                border_width=2,
                                corner_radius=10)
entry2.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

# Метка для вывода статуса операции
status_label = customtkinter.CTkLabel(master=app, text="", text_color="white")
status_label.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

def button_event():
    # Сбрасываем статус
    status_label.configure(text="", text_color="white")

    try:
        process_name = entry.get()
        if not process_name:
            status_label.configure(text="Error: Process name cannot be empty.", text_color="#FF5733")
            return

        address = int(entry1.get(), 0) # base=0 позволяет вводить hex (0x...) и dec
        length = int(entry2.get())

        status_label.configure(text=f"Searching for process: {process_name}...", text_color="yellow")
        app.update_idletasks() # Обновляем GUI, чтобы показать сообщение

        # Открываем процесс по его имени
        pm = pymem.Pymem(process_name)

        status_label.configure(text=f"Process found! PID: {pm.process_id}. Writing memory...", text_color="cyan")
        app.update_idletasks()

        # Создаем последовательность нулевых байтов
        null_bytes = b'\x00' * length

        # Записываем байты в память по указанному адресу
        pm.write_bytes(address, null_bytes, length)

        success_message = f"Success! Wrote {length} null bytes to {hex(address)}."
        status_label.configure(text=success_message, text_color="#00FF00") # Зеленый цвет для успеха

    except ValueError:
        status_label.configure(text="Error: Invalid address or length. Please enter numbers.", text_color="#FF5733")
    except pymem.exception.ProcessNotFound:
        status_label.configure(text=f"Error: Process '{entry.get()}' not found.", text_color="#FF5733")
    except pymem.exception.MemoryWriteError:
        error_msg = f"Error: Could not write to {entry1.get()}.\nTry running the script as an Administrator."
        status_label.configure(text=error_msg, text_color="#FF5733")
    except Exception as e:
        status_label.configure(text=f"An unexpected error occurred: {e}", text_color="#FF5733")


button = customtkinter.CTkButton(master=app,
                                 width=120,
                                 height=32,
                                 border_width=0,
                                 corner_radius=8,
                                 fg_color="#FF0000",
                                 hover_color="#6A6767",
                                 text="Remove String",
                                 command=button_event)

button.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)
app.mainloop()
