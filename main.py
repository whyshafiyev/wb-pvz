import sys
import datetime
from abc import ABC, abstractmethod
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QListWidget, QMessageBox)


# 1. Абстрактный класс (Критерий: наследование от абстрактного класса)
class BaseEntity(ABC):
    @abstractmethod
    def get_info(self):
        pass


# 2. Сущность (Критерий: геттеры/сеттеры, 3 магических метода, сравнение)
class Order(BaseEntity):
    def __init__(self, login, time_in):
        self._login = login
        self._time_in = time_in
        self._time_out = None

    # Геттеры и сеттеры (Критерий: атрибуты с геттерами/сеттерами)
    @property
    def login(self): return self._login

    @login.setter
    def login(self, value):
        if not value: raise ValueError("Пустой логин")
        self._login = value

    # Магические методы (Критерий: минимум 3)
    def __str__(self):
        return f"{self._login} | Вход: {self._time_in} | Выход: {self._time_out or '---'}"

    def __eq__(self, other):
        return self._login == other.login if isinstance(other, Order) else False

    def __lt__(self, other):
        return self._time_in < other._time_in  # Для сортировки (Критерий: сравнимость)

    def get_info(self):
        return str(self)

    # Статический метод (Критерий: функциональность через staticmethod)
    @staticmethod
    def is_valid(login):
        return len(login) >= 3


# 3. Кастомная коллекция (Критерий: запрет dict, свой класс)
class OrderStorage:
    def __init__(self):
        self._data = []  # Используем list вместо dict

    def add(self, order):
        self._data.append(order)

    def find(self, login):
        for o in self._data:
            if o.login == login: return o
        return None

    def get_sorted(self):
        return sorted(self._data)  # Использует __lt__


# 4. Интерфейс (Критерий: 5+ UI, выравнивание)
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ПВЗ WB (Упрощенно)")
        self.resize(400, 400)

        self.storage = OrderStorage()
        layout = QVBoxLayout(self)  # Выравнивание через компоновщик

        # UI Компоненты
        self.lbl = QLabel("Введите логин клиента:")
        self.inp = QLineEdit()
        self.btn_in = QPushButton("Принять (Вход)")
        self.btn_out = QPushButton("Выдать (Выход)")
        self.list_ui = QListWidget()

        layout.addWidget(self.lbl)
        layout.addWidget(self.inp)
        layout.addWidget(self.btn_in)
        layout.addWidget(self.btn_out)
        layout.addWidget(self.list_ui)

        # Связка кнопок с логикой
        self.btn_in.clicked.connect(self.add_order)
        self.btn_out.clicked.connect(self.issue_order)

    def add_order(self):
        login = self.inp.text()
        if not Order.is_valid(login):
            QMessageBox.warning(self, "Ошибка", "Логин слишком короткий!")
            return

        now = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")
        self.storage.add(Order(login, now))
        self.update_ui()
        self.inp.clear()

    def issue_order(self):
        order = self.storage.find(self.inp.text())
        if order and not order._time_out:
            order._time_out = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")
            self.update_ui()
        else:
            QMessageBox.warning(self, "Ошибка", "Клиент не найден или уже выдан.")

    def update_ui(self):
        self.list_ui.clear()
        for order in self.storage.get_sorted():
            self.list_ui.addItem(str(order))  # Использует __str__

    # Сохранение отчета (Критерий: сохранение в файл при закрытии)
    def closeEvent(self, event):
        with open("report.txt", "w", encoding="utf-8") as f:
            f.write("+----------+---------------------+---------------------+\n")
            f.write("|  login   |       time_in       |      time_out       |\n")
            f.write("+----------+---------------------+---------------------+\n")
            for o in self.storage.get_sorted():
                t_out = o._time_out if o._time_out else "None"
                f.write(f"| {o.login:<8} | {o._time_in:<19} | {t_out:<19} |\n")
            f.write("+----------+---------------------+---------------------+\n")
            event.accept()

        if __name__ == "__main__":
            app = QApplication(sys.argv)
            window = App()
            window.show()
            sys.exit(app.exec_())