import pymem
import customtkinter
import tkinter

# Устанавливаем стандартную темную тему
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue") # Опционально, для лучшего вида

app = customtkinter.CTk()
# app.configure(bg="black") # Это уже не нужно при установке темной темы
app.geometry("700x350") # Немного увеличим высоту для статусной строки
app.title("GITHUB.COM/BLAST3X     |     MEMORY STRING REMOVER (FREE TOOL)")

# --- ВИДЖЕТЫ ИНТЕРФЕЙСА ---

label = customtkinter.CTkLabel(master=app, text="MADE BY GITHUB.COM/BLAST3X", text_color="#FF0000", font=("Arial", 16, "bold"))
label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

entry = customtkinter.CTkEntry(master=app,
                               placeholder_text="process.exe",
                               width=150,
                               height=30,
                               border_width=2,
                               corner_radius=10)
entry.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

entry1 = customtkinter.CTkEntry(master=app,
                                placeholder_text="0xMemoryAddress",
                                width=150,
                                height=30,
                                border_width=2,
                                corner_radius=10)
entry1.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

entry2 = customtkinter.CTkEntry(master=app,
                                placeholder_text="length",
                                width=150,
                                height=30,
                                border_width=2,
                                corner_radius=10)
entry2.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

# Добавим метку для вывода статуса операции
status_label = customtkinter.CTkLabel(master=app, text="", text_color="yellow")
status_label.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)


# --- ОСНОВНАЯ ЛОГИКА ---

def button_event():
    """
    Функция, которая выполняется при нажатии на кнопку.
    Она подключается к процессу и записывает нули по указанному адресу.
    """
    try:
        proc_name = entry.get()
        # Проверяем, что все поля заполнены
        if not proc_name or not entry1.get() or not entry2.get():
            status_label.configure(text="Ошибка: Все поля должны быть заполнены.", text_color="orange")
            return

        # Получаем адрес и длину. int(..., 0) позволяет вводить как '123' так и '0x...'
        address = int(entry1.get(), 0)
        length = int(entry2.get(), 0) # Исправлена опечатка lenght -> length

        status_label.configure(text=f"Поиск процесса: {proc_name}...", text_color="yellow")
        app.update_idletasks() # Обновляем интерфейс, чтобы пользователь видел сообщение

        # Подключаемся к процессу, используя современный синтаксис pymem
        pm = pymem.Pymem(proc_name)

        # "Удаление" строки - это, по сути, перезапись её памяти.
        # Лучший способ - записать туда нулевые байты (b'\x00').
        payload = b'\x00' * length

        # Записываем байты в память процесса
        pm.write_bytes(address, payload, length)

        # Выводим сообщение об успехе
        status_label.configure(text=f"Успешно! {length} байт записано по адресу {hex(address)}", text_color="green")

    except pymem.exception.ProcessNotFound:
        status_label.configure(text=f"Ошибка: Процесс '{proc_name}' не найден.", text_color="red")
    except ValueError:
        status_label.configure(text="Ошибка: Неверный формат адреса или длины.", text_color="red")
    except Exception as e:
        # Отлавливаем другие возможные ошибки (например, отказ в доступе)
        status_label.configure(text=f"Произошла ошибка: {e}", text_color="red")


button = customtkinter.CTkButton(master=app,
                                 width=150,
                                 height=40,
                                 border_width=0,
                                 corner_radius=8,
                                 fg_color="#FF0000",
                                 hover_color="#C00000",
                                 text="Remove String",
                                 font=("Arial", 14, "bold"),
                                 command=button_event)

button.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)
app.mainloop()

