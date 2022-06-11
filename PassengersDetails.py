from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from ChoosePlace import Chooseplace


class Passengers_details(QMainWindow):
    def __init__(self, departure, arrival, date, times, money, sid):
        super().__init__()
        self.status = False
        self.departure, self.arrival, \
        self.date, self.times, \
        self.money = departure, \
                     arrival, date, \
                     times, money
        self.sid = sid
        self.initUI()

    def initUI(self):
        uic.loadUi('passanger.ui', self)
        self.pay.clicked.connect(self.pay_ticket)

    def is_correct(self, string):
        try:
            assert len(string) > 0
            assert not string.isdigit()
            assert len(set(string) & set([str(i) for i in range(10)])) == 0
            assert len(set(string) & set(['/', '!', '@', '#', '.', '?',
                                          ',', '"', "'", ')',
                                          '(', '*', '^'])) == 0
            return True
        except AssertionError:
            return False

    def pay_ticket(self):
        self.status = False
        self.Error.setText('')
        self.names = self.name.text()
        self.surnames = self.surname.text()
        self.patrs = self.patr.text()
        self.seriess = self.p_s.text()
        self.numbers = self.p_n.text()
        self.emails = self.mail.text()
        if not self.is_correct(self.names):
            self.status = True
            self.Error.setText('Ошибка в имени!')
        elif not self.is_correct(self.surnames):
            self.status = True
            self.Error.setText('Ошибка в фамилии!')
        elif not self.is_correct(self.patrs):
            self.status = True
            self.Error.setText('Ошибка в отчестве!')
        elif len(self.seriess) != 4 or not self.seriess.isdigit():
            self.status = True
            self.Error.setText('Ошибка в серии паспорта!')
        elif len(self.numbers) != 6 or not self.numbers.isdigit():
            self.status = True
            self.Error.setText('Ошибка в номере паспорта!')
        elif self.emails.count('@') != 1 or self.emails.split('.')[-1] not in ['ru', 'com']:
            self.status = True
            self.Error.setText('Ошибка в email!')

        if not self.status:
            self.open_new3 = BankCard(self.departure, self.arrival,
                                      self.date, self.times, self.money,
                                      self.names, self.surnames, self.sid)
            self.open_new3.show()
            self.close()


class BankCard(QMainWindow):
    def __init__(self, *spic):
        super().__init__()
        self.spic = spic
        self.status = False
        self.initUI()

    def initUI(self):
        uic.loadUi('bank_card.ui', self)
        self.pay.clicked.connect(self.res)

    def correct_number(self, string):
        st = ''.join(string.split())
        try:
            assert 13 <= len(st) <= 19
            assert st.isdigit()
            return True
        except AssertionError:
            return False

    def correct_date(self, st, mn=False):
        try:
            assert 1 <= len(st) <= 2
            assert st.isdigit()
            assert (mn and int(st) <= 12) or (not mn and int(st) >= 21)
            return True
        except AssertionError:
            return False

    def correct_name(self, string):
        st = ''.join(string.split())
        try:
            assert len(string) > 0
            assert not string.isdigit()
            assert len(set(string) & set([str(i) for i in range(10)])) == 0
            assert len(set(string) & set(['/', '!', '@', '#', '.', '?',
                                          ',', '"', "'", ')',
                                          '(', '*', '^'])) == 0
            return True
        except AssertionError:
            return False

    def correct_cvv(self, cvv):
        try:
            assert len(cvv) == 3
            assert cvv.isdigit()
            return True
        except AssertionError:
            return False

    def res(self):
        self.status = False
        self.number = self.cardData.text()
        self.dt1 = self.date_1.text()
        self.dt2 = self.date_2.text()
        self.names = self.name.text()
        self.cvv = self.cvc.text()
        if not self.correct_number(self.number):
            self.status = True
        elif not self.correct_date(self.dt1, True) or not self.correct_date(self.dt2):
            self.status = True
        elif not self.correct_name(self.names):
            self.status = True
        elif not self.correct_cvv(self.cvv):
            self.status = True

        if not self.status:
            self.open_new3 = Chooseplace(*self.spic)
            self.open_new3.show()
            self.close()