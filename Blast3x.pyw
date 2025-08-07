from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPoint
import pymem
import pymem.process
import sys # <-- Добавил импорт sys

# --- Ваша функция выхода, но лучше использовать self.close() ---
def close_app():
    sys.exit(0)

class Ui_Dialog(QtWidgets.QDialog):
    def setupUi(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setObjectName("Dialog")
        # Увеличим размер окна для метки статуса
        self.resize(500, 210)
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(10, 10, 481, 191)) # Увеличим высоту
        self.frame.setStyleSheet("QFrame { \n"
                                 "background-color: rgb(25, 25, 25);\n"
                                 "border-radius: 15px;\n"
                                 "}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(440, 0, 41, 31))
        self.pushButton.setStyleSheet("background-color: rgb(25, 25, 25);\n"
                                      "border-radius: 15px;\n"
                                      "")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        # Используем встроенный метод self.close() для закрытия окна
        self.pushButton.clicked.connect(self.close)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(460, 10, 47, 13))
        self.label.setStyleSheet("color: white;")
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(10, 40, 461, 30))
        self.lineEdit.setStyleSheet("QLineEdit {\n"
                                    "    background-color: rgb(28, 28, 28);\n"
                                    "    border-radius: 5px;\n"
                                    "    border: 2px solid rgb(27, 29, 35);\n"
                                    "    padding-left: 10px;\n"
                                    "    color: white;\n"
                                    "    border: 2px solid rgb(255, 59, 59);\n"
                                    "}")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_2.setGeometry(QtCore.QRect(10, 80, 461, 30))
        self.lineEdit_2.setStyleSheet("QLineEdit {\n"
                                      "    background-color: rgb(28, 28, 28);\n"
                                      "    border-radius: 5px;\n"
                                      "    border: 2px solid rgb(27, 29, 35);\n"
                                      "    padding-left: 10px;\n"
                                      "    color: white;\n"
                                      "    border: 2px solid rgb(255, 59, 59);\n"
                                      "}")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_3.setGeometry(QtCore.QRect(10, 120, 301, 30))
        self.lineEdit_3.setStyleSheet("QLineEdit {\n"
                                      "    background-color: rgb(28, 28, 28);\n"
                                      "    border-radius: 5px;\n"
                                      "    border: 2px solid rgb(27, 29, 35);\n"
                                      "    padding-left: 10px;\n"
                                      "    color: white;\n"
                                      "    border: 2px solid rgb(255, 59, 59);\n"
                                      "}")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(320, 120, 150, 30))
        self.pushButton_2.setStyleSheet("QPushButton {\n"
                                        "    border-radius: 10px;    \n"
                                        "    background-color: rgb(255, 59, 59);\n"
                                        "    color: white;\n"
                                        "}\n"
                                        "QPushButton:hover {\n"
                                        "    background-color: rgb(219, 55, 55);\n"
                                        "}\n"
                                        "QPushButton:pressed {    \n"
                                        "    background-color: rgb(255, 59, 59);\n"
                                        "}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(20, 10, 271, 16))
        self.label_2.setStyleSheet("color: white;")
        self.label_2.setObjectName("label_2")

        # <<< ДОБАВЛЕНО: Метка для вывода статуса
        self.status_label = QtWidgets.QLabel(self.frame)
        self.status_label.setGeometry(QtCore.QRect(10, 160, 461, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.status_label.setFont(font)
        self.status_label.setStyleSheet("color: white;")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setObjectName("status_label")

        self.pushButton_2.clicked.connect(self.remove)
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("String Remover", "String Remover"))
        self.label.setText(_translate("Dialog", "X"))
        self.lineEdit.setPlaceholderText(_translate("Dialog", "Process ID (PID)"))
        self.lineEdit_2.setPlaceholderText(_translate("Dialog", "Memory Address (e.g., 0x140AC30)"))
        self.lineEdit_3.setPlaceholderText(_translate("Dialog", "Length (number of bytes to clear)"))
        self.pushButton_2.setText(_translate("Dialog", "Remove"))
        self.label_2.setText(_translate("Dialog", "String Remover v1.0 [Author: @bush1root]"))
        self.status_label.setText(_translate("Dialog", "")) # Статус по умолчанию пустой

    # <<< ИСПРАВЛЕНО: Полностью переписанная функция
    def remove(self):
        try:
            pid = int(self.lineEdit.text())
            address = int(self.lineEdit_2.text(), 0) # base=0 для поддержки hex (0x...)
            length = int(self.lineEdit_3.text())

            if length <= 0:
                self.status_label.setStyleSheet("color: yellow;")
                self.status_label.setText("Length must be a positive number.")
                return

            # Открываем процесс
            pm = pymem.Pymem(pid)

            # Создаем правильную последовательность байт для затирания
            null_bytes = b'\x00' * length

            # ИСПОЛЬЗУЕМ ПРАВИЛЬНУЮ ФУНКЦИЮ: write_bytes
            pm.write_bytes(address, null_bytes, length)
            
            # Сообщаем об успехе
            self.status_label.setStyleSheet("color: #00FF00;") # Зеленый
            self.status_label.setText(f"Success! Wrote {length} null bytes to {hex(address)}.")

        # ДОБАВЛЕНА ПРАВИЛЬНАЯ ОБРАБОТКА ОШИБОК
        except pymem.exception.ProcessNotFound:
            self.status_label.setStyleSheet("color: #FF5733;") # Оранжевый
            self.status_label.setText(f"Error: Process with PID '{self.lineEdit.text()}' not found.")
        except pymem.exception.MemoryWriteError:
            self.status_label.setStyleSheet("color: #FF0000;") # Красный
            self.status_label.setText("Memory Write Error. RUN AS ADMINISTRATOR!")
        except ValueError:
            self.status_label.setStyleSheet("color: #FF5733;") # Оранжевый
            self.status_label.setText("Error: PID, Address, and Length must be valid numbers.")
        except Exception as e:
            self.status_label.setStyleSheet("color: #FF0000;") # Красный
            self.status_label.setText(f"An unexpected error occurred: {e}")

    # --- Функции для перетаскивания окна ---
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Dialog()
    ui.setupUi()
    ui.show()
    sys.exit(app.exec_())
