import sqlite3

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic


class Chooseplace(QMainWindow):
    def __init__(self, *spic):
        super().__init__()
        self.spic = spic
        # print(*self.spic, sep='\n')
        self.closed_sid = []  # занятые места
        self.initUI()

    def initUI(self):
        uic.loadUi('first.ui', self)
        self.spic_seats = {"a1": self.seat_a1, "a2": self.seat_a2, "a3": self.seat_a3,
                           "a4": self.seat_a4, "a5": self.seat_a5, "a6": self.seat_a6,
                           "a7": self.seat_a7, "a8": self.seat_a8, "a9": self.seat_a9,
                           "a10": self.seat_a10, "a11": self.seat_a11, "c1": self.seat_c1,
                           "c2": self.seat_c2, "c3": self.seat_c3, "c4": self.seat_c4,
                           "c5": self.seat_c5, "c6": self.seat_c6, "c7": self.seat_c7,
                           "c8": self.seat_c8, "c9": self.seat_c9, "c10": self.seat_c10,
                           "c11": self.seat_c11, "d1": self.seat_d1, "d2": self.seat_d2,
                           "d3": self.seat_d3, "d4": self.seat_d4, "d5": self.seat_d5,
                           "d6": self.seat_d6, "d7": self.seat_d7, "d8": self.seat_d8,
                           "d9": self.seat_d9, "d10": self.seat_d10, "d11": self.seat_d11,
                           "e1": self.seat_e1, "e2": self.seat_e2, "e3": self.seat_e3,
                           "e4": self.seat_e4, "e5": self.seat_e5, "e6": self.seat_e6,
                           "e7": self.seat_e7, "e8": self.seat_e8, "e9": self.seat_e9,
                           "e10": self.seat_e10, "e11": self.seat_e11, "f1": self.seat_f1,
                           "f2": self.seat_f2, "f3": self.seat_f3, "f4": self.seat_f4,
                           "f5": self.seat_f5, "f6": self.seat_f6, "f7": self.seat_f7,
                           "f8": self.seat_f8, "f9": self.seat_f9, "f10": self.seat_f10, "f11": self.seat_f11}
        for i in list(self.spic_seats):
            self.spic_seats[i].clicked.connect(self.next)
        self.sid = self.spic[-1].split('-')
        string = 'QPushButton {color: #000000; border: 2px solid #908B81; ' \
                 'border-radius: 15px; border-style: outset; ' \
                 'background: ' \
                 'qradialgradient( cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4, ' \
                 'radius: 1, stop: 0 #BB0000, stop: 1 #DE0000); ' \
                 'padding: 7px;}'
        for i in self.sid:
            if i in self.spic_seats:
                self.closed_sid.append(i)
                self.spic_seats[i].setStyleSheet(string)

    def next(self):
        sring = self.sender().text().lower()
        if sring not in self.closed_sid:
            self.closed_sid.append(sring)
            con = sqlite3.connect('fly.db')

            # Создание курсора
            cur = con.cursor()

            # Выполнение запроса и получение всех результатов
            result = cur.execute("""SELECT * FROM cities""").fetchall()

            self.spic_cities = {}
            for elem in result:
                self.spic_cities[f'{elem[1]} ({elem[2]})'] = elem[0]
            result = cur.execute("""UPDATE flights
            SET people = ?
            WHERE start = ? AND finish = ? AND date = ? AND time = ?""", (
                '-'.join(self.closed_sid), self.spic_cities[self.spic[0]],
                self.spic_cities[self.spic[1]], self.spic[2], self.spic[3]
            ))
            con.commit()
            con.close()
            hi = f"""Здравствуйтe, {self.spic[6]} {self.spic[5]}!
Вы летите из {self.spic[0]} в {self.spic[1]} {self.spic[2]},
время вылета: {self.spic[3]}. Обратите внимание, что вы должны прибыть в аэропорт 
минимум за 2 часа до вылета.\nВаше место в 
самолете {sring.upper()}. Желаем Вам хорошего полета и мягкой 
посадки!"""
            f = open('ticket.txt', 'w').write(hi)
            self.close()