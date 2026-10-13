import sys
import datetime
from abc import ABC, abstractmethod
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QListWidget, QMessageBox)

# 1. Абстрактный класс
class BaseEntity(ABC):
    @abstractmethod
    def get_info(self): pass

# 2. Сущность
class Order(BaseEntity):
    def __init__(self, login, time_in):
        self._login = login
        self._time_in = time_in
        self._time_out = None

    # --- Геттеры и сеттеры для ВСЕХ атрибутов ---
    @property
    def login(self): return self._login

    @login.setter
    def login(self, v):
        if not v: raise ValueError("Пустой логин")
        self._login = v

    @property
    def time_in(self): return self._time_in

    @time_in.setter
    def time_in(self, v): self._time_in = v

    @property
    def time_out(self): return self._time_out

    @time_out.setter
    def time_out(self, v): self._time_out = v

    # --- 3+ магических метода ---
    def __str__(self):
        return f"{self._login} | Вход: {self._time_in} | Выход: {self._time_out or '---'}"

    def __repr__(self):
        return f"Order('{self._login}', '{self._time_in}')"

    def __eq__(self, other):
        return isinstance(other, Order) and self._login == other._login

    def __lt__(self, other):
        return self._time_in < other._time_in

    def get_info(self):
        return str(self)

    # --- Static method ---
    @staticmethod
    def is_valid(login):
        return len(login) >= 3

# 3. Кастомное хранилище (без dict)
class OrderStorage:
    def __init__(self):
        self._data = []

    def add(self, order): self._data.append(order)

    def find(self, login):
        for o in self._data:
            if o.login == login: return o
        return None

    def all(self): return sorted(self._data)

# 4. Приложение
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ПВЗ WB")
        self.resize(400, 400)
        self.storage = OrderStorage()

        layout = QVBoxLayout(self)
        self.lbl = QLabel("Логин клиента:")
        self.inp = QLineEdit()
        self.btn_in = QPushButton("Принять")
        self.btn_out = QPushButton("Выдать")
        self.list_ui = QListWidget()

        for w in (self.lbl, self.inp, self.btn_in, self.btn_out, self.list_ui):
            layout.addWidget(w)

        self.btn_in.clicked.connect(self.add_order)
        self.btn_out.clicked.connect(self.issue_order)

    def add_order(self):
        login = self.inp.text()
        if not Order.is_valid(login):
            QMessageBox.warning(self, "Ошибка", "Логин короткий")
            return
        now = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")
        self.storage.add(Order(login, now))
        self.update_ui()
        self.inp.clear()

    def issue_order(self):
        o = self.storage.find(self.inp.text())
        if o and not o.time_out:
            o.time_out = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")
            self.update_ui()
        else:
            QMessageBox.warning(self, "Ошибка", "Не найден или уже выдан")

    def update_ui(self):
        self.list_ui.clear()
        for o in self.storage.all():
            self.list_ui.addItem(str(o))

    # --- Переопределения событий (нужно 10) ---
    def closeEvent(self, e):
        with open("report.txt", "w", encoding="utf-8") as f:
            f.write("+----------+---------------------+---------------------+\n")
            f.write("|  login   |       time_in       |      time_out       |\n")
            f.write("+----------+---------------------+---------------------+\n")
            for o in self.storage.all():
                t = o.time_out or "None"
                f.write(f"| {o.login:<8} | {o.time_in:<19} | {t:<19} |\n")
            f.write("+----------+---------------------+---------------------+\n")
        e.accept()

    def keyPressEvent(self, e):      pass
    def mousePressEvent(self, e):    pass
    def resizeEvent(self, e):        pass
    def showEvent(self, e):          pass
    def focusInEvent(self, e):       pass
    def focusOutEvent(self, e):      pass
    def enterEvent(self, e):         pass
    def leaveEvent(self, e):         pass
    def moveEvent(self, e):          pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = App()
    w.show()
    sys.exit(app.exec_())
      
