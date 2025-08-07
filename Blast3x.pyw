import pymem
import customtkinter
import tkinter

customtkinter.set_appearance_mode("dark")

app = customtkinter.CTk()
app.configure(bg="black")
app.geometry("700x300")
app.title("GITHUB.COM/BLAST3X     |     THIS TOOL IS FREE")

label = customtkinter.CTkLabel(master=app, text="MADE BY GITHUB.COM/BLAST3X", text_color="#FF0000")
label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

entry = customtkinter.CTkEntry(master=app, placeholder_text="process name", width=120, height=25, border_width=2, corner_radius=10)
entry.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

entry1 = customtkinter.CTkEntry(master=app, placeholder_text="memory address (hex)", width=120, height=25, border_width=2, corner_radius=10)
entry1.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

entry2 = customtkinter.CTkEntry(master=app, placeholder_text="length", width=120, height=25, border_width=2, corner_radius=10)
entry2.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

def button_event():
    try:
        procname = entry.get()
        address = int(entry1.get(), 0)  # Поддержка шестнадцатеричного формата (например, 0x1234)
        length = int(entry2.get(), 0)
        
        # Находим процесс по имени
        pm = pymem.Pymem()
        process_id = None
        for proc in pymem.process.list_processes():
            if proc.name.lower() == procname.lower():
                process_id = proc.pid
                break
        
        if not process_id:
            print(f"Процесс {procname} не найден")
            return
        
        # Открываем процесс
        handle = pymem.Pymem(procname)
        
        # Читаем текущую строку
        current_string = pymem.memory.read_string(handle.process_handle, address, length)
        print(f"Текущая строка: {current_string}")
        
        # Заменяем строку на точки
        new_value = "." * length
        pymem.memory.write_string(handle.process_handle, address, new_value.encode())
        print(f"Строка по адресу {hex(address)} заменена на {new_value}")
        
    except Exception as e:
        print(f"Ошибка: {e}")

button = customtkinter.CTkButton(master=app, width=120, height=32, border_width=0, corner_radius=8,
                                fg_color="#FF0000", hover_color="#6A6767", text="remove string", command=button_event)
button.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

app.mainloop()
