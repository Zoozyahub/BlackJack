import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QButtonGroup
from random import shuffle

names = ['tus1', 'two1', 'three1', 'four1', 'five1', 'six1', 'seven1', 'eight1', 'nine1', 'ten1',
         'queen1', 'jack1', 'king1',
         'tus2', 'two2', 'three2', 'four2', 'five2', 'six2', 'seven2', 'eight2', 'nine2', 'ten2',
         'queen2', 'jack2', 'king2',
         'tus3', 'two3', 'three3', 'four3', 'five3', 'six3', 'seven3', 'eight3', 'nine3', 'ten3',
         'queen3', 'jack3', 'king3',
         'tus4', 'two4', 'three4', 'four4', 'five4', 'six4', 'seven4', 'eight4', 'nine4', 'ten4',
         'queen4', 'jack4', 'king4']  # список названий картинок карт. Все что надо дописать .png

class Start(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('StartWindow.ui', self)  # Загружаем дизайн

        self.db = sqlite3.connect('base.db')
        self.base = self.db.cursor()

        self.Register.clicked.connect(self.openReg)
        self.pashalka.clicked.connect(self.pas)
        self.but_log.clicked.connect(self.logfunc)

    def openReg(self):
        self.regWind = RegWindow(self)
        self.regWind.show()
        self.close()

    def pas(self):
        print('abc')

    def logfunc(self):
        self.a = self.base.execute("""SELECT login FROM base""").fetchall()
        self.b = [list(x)[0] for x in self.a]  # делаю это чтобы было можно сравнить со строкой а то '[(login,)]' не работает

        self.c = self.base.execute(f"""SELECT password FROM base WHERE
                                       login = '{self.log.text()}'""").fetchall()  # беру пароль от логина и делаю тоже самое
        self.d = [list(x)[0] for x in self.c]

        if self.log.text() not in self.b:  # проверяю
            self.wrong.setText('Неверный логин или пароль')
        elif self.passw.text() != self.d[0]:
            self.wrong.setText('Неверный логин или пароль')
        else:
            self.login = self.log.text()
            self.MenWind = MenuWindow(self)
            self.MenWind.show()
            self.close()


class RegWindow(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('RegWindow.ui', self)
        self.But_plug.clicked.connect(self.register)

    def register(self):
        self.ru = list('абвгдеёжзийкмлнопрстуфхцчшщъьыэюя')
        self.rus = set(self.ru)
        try:
            if self.reg_log.text().isalnum() and len(set(self.reg_log.text()) & self.rus) == 0:
                if self.reg_pass.text().isalnum() and len(set(self.reg_pass.text()) & self.rus) == 0:  # проверка пароля на цифры и буквы (кириллицу можно)
                    self.data = list()  # спиксок для удобства добавления в бд
                    self.data.append(self.reg_log.text())
                    self.data.append(self.reg_pass.text())
                    self.data.append(0)
                    self.data.append(1000)
                    self.data.append(0)
                    self.data = tuple(self.data)
                    self.db = sqlite3.connect('base.db')
                    self.base = self.db.cursor()
                    self.base.execute("INSERT INTO base VALUES(?, ?, ?, ?, ?);", self.data)   # добавляем все данные в бд (стартовые деньги 1000, достижений нет)
                    self.db.commit()
                    ex.show()
                    self.close()
            else:
                self.wrong.setText('Попробуйте другой логин или пароль')
        except sqlite3.IntegrityError:
            self.wrong.setText('Логин уже занят')


class MenuWindow(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('MenuWindow.ui', self)
        self.play_but.clicked.connect(self.play)
        self.exit_but.clicked.connect(self.exit)
        self.achivbut.clicked.connect(self.achivwnd)

    def play(self):
        self.Main = MainWindow(self)
        self.Main.show()
        self.close()

    def exit(self):
        self.close()

    def achivwnd(self):
        self.Achiv = AchievementWindow()
        self.Achiv.show()


class MainWindow(QWidget):
    def __init__(self, *args):
        super().__init__()
        global names

        names = ['tus1', 'two1', 'three1', 'four1', 'five1', 'six1', 'seven1', 'eight1', 'nine1', 'ten1',
                 'queen1', 'jack1', 'king1',
                 'tus2', 'two2', 'three2', 'four2', 'five2', 'six2', 'seven2', 'eight2', 'nine2', 'ten2',
                 'queen2', 'jack2', 'king2',
                 'tus3', 'two3', 'three3', 'four3', 'five3', 'six3', 'seven3', 'eight3', 'nine3', 'ten3',
                 'queen3', 'jack3', 'king3',
                 'tus4', 'two4', 'three4', 'four4', 'five4', 'six4', 'seven4', 'eight4', 'nine4', 'ten4',
                 'queen4', 'jack4', 'king4']

        uic.loadUi('MainWindow.ui', self)
        self.give_but.setEnabled(False)
        self.skip_but.setEnabled(False)
        self.db = sqlite3.connect('base.db')
        self.base = self.db.cursor()
        self.balance.setText(str(self.base.execute(f"""SELECT money FROM base
                                                  WHERE login = '{ex.login}'""").fetchone()[0]))  # выводим баланс из бд

        self.btn_grp = QButtonGroup()   # добавляем все кнопки повышения ставки в группу чтобы не прописывать для всех одно и тоже
        self.btn_grp.addButton(self.up50)
        self.btn_grp.addButton(self.up100)
        self.btn_grp.addButton(self.up500)
        self.btn_grp.addButton(self.up1000)
        self.btn_grp.buttonClicked.connect(self.upbet)


        self.btn_grp2 = QButtonGroup()  # тоже самое делаем с кнопками понижения
        self.btn_grp2.addButton(self.down50)
        self.btn_grp2.addButton(self.down100)
        self.btn_grp2.addButton(self.down500)
        self.btn_grp2.addButton(self.down1000)
        self.btn_grp2.buttonClicked.connect(self.downbet)

        self.give_but.clicked.connect(self.game_give)  # кнопка взять

        self.back_but.clicked.connect(self.back)  # кнопка назад

        self.skip_but.clicked.connect(self.skip)

        self.first = True

    def game_give(self):
        if self.first:
            self.db.commit()  # сохраняем изменение баланса
            self.player = Hand()  # создаем игрок и компьютер и выдем по две карты
            self.computer = Hand()
            self.player.add_card(Card())
            self.player.add_card(Card())
            self.computer.add_card(Card())
            self.computer.add_card(Card())

            self.card1_open = QPixmap('карты/' + self.player[0] + '.png')
            self.card2_open = QPixmap('карты/' + self.player[1] + '.png')
            self.card1_end = self.card1_open.scaled(111, 141)
            self.card2_end = self.card2_open.scaled(111, 141)
            self.card1.setPixmap(self.card1_end)
            self.card2.setPixmap(self.card2_end)

            self.botcard1_open = QPixmap('карты/' + self.computer[0] + '.png')
            self.botcard2_open = QPixmap('карты/' + 'back' + '.png')
            self.botcard1_end = self.botcard1_open.scaled(111, 141)
            self.botcard2_end = self.botcard2_open.scaled(111, 141)
            self.botcard1.setPixmap(self.botcard1_end)
            self.botcard2.setPixmap(self.botcard2_end)

            self.score.setText(str(self.player.get_value()))  # выводим начальное количество очков
            self.first = False  # обозначим что первое нажатие было и дальше надо брать не 2 карты а 1
            self.up50.setEnabled(False)  # полсе нажатия кнопки взять, блокируем изменение ставки
            self.up100.setEnabled(False)
            self.up500.setEnabled(False)
            self.up1000.setEnabled(False)
            self.down50.setEnabled(False)
            self.down100.setEnabled(False)
            self.down500.setEnabled(False)
            self.down1000.setEnabled(False)
            self.skip_but.setEnabled(True)
            self.labels = [self.card3, self.card4, self.card5, self.card6, self.card7, self.card8, self.card9,
                           self.card10, self.card11]
            self.press = 0
        else:
            self.player.add_card(Card())  # 2 и далее нажатие дают одну карту и обновляют количество очков
            self.score.setText(str(self.player.get_value()))
            self.player_open = QPixmap('карты/' + self.player[self.press + 2] + '.png')
            self.player_end = self.player_open.scaled(111, 141)
            self.labels[self.press].setPixmap(self.player_end)
            self.press += 1
            if self.player.get_value() > 21:
                self.end = EndWindow()
                self.end.show()
                self.give_but.setEnabled(False)
                self.skip_but.setEnabled(False)

    def skip(self):
        self.db.commit()
        self.give_but.setEnabled(False)
        self.skip_but.setEnabled(False)
        self.botcard_open = QPixmap('карты/' + self.computer[1] + '.png')
        self.botcard_end = self.botcard_open.scaled(111, 141)
        self.botcard2.setPixmap(self.botcard_end)
        self.lab_bot = [self.botcard3, self.botcard4, self.botcard5, self.botcard6, self.botcard7, self.botcard8]
        self.lab = 0
        self.draw = DrawWindow()
        self.win = WinWindow()
        self.end = EndWindow()
        self.winres = False
        self.lossres = False
        self.drawres = False
        if self.computer.get_value() > 16:
            if self.player.get_value() > self.computer.get_value() and self.computer.get_value() <= 21:
                self.win.show()
                self.winres = True
            elif self.player.get_value() < self.computer.get_value() or self.computer.get_value() > 21:
                self.end.show()
                self.lossres = True
            else:
                self.draw.show()
                self.drawres = True
        while self.computer.get_value() <= 16:
            self.computer.add_card(Card())
            self.botcard_open = QPixmap('карты/' + self.computer[self.lab + 2] + '.png')
            self.botcard_end = self.botcard_open.scaled(111, 141)
            self.lab_bot[self.lab].setPixmap(self.botcard_end)
            self.lab += 1
        if self.computer.get_value() > 21:
            self.win.show()
            self.winres = True
        elif self.player.get_value() > self.computer.get_value():
            self.win.show()
            self.winres = True
        elif self.player.get_value() < self.computer.get_value():
            self.end.show()
            self.lossres = True
        else:
            self.draw.show()
            self.drawres = True
        self.coin = self.base.execute(f"""SELECT money FROM base
                                          WHERE login = '{ex.login}'""").fetchone()[0]
        if self.winres:
            self.base.execute(f"""UPDATE base SET money = {int(self.bet.text()) * 2 + self.coin}
                                              WHERE login = '{ex.login}'""")
            self.wins = self.base.execute(f"""SELECT wins FROM base
                                              WHERE login = '{ex.login}'""").fetchone()[0]
            self.base.execute(f"""UPDATE base SET wins = {self.wins + 1}
                                  WHERE login = '{ex.login}'""")
            if self.wins == 0:
                self.base.execute(f"""UPDATE base SET achivment = '3'
                                      WHERE login = '{ex.login}'""")
            if self.player.get_value() == 21:
                self.ach = self.base.execute(f"""SELECT achivment FROM base
                                                  WHERE login = '{ex.login}'""").fetchone()[0]
                if '1' not in self.ach:
                    self.base.execute(f"""UPDATE base SET achivment = {self.ach + '1'}
                                          WHERE login = '{ex.login}'""")
            if self.wins + 1 == 10:
                self.ach = self.base.execute(f"""SELECT achivment FROM base
                                                 WHERE login = '{ex.login}'""").fetchone()[0]
                self.base.execute(f"""UPDATE base SET achivment = {self.ach + '2'}
                                                          WHERE login = '{ex.login}'""")
            elif self.wins + 1 == 50:
                self.ach = self.base.execute(f"""SELECT achivment FROM base
                                                 WHERE login = '{ex.login}'""").fetchone()[0]
                self.base.execute(f"""UPDATE base SET achivment = {self.ach + '5'}
                                                          WHERE login = '{ex.login}'""")
            print(int(self.bet.text()))
            if int(self.bet.text()) >= 1000:
                print(1)
                self.ach = self.base.execute(f"""SELECT achivment FROM base
                                                  WHERE login = '{ex.login}'""").fetchone()[0]
                self.base.execute(f"""UPDATE base SET achivment = {self.ach + '4'}
                                      WHERE login = '{ex.login}'""")

            self.db.commit()
        elif self.drawres:
            self.base.execute(f"""UPDATE base SET money = {int(self.bet.text()) + self.coin}
                                                          WHERE login = '{ex.login}'""")
            self.db.commit()
            if int(self.bet.text()) >= 1000:
                self.ach = self.base.execute(f"""SELECT achivment FROM base
                                                  WHERE login = '{ex.login}'""").fetchone()[0]
                self.base.execute(f"""UPDATE base SET achivment = {self.ach + '4'}
                                      WHERE login = '{ex.login}'""")
            self.db.commit()
        elif self.lossres:
            if int(self.bet.text()) >= 1000:
                self.ach = self.base.execute(f"""SELECT achivment FROM base
                                                  WHERE login = '{ex.login}'""").fetchone()[0]
                if '4' not in self.ach:
                    self.base.execute(f"""UPDATE base SET achivment = {self.ach + '4'}
                                          WHERE login = '{ex.login}'""")
            self.db.commit()

    def back(self):
        self.db.commit()
        self.Menu = MenuWindow()
        self.Menu.show()
        self.close()

    def upbet(self, btn):
        if int(self.balance.text()) >= int(btn.text()):  # кнопка повышения ставки
            self.bet.setText(f'{int(self.bet.text()) + int(btn.text())}')  # выводим ставку на экран
            self.base.execute(f"""UPDATE base SET money = {int(self.balance.text()) - int(btn.text())}
                                  WHERE login = '{ex.login}'""")  # обновляем базу с балансом (вычитаем ставку после нажатия кнопки взять)
            self.balance.setText(str(self.base.execute(f"""SELECT money FROM base
                                                              WHERE login = '{ex.login}'""").fetchone()[0]))  # выводим баланс - ставка
            if self.bet.text() == '0':
                self.give_but.setEnabled(False)
                self.skip_but.setEnabled(False)
            else:
                self.give_but.setEnabled(True)

    def downbet(self, btn):  # кнопка понижения ставки
        if int(self.bet.text()) >= abs(int(btn.text())):
            self.bet.setText(f'{int(self.bet.text()) + int(btn.text())}')
            self.base.execute(f"""UPDATE base SET money = {int(self.balance.text()) - int(btn.text())}
                                  WHERE login = '{ex.login}'""")
            self.balance.setText(str(self.base.execute(f"""SELECT money FROM base
                                                              WHERE login = '{ex.login}'""").fetchone()[0]))
            if self.bet.text() == '0':
                self.give_but.setEnabled(False)
                self.skip_but.setEnabled(False)
            else:
                self.give_but.setEnabled(True)


class AchievementWindow(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('AchievementWindow.ui', self)
        self.db = sqlite3.connect('base.db')
        self.base = self.db.cursor()
        self.name1.setText(str(self.base.execute(f"""SELECT name FROM achivments
                                                     WHERE id = '1'""").fetchone()[0]))
        self.name2.setText(str(self.base.execute(f"""SELECT name FROM achivments
                                                     WHERE id = '2'""").fetchone()[0]))
        self.name3.setText(str(self.base.execute(f"""SELECT name FROM achivments
                                                     WHERE id = '3'""").fetchone()[0]))
        self.name4.setText(str(self.base.execute(f"""SELECT name FROM achivments
                                                     WHERE id = '4'""").fetchone()[0]))
        self.name5.setText(str(self.base.execute(f"""SELECT name FROM achivments
                                                     WHERE id = '5'""").fetchone()[0]))
        self.desc1.setText(str(self.base.execute(f"""SELECT desc FROM achivments
                                                     WHERE id = '1'""").fetchone()[0]))
        self.desc2.setText(str(self.base.execute(f"""SELECT desc FROM achivments
                                                     WHERE id = '2'""").fetchone()[0]))
        self.desc3.setText(str(self.base.execute(f"""SELECT desc FROM achivments
                                                     WHERE id = '3'""").fetchone()[0]))
        self.desc4.setText(str(self.base.execute(f"""SELECT desc FROM achivments
                                                     WHERE id = '4'""").fetchone()[0]))
        self.desc5.setText(str(self.base.execute(f"""SELECT desc FROM achivments
                                                     WHERE id = '5'""").fetchone()[0]))
        self.c = self.base.execute(f"""SELECT achivment FROM base WHERE
                                       login = '{ex.login}'""").fetchall()
        self.achivments = [list(x)[0] for x in self.c]
        if '1' not in ''.join(self.achivments):
            self.name1.setEnabled(False)
            self.desc1.setEnabled(False)
        if '2' not in ''.join(self.achivments):
            self.name2.setEnabled(False)
            self.desc2.setEnabled(False)
        if '3' not in ''.join(self.achivments):
            self.name3.setEnabled(False)
            self.desc3.setEnabled(False)
        if '4' not in ''.join(self.achivments):
            self.name4.setEnabled(False)
            self.desc4.setEnabled(False)
        if '5' not in ''.join(self.achivments):
            self.name5.setEnabled(False)
            self.desc5.setEnabled(False)


class EndWindow(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('EndWindow.ui', self)


class WinWindow(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('WinWindow.ui', self)


class DrawWindow(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('DrawWindow.ui', self)


class Card:
    def __init__(self):
        global names
        shuffle(names)  # перемешиваем колоду
        self.card = names.pop(1)  # достаем и удаляем первую карту

    def get_card(self):  # получить карту
        return self.card

    def get_value(self):  # очки за карты без туза (тузы будем считать не тут)
        if 'tus' not in self.card:
            if 'two' in self.card:
                return 2
            elif 'three' in self.card:
                return 3
            elif 'four' in self.card:
                return 4
            elif 'five' in self.card:
                return 5
            elif 'six' in self.card:
                return 6
            elif 'seven' in self.card:
                return 7
            elif 'eight' in self.card:
                return 8
            elif 'nine' in self.card:
                return 9
            elif 'ten' in self.card:
                return 10
            else:
                return 10
        else:
            return 0

    def __str__(self):
        return self.card


class Hand:
    def __init__(self):
        self.cards = list()
        self.points = 0
        self.tuses = 0

    def add_card(self, card):
        self.cards.append(card.get_card())
        if 'tus' not in card.get_card():  # считаем очки если тузов нет
            self.points += card.get_value()
        elif self.tuses == 0:  # решаем считать тузы за 1 или 11 и считаем все очки
            self.tuses += 1
            if (self.points + 11) <= 21:
                self.points += 11
            else:
                self.points += 1
        else:
            self.points += 1

    def get_value(self):  # колво очков
        return self.points

    def get_cards(self):  # получить список карт
        return self.cards

    def __str__(self):
        self.printer = list()
        for i in self.cards:
            self.printer.append(i)
        return ' '.join(self.printer)

    def __getitem__(self, key):  # доступ к картам по ключу
        return self.cards[key]

    def __len__(self):
        return len(self.cards)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Start()
    ex.show()
    sys.exit(app.exec_())
