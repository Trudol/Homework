import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QColor, QIcon
from PyQt5 import uic
from random import randint


class CycleDrawer(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI.ui", self)
        self.pushButton.clicked.connect(self.paint)
        self.setWindowIcon(QIcon("my_icon.png"))
        self.do_paint = False

    def paint(self):
        self.do_paint = True
        self.repaint()

    def paintEvent(self, event):
        if self.do_paint:
            # Создаем объект QPainter для рисования
            qp = QPainter()
            # Начинаем процесс рисования
            qp.begin(self)
            self.draw_cycle(qp)
            # Завершаем рисование
            qp.end()
            self.do_paint = False

    def draw_cycle(self, qp):
        # Задаем кисть
        # color = randint(0, 0xFFFFFF)
        color = "yellow"
        qp.setBrush(QColor(color))
        r = randint(1, 600)
        qp.drawEllipse(0, 0, r, r)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = CycleDrawer()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
