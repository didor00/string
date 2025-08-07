import pymem
import customtkinter
import traceback

# Настройка темной темы
customtkinter.set_appearance_mode("dark")

# Создание главного окна
app = customtkinter.CTk()
app.geometry("700x300")
app.title("String Remover | GITHUB.COM/BLAST3X")

# Метка с информацией об авторе
label = customtkinter.CTkLabel(master=app, text="Создано: GITHUB.COM/BLAST3X", text_color="#FF0000", font=("Arial", 16))
label.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)

# Поле ввода PID процесса
entry = customtkinter.CTkEntry(master=app, placeholder_text="PID процесса (например, 1234)", width=200, height=30, border_width=2, corner_radius=10)
entry.place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)

# Поле ввода адреса памяти
entry1 = customtkinter.CTkEntry(master=app, placeholder_text="Адрес памяти (hex, например, 0x12345678)", width=200, height=30, border_width=2, corner_radius=10)
entry1.place(relx=0.5, rely=0.45, anchor=customtkinter.CENTER)

# Поле ввода длины
entry2 = customtkinter.CTkEntry(master=app, placeholder_text="Длина (байт)", width=200, height=30, border_width=2, corner_radius=10)
entry2.place(relx=0.5, rely=0.6, anchor=customtkinter.CENTER)

# Метка для отображения статуса
status_label = customtkinter.CTkLabel(master=app, text="", text_color="#FFFFFF", font=("Arial", 12))
status_label.place(relx=0.5, rely=0.75, anchor=customtkinter.CENTER)

def remove():
    try:
        # Получение входных данных
        pid_str = entry.get().strip()
        address_str = entry1.get().strip()
        length_str = entry2.get().strip()

        # Проверка заполненности полей
        if not pid_str or not address_str or not length_str:
            status_label.configure(text="Ошибка: Все поля должны быть заполнены!", text_color="#FF0000")
            return

        # Проверка PID, адреса и длины
        try:
            pid = int(pid_str)  # PID как целое число
            address = int(address_str, 16)  # Шестнадцатеричный адрес
            length = int(length_str)  # Длина в байтах
            if length <= 0:
                raise ValueError("Длина должна быть положительной")
        except ValueError as e:
            status_label.configure(text=f"Ошибка: Неверный PID, адрес или длина ({str(e)})", text_color="#FF0000")
            return

        # Открытие процесса
        status_label.configure(text="Открытие процесса...", text_color="#FFFFFF")
        pm = pymem.Pymem()
        pm.open_process(pid)

        # Чтение текущей строки из памяти
        status_label.configure(text="Чтение данных из памяти...", text_color="#FFFFFF")
        current_string = pymem.memory.read_string(pm.process_handle, address, length)
        status_label.configure(text=f"Прочитано: {current_string}", text_color="#00FF00")

        # Запись строки из точек в память
        status_label.configure(text="Запись данных в память...", text_color="#FFFFFF")
        pymem.memory.write_string(pm.process_handle, address, b'.' * length)
        status_label.configure(text=f"Успешно записано {length} байт по адресу {hex(address)}", text_color="#00FF00")

        # Закрытие процесса
        pm.close_process()

    except pymem.exception.PymemError as e:
        status_label.configure(text=f"Ошибка Pymem: {str(e)}", text_color="#FF0000")
    except Exception as e:
        status_label.configure(text=f"Неожиданная ошибка: {str(e)}", text_color="#FF0000")
        print("Полная ошибка:", traceback.format_exc())  # Вывод трассировки в консоль

# Кнопка для выполнения операции
button = customtkinter.CTkButton(master=app,
                                 width=120,
                                 height=32,
                                 border_width=0,
                                 corner_radius=8,
                                 fg_color="#FF0000",
                                 hover_color="#6A6767",
                                 text="Заменить строку",
                                 command=remove)
button.place(relx=0.5, rely=0.9, anchor=customtkinter.CENTER)

# Запуск приложения
app.mainloop()
