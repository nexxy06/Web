import sys
import os

try:
    import requests
except:
    os.system("pip3 install requests")
    import requests
try:
    import PyQt5
except:
    os.system("pip3 install PyQt5")
    import PyQt5

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5 import QtCore


class Api(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('api5.ui', self)

        self.lib = ['map', 'sat', 'sat,skl']
        self.counter = 0
        self.l = self.lib[0]
        self.delta = 17
        self.api_server = "http://static-maps.yandex.ru/1.x/"

        self.modebtn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.modebtn.clicked.connect(self.modes)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.searchbtn.clicked.connect(self.address_finder)

    def initUI(self):
        self.sh = str(50)
        self.dl = str(50)

        print(self.l)
        self.params = {
            "ll": ",".join([self.dl, self.sh]),
            "z": self.delta,
            "l": self.l,
            "pt": self.pt
        }

        self.create_image()

    def modes(self):
        self.counter += 1
        if self.counter > 2:
            self.counter = 0
        self.l = self.lib[self.counter]

        self.params = {
            "ll": ",".join([self.dl, self.sh]),
            "z": self.delta,
            "l": self.l,
            "pt": self.pt
        }

        self.create_image()

    def address_finder(self):
        geocoder_api_server = 'http://geocode-maps.yandex.ru/1.x/'
        params = {
            'apikey': "40d1649f-0493-4b70-98ba-98533de7710b",
            'geocode': self.adress.text(),
            'format': 'json'
        }
        response = requests.get(geocoder_api_server, params=params).json()

        if not response:
            print('Ошибка в геокодере')
        else:
            self.toponym = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
            self.toponym_coordinates = self.toponym['Point']['pos'].split()

            self.dl, self.sh = self.toponym_coordinates
            self.pt = f'{self.dl},{self.sh},pm2rdm'

        self.params = {
            "ll": ",".join([self.dl, self.sh]),
            "z": self.delta,
            "l": self.l,
            "pt": self.pt
        }

        self.create_image()

    def create_image(self):
        self.response = requests.get(self.api_server, params=self.params)
        if not self.response:
            print('Problem')

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(self.response.content)

        self.pixmap = QPixmap(self.map_file)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown:
            self.delta -= 1
            self.params = {
                "ll": ",".join([self.dl, self.sh]),
                "z": self.delta,
                "l": self.l,
                "pt": self.pt
            }

        if event.key() == Qt.Key_PageUp:
            self.delta += 1
            self.params = {
                "ll": ",".join([self.dl, self.sh]),
                "z": self.delta,
                "l": self.l,
                "pt": self.pt
            }

        if event.key() == PyQt5.QtCore.Qt.Key_Up:
            self.sh = str(float(self.sh) + 0.5)
            self.params = {
                "ll": ",".join([self.dl, self.sh]),
                "z": self.delta,
                "l": self.l,
                "pt": self.pt
            }

        if event.key() == Qt.Key_Down:
            self.sh = str(float(self.sh) - 0.5)
            self.params = {
                "ll": ",".join([self.dl, self.sh]),
                "z": self.delta,
                "l": self.l,
                "pt": self.pt
            }

        if event.key() == Qt.Key_Right:
            self.dl = str(float(self.dl) + 0.5)
            self.params = {
                "ll": ",".join([self.dl, self.sh]),
                "z": self.delta,
                "l": self.l,
                "pt": self.pt
            }

        if event.key() == Qt.Key_Left:
            self.dl = str(float(self.dl) - 0.5)
            self.params = {
                "ll": ",".join([self.dl, self.sh]),
                "z": self.delta,
                "l": self.l,
                "pt": self.pt
            }

        self.create_image()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Api()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
