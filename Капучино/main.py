import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QIcon


class Change(QMainWindow):
    def __init__(self, con):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.setWindowIcon(QIcon("my_icon.png"))

        self.con = con
        self.pushButton.clicked.connect(self.show_cof)
        self.pushButton_2.clicked.connect(self.add_cof)
        self.pushButton_3.clicked.connect(self.del_cof)
        self.pushButton_4.clicked.connect(self.save_results)

        self.lines = (self.lineEdit, self.lineEdit_2, self.lineEdit_3, self.lineEdit_4,
                      self.lineEdit_5, self.lineEdit_6)
        self.colums = "Name", "Roast", "Grinding", "Description", "Price", "Volume"

    def show_cof(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute("SELECT * FROM coffees WHERE CoffeeId=?",
                             (item_id := self.spinBox.text(),)).fetchall()
        # Если запись не нашлась, то не будем ничего делать
        if not result:
            for line in self.lines:
                line.setText("")
            return
        # Заполнили таблицу полученными элементами
        [self.lines[i].setText(str(result[0][i + 1])) for i in range(6)]

    def add_cof(self):
        cur = self.con.cursor()
        cur.execute(f"INSERT INTO coffees{self.colums} "
                    f"VALUES{tuple([i.text() for i in self.lines])}")

    def save_results(self):
        cur = self.con.cursor()
        ids = [i[0] for i in cur.execute("SELECT CoffeeId from coffees").fetchall()]
        if int(self.spinBox.text()) not in ids:
            return
        cur.execute("UPDATE coffees SET %s WHERE CoffeeId=%d" % (
            ', '.join([f"{self.colums[i]}='{self.lines[i].text()}'" for i in range(6)]),
            int(self.spinBox.text())))
        self.con.commit()

    def del_cof(self):
        cur = self.con.cursor()
        cur.execute("DELETE from coffees WHERE CoffeeId=%d" % (int(self.spinBox.text())))
        d = cur.execute("SELECT CoffeeId from coffees").fetchall()[-1][0]
        for i in range(d + 2)[int(self.spinBox.text()) + 1:]:
            self.con.commit()
            print(i)
            cur.execute("UPDATE coffees SET CoffeeId=%d WHERE CoffeeId=%d" % (i - 1, i))
        self.con.commit()


class View(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setWindowIcon(QIcon("my_icon.png"))
        self.pushButton.clicked.connect(self.changer)

        self.connection = sqlite3.connect("coffee.sqlite")
        self.chngr = Change(self.connection)

        # Заполним размеры таблицы
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setWordWrap(True)
        self.table()

    def table(self):
        # Заполняем таблицу элементами
        res = self.connection.cursor().execute("SELECT * FROM coffees").fetchall()
        self.tableWidget.clear()
        for i, row in enumerate(res):
            if i > (self.tableWidget.rowCount() - 1):
                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def changer(self):
        self.chngr.show()
        self.table()

    def closeEvent(self, event):
        # При закрытии формы закроем и наше соединение
        # с базой данных
        self.connection.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = View()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
