"""Функціонал для консольного бота помічника(2.0), який розпізнає команди, що вводяться з клавіатури,
                                    та відповідає відповідно до введеної команди."""
from collections import UserDict


class ValidationError(Exception):
    def __init__(self):
        super().__init__('The phone must have 10 numbers.')


class Field:
    """Базовий клас для полів запису."""

    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Клас для зберігання імені контакту."""
    pass


class Phone(Field):
    """Клас для зберігання номера телефону. Має валідацію формату (10 цифр)."""

    def __init__(self, value: str):
        if value.isdigit() and len(value) == 10:
            super().__init__(value)
        else:
            raise ValidationError


class Record:
    """Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів."""

    def __init__(self, name: str, phones: list[str, ...] = None):
        self.name = Name(name)
        self.phones = [Phone(phone) for phone in phones] if phones else []

    def add_phone(self, phone: str):
        """
        Додавання телефонів.

        :param phone: Бажаний номер телефону.
        """
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        """
        Видалення телефонів.

        :param phone: Бажаний номер телефону.
        """
        i = [v.value for v in self.phones].index(Phone(phone).value)
        self.phones.pop(i)

    def edit_phone(self, old_phone: str, new_phone: str):
        """
        Редагування телефонів.

        :param old_phone: Старий номер телефону.
        :param new_phone: Новий номер телефону.
        """
        i = [v.value for v in self.phones].index(Phone(old_phone).value)
        self.phones[i] = Phone(new_phone)

    def find_phone(self, phone: str) -> Phone | None:
        """
        Пошук телефону.

        :param phone: Бажаний номер телефону.
        :return: Об'єкт номера телефону(Phone) за вказаним номером(phone).
        """
        res = [p for p in self.phones if p.value == Phone(phone).value]
        if not res:
            return None
        return res[0]

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    """Клас для зберігання та управління записами."""

    def add_record(self, record: Record):
        """
        Додавання записів.

        :param record: Бажаний запис.
        """
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        """
        Пошук записів за іменем.

        :param name: Бажане ім'я для пошуку запису.
        :return: Об'єкт запису(Records) за вказаним ім'ям(name).
        """
        return self.data.get(name)

    def delete(self, name: str):
        """
        Видалення записів за іменем.

        :param name: Бажане ім'я для видалення запису.
        """
        self.data.pop(name)

    def __str__(self):
        res = ''
        n = 1
        for key in self.data:
            res += f'{n}. {self.data[key]}\n'
            n += 1
        return res
