import sys

from PyQt5.QtWidgets import QWidget, QApplication, QPushButton

from PyQt5.QtWidgets import QInputDialog, QColorDialog

from PyQt5.QtWidgets import QLineEdit, QLabel

from PyQt5.QtGui import QPen, QPainter

from math import pi, cos, sin

from PyQt5.QtCore import Qt

SCREEN_SIZE = [500, 500]


class Example(QWidget):

    def __init__(self):

        super().__init__()

        self.initUI()

        self.flag = False

        # self.draw.clicked.connect(self.draf)

    def initUI(self):

        self.setGeometry(300, 300, *SCREEN_SIZE)

        self.setWindowTitle('Квадрат-объектив')

        self.Lab1 = QLabel(self)

        self.Lab1.move(20, 40)

        self.Lab1.setText("Сторона квадрата")

        self.Lab2 = QLabel(self)

        self.Lab2.move(20, 70)

        self.Lab2.setText("Коэф. Мастабирования")

        self.Lab3 = QLabel(self)

        self.Lab3.move(20, 100)

        self.Lab3.setText("Кол-во повторений")

        self.line = QLineEdit(self)

        self.line.move(50, 40)

        self.line1 = QLineEdit(self)

        self.line1.move(50, 70)

        self.line2 = QLineEdit(self)

        self.line2.move(50, 100)

        self.button = QPushButton(self)

        self.button.move(100, 100)

        self.button.setText("ПУСК")

        self.button.clicked.connect(self.draf)

        self.show()

    def paintEvent(self, event):

        qp = QPainter()

        qp.begin(self)

        self.draf(qp)

        qp.end()

    def xs(self, x):

        return x + SCREEN_SIZE[0] // 2

    def ys(self, y):

        return SCREEN_SIZE[1] // 2 - y

    def draf(self, qp):

        Leng = self.line.text()

        Koef = self.line1.text()

        N = self.line2.text()

        RAD = int(Leng)

        p = 4

        nodes = [(RAD * cos(i * 2 * pi / p), RAD * sin(i * 2 * pi / p)) for i in range(p)]

        nodes2 = [(self.xs(node[0]), self.ys(node[1])) for node in nodes]

        for i in range(-1, len(nodes2) - 1):
            qp.drawLine(*nodes2[i], *nodes2[i + 1])

            pen = QPen(Qt.red, 2)

            qp.setPen(pen)

        for i in range(-2, len(nodes2) - 2):
            qp.drawLine(*nodes2[i], *nodes2[i + 2])


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = Example()

    sys.exit(app.exec_())

