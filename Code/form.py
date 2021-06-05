import json
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap
import interface
from recognizer import Executor

class Window(QtWidgets.QMainWindow, interface.Ui_MainWindow):

    # Инициация формы и подключение функций к событиям
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.work = False

        self.startButt.clicked.connect(self.start)
        self.stopButt.clicked.connect(self.stop)
        self.quickSlot1.clicked.connect(lambda checked, i=1, text_box=self.quick_slot_path1: self.overview(text_box, i))
        self.quickSlot2.clicked.connect(lambda checked, i=2, text_box=self.quick_slot_path2: self.overview(text_box, i))
        self.quickSlot3.clicked.connect(lambda checked, i=3, text_box=self.quick_slot_path3: self.overview(text_box, i))

        with open('matrix.json', 'r', encoding='utf-8') as file:
            self.matrix = json.load(file)
        self.quick_slot_path1.setText(self.matrix[1][1])
        self.quick_slot_path2.setText(self.matrix[1][2])
        self.quick_slot_path3.setText(self.matrix[1][3])
        self.state_label.setPixmap(QPixmap('stop.png'))

    def start(self):
        if not self.work:
            self.state_label.setPixmap(QPixmap('play.png'))
            self.work = True
            self.executor = Executor(self.matrix)
            self.executor.start()

    def stop(self):
        if self.work:
            self.state_label.setPixmap(QPixmap('stop.png'))
            self.work = False
            self.executor.stop()

    def overview(self, text_box : QtWidgets.QLineEdit, i):
        name = QFileDialog. getOpenFileName(self, "Select Program", "", "*.exe")[0]
        text_box.setText('\"' + name + '\"')
        self.matrix[1][i] = text_box.text()

    def closeEvent(self, event):
        self.matrix[1][1] = self.quick_slot_path1.text()
        self.matrix[1][2] = self.quick_slot_path2.text()
        self.matrix[1][3] = self.quick_slot_path3.text()

        with open('matrix.json', 'w', encoding='utf-8') as file:
            json.dump(self.matrix, file, ensure_ascii=False)

        event.accept()

data = [
    ['2',	'0',	'0',	'0',	'explorer',	'notepad',	'control',	'3',	'0'],
    ['0',	'',	    '',	    '',	    '0',	    '0',	    '0',	    '0',	'0'],
    ['0',	'0',	'0',	'0',	'0',	    '0',	    '0',	    '0',	'taskmgr.exe']
]
# with open('matrix.json', 'w', encoding='utf-8') as file:
#     json.dump(data, file, ensure_ascii=False)

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = Window()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()