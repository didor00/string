import pymem
import pymem.exception
import customtkinter
import tkinter

# --- НАСТРОЙКА ИНТЕРФЕЙСА ---
customtkinter.set_appearance_mode("dark") # Рекомендуется использовать "dark" или "light" вместо HEX
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("700x400") # Немного увеличим высоту для метки статуса
app.title("GITHUB.COM/BLAST3X     |     THIS TOOL IS FREE")
# app.configure(bg="black") # CTk делает это автоматически при темной теме

label = customtkinter.CTkLabel(master=app, text="MADE BY GITHUB.COM/BLAST3X", text_color="#FF0000", font=("Arial", 16, "bold"))
label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

entry_process = customtkinter.CTkEntry(master=app,
                                       placeholder_text="имя процесса (например, notepad.exe)",
                                       width=250,
                                       height=30,
                                       border_width=2,
                                       corner_radius=10)
entry_process.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

entry_address = customtkinter.CTkEntry(master=app,
                                       placeholder_text="адрес памяти (например, 0x140A7B0)",
                                       width=250,
                                       height=30,
                                       border_width=2,
                                       corner_radius=10)
entry_address.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

entry_length = customtkinter.CTkEntry(master=app,
                                      placeholder_text="длина для очистки (в байтах)",
                                      width=250,
                                      height=30,
                                      border_width=2,
                                      corner_radius=10)
entry_length.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

# Метка для вывода статуса операции
status_label = customtkinter.CTkLabel(master=app, text="", font=("Arial", 12))
status_label.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

def button_event():
    """
    Основная функция, которая выполняется при нажатии на кнопку.
    """
    try:
        # 1. Получаем данные из полей ввода
        procname = entry_process.get()
        # Проверяем, что поля не пустые
        if not procname or not entry_address.get() or not entry_length.get():
            status_label.configure(text="Ошибка: Все поля должны быть заполнены.", text_color="orange")
            return

        # int(..., 0) позволяет вводить как обычные числа (12345), так и hex (0xABC)
        address = int(entry_address.get(), 0)
        length = int(entry_length.get(), 0)

        status_label.configure(text=f"Попытка подключиться к процессу: {procname}...", text_color="gray")
        app.update_idletasks() # Обновляем интерфейс, чтобы показать сообщение

        # 2. Открываем процесс по имени
        pm = pymem.Pymem(procname)
        status_label.configure(text=f"Успешно подключено. PID: {pm.process_id}", text_color="cyan")
        app.update_idletasks()

        # 3. Готовим байты для записи (нулевые байты для "очистки" строки)
        bytes_to_write = b'\x00' * length

        # 4. Записываем байты по указанному адресу
        pm.write_bytes(address, bytes_to_write, length)
        
        # 5. Сообщаем об успехе
        status_label.configure(text=f"Успешно! {length} байт(ов) по адресу {hex(address)} заполнено нулями.", text_color="green")

    except pymem.exception.ProcessNotFound:
        status_label.configure(text=f"Ошибка: Процесс '{procname}' не найден!", text_color="red")
    except ValueError:
        status_label.configure(text="Ошибка: Адрес и длина должны быть числами (можно в hex, например 0x...).", text_color="red")
    except pymem.exception.MemoryWriteError as e:
        status_label.configure(text=f"Ошибка записи в память: {e}\n(Попробуйте запустить от имени администратора)", text_color="red")
    except Exception as e:
        # Отлавливаем любые другие возможные ошибки
        status_label.configure(text=f"Произошла непредвиденная ошибка: {e}", text_color="red")


button = customtkinter.CTkButton(master=app,
                                 width=150,
                                 height=40,
                                 border_width=0,
                                 corner_radius=8,
                                 fg_color="#FF0000",
                                 hover_color="#C00000",
                                 text="Очистить память",
                                 font=("Arial", 14, "bold"),
                                 command=button_event)

button.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)

# --- ЗАПУСК ПРИЛОЖЕНИЯ ---
app.mainloop()
