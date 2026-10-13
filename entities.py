from abc import ABC, abstractmethod


#Абстрактный базовый класс для всех сущностей приложения
class BaseEntity(ABC):

    @abstractmethod
    def get_info(self):
        pass


#Заказ клиента в пвз
class Order(BaseEntity):

    def __init__(self, login, time_in):
        self._login = login
        self._time_in = time_in
        self._time_out = None

    #геттеры и сеттеры

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        if not value:
            raise ValueError("Логин не может быть пустым")
        self._login = value

    @property
    def time_in(self):
        return self._time_in

    @time_in.setter
    def time_in(self, value):
        self._time_in = value

    @property
    def time_out(self):
        return self._time_out

    @time_out.setter
    def time_out(self, value):
        self._time_out = value

    #специальные методы
    def __str__(self):
        out = self._time_out if self._time_out else "---"
        return f"{self._login} | вход: {self._time_in} | выход: {out}"

    def __repr__(self):
        return f"Order('{self._login}', '{self._time_in}')"

    def __eq__(self, other):
        if not isinstance(other, Order):
            return False
        return self._login == other._login

    def __lt__(self, other):
        # сортировка по времени входа
        return self._time_in < other._time_in

    def get_info(self):
        return str(self)

    #статический метод

    @staticmethod
    def is_valid_login(login):
        return len(login) >= 3