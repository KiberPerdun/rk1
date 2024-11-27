from dataclasses import dataclass
from typing import List, Dict
from itertools import groupby
from pprint import pprint


@dataclass(order=True)
class Book:
    """Книга"""
    id:       int
    title:    str
    price:    float
    store_id: int

    @property
    def first_letter(self) -> str:
        return self.title[0]


@dataclass(order=True)
class Bookstore:
    """Книжный магазин"""
    id:   int
    name: str


@dataclass
class BookBookstore:
    """Связи многие-ко-многим"""
    book_id:  int
    store_id: int


bookstores: List[Bookstore] = \
    [
        Bookstore(1, 'Книжный мир'),
        Bookstore(2, 'Буквоед'),
        Bookstore(3, 'Азбука-Аттикус'),
        Bookstore(4, 'Читай-город'),
        Bookstore(5, 'Дом книги'),
    ]

books: List[Book] = \
    [
        Book(1, 'Анна Каренина', 500.0, 1),
        Book(2, 'Преступление и наказание', 600.0, 2),
        Book(3, 'Алые паруса', 450.0, 3),
        Book(4, 'Мастер и Маргарита', 550.0, 2),
        Book(5, 'Алиса в стране чудес', 700.0, 1),
    ]

book_bookstores: List[BookBookstore] = \
    [
        BookBookstore(1, 1),
        BookBookstore(2, 2),
        BookBookstore(3, 3),
        BookBookstore(4, 2),
        BookBookstore(5, 1),
        BookBookstore(1, 3),
        BookBookstore(3, 2),
        BookBookstore(5, 2),
    ]


def main():

    store_dict: Dict[int, Bookstore] = {store.id: store for store in bookstores}

    one_to_many = \
        [
            (book, store_dict[book.store_id])
            for book in books
            if book.store_id in store_dict
        ]

    book_dict = {book.id: book for book in books}

    many_to_many = \
        [
            (book_dict[bb.book_id], store_dict[bb.store_id])
            for bb in book_bookstores
            if bb.book_id in book_dict and bb.store_id in store_dict
        ]

    print('Задание В1')
    res_1 = \
        [
            (book.title, store.name)
            for book, store in one_to_many
            if book.first_letter == 'А'
        ]
    pprint(res_1)

    print('\nЗадание В2')

    sorted_one_to_many = sorted(one_to_many, key=lambda x: x[1].name)
    grouped = groupby(sorted_one_to_many, key=lambda x: x[1].name)

    res_2 = sorted(
        [
            (store_name, min(book.price for book, _ in books_in_store))
            for store_name, books_in_store in grouped
        ],
        key=lambda x: x[1]
    )
    pprint(res_2, width=60)

    print('\nЗадание В3')

    pprint([(book.title, book.price, store.name) for book, store in sorted(many_to_many, key=lambda x: x[0].title)])


if __name__ == '__main__':
    main()
