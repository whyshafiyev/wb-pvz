#складская система выюранного пункта
#поиск выполняется вручную перебором списка.
class OrderStorage:

    def __init__(self):
        self._items = []

    def add(self, order):
        self._items.append(order)

    def find_by_login(self, login):
        for item in self._items:
            if item.login == login:
                return item
        return None

    def get_all_sorted(self):
        return sorted(self._items)

    def __len__(self):
        return len(self._items)