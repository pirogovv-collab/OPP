from abc import ABC, abstractmethod
from datetime import date



class MenuItem(ABC):

    def __init__(self, name: str, base_price: float):
        if base_price < 0:
            raise ValueError("Цена не может быть отрицательной")
        self.name = name
        self.base_price = base_price

    @abstractmethod
    def calculatePrice(self) -> float:
        """Итоговая стоимость конкретного блюда."""
        pass

    def getDisplayName(self) -> str:
        """Название для вывода (наследники могут переопределить)."""
        return self.name

    def __str__(self):
        return f"{self.getDisplayName()} — {self.calculatePrice():.2f}"


class Pizza(MenuItem):
    SIZES = ("маленькая", "средняя", "большая")

    def __init__(self, name: str, base_price: float, size: str = "средняя"):
        super().__init__(name, base_price)
        if size not in self.SIZES:
            raise ValueError(f"Неизвестный размер: {size}")
        self.size = size

    def calculatePrice(self) -> float:
        if self.size == "большая":
            return self.base_price * 1.30
        return self.base_price

    def getDisplayName(self) -> str:
        return f"Пицца «{self.name}» ({self.size})"


class Drink(MenuItem):
    def __init__(self, name: str, base_price: float, isIce: bool = False):
        super().__init__(name, base_price)
        self.isIce = isIce

    def calculatePrice(self) -> float:
        return self.base_price

    def getDisplayName(self) -> str:
        return f"{self.name} со льдом" if self.isIce else self.name


class ComboSet(MenuItem):
    DISCOUNT = 0.15

    def __init__(self, name: str, items: list):
        self.items = list(items)
        super().__init__(name, sum(i.calculatePrice() for i in self.items))

    def calculatePrice(self) -> float:
        total = sum(item.calculatePrice() for item in self.items)
        return total * (1 - self.DISCOUNT)     # скидка 15%

    def getDisplayName(self) -> str:
        inner = ", ".join(item.getDisplayName() for item in self.items)
        return f"Комбо «{self.name}» [{inner}] (-15%)"


class PaymentStrategy(ABC):

    def collectPayment(self, amount: float) -> bool:
        pass


class CardPayment(PaymentStrategy):
    def __init__(self, card_number: str, exp_month: int, exp_year: int, balance: float):
        self.__card_number = card_number
        self.__exp_month = exp_month
        self.__exp_year = exp_year
        self.__balance = balance

    def __isExpired(self) -> bool:
        today = date.today()
        return (self.__exp_year, self.__exp_month) < (today.year, today.month)

    def collectPayment(self, amount: float) -> bool:
        masked = "**** " + self.__card_number[-4:]
        if self.__isExpired():
            print(f"Карта {masked}: срок действия истёк "
                  f"({self.__exp_month:02d}/{self.__exp_year}). Оплата отклонена.")
            return False
        if amount > self.__balance:
            print(f"Карта {masked}: недостаточно средств. Оплата отклонена.")
            return False
        self.__balance -= amount
        print(f"С карты {masked} списано {amount:.2f}. Остаток: {self.__balance:.2f}")
        return True


class CashPayment(PaymentStrategy):
    def collectPayment(self, amount: float) -> bool:
        print(f"Оплата наличными курьеру при получении: {amount:.2f}")
        return True


class Order:
    STATUSES = ("Новый", "Готовится", "Доставляется", "Доставлен")

    def __init__(self):
        self.__items = []
        self.__status_index = 0
        self.__paid = False

    # --- только чтение снаружи ---
    @property
    def status(self) -> str:
        return self.STATUSES[self.__status_index]

    @property
    def items(self) -> tuple:
        return tuple(self.__items)

    @property
    def isPaid(self) -> bool:
        return self.__paid

    # --- управление заказом ---
    def addItem(self, item: MenuItem):
        if not isinstance(item, MenuItem):
            raise TypeError("В заказ можно добавлять только позиции меню")
        if self.__status_index >= 1:
            raise RuntimeError(
                f"Нельзя добавить блюдо: заказ уже в статусе «{self.status}»")
        self.__items.append(item)
        print(f"Добавлено: {item}")

    def nextStep(self):
        if self.__status_index == len(self.STATUSES) - 1:
            raise RuntimeError("Заказ уже доставлен, дальше этапов нет")
        if self.__status_index == 0:
            if not self.__items:
                raise RuntimeError("Нельзя начать готовить пустой заказ")
            if not self.__paid:
                raise RuntimeError("Сначала нужно оплатить заказ")
        self.__status_index += 1
        print(f"Статус заказа: {self.status}")

    def getTotalCost(self) -> float:
        return sum(item.calculatePrice() for item in self.__items)

    def pay(self, paymentMethod: PaymentStrategy) -> bool:
        if self.__paid:
            print("Заказ уже оплачен.")
            return True
        if not self.__items:
            raise RuntimeError("Нельзя оплатить пустой заказ")
        self.__paid = paymentMethod.collectPayment(self.getTotalCost())
        return self.__paid

    def printReceipt(self):
        print("\n----- ЧЕК -----")
        for i, item in enumerate(self.__items, 1):
            print(f"{i}. {item}")
        print(f"ИТОГО: {self.getTotalCost():.2f}")
        print(f"Статус: {self.status} | Оплачен: {'да' if self.__paid else 'нет'}")
        print("---------------\n")


if __name__ == "__main__":
    try:
        MenuItem("Что-то", 100)
    except TypeError as e:
        print("Ошибка абстракции:", e)

    order = Order()

    # Корзина
    order.addItem(Pizza("Маргарита", 500, "большая"))
    order.addItem(Drink("Кола", 100, isIce=True))
    combo = ComboSet("Обед", [
        Pizza("Пепперони", 600),
        Drink("Сок", 150),                               
    ])                                                   

    order.printReceipt()

    try:
        order.status = "Доставлен"
    except AttributeError:
        print("Ошибка инкапсуляции: статус нельзя менять напрямую\n")

    try:
        order.nextStep()
    except RuntimeError as e:
        print("Ошибка:", e)

    expired_card = CardPayment("1234567812345678", 1, 2024, balance=5000)
    order.pay(expired_card)
    order.pay(CashPayment())

    order.nextStep()
    try:
        order.addItem(Drink("Вода", 50))
    except RuntimeError as e:
        print("Ошибка:", e)

    order.nextStep()   
    order.nextStep()
    order.printReceipt()
    order2 = Order()
    order2.addItem(Pizza("Четыре сыра", 700, "маленькая"))
    valid_card = CardPayment("8765432187654321", 12, 2030, balance=1000)
    order2.pay(valid_card)
    order2.printReceipt()