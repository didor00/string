import pymem
import customtkinter
import tkinter
import tkinter.messagebox as messagebox
import sys

# Устанавливаем яркую цветовую схему
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.configure(bg="#f0f0f0")  # Светло-серый фон
app.geometry("800x400")  # Немного увеличим размер окна
app.title("STRING CLEANER | GITHUB.COM/BLAST3X")

# Яркий заголовок
title_frame = customtkinter.CTkFrame(master=app, fg_color="#4e8cff", corner_radius=10)
title_frame.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER, relwidth=0.9, height=50)

label = customtkinter.CTkLabel(master=title_frame, 
                               text="STRING CLEANER BY GITHUB.COM/BLAST3X", 
                               text_color="#ffffff",  # Белый текст
                               font=("Arial", 16, "bold"))
label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# Контейнер для полей ввода
input_frame = customtkinter.CTkFrame(master=app, fg_color="#ffffff", corner_radius=15)
input_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER, relwidth=0.8, relheight=0.6)

# Поле для ввода PID процесса
entry_pid = customtkinter.CTkEntry(master=input_frame,
                                  placeholder_text="Process PID",
                                  width=200,
                                  height=35,
                                  border_width=2,
                                  corner_radius=10,
                                  fg_color="#f8f8f8",
                                  text_color="#333333",
                                  placeholder_text_color="#888888")
entry_pid.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

# Поле для ввода адреса памяти
entry_address = customtkinter.CTkEntry(master=input_frame,
                                      placeholder_text="Memory address (hex, e.g., 0x7FFE0000)",
                                      width=200,
                                      height=35,
                                      border_width=2,
                                      corner_radius=10,
                                      fg_color="#f8f8f8",
                                      text_color="#333333",
                                      placeholder_text_color="#888888")
entry_address.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

# Поле для ввода длины строки
entry_length = customtkinter.CTkEntry(master=input_frame,
                                     placeholder_text="String length",
                                     width=200,
                                     height=35,
                                     border_width=2,
                                     corner_radius=10,
                                     fg_color="#f8f8f8",
                                     text_color="#333333",
                                     placeholder_text_color="#888888")
entry_length.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

def button_event():
    try:
        # Получаем PID процесса
        pid = int(entry_pid.get().strip())
        
        # Получаем адрес памяти
        address_str = entry_address.get().strip()
        if address_str.startswith("0x"):
            address = int(address_str, 16)
        else:
            address = int(address_str, 16)
        
        # Получаем длину строки
        length = int(entry_length.get().strip())
        
        # Создаём строку из точек
        dot_string = '.' * length
        dot_bytes = dot_string.encode('ascii')
        
        # Открываем процесс по PID
        pm = pymem.Pymem()
        pm.open_process_from_id(pid)
        
        # Записываем точки в память
        pm.write_bytes(address, dot_bytes, length)
        
        # Показываем сообщение об успехе
        messagebox.showinfo("Success", 
                           f"Replaced {length} bytes with dots at address 0x{address:X}\n"
                           f"Process PID: {pid}")
        
    except pymem.exception.ProcessNotFound:
        messagebox.showerror("Error", "Process not found! Check PID.")
    except pymem.exception.ProcessError:
        messagebox.showerror("Error", "Access denied. Run as administrator!")
    except ValueError as ve:
        messagebox.showerror("Input Error", f"Invalid input: {str(ve)}")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {str(e)}")
    finally:
        # Закрываем процесс, если был открыт
        if 'pm' in locals() and pm.process_handle:
            pm.close_process()

# Яркая кнопка с градиентом
button = customtkinter.CTkButton(master=input_frame,
                                 width=220,
                                 height=45,
                                 border_width=0,
                                 corner_radius=12,
                                 fg_color="#ff6b6b",  # Яркий красный
                                 hover_color="#ff8e8e",  # Светлее при наведении
                                 text="REMOVE STRING",
                                 font=("Arial", 14, "bold"),
                                 text_color="#ffffff",  # Белый текст
                                 command=button_event)
button.place(relx=0.5, rely=0.85, anchor=tkinter.CENTER)

# Кнопка для выхода
def exit_app():
    app.destroy()
    sys.exit()

exit_button = customtkinter.CTkButton(master=app,
                                     width=100,
                                     height=35,
                                     text="EXIT",
                                     fg_color="#ff9800",  # Оранжевый
                                     hover_color="#ffb74d",
                                     font=("Arial", 12, "bold"),
                                     text_color="#ffffff",
                                     command=exit_app)
exit_button.place(relx=0.95, rely=0.05, anchor=tkinter.CENTER)

# Статус бар внизу
status_bar = customtkinter.CTkLabel(master=app, 
                                   text="Ready", 
                                   fg_color="#4e8cff",  # Синий
                                   text_color="#ffffff",
                                   corner_radius=0,
                                   height=25)
status_bar.place(relx=0.5, rely=0.95, anchor=tkinter.CENTER, relwidth=1.0)

app.mainloop()
