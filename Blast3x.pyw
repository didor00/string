import pymem
import pymem.process
import customtkinter
import tkinter

# Устанавливаем тёмную тему, так как "#000000" не является валидным параметром
customtkinter.set_appearance_mode("Dark")

app = customtkinter.CTk()
# app.configure(bg="black") # Этот параметр не нужен при использовании темы
app.geometry("700x300")
app.title("GITHUB.COM/BLAST3X     |     THIS TOOL IS FREE")

label = customtkinter.CTkLabel(master=app, text="MADE BY GITHUB.COM/BLAST3X", text_color="#FF0000")
label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

# Изменили placeholder, чтобы было понятно, что нужно вводить PID
entry = customtkinter.CTkEntry(master=app,
                               placeholder_text="Process ID (PID)",
                               width=120,
                               height=25,
                               border_width=2,
                               corner_radius=10)
entry.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

entry1 = customtkinter.CTkEntry(master=app,
                                placeholder_text="memory address",
                                width=120,
                                height=25,
                                border_width=2,
                                corner_radius=10)
entry1.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

entry2 = customtkinter.CTkEntry(master=app,
                                placeholder_text="length",
                                width=120,
                                height=25,
                                border_width=2,
                                corner_radius=10)
entry2.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

def button_event():
    try:
        # Получаем данные из полей ввода
        # entry.get() теперь содержит PID процесса
        process_id = int(entry.get())
        address = int(entry1.get(), 0) # base=0 позволяет вводить hex (0x...) и dec
        length = int(entry2.get())

        print(f"Attempting to modify PID: {process_id}")
        print(f"Address: {hex(address)}")
        print(f"Length: {length}")

        # Открываем процесс по его PID
        pm = pymem.Pymem(process_id)

        # Создаем последовательность нулевых байтов для "удаления" строки
        # Это более правильный способ, чем запись точек
        null_bytes = b'\x00' * length

        # Записываем байты в память по указанному адресу
        pm.write_bytes(address, null_bytes, length)

        print(f"Success! Wrote {length} null bytes to address {hex(address)} in PID {process_id}.")

    # Обработка возможных ошибок, чтобы приложение не падало
    except ValueError:
        print("Error: PID and length must be integers. Address can be integer or hex (e.g., 0x...).")
    except pymem.exception.ProcessNotFound:
        print(f"Error: Process with PID {entry.get()} not found.")
    except pymem.exception.MemoryWriteError:
        print(f"Error: Could not write to memory address {entry1.get()}. It might be protected.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


button = customtkinter.CTkButton(master=app,
                                 width=120,
                                 height=32,
                                 border_width=0,
                                 corner_radius=8,
                                 fg_color="#FF0000",
                                 hover_color="#6A6767",
                                 text="Remove String",
                                 command=button_event)

button.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
app.mainloop()
