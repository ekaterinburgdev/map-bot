from datetime import datetime

class Okn:
    def __init__(self, name: str, order_link: str, date: datetime.date) -> None:
        self.name = name
        self.order_link = order_link
        self.date = date

    def __str__(self) -> str:
        return f'{self.name}\n{self.order_link}\n'