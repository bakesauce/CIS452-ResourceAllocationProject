import sys
from PyQt5.QtWidgets import QApplication, QLabel
from model import Model


class View:

    app = QApplication([])

    label = QLabel('Hello Word!')
    label.show()
    app.exec_()


