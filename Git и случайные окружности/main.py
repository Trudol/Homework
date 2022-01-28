import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtGui import QPainter, QColor, QIcon
from random import randint


class CycleDrawer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 300, 800, 600)
        self.setWindowIcon(QIcon("my_icon.png"))
        self.setWindowTitle("Git и случайные окружности")

        self.pushButton = QPushButton(self)
        self.pushButton.setGeometry(320, 245, 160, 110)
        self.pushButton.setText("Создать\nокружность")
        self.pushButton.setStyleSheet('font: 16pt "Segoe Print";\nbackground-color:'
                                      ' rgb(245, 194, 10);')
        self.pushButton.clicked.connect(self.paint)

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
        color = randint(0, 0xFFFFFF)
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
