class Animal:

    def __init__(self, name, species, age, weight, habitat):
        self.name = name
        self.species = species
        self.age = age
        self.weight = weight
        self.habitat = habitat

    def eat(self, food):
        return f"{self.name} ({self.species}) ест: {food}."

    def info(self):
        return (f"Имя: {self.name}, вид: {self.species}, возраст: {self.age} лет, "
                f"вес: {self.weight} кг, среда обитания: {self.habitat}")


class Reptile(Animal):
    """Пресмыкающиеся (рептилии)."""

    def __init__(self, name, species, age, weight, habitat,
                 scale_type, is_venomous, body_temperature):
        super().__init__(name, species, age, weight, habitat)
        self.scale_type = scale_type
        self.is_venomous = is_venomous
        self.body_temperature = body_temperature

    def bask_in_sun(self):
        self.body_temperature += 5
        return (f"{self.name} греется на солнце. "
                f"Температура тела: {self.body_temperature} °C.")

    def shed_skin(self):
        return f"{self.name} линяет и сбрасывает старую кожу ({self.scale_type})."


class Amphibian(Animal):

    def __init__(self, name, species, age, weight, habitat,
                 skin_moisture, has_tail, larval_stage):
        super().__init__(name, species, age, weight, habitat)
        self.skin_moisture = skin_moisture
        self.has_tail = has_tail
        self.larval_stage = larval_stage

    def breathe_through_skin(self):
        return (f"{self.name} дышит через кожу. "
                f"Влажность кожи: {self.skin_moisture}%.")

    def metamorphose(self):
        if self.larval_stage == "головастик":
            self.larval_stage = "взрослая особь"
            return f"{self.name} прошел метаморфоз и стал взрослой особью."
        return f"{self.name} сейчас на стадии: {self.larval_stage}."


if __name__ == "__main__":
    snake = Reptile("Каа", "Питон", 6, 12.5, "тропический лес",
                    "ороговевшая чешуя", False, 28)
    frog = Amphibian("Квака", "Лягушка", 1, 0.05, "пруд",
                     85, False, "головастик")

    print(snake.info())
    print(snake.eat("мышь"))
    print(snake.bask_in_sun())
    print(snake.shed_skin())
    print()
    print(frog.info())
    print(frog.eat("комаров"))
    print(frog.breathe_through_skin())
    print(frog.metamorphose())
