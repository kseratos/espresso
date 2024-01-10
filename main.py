# requirements.txt сгенерировал через `pip freeze > requirements.txt`

import os.path
import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class CoffeeApp(QMainWindow):
    def __init__(self):
        self.connect = self.cursor = None
        self.db_file = "coffee.sqlite"

        super().__init__()
        self.initDB()
        uic.loadUi("main.ui", self)
        self.initLogic()

    def initDB(self):
        if not os.path.isfile(self.db_file):
            self.connect = sqlite3.connect(self.db_file)
            self.cursor = self.connect.cursor()

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS coffee (
                    ID INTEGER PRIMARY KEY,
                    "НАЗВАНИЕ СОРТА" TEXT,
                    "СТЕПЕНЬ ОБЖАРКИ" TEXT,
                    "МОЛОТЫЙ/В ЗЕРНАХ" TEXT,
                    "ОПИСАНИЕ ВКУСА" TEXT,
                    "ЦЕНА (в рублях)" INTEGER,
                    "ОБЪЕМ УПАКОВКИ (в граммах)" INTEGER
                )
            """)

            self.cursor.execute("""
                INSERT INTO coffee ("НАЗВАНИЕ СОРТА", "СТЕПЕНЬ ОБЖАРКИ", "МОЛОТЫЙ/В ЗЕРНАХ", "ОПИСАНИЕ ВКУСА", "ЦЕНА (в рублях)", "ОБЪЕМ УПАКОВКИ (в граммах)")
                VALUES ('Arabica', 'Средняя', 'Молотый', 'Насыщенный и фруктовый вкус', 500, 250),
                       ('Robusta', 'Темная', 'В зернах', 'Сильный и горький вкус', 300, 500),
                       ('Liberica', 'Светлая', 'Молотый', 'Экзотический и сладкий вкус', 700, 100),
                       ('Ethiopian Yirgacheffe', 'Светлая', 'В зернах', 'Цветочный и фруктовый аромат', 800, 200)
            """)

            self.connect.commit()
            self.connect.close()

    def initLogic(self):
        self.connect = sqlite3.connect(self.db_file)
        self.cursor = self.connect.cursor()
        self.cursor.execute("SELECT * FROM coffee")
        data = self.cursor.fetchall()
        self.connect.close()

        self.tableWidget: QTableWidget
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(len(data[0]))
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setHorizontalHeaderLabels([info[0] for info in self.cursor.description])

        for row_index, row_data in enumerate(data):
            self.tableWidget.insertRow(row_index)
            for col_index, col_data in enumerate(row_data):
                self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

        self.tableWidget.setColumnWidth(0, 1)
        self.tableWidget.setColumnWidth(1, 180)
        self.tableWidget.setColumnWidth(2, 160)
        self.tableWidget.setColumnWidth(3, 160)
        self.tableWidget.setColumnWidth(4, 240)
        self.tableWidget.setColumnWidth(5, 130)
        self.tableWidget.setColumnWidth(6, 230)



if __name__ == "__main__":
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = CoffeeApp()
    ex.show()
    sys.exit(app.exec())
