import sys
import pymem
import pymem.exception
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPoint

class StringRemoverApp(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        # Инициализируем UI в конструкторе
        self.setupUi()
        # Центрируем окно при запуске
        self.center()
        # Сохраняем позицию для перетаскивания окна
        self.oldPos = self.pos()

    def setupUi(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setObjectName("StringRemover")
        self.resize(500, 183)

        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(10, 10, 481, 161))
        self.frame.setStyleSheet("""
            QFrame { 
                background-color: rgb(25, 25, 25);
                border-radius: 15px;
            }
        """)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)

        # Кнопка закрытия
        self.close_button = QtWidgets.QPushButton("X", self.frame)
        self.close_button.setGeometry(QtCore.QRect(440, 5, 31, 25))
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: rgb(255, 59, 59);
            }
        """)
        # Подключаем к встроенному слоту close()
        self.close_button.clicked.connect(self.close)

        # Поля для ввода (с более осмысленными именами)
        self.pid_input = QtWidgets.QLineEdit(self.frame)
        self.pid_input.setGeometry(QtCore.QRect(10, 40, 461, 30))
        self.pid_input.setPlaceholderText("PID процесса (напр. 1234 или 0x4D2)")

        self.address_input = QtWidgets.QLineEdit(self.frame)
        self.address_input.setGeometry(QtCore.QRect(10, 80, 461, 30))
        self.address_input.setPlaceholderText("Адрес строки (в hex, напр. 0x1A2B3C)")

        self.length_input = QtWidgets.QLineEdit(self.frame)
        self.length_input.setGeometry(QtCore.QRect(10, 120, 301, 30))
        self.length_input.setPlaceholderText("Длина для очистки (в байтах)")

        # Стили для полей ввода
        line_edit_style = """
            QLineEdit {
                background-color: rgb(28, 28, 28);
                border-radius: 5px;
                padding-left: 10px;
                color: white;
                border: 2px solid rgb(60, 60, 60);
            }
            QLineEdit:focus {
                border: 2px solid rgb(255, 59, 59);
            }
        """
        self.pid_input.setStyleSheet(line_edit_style)
        self.address_input.setStyleSheet(line_edit_style)
        self.length_input.setStyleSheet(line_edit_style)
        
        # Кнопка действия
        self.remove_button = QtWidgets.QPushButton("Очистить память", self.frame)
        self.remove_button.setGeometry(QtCore.QRect(320, 120, 150, 30))
        self.remove_button.setMinimumSize(QtCore.QSize(150, 30))
        self.remove_button.setFont(QtGui.QFont("Segoe UI", 9))
        self.remove_button.setStyleSheet("""
            QPushButton {
                border-radius: 10px;    
                background-color: rgb(255, 59, 59);
                color: white;
            }
            QPushButton:hover {
                background-color: rgb(219, 55, 55);
            }
            QPushButton:pressed {    
                background-color: rgb(180, 40, 40);
            }
        """)
        self.remove_button.clicked.connect(self.remove_string_from_memory)

        # Заголовок
        self.title_label = QtWidgets.QLabel("String Remover v1.1 [Author: @bush1root]", self.frame)
        self.title_label.setGeometry(QtCore.QRect(20, 10, 271, 16))
        self.title_label.setStyleSheet("color: #AAAAAA;")

    def center(self):
        # Современный способ центрирования окна
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def remove_string_from_memory(self):
        """
        Основная логика очистки памяти с правильной обработкой ошибок.
        """
        try:
            # Получаем значения из полей, база 0 позволяет вводить hex (0x...) и dec
            pid = int(self.pid_input.text(), 0)
            address = int(self.address_input.text(), 0)
            length = int(self.length_input.text(), 0)

            if length <= 0:
                print("Ошибка: Длина должна быть положительным числом.")
                return

            print(f"Попытка подключения к процессу PID: {pid}...")

            # Используем менеджер контекста для автоматического закрытия процесса
            with pymem.Pymem(pid) as pm:
                print(f"Подключение к процессу {pm.process_id} успешно.")
                
                # Создаем массив нулевых байтов нужной длины
                null_bytes = b'\x00' * length
                
                print(f"Запись {length} нулевых байтов по адресу 0x{address:X}...")
                
                # Используем write_bytes для записи
                pm.write_bytes(address, null_bytes, length)
                
                print("Готово! Память успешно очищена.")

        except ValueError:
            print("Ошибка: Неверный формат PID, адреса или длины. Убедитесь, что это целые числа.")
        except pymem.exception.ProcessNotFound:
            print(f"Ошибка: Процесс с PID {self.pid_input.text()} не найден.")
        except pymem.exception.CouldNotOpenProcess:
            print(f"Ошибка: Не удалось открыть процесс. Попробуйте запустить скрипт от имени администратора.")
        except pymem.exception.CouldNotWriteMemory:
            print(f"Ошибка: Не удалось записать данные в память по адресу {self.address_input.text()}. Возможно, адрес защищен.")
        except Exception as e:
            # Ловим все остальные возможные ошибки
            print(f"Произошла непредвиденная ошибка: {e}")

    # --- Функции для перетаскивания окна без рамки ---
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()


if __name__ == "__main__":
    # Убедимся, что приложение правильно масштабируется на разных экранах
    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QtWidgets.QApplication(sys.argv)
    window = StringRemoverApp()
    window.show()
    sys.exit(app.exec_())
