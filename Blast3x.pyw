import pymem
import pymem.process
import customtkinter
import tkinter

# --- Настройка окна ---
customtkinter.set_appearance_mode("light")  # Светлая тема для "тяночного" стиля
app = customtkinter.CTk()
app.configure(bg="#FFF0F5")  # Резервный светло-розовый фон
app.geometry("700x400")  # Сделал окно чуть выше для статус-бара
app.title("spastil DarkFred     |     THIS TOOL IS FREE")

# --- Установка фона с изображением ---
def set_background(image_path):
    try:
        from PIL import Image, ImageTk
        import os
        if os.path.exists(image_path):
            img = Image.open(image_path)
            img = img.resize((700, 400), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            bg_label = tkinter.Label(app, image=photo)
            bg_label.image = photo  # Сохраняем ссылку
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            print(f"Изображение не найдено по пути: {image_path}")
    except Exception as e:
        print(f"Ошибка загрузки фона: {e}")

# Укажите путь к изображению "тяночки" (замените на свой файл)
background_image = "C:/Users/yaric/tyanochka.png"  # Замените на реальный путь!
set_background(background_image)

# --- Элементы интерфейса ---
label_title = customtkinter.CTkLabel(master=app, text="spastil DarkFred", text_color="#FF69B4", font=("Arial", 20))
label_title.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

entry_pid = customtkinter.CTkEntry(master=app,
                                   placeholder_text="PID процесса",
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

# Логика кнопки
def button_event():
    try:
        pid = int(entry_pid.get())  # Конвертируем PID в число
        address = int(entry_address.get(), 0)  # 0 позволяет вводить hex (0x...)
        length = int(entry_length.get())  # Длина как десятичное число
    except ValueError:
        status_label.configure(text="Ошибка: PID и длина должны быть числами.", text_color="orange")
        return

    try:
        pm = pymem.Pymem(pid)
        status_label.configure(text=f"Процесс '{pm.process_name}' (PID: {pid}) найден.", text_color="cyan")
        app.update_idletasks()

        # Готовим данные для записи
        replacement_bytes = b'.' * length
        
        # Перезаписываем память
        pm.write_bytes(address, replacement_bytes, length)
        
        # Читаем обратно для проверки с обработкой некорректных данных
        read_buffer = pm.read_bytes(address, length)
        current_string = read_buffer.decode('ascii', errors='replace').replace('\x00', '.')  # Убираем знаки вопроса
        status_label.configure(text=f"УСПЕХ! {length} байт по адресу {hex(address)} перезаписано. Текущее: {current_string}", text_color="green")

    except pymem.exception.ProcessNotFound:
        status_label.configure(text=f"Ошибка: Процесс с PID {pid} не найден.", text_color="red")
    except pymem.exception.MemoryWriteError:
        status_label.configure(text=f"Ошибка: Не удалось записать в память. Адрес защищен?", text_color="red")
    except Exception as e:
        status_label.configure(text=f"Неизвестная ошибка: {e}", text_color="red")

button = customtkinter.CTkButton(master=app,
                                 width=120,
                                 height=32,
                                 border_width=0,
                                 corner_radius=8,
                                 fg_color="#00CED1",
                                 hover_color="#87CEEB",
                                 text="Remove String",
                                 command=button_event)
button.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)

app.mainloop()
