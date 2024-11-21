from dataclasses import dataclass
from termcolor import colored


@dataclass
class Player:
    name: str
    symbol: str
    color: str

    def __str__(self):
        return colored(self.symbol, self.color)

    def hl(self):
        return colored(self.symbol, "blue")

    def __eq__(self, other):
        return type(other) is Player and self.symbol == other.symbol
