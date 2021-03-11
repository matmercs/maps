import os
import sys

import requests
from PyQt5 import uic, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

SCREEN_SIZE = [1080, 720]


class Map(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('map.ui', self)
        self.getImage("49.157355", "55.79313", "0.05", ["map"])
        self.cur_dol = "49.157355"
        self.cur_shir = "55.79313"
        self.cur_de = "0.05"
        self.cur_type = ["map"]
        self.initUI()

    def getImage(self, dol, shir, delta, type):
        api_server = "http://static-maps.yandex.ru/1.x/"

        params = {
            "ll": ",".join([dol, shir]),
            "spn": ",".join([delta, delta]),
            "l": ",".join(type)
        }
        response = requests.get(api_server, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def show_map(self):
        dol = self.dol_edit.text()
        shir = self.shir_edit.text()
        if dol != '' and shir != '':
            if (dol.isdigit() or dol.count('.') == 1 or dol[0] == '-') and \
                    (shir.isdigit() or shir.count('.') == 1 or shir[0] == '-'):
                dd = ''
                ss = ''
                if dol[0] == '-':
                    dol = dol[1:]
                    dd = '-'
                if shir[0] == '-':
                    shir = shir[1:]
                    ss = '-'
                check = True
                if dol.count('.') == 1:
                    if not (dol.split('.')[0].isdigit() and dol.split('.')[1].isdigit()):
                        check = False
                if shir.count('.') == 1:
                    if not (shir.split('.')[0].isdigit() and shir.split('.')[1].isdigit()):
                        check = False
                if check:
                    if -85 < float(shir) < 85 and -180 < float(dol) < 180:
                        self.warning_txt.setText('')
                        self.cur_dol = dd + dol
                        self.cur_shir = ss + shir
                        self.getImage(self.cur_dol, self.cur_shir, self.cur_de, self.cur_type)
                        pixmap = QtGui.QPixmap('map.png')
                        self.image.setPixmap(pixmap)
                    else:
                        self.warning_txt.setText('Ошибка в введенных координатах')
                else:
                    self.warning_txt.setText('Ошибка в введенных координатах')
            else:
                self.warning_txt.setText('Ошибка в введенных координатах.')
        else:
            self.warning_txt.setText('Ошибка в введенных координатах')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if float(self.cur_de) + float(self.cur_de) * 0.5 <= 100:
                self.warning_txt.setText('')
                self.cur_de = str(float(self.cur_de) + float(self.cur_de) * 0.5)
                self.getImage(self.cur_dol, self.cur_shir, self.cur_de, self.cur_type)
                pixmap = QtGui.QPixmap('map.png')
                self.image.setPixmap(pixmap)
        if event.key() == Qt.Key_PageDown:
            if float(self.cur_de) - float(self.cur_de) * 0.5 > 0.001:
                self.warning_txt.setText('')
                self.cur_de = str(float(self.cur_de) - float(self.cur_de) * 0.5)
                self.getImage(self.cur_dol, self.cur_shir, self.cur_de, self.cur_type)
                pixmap = QtGui.QPixmap('map.png')
                self.image.setPixmap(pixmap)
        if event.key() == Qt.Key_Up:
            if float(self.cur_de) / 2 + float(self.cur_shir) <= 85:
                self.warning_txt.setText('')
                self.cur_shir = str(float(self.cur_de) / 2 + float(self.cur_shir))
                self.getImage(self.cur_dol, self.cur_shir, self.cur_de, self.cur_type)
                pixmap = QtGui.QPixmap('map.png')
                self.image.setPixmap(pixmap)
        if event.key() == Qt.Key_Down:
            if -float(self.cur_de) / 2 + float(self.cur_shir) >= -85:
                self.warning_txt.setText('')
                self.cur_shir = str(-float(self.cur_de) / 2 + float(self.cur_shir))
                self.getImage(self.cur_dol, self.cur_shir, self.cur_de, self.cur_type)
                pixmap = QtGui.QPixmap('map.png')
                self.image.setPixmap(pixmap)
        if event.key() == Qt.Key_Right:
            if float(self.cur_de) / 2 + float(self.cur_dol) <= 180:
                self.cur_dol = str(float(self.cur_de) / 2 + float(self.cur_dol))
            else:
                self.cur_dol = str(float(self.cur_de) / 2 + float(self.cur_dol) - 360)
            self.warning_txt.setText('')
            self.getImage(self.cur_dol, self.cur_shir, self.cur_de, self.cur_type)
            pixmap = QtGui.QPixmap('map.png')
            self.image.setPixmap(pixmap)
        if event.key() == Qt.Key_Left:
            if -float(self.cur_de) / 2 + float(self.cur_dol) >= -180:
                self.cur_dol = str(-float(self.cur_de) / 2 + float(self.cur_dol))
            else:
                self.cur_dol = str(-float(self.cur_de) / 2 + float(self.cur_dol) + 360)
            self.warning_txt.setText('')
            self.getImage(self.cur_dol, self.cur_shir, self.cur_de, self.cur_type)
            pixmap = QtGui.QPixmap('map.png')
            self.image.setPixmap(pixmap)

    def set_type_m(self):
        self.btn1.setChecked(True)
        if self.cur_type != ['map']:
            self.cur_type = ['map']
            self.btn2.setChecked(False)
            self.btn3.setChecked(False)
            self.getImage(self.cur_dol, self.cur_shir, self.cur_de, self.cur_type)
            pixmap = QtGui.QPixmap('map.png')
            self.image.setPixmap(pixmap)

    def set_type_s(self):
        self.btn2.setChecked(True)
        if self.cur_type != ['sat']:
            self.cur_type = ['sat']
            self.btn1.setChecked(False)
            self.btn3.setChecked(False)
            self.getImage(self.cur_dol, self.cur_shir, self.cur_de, self.cur_type)
            pixmap = QtGui.QPixmap('map.png')
            self.image.setPixmap(pixmap)

    def set_type_ss(self):
        self.btn3.setChecked(True)
        if self.cur_type != ['sat', 'skl']:
            self.cur_type = ['sat', 'skl']
            self.btn1.setChecked(False)
            self.btn2.setChecked(False)
            self.getImage(self.cur_dol, self.cur_shir, self.cur_de, self.cur_type)
            pixmap = QtGui.QPixmap('map.png')
            self.image.setPixmap(pixmap)

    def find_obj(self):
        obj = self.address.text()
        geocoder_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={}&format=json".format(obj)
        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()
            if int(json_response['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData'][
                       'found']) > 0:
                self.warning_txt_2.setText("")
                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                coord = toponym['boundedBy']['Envelope']['lowerCorner'].split()
                self.cur_dol = coord[0]
                self.cur_shir = coord[1]
                self.cur_de = '0.001'
                self.getImage(self.cur_dol, self.cur_shir, self.cur_de, self.cur_type)
                pixmap = QtGui.QPixmap('map.png')
                self.image.setPixmap(pixmap)
            else:
                self.warning_txt_2.setText("Ничего не найдено")

        else:
            self.warning_txt_2.setText("Ошибка выполнения запроса")

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Карты')
        self.show_btn.clicked.connect(self.show_map)
        self.btn1.clicked.connect(self.set_type_m)
        self.btn2.clicked.connect(self.set_type_s)
        self.btn3.clicked.connect(self.set_type_ss)
        self.find_btn.clicked.connect(self.find_obj)

        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Map()
    ex.show()
    sys.exit(app.exec())
