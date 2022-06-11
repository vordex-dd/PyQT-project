from PyQt5.QtWidgets import QMainWindow
# import copy
from PyQt5 import uic
# import time
from PassengersDetails import Passengers_details
import sqlite3


class OpenNew_finddata(QMainWindow):
    def __init__(self, cities):
        super().__init__()
        self.gl_moths = {1: 'Январь',
                         2: "Февраль",
                         3: "Март",
                         4: "Апрель",
                         5: "Май",
                         6: "Июнь",
                         7: 'Июль',
                         8: "Август",
                         9: "Сентябрь",
                         10: "Октябрь",
                         11: "Ноябрь",
                         12: "Декабрь"
                         }
        self.gl_moths_reverse = {}
        for i in list(self.gl_moths.keys()):
            self.gl_moths_reverse[self.gl_moths[i]] = i
        self.flights = []
        self.spic_cities = []
        self.id_of_cities = {}  # id - name
        self.id_of_cities_reverse = {}  # name - id
        self.actual = []  # информация о вылете из определенного города
        self.departure, self.arrive, self.months, self.days, self.times = '', '', '', '', ''
        self.date, self.money = '', ''
        self.sid = ''
        for i in cities:
            self.id_of_cities[i[0]] = i[1]
            self.id_of_cities_reverse[i[1]] = i[0]
        self.error = False  # возможен ли маршрут
        self.initUI()

    def initUI(self):
        uic.loadUi('buytickets.ui', self)
        self.choose.clicked.connect(self.add_data)

        con = sqlite3.connect('fly.db')

        # Создание курсора
        cur = con.cursor()

        # Выполнение запроса и получение всех результатов
        result = cur.execute("""SELECT * FROM flights""").fetchall()
        for i in result:
            self.flights.append([self.id_of_cities[i[0]], self.id_of_cities[i[1]], *i[2:]])
            self.spic_cities.append(self.id_of_cities[i[0]])
        self.spic_cities = list(set(self.spic_cities))
        self.spic_cities.sort()
        for city in self.spic_cities:
            self.depart.addItem(city)
        self.year.addItem('2021')
        self.month.addItem('-')
        self.day.addItem('-')
        self.depart.activated.connect(self.restart)
        self.month.activated.connect(self.restart_date_day)
        self.arrival.activated.connect(self.restart_date_month)
        self.day.activated.connect(self.restart_time)
        self.restart()

    def restart(self):
        # обновление информации, в зависимомти от точки вылета
        self.actual.clear()
        self.arrival.clear()
        self.departure = self.depart.currentText()
        c = 0
        for i in filter(lambda x: x[0] == self.departure, self.flights):
            self.actual.append(i[1])
            c += 1
        if c == 0:
            self.error = True
            self.arrival.addItem('Из данного города нету рейсов')
        else:
            self.error = False
            self.actual = list(set(self.actual))
            self.actual.sort()
            for i in self.actual:
                self.arrival.addItem(i)
            self.restart_date_month()

    def restart_date_month(self):
        # обновление даты в зависимости от точки вылета
        month = []
        self.arrive = self.arrival.currentText()
        if not self.error:
            self.month.clear()
            for i in filter(lambda x: x[0] == self.departure and x[1] == self.arrive, self.flights):
                month.append(i[3].split('-')[1])
            month = list(set(month))
            month.sort()
            for i in month:
                self.month.addItem(self.gl_moths[int(i)])
            self.restart_date_day()

    def restart_date_day(self):
        if not self.error:
            self.day.clear()
            self.months = self.gl_moths_reverse[self.month.currentText()]
            days = []
            for i in filter(lambda x: x[0] == self.departure and x[1] == self.arrive
                                      and '-' + str(self.months) + '-' in x[3], self.flights):
                days.append(int(i[3].split('-')[2]))
            days = list(set(days))
            days.sort()
            for i in days:
                self.day.addItem(str(i))
            self.restart_time()

    def restart_time(self):
        if not self.error:
            self.time.clear()
            self.days = self.day.currentText()
            times = []
            self.date = f'2021-{self.months}-{self.days}'
            for i in filter(lambda x: x[0] == self.departure and
                                      x[1] == self.arrive and x[3] == self.date,
                            self.flights):
                times.append(i[2])
            for i in times:
                self.time.addItem(i)
            self.restart_money()

    def restart_money(self):
        if not self.error:
            self.price.clear()
            self.times = self.time.currentText()
            pr = 0
            for i in filter(lambda x: x[0] == self.departure and
                                      x[1] == self.arrive and x[3] == self.date and
                                      x[2] == self.times,
                            self.flights):
                pr = i[4]
                self.sid = i[-1]
            self.price.setText(f'{pr}₽')
            self.money = pr

    def add_data(self):
        if not self.error:
            spic = [self.departure, self.arrive, self.date, self.times, self.money, self.sid]
            self.open_new3 = Passengers_details(*spic)
            self.open_new3.show()
            self.close()
