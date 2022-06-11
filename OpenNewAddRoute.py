from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
import sqlite3


class OpenNew_addroute(QMainWindow):
    def __init__(self, cities):
        super().__init__()
        self.spic_cities = []
        self.id_of_cities = {}
        self.id_of_cities_reverse = {}
        self.times = ''
        for i in cities:
            self.id_of_cities[i[0]] = i[1]
            self.id_of_cities_reverse[i[1]] = i[0]
            self.spic_cities.append(i[1])
        self.initUI()

    def initUI(self):
        uic.loadUi('newroute.ui', self)
        self.spic_cities.sort()
        for city in self.spic_cities:
            self.depart.addItem(city)
            self.arrival.addItem(city)
        self.flag1 = False  # заводим флаги, чтобы уметь вывести возникающую ошибку
        self.flag2 = False  # и следить за тем, введены ли правльные данные
        self.flag3 = False
        self.information.clicked.connect(self.inf)
        self.to_database.clicked.connect(self.add_base)

    def fr(self):
        departure = self.depart.currentText()
        if not departure:  # обработка ошибок
            self.listWidget.addItem('Ошибка с городом отправления')
            return False
        else:
            self.listWidget.clear()
            return True

    def to(self):
        arrival = self.arrival.currentText()
        if not arrival:  # обработка ошибок
            self.listWidget.addItem('Ошибка с местом прибытия')
            return False
        else:
            self.listWidget.clear()
            return True

    def cost_ticket(self):
        try:
            cost = int(self.cost.toPlainText())
            if cost <= 0:  # обработка ошибок
                self.listWidget.addItem('Неправильная цена билета!')
                return False
            else:
                self.listWidget.clear()
                return True
        except ValueError:
            self.listWidget.addItem('Неправильная цена билета!')

    def inf(self):
        self.listWidget.clear()
        self.flag1 = self.fr()
        self.flag2 = self.to()
        self.flag3 = self.cost_ticket()
        if self.flag1 and self.flag2 and self.flag3 and self.depart.currentText() != self.arrival.currentText():
            departure = self.depart.currentText()
            arrival = self.arrival.currentText()
            cost = int(self.cost.toPlainText())
            hour, minute = self.time.time().hour(), self.time.time().minute()
            self.times = str(hour) if hour >= 10 else '0' + str(hour)
            self.times += ':'
            self.times += str(minute) if minute >= 10 else '0' + str(minute)
            self.listWidget.addItem(f"Детали нового авиаперелета:"
                                    f"\nВремя вылета: {self.times}\n"
                                    f"Дата: {self.calendar.selectedDate().year()}-"
                                    f"{self.calendar.selectedDate().month()}-"
                                    f"{self.calendar.selectedDate().day()}  "
                                    "\n"
                                    f"Из {departure} "
                                    f"в {arrival}, "
                                    f"цена билета - {cost}₽")
        else:
            if self.depart.currentText() == self.arrival.currentText():
                self.listWidget.addItem('Место прибытия должно отличаться от места отправления!')

    def add_base(self):
        self.listWidget.clear()
        self.flag1 = self.fr()
        self.flag2 = self.to()
        self.flag3 = self.cost_ticket()
        if self.depart.currentText() == self.arrival.currentText():
            self.listWidget.addItem('Место прибытия должно отличаться от места отправления!')
        elif self.flag1 and self.flag2 and self.flag3:
            self.it_err.setText('')
            hours = str(self.time.time().hour())
            minutes = str(self.time.time().minute())
            year = str(self.calendar.selectedDate().year())
            month = str(self.calendar.selectedDate().month())
            day = str(self.calendar.selectedDate().day())
            depart_it = str(self.depart.currentText())
            arrive_it = str(self.arrival.currentText())
            cost_it = str(self.cost.toPlainText())  # сохрним все данные авиаперелета в бд
            self.saveData(depart_it, arrive_it, year, month, day, cost_it)

    def saveData(self, *spic):  # сохранения данных в бд
        # Подключение к БД
        depart_it, arrive_it, year, month, day, cost_it = spic
        start = self.id_of_cities_reverse[depart_it]
        finish = self.id_of_cities_reverse[arrive_it]
        time = self.times
        date = f'{year}-{month}-{day}'
        con = sqlite3.connect('fly.db')

        # Создание курсора
        cur = con.cursor()
        cur.execute("""INSERT INTO flights VALUES(?, ?, ?, ?, ?, ?)""", (start,
                                                                      finish,
                                                                      time,
                                                                      date,
                                                                      int(cost_it), 'all'))
        con.commit()
        self.close()