# -- РАБОЧИЙ КОД (ЯРКИЙ ДИЗАЙН) --

import pymem
import pymem.process
import customtkinter
import tkinter

# Устанавливаем светлую тему
customtkinter.set_appearance_mode("light") 

app = customtkinter.CTk()
# Устанавливаем светлый фон для окна
app.configure(fg_color="#ECECEC") 
app.geometry("700x400")
app.title("GITHUB.COM/BLAST3X     |     THIS TOOL IS FREE")

# Яркий цвет для заголовка
label_title = customtkinter.CTkLabel(master=app, 
                                     text="MADE BY GITHUB.COM/BLAST3X", 
                                     text_color="#0052cc", 
                                     font=("Arial", 20, "bold"))
label_title.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

# Поля для ввода
entry_proc = customtkinter.CTkEntry(master=app,
                                    placeholder_text="process_name.exe",
                                    width=200,
                                    height=30,
                                    border_width=1)
entry_proc.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

entry_address = customtkinter.CTkEntry(master=app,
                                       placeholder_text="Адрес в памяти (напр. 0x123ABC)",
                                       width=200,
                                       height=30,
                                       border_width=1)
entry_address.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

entry_length = customtkinter.CTkEntry(master=app,
                                      placeholder_text="Длина для перезаписи",
                                      width=200,
                                      height=30,
                                      border_width=1)
entry_length.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

# Строка статуса для обратной связи
status_label = customtkinter.CTkLabel(master=app, text="Статус: ожидание ввода", text_color="grey")
status_label.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

# Полностью исправленная логика кнопки
def button_event():
    proc_name = entry_proc.get()
    try:
        address = int(entry_address.get(), 0)
        length = int(entry_length.get(), 0)
    except ValueError:
        status_label.configure(text="Ошибка: Адрес и длина должны быть числами.", text_color="orange")
        return

    if not proc_name or not length: # Адрес может быть 0, поэтому не проверяем его на "пустоту"
        status_label.configure(text="Ошибка: Имя процесса и длина должны быть заполнены.", text_color="orange")
        return

    try:
        pm = pymem.Pymem(proc_name)
        status_label.configure(text=f"Процесс '{proc_name}' (PID: {pm.process_id}) найден.", text_color="#0b5ed7")
        app.update_idletasks()
        
        replacement_bytes = b'.' * length
        pm.write_bytes(address, replacement_bytes, length)
        
        status_label.configure(text=f"УСПЕХ! {length} байт по адресу {hex(address)} перезаписано.", text_color="#157347")

    except pymem.exception.ProcessNotFound:
        status_label.configure(text=f"Ошибка: Процесс '{proc_name}' не найден.", text_color="#dc3545")
    except pymem.exception.MemoryWriteError:
        status_label.configure(text=f"Ошибка: Не удалось записать в память. Запустите от админа?", text_color="#dc3545")
    except Exception as e:
        status_label.configure(text=f"Неизвестная ошибка: {e}", text_color="#dc3545")

# Новые цвета для кнопки
button = customtkinter.CTkButton(master=app,
                                 width=150,
                                 height=40,
                                 text="Remove String",
                                 command=button_event,
                                 fg_color="#d32f2f",
                                 hover_color="#b71c1c",
                                 text_color="white",
                                 font=("Arial", 14, "bold"))
button.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)

app.mainloop()

