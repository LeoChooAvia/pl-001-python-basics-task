import pytest
from decimal import Decimal
from typing import Final

type Product = tuple[int, str, Decimal, int]

from ..utils import normalize_product_name, get_storage_str_representation
from ..crud import create_product, update_product

def test_normalize_product_name():
    assert normalize_product_name("  Cordless Drill  ") == "cordless drill"
    assert normalize_product_name("abc    def\tghi\tjkl") ==  "abc def ghi jkl"
    assert normalize_product_name(" \t\n ") ==  ""
    assert normalize_product_name("claw hammer") ==  "claw hammer"

def test_get_storage_str_representation():
    print(repr(get_storage_str_representation([(1, "saw", Decimal("9.90"), 5), (2, "axe", Decimal("12.00"), 8)])))
    print()
    print((get_storage_str_representation([(1, "saw", Decimal("9.90"), 5), (2, "axe", Decimal("12.00"), 8)])))
    print()

    print(repr(get_storage_str_representation([(10, "compressor", Decimal("1299.99"), 3), (2, "nail", Decimal("2.50"), 500)])))
    print()
    print(get_storage_str_representation([(10, "compressor", Decimal("1299.99"), 3), (2, "nail", Decimal("2.50"), 500)]))
    print()

    test1_str = """| ID | name | price | quantity |
|----|------|-------|----------|
| 1  | saw  | 9.90  | 5        |
| 2  | axe  | 12.00 | 8        |"""

    test2_str = """| ID | name       | price   | quantity |
|----|------------|---------|----------|
| 10 | compressor | 1299.99 | 3        |
| 2  | nail       | 2.50    | 500      |"""

    assert get_storage_str_representation([(1, "saw", Decimal("9.90"), 5), (2, "axe", Decimal("12.00"), 8)]) == test1_str
    assert get_storage_str_representation([(10, "compressor", Decimal("1299.99"), 3), (2, "nail", Decimal("2.50"), 500)]) == test2_str

def test_create_product(capsys):
    # Мои личные тесты
    assert create_product([(1, "saw", Decimal("9.90"), 5), (2, "axe", Decimal("12.00"), 8)], ("", Decimal("1.00"), 1)) == None
    captured = capsys.readouterr()
    assert captured.out == "product name must not be blank\n"

    assert create_product([(1, "saw", Decimal("9.90"), 5), (2, "axe", Decimal("12.00"), 8)], ("   ", Decimal("1.00"), 1)) == None
    captured = capsys.readouterr()
    assert captured.out == "product name must not be blank\n"

    assert create_product([(1, "saw", Decimal("9.90"), 5), (2, "axe", Decimal("12.00"), 8)], (" \n \t ", Decimal("1.00"), 1)) == None
    captured = capsys.readouterr()
    assert captured.out == "product name must not be blank\n"

    assert create_product([(1, "saw", Decimal("9.90"), 5), (2, "axe", Decimal("12.00"), 8)], ("saw", Decimal("1.00"), 1)) == None
    captured = capsys.readouterr()
    assert captured.out == "product name 'saw' is already taken\n"
    
    assert create_product([(1, "saw", Decimal("9.90"), 5), (2, "axe", Decimal("12.00"), 8)], (" SAw   ", Decimal("1.00"), 1)) == None
    captured = capsys.readouterr()
    assert captured.out == "product name 'saw' is already taken\n"

    assert create_product([(1, "saw", Decimal("9.90"), 5), (2, "axe", Decimal("12.00"), 8)], ("sword", Decimal("1.00"), 1)) == 3



    # Примеры из репы
    storage: list[Product] = []
    first_id = create_product(storage, ("  Cordless   Drill ", Decimal("89.999"), 12))
    second_id = create_product(storage, ("Claw Hammer", Decimal("9.9"), 40))
    # print(first_id)   # 1
    assert first_id == 1
    # print(second_id)  # 2
    assert second_id == 2
    # print(storage)
    # [(1, 'cordless drill', Decimal('90.00'), 12),
    #  (2, 'claw hammer', Decimal('9.90'), 40)]
    assert storage == [(1, 'cordless drill', Decimal('90.00'), 12), (2, 'claw hammer', Decimal('9.90'), 40)]

    storage: list[Product] = []
    create_product(storage, ("cordless drill", Decimal("50"), 3))
    result = create_product(storage, ("  CORDLESS   DRILL  ", Decimal("75"), 1))
    # печатает: product name 'cordless drill' is already taken
    captured = capsys.readouterr()
    assert captured.out == "product name 'cordless drill' is already taken\n"
    # print(result)   # None
    assert result == None
    # print(storage)  # [(1, 'cordless drill', Decimal('50.00'), 3)]
    assert storage == [(1, 'cordless drill', Decimal('50.00'), 3)]

    storage: list[Product] = []
    result = create_product(storage, ("     ", Decimal("10"), 5))
    # печатает: product name must not be blank
    captured = capsys.readouterr()
    assert captured.out == "product name must not be blank\n"
    # print(result)   # None
    assert result == None
    # print(storage)  # []
    assert storage == []

def test_update_product(capsys):
    storage: list[Product] = [
    (1, "cordless drill", Decimal("90.00"), 12),
    (2, "claw hammer", Decimal("9.90"), 40),
    ]

    result = update_product(storage, 2, ("  Rubber   Mallet ", Decimal("7.505"), 25))
    # print(result)   # (2, 'rubber mallet', Decimal('7.51'), 25)
    assert result == (2, 'rubber mallet', Decimal('7.51'), 25)
    # print(storage)
    # [(1, 'cordless drill', Decimal('90.00'), 12),
    #  (2, 'rubber mallet', Decimal('7.51'), 25)]
    assert storage == [(1, 'cordless drill', Decimal('90.00'), 12), (2, 'rubber mallet', Decimal('7.51'), 25)]

    storage: list[Product] = [
    (1, "cordless drill", Decimal("90.00"), 12),
    (2, "claw hammer", Decimal("9.90"), 40),
    ]

    result = update_product(storage, 1, ("CORDLESS  Drill", Decimal("85"), 10))
    # print(result)   # (1, 'cordless drill', Decimal('85.00'), 10)
    assert result == (1, 'cordless drill', Decimal('85.00'), 10)

    storage: list[Product] = [
    (1, "cordless drill", Decimal("90.00"), 12),
    (2, "claw hammer", Decimal("9.90"), 40),
    ]

    result = update_product(storage, 1, (" Claw Hammer ", Decimal("85"), 10))
    # печатает: product name 'claw hammer' is already taken
    captured = capsys.readouterr()
    assert captured.out == "product name 'claw hammer' is already taken\n"
    # print(result)   # None
    assert result == None
    # print(storage)
    # [(1, 'cordless drill', Decimal('90.00'), 12),
    #  (2, 'claw hammer', Decimal('9.90'), 40)]
    assert storage == [(1, 'cordless drill', Decimal('90.00'), 12), (2, 'claw hammer', Decimal('9.90'), 40)]

    storage: list[Product] = [
    (1, "cordless drill", Decimal("90.00"), 12),
    (2, "claw hammer", Decimal("9.90"), 40),
    ]

    result = update_product(storage, 99, ("saw", Decimal("20"), 5))
    # печатает: no product with id 99
    captured = capsys.readouterr()
    assert captured.out == "no product with id 99\n"
    # print(result)   # None
    assert result == None
    result = update_product(storage, 99, ("     ", Decimal("20"), 5))
    # печатает: product name must not be blank (а не no product with id 99)
    captured = capsys.readouterr()
    assert captured.out == "product name must not be blank\n"
    # print(result)   # None
    assert result == None