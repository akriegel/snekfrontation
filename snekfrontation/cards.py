from abc import ABC


class Card(ABC):

    pass


class NumberCard(Card):

    def __init__(self, value: int):
        self.value = value


class TextCard(Card):

    def __init__(self, text: str):
        self.text = text
