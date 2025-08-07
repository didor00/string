import pymem
import pymem.exception
import customtkinter
import tkinter

# Устанавливаем темную тему для окна
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue") # Можно выбрать "blue", "green" или "dark-blue"

app = customtkinter.CTk()
# app.configure(bg="black") # Это уже не нужно при использовании темы
app.geometry("700x350") # Немного увеличим высоту для метки состояния
app.title("GITHUB.COM/BLAST3X | Memory Patcher (by PID)")

label = customtkinter.CTkLabel(master=app, text="MADE BY GITHUB.COM/BLAST3X", text_color="#FF0000")
label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

# --- Изменено: теперь это поле для PID, а не для имени процесса ---
entry_pid = customtkinter.CTkEntry(master=app,
                                   placeholder_text="Process ID (PID)",
                                   width=150,
                                   height=25,
                                   border_width=2,
                                   corner_radius=10)
entry_pid.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

entry_address = customtkinter.CTkEntry(master=app,
                                       placeholder_text="Memory Address (e.g. 0x1A2B3C)",
                                       width=150,
                                       height=25,
                                       border_width=2,
                                       corner_radius=10)
entry_address.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

entry_length = customtkinter.CTkEntry(master=app,
                                      placeholder_text="Length (bytes to overwrite)",
                                      width=150,
                                      height=25,
                                      border_width=2,
                                      corner_radius=10)
entry_length.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

# Функция, которая будет вызываться при нажатии на кнопку
def button_event():
    # Очищаем метку состояния перед новой операцией
    status_label.configure(text="")
    
    try:
        # --- ИСПРАВЛЕНО: Получаем значения из полей ---
        # Получаем PID как число
        pid = int(entry_pid.get())
        # Получаем адрес как число (0 означает, что Python сам определит систему счисления, например, 0x для hex)
        address = int(entry_address.get(), 0)
        # Получаем длину как число
        length = int(entry_length.get())

        # --- ИСПРАВЛЕНО: Открываем процесс по PID ---
        # Оборачиваем открытие процесса и запись в память в еще один try-except
        try:
            # Создаем объект Pymem для работы с процессом
            pm = pymem.Pymem(pid)
            
            # Создаем последовательность байтов для записи (в данном случае - точки)
            # b'.' создает байтовую строку, а не обычную. Это важно для write_bytes.
            bytes_to_write = b'.' * length
            
            # --- ИСПРАВЛЕНО: Записываем байты в память ---
            pm.write_bytes(address, bytes_to_write, length)
            
            # Выводим сообщение об успехе в GUI
            success_message = f"Successfully wrote {length} bytes to 0x{address:X} in PID {pid}"
            print(success_message) # Также выводим в консоль
            status_label.configure(text=success_message, text_color="green")

        except pymem.exception.ProcessNotFound:
            error_msg = f"Error: Process with PID {pid} not found."
            print(error_msg)
            status_label.configure(text=error_msg, text_color="red")
        except pymem.exception.CouldNotOpenProcess:
            error_msg = f"Error: Could not open process {pid}. Try running script as Administrator."
            print(error_msg)
            status_label.configure(text=error_msg, text_color="red")
        except Exception as e:
            # Ловим другие возможные ошибки (например, неправильный адрес, нет доступа к памяти)
            error_msg = f"An error occurred: {e}"
            print(error_msg)
            status_label.configure(text=error_msg, text_color="red")

    except ValueError:
        # Эта ошибка возникнет, если в поля ввели не числа
        error_msg = "Error: PID, Address and Length must be valid numbers."
        print(error_msg)
        status_label.configure(text=error_msg, text_color="red")


button = customtkinter.CTkButton(master=app,
                                 width=150,
                                 height=32,
                                 border_width=0,
                                 corner_radius=8,
                                 fg_color="#FF0000",
                                 hover_color="#6A6767",
                                 text="Overwrite Memory",
                                 command=button_event) # Привязываем нашу функцию к кнопке
button.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)

# Метка для вывода статуса операции (успех/ошибка)
status_label = customtkinter.CTkLabel(master=app, text="", font=("Arial", 12))
status_label.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

app.mainloop()
