import pymem
import pymem.process
import customtkinter
import tkinter

# --- Настройка окна ---
customtkinter.set_appearance_mode("dark")  # Используем темную тему
app = customtkinter.CTk()
app.configure(bg="black")
app.geometry("700x400") # Сделал окно чуть выше для статус-бара
app.title("spastil DarkFred     |     THIS TOOL IS FREE")

# --- Элементы интерфейса ---
label_title = customtkinter.CTkLabel(master=app, text="spastil DarkFred", text_color="#FF0000", font=("Arial", 20))
label_title.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

# ИЗМЕНЕНИЕ №1: Запрашиваем PID вместо имени процесса
entry_pid = customtkinter.CTkEntry(master=app,
                                   placeholder_text="PID процесса", # Изменен текст-подсказка
                                   width=150,
                                   height=30,
                                   border_width=2,
                                   corner_radius=10)
entry_pid.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

entry_address = customtkinter.CTkEntry(master=app,
                                       placeholder_text="Адрес в памяти (напр. 0x123ABC)",
                                       width=150,
                                       height=30,
                                       border_width=2,
                                       corner_radius=10)
entry_address.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

entry_length = customtkinter.CTkEntry(master=app,
                                      placeholder_text="Длина для перезаписи",
                                      width=150,
                                      height=30,
                                      border_width=2,
                                      corner_radius=10)
entry_length.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

# Добавим метку для отображения статуса операции
status_label = customtkinter.CTkLabel(master=app, text="Статус: ожидание ввода", text_color="grey")
status_label.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)


# ИЗМЕНЕНИЕ №2: Полностью переписанная логика кнопки
def button_event():
    try:
        # Получаем данные из полей ввода
        pid = int(entry_pid.get()) # Конвертируем PID в число
        address = int(entry_address.get(), 0) # 0 позволяет вводить hex (0x...)
        length = int(entry_length.get(), 0)
    except ValueError:
        # Если пользователь ввел текст вместо числа
        status_label.configure(text="Ошибка: PID и длина должны быть числами.", text_color="orange")
        return

    try:
        # 1. Открываем процесс по его PID
        pm = pymem.Pymem(pid)
        status_label.configure(text=f"Процесс '{pm.process_name}' (PID: {pid}) найден.", text_color="cyan")
        app.update_idletasks() # Обновляем текст до начала записи

        # 2. Готовим данные для записи (байтовая строка из точек)
        # Это правильный и эффективный способ
        replacement_bytes = b'.' * length
        
        # 3. ГЛАВНОЕ: Перезаписываем память по адресу
        pm.write_bytes(address, replacement_bytes, length)
        
        status_label.configure(text=f"УСПЕХ! {length} байт по адресу {hex(address)} перезаписано.", text_color="green")

    except pymem.exception.ProcessNotFound:
        status_label.configure(text=f"Ошибка: Процесс с PID {pid} не найден.", text_color="red")
    except pymem.exception.MemoryWriteError:
        status_label.configure(text=f"Ошибка: Не удалось записать в память. Адрес защищен?", text_color="red")
    except Exception as e:
        # Ловим любые другие непредвиденные ошибки
        status_label.configure(text=f"Неизвестная ошибка: {e}", text_color="red")


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
