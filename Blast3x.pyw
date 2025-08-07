import pymem
import pymem.exception
import customtkinter
import tkinter

# --- НАСТРОЙКИ ОКНА ---
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("700x450") # Увеличим высоту для новых элементов
app.title("GITHUB.COM/BLAST3X | Memory Patcher v2")

# --- ВИДЖЕТЫ ИНТЕРФЕЙСА ---

# Заголовок
title_label = customtkinter.CTkLabel(master=app, text="MADE BY GITHUB.COM/BLAST3X", text_color="#FF0000", font=("Arial", 16, "bold"))
title_label.place(relx=0.5, rely=0.08, anchor=tkinter.CENTER)

# --- НОВОЕ: Блок для поиска PID по имени процесса ---
proc_name_label = customtkinter.CTkLabel(master=app, text="1. Найти процесс по имени (.exe)")
proc_name_label.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

entry_proc_name = customtkinter.CTkEntry(master=app,
                                         placeholder_text="Например, notepad.exe",
                                         width=200, height=30)
entry_proc_name.place(relx=0.4, rely=0.28, anchor=tkinter.CENTER)

# --- НОВОЕ: Функция для поиска PID ---
def find_pid_event():
    proc_name = entry_proc_name.get()
    if not proc_name:
        status_label.configure(text="Введите имя процесса!", text_color="orange")
        return
    try:
        # Находим процесс по имени
        process = pymem.process.process_from_name(proc_name)
        pid = process.process_id
        # Очищаем поле для PID и вставляем найденное значение
        entry_pid.delete(0, 'end')
        entry_pid.insert(0, str(pid))
        status_label.configure(text=f"Процесс '{proc_name}' найден! PID: {pid}", text_color="green")
    except pymem.exception.ProcessNotFound:
        status_label.configure(text=f"Процесс '{proc_name}' не найден!", text_color="red")

find_pid_button = customtkinter.CTkButton(master=app,
                                          text="Найти PID",
                                          command=find_pid_event,
                                          width=100, height=30)
find_pid_button.place(relx=0.65, rely=0.28, anchor=tkinter.CENTER)

# --- Блок для перезаписи памяти ---
write_label = customtkinter.CTkLabel(master=app, text="2. Перезаписать память по PID и адресу")
write_label.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

entry_pid = customtkinter.CTkEntry(master=app,
                                   placeholder_text="Process ID (PID)",
                                   width=200, height=30)
entry_pid.place(relx=0.5, rely=0.48, anchor=tkinter.CENTER)

entry_address = customtkinter.CTkEntry(master=app,
                                       placeholder_text="Адрес памяти (например, 0x1A2B3C)",
                                       width=200, height=30)
entry_address.place(relx=0.5, rely=0.58, anchor=tkinter.CENTER)

entry_length = customtkinter.CTkEntry(master=app,
                                      placeholder_text="Длина (сколько байт затереть)",
                                      width=200, height=30)
entry_length.place(relx=0.5, rely=0.68, anchor=tkinter.CENTER)

# --- Основная функция перезаписи ---
def overwrite_memory_event():
    try:
        pid = int(entry_pid.get())
        address = int(entry_address.get(), 0) # 0 - автоопределение системы (10 или 16)
        length = int(entry_length.get())

        if length <= 0:
            status_label.configure(text="Длина должна быть больше нуля!", text_color="orange")
            return
            
        pm = pymem.Pymem(pid)
        
        # Создаем байтовую строку из точек для записи
        bytes_to_write = b'.' * length
        
        pm.write_bytes(address, bytes_to_write, length)
        
        success_message = f"Успех! Записано {length} байт в PID {pid} по адресу 0x{address:X}"
        print(success_message)
        status_label.configure(text=success_message, text_color="green")

    except ValueError:
        status_label.configure(text="Ошибка: PID, адрес и длина должны быть числами.", text_color="red")
    except pymem.exception.ProcessNotFound:
        status_label.configure(text=f"Ошибка: Процесс с PID {entry_pid.get()} не найден.", text_color="red")
    except pymem.exception.CouldNotOpenProcess:
        status_label.configure(text=f"Ошибка доступа к PID {entry_pid.get()}. Запустите от имени Администратора.", text_color="red")
    except Exception as e:
        status_label.configure(text=f"Произошла ошибка: {e}", text_color="red")

# Кнопка для запуска перезаписи
overwrite_button = customtkinter.CTkButton(master=app,
                                           text="Перезаписать память",
                                           command=overwrite_memory_event,
                                           width=200, height=40,
                                           fg_color="#FF0000", hover_color="#C00000")
overwrite_button.place(relx=0.5, rely=0.82, anchor=tkinter.CENTER)

# Метка для вывода статуса
status_label = customtkinter.CTkLabel(master=app, text="Ожидание действий...", font=("Arial", 12))
status_label.place(relx=0.5, rely=0.93, anchor=tkinter.CENTER)

# Запуск главного цикла приложения
app.mainloop()
