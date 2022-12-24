from dataclasses import dataclass

@dataclass
class Trip:
    def __init__(self):
        self.user = ""
        self.type = ""
        self.city = ""
        self.date = ""

    def __str__(self):
        return f"Персонаж: {self.user} \nТип поездки: {self.type} \nГород: {self.city} \nДата: {self.date}"
