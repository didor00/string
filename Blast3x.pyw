import pymem
import customtkinter
import tkinter
from pymem.process import PROCESS_ALL_ACCESS

# Установка тёмной темы с кастомной цветовой схемой
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# Инициализация главного окна
app = customtkinter.CTk()
app.geometry("800x400")
app.title("Редактор памяти | github.com/BLAST3X")
app.resizable(False, False)

# Создание фрейма для лучшей организации
main_frame = customtkinter.CTkFrame(master=app, corner_radius=10)
main_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER, relwidth=0.9, relheight=0.9)

# Заголовок
title_label = customtkinter.CTkLabel(
    master=main_frame,
    text="Редактор памяти от github.com/BLAST3X",
    font=("Arial", 20, "bold"),
    text_color="#FF5555"
)
title_label.pack(pady=20)

# Поле для ввода PID
pid_entry = customtkinter.CTkEntry(
    master=main_frame,
    placeholder_text="Введите PID процесса",
    width=300,
    height=35,
    font=("Arial", 14),
    corner_radius=10,
    border_color="#FF5555"
)
pid_entry.pack(pady=10)

# Поле для ввода адреса памяти
address_entry = customtkinter.CTkEntry(
    master=main_frame,
    placeholder_text="Адрес памяти (hex)",
    width=300,
    height=35,
    font=("Arial", 14),
    corner_radius=10,
    border_color="#FF5555"
)
address_entry.pack(pady=10)

# Поле для ввода длины
length_entry = customtkinter.CTkEntry(
    master=main_frame,
    placeholder_text="Длина в байтах",
    width=300,
    height=35,
    font=("Arial", 14),
    corner_radius=10,
    border_color="#FF5555"
)
length_entry.pack(pady=10)

# Метка для статуса
status_label = customtkinter.CTkLabel(
    master=main_frame,
    text="",
    font=("Arial", 12),
    text_color="#55FF55"
)
status_label.pack(pady=10)

def remove_string():
    try:
        # Получение введённых данных
        pid = int(pid_entry.get())
        address = int(address_entry.get(), 16)  # Преобразование hex-строки в число
        length = int(length_entry.get())

        # Проверка ввода
        if length <= 0:
            status_label.configure(text="Ошибка: Длина должна быть положительной", text_color="#FF5555")
            return

        # Открытие процесса
        pm = pymem.Pymem()
        pm.open_process(pid)

        try:
            # Чтение исходных байтов
            original_bytes = pm.read_bytes(address, length)
            original_string = original_bytes.decode('utf-8', errors='ignore')
            
            # Создание заменяющих байтов (точки)
            replacement = b'.' * length
            
            # Запись точек в память
            pm.write_bytes(address, replacement, length)
            
            status_label.configure(
                text=f"Успех! Заменено {length} байт\nИсходная строка: {original_string}",
                text_color="#55FF55"
            )
            
        finally:
            pm.close_process()
            
    except Exception as e:
        status_label.configure(text=f"Ошибка: {str(e)}", text_color="#FF5555")

# Кнопка действия
action_button = customtkinter.CTkButton(
    master=main_frame,
    text="Заменить строку",
    width=200,
    height=40,
    font=("Arial", 14, "bold"),
    fg_color="#FF5555",
    hover_color="#CC4444",
    command=remove_string
)
action_button.pack(pady=20)

# Запуск главного цикла
app.mainloop()
