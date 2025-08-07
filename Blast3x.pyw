import pymem
import customtkinter
import tkinter

customtkinter.set_appearance_mode("Dark")

app = customtkinter.CTk()
app.geometry("700x400")
app.title("GITHUB.COM/BLAST3X | THIS TOOL IS FREE")
app.resizable(False, False)

# Метка вверху
label_top = customtkinter.CTkLabel(master=app, text="MADE BY GITHUB.COM/BLAST3X", text_color="#FF0000")
label_top.place(relx=0.5, rely=0.05, anchor=tkinter.CENTER)

# Метки для полей ввода
label_proc = customtkinter.CTkLabel(master=app, text="Process name (e.g., notepad.exe):", text_color="#FFFFFF")
label_proc.place(relx=0.3, rely=0.15, anchor=tkinter.E)

label_addr = customtkinter.CTkLabel(master=app, text="Memory address (hex, e.g., 0x10000000):", text_color="#FFFFFF")
label_addr.place(relx=0.3, rely=0.25, anchor=tkinter.E)

label_len = customtkinter.CTkLabel(master=app, text="Length (e.g., 10):", text_color="#FFFFFF")
label_len.place(relx=0.3, rely=0.35, anchor=tkinter.E)

# Поля ввода
entry_proc = customtkinter.CTkEntry(master=app, width=200, placeholder_text="notepad.exe")
entry_proc.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

entry_addr = customtkinter.CTkEntry(master=app, width=200, placeholder_text="0x10000000")
entry_addr.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

entry_len = customtkinter.CTkEntry(master=app, width=200, placeholder_text="10")
entry_len.place(relx=0.5, rely=0.35, anchor=tkinter.CENTER)

# Текстовое поле для результата
result_text = customtkinter.CTkTextbox(master=app, width=400, height=100)
result_text.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)

# Функция для кнопки
def button_event():
    process_name = entry_proc.get()
    address_str = entry_addr.get()
    length_str = entry_len.get()

    # Проверка корректности ввода
    try:
        address = int(address_str, 16)  # Преобразование hex-адреса
        length = int(length_str)        # Преобразование длины
        if length <= 0:
            raise ValueError("Length must be positive")
    except ValueError as e:
        result_text.delete("1.0", tkinter.END)
        result_text.insert("1.0", f"Error: Invalid address or length ({str(e)})")
        return

    # Работа с процессом
    try:
        pm = pymem.Pymem(process_name)  # Открытие процесса
        rs = pm.read_string(address, length)  # Чтение строки
        rb = pm.read_bytes(address, length)   # Чтение байтов
        result_text.delete("1.0", tkinter.END)
        result_text.insert("1.0", f"Read string: {rs}\nRead bytes: {rb}")
    except Exception as e:
        result_text.delete("1.0", tkinter.END)
        result_text.insert("1.0", f"Error: {str(e)}")

# Кнопка
button = customtkinter.CTkButton(master=app, 
                                width=120,
                                height=32,
                                border_width=0,
                                corner_radius=8,
                                fg_color="#FF0000",
                                hover_color="#6A6767",
                                text="Read Data",
                                command=button_event)
button.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

app.mainloop()
