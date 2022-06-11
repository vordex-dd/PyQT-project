import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from OpenNewAddRoute import OpenNew_addroute
from OpenNewFindData import OpenNew_finddata
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.bought_places = [[], [], []]
        # Подключение к БД
        con = sqlite3.connect('fly.db')

        # Создание курсора
        cur = con.cursor()

        # Выполнение запроса и получение всех результатов
        result = cur.execute("""SELECT * FROM cities""").fetchall()

        self.spic_cities = []
        for elem in result:
            self.spic_cities.append((elem[0], f'{elem[1]} ({elem[2]})'))
        self.initUI()

    def initUI(self):
        uic.loadUi('mainmenu.ui', self)
        self.ex.clicked.connect(self.end)
        self.new_route.clicked.connect(self.new_r)
        self.buy.clicked.connect(self.tickets)

    def end(self):
        exit()

    def new_r(self):
        self.open_new1 = OpenNew_addroute(self.spic_cities)
        self.open_new1.show()

    def tickets(self):
        self.open_new2 = OpenNew_finddata(self.spic_cities)
        self.open_new2.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
