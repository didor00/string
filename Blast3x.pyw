import pymem
import pymem.process
import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter as tk
import os

# --- Настройка окна ---
ctk.set_appearance_mode("light")  # Светлая тема для "тяночного" стиля
app = ctk.CTk()
app.geometry("700x400")
app.title("spastil DarkFred | THIS TOOL IS FREE")

# --- Установка фона с изображением ---
def set_background(image_path):
    try:
        if os.path.exists(image_path):
            img = Image.open(image_path)
            img = img.resize((700, 400), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            bg_label = tk.Label(app, image=photo)
            bg_label.image = photo  # Сохраняем ссылку
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            print(f"Изображение не найдено по пути: {image_path}")
            app.configure(bg="#FFF0F5")  # Резервный светло-розовый фон
    except Exception as e:
        print(f"Ошибка загрузки фона: {e}")
        app.configure(bg="#FFF0F5")  # Резервный фон при ошибке

# Укажите путь к изображению "тяночки" (замените на свой файл)
# Пример: замените на "C:/Users/yaric/tyanochka.png"
background_image = "C:/Users/yaric/tyanochka.png"  # Укажите реальный путь!
set_background(background_image)

# --- Элементы интерфейса ---
label_title = ctk.CTkLabel(master=app, text="spastil DarkFred", text_color="#FF69B4", font=("Arial", 20))
label_title.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

entry_pid = ctk.CTkEntry(master=app, placeholder_text="PID процесса", width=150, height=30, border_width=2, corner_radius=10)
entry_pid.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

entry_address = ctk.CTkEntry(master=app, placeholder_text="Адрес в памяти (напр. 0x123ABC)", width=150, height=30, border_width=2, corner_radius=10)
entry_address.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

entry_length = ctk.CTkEntry(master=app, placeholder_text="Длина для перезаписи", width=150, height=30, border_width=2, corner_radius=10)
entry_length.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

status_label = ctk.CTkLabel(master=app, text="Статус: ожидание ввода (04:31 PM EEST, Aug 07, 2025)", text_color="grey")
status_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

# --- Логика кнопки ---
def button_event():
    try:
        pid = int(entry_pid.get())
        address = int(entry_address.get(), 16)  # Явно шестнадцатеричный формат
        length = int(entry_length.get())
    except ValueError:
        status_label.configure(text="Ошибка: PID и длина должны быть числами.", text_color="orange")
        return

    try:
        pm = pymem.Pymem(pid)
        status_label.configure(text=f"Процесс '{pm.process_name}' (PID: {pid}) найден.", text_color="cyan")
        app.update_idletasks()

        replacement_bytes = b'.' * length
        pm.write_bytes(address, replacement_bytes, length)
        
        read_buffer = pm.read_bytes(address, length)
        current_string = read_buffer.decode('ascii', errors='replace').replace('\x00', '.')  # Обработка некорректных байтов
        status_label.configure(text=f"УСПЕХ! {length} байт по адресу {hex(address)} перезаписано. Текущее: {current_string}", text_color="green")

    except pymem.exception.ProcessNotFound:
        status_label.configure(text=f"Ошибка: Процесс с PID {pid} не найден.", text_color="red")
    except pymem.exception.MemoryWriteError:
        status_label.configure(text=f"Ошибка: Не удалось записать в память. Адрес защищен?", text_color="red")
    except Exception as e:
        status_label.configure(text=f"Неизвестная ошибка: {e}", text_color="red")

button = ctk.CTkButton(master=app, width=120, height=32, border_width=0, corner_radius=8, fg_color="#00CED1", hover_color="#87CEEB", text="Remove String", command=button_event)
button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

app.mainloop()
