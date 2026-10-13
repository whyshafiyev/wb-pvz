import datetime

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QMessageBox
)

from entities import Order
from storage import OrderStorage


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Пункт выдачи заказов")
        self.resize(420, 420)

        self.storage = OrderStorage()

        #компоновка и виджеты
        layout = QVBoxLayout(self)

        self.label = QLabel("Логин клиента:")
        self.input = QLineEdit()
        self.input.setPlaceholderText("например, ivan_01")

        self.btn_accept = QPushButton("Принять заказ")
        self.btn_issue = QPushButton("Выдать заказ")
        self.list_widget = QListWidget()

        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.btn_accept)
        layout.addWidget(self.btn_issue)
        layout.addWidget(self.list_widget)

        #сигналы
        self.btn_accept.clicked.connect(self.on_accept)
        self.btn_issue.clicked.connect(self.on_issue)

    #обработчики кнопок

    def on_accept(self):
        login = self.input.text().strip()

        if not Order.is_valid_login(login):
            QMessageBox.warning(self, "Ошибка", "Логин слишком короткий")
            return

        if self.storage.find_by_login(login):
            QMessageBox.warning(self, "Ошибка", "Такой клиент уже есть")
            return

        now = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")
        self.storage.add(Order(login, now))
        self.refresh_list()
        self.input.clear()

    def on_issue(self):
        login = self.input.text().strip()
        order = self.storage.find_by_login(login)

        if order is None:
            QMessageBox.warning(self, "Ошибка", "Клиент не найден")
            return

        if order.time_out is not None:
            QMessageBox.warning(self, "Ошибка", "Заказ уже выдан")
            return

        order.time_out = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")
        self.refresh_list()

    def refresh_list(self):
        self.list_widget.clear()
        for order in self.storage.get_all_sorted():
            self.list_widget.addItem(str(order))

    #переопределения событий окна

    def closeEvent(self, event):
        self.save_report()
        event.accept()

    def keyPressEvent(self, event):
        if event.key() == 16777220:  # Enter
            self.on_accept()
        else:
            super().keyPressEvent(event)

    def mousePressEvent(self, event):
        pass

    def resizeEvent(self, event):
        pass

    def showEvent(self, event):
        pass

    def focusInEvent(self, event):
        pass

    def focusOutEvent(self, event):
        pass

    def enterEvent(self, event):
        pass

    def leaveEvent(self, event):
        pass

    def moveEvent(self, event):
        pass

    #сохранение отчёта

    def save_report(self):
        with open("report.txt", "w", encoding="utf-8") as f:
            f.write("+----------+---------------------+---------------------+\n")
            f.write("|  login   |       time_in       |      time_out       |\n")
            f.write("+----------+---------------------+---------------------+\n")

            for order in self.storage.get_all_sorted():
                t_out = order.time_out if order.time_out else "None"
                f.write(
                    f"| {order.login:<8} | {order.time_in:<19} | {t_out:<19} |\n"
                )

            f.write("+----------+---------------------+---------------------+\n")