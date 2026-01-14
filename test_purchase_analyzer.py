import pytest
import os
import tempfile
from purchase_analyzer import *


def create_test_file(content: str) -> str:
    """Создает временный файл с заданным содержимым."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        f.write(content)
    return f.name


def test_read_valid_purchases():
    """Тест чтения валидных записей."""
    content = """2025-09-01;food;Milk;1.20;2
2025-09-01;transport;Bus;1.50;4"""
    
    filename = create_test_file(content)
    purchases = read_purchases(filename)
    
    assert len(purchases) == 2
    assert purchases[0]['category'] == 'food'
    assert purchases[0]['price'] == 1.20
    assert purchases[0]['qty'] == 2.0
    assert purchases[1]['category'] == 'transport'
    
    os.unlink(filename)


def test_skip_invalid_lines():
    """Тест пропуска строк с ошибками."""
    content = """2025-09-01;food;Milk;1.20;2
invalid_line
2025-09-01;food;;1.20;2
2025-09-01;food;Bread;not_number;1
2025-09-01;food;Eggs;-1.20;2
2025-09-01;food;Butter;1.20;-1
2025-09-01;food;Cheese;1.20;1;extra_field"""
    
    filename = create_test_file(content)
    purchases = read_purchases(filename)
    
    assert len(purchases) == 1  # Только первая строка валидна
    
    os.unlink(filename)


def test_count_errors():
    """Тест подсчета ошибок."""
    content = """2025-09-01;food;Milk;1.20;2
invalid_line
2025-09-01;food;Bread;not_number;1
2025-09-01;food;Eggs;1.50;3"""
    
    filename = create_test_file(content)
    errors = count_errors(filename)
    
    assert errors == 2  # 2 строки с ошибками
    
    os.unlink(filename)


def test_total_spent():
    """Тест расчета общей суммы."""
    purchases = [
        {'price': 1.20, 'qty': 2},
        {'price': 2.50, 'qty': 1},
        {'price': 0.85, 'qty': 3}
    ]
    
    total = total_spent(purchases)
    expected = (1.20 * 2) + (2.50 * 1) + (0.85 * 3)
    
    assert total == round(expected, 2)


def test_spent_by_category():
    """Тест расчета сумм по категориям."""
    purchases = [
        {'category': 'food', 'price': 1.20, 'qty': 2},
        {'category': 'food', 'price': 0.85, 'qty': 1},
        {'category': 'transport', 'price': 1.50, 'qty': 4},
        {'category': 'transport', 'price': 12.00, 'qty': 1}
    ]
    
    categories = spent_by_category(purchases)
    
    assert round(categories['food'], 2) == round((1.20 * 2) + (0.85 * 1), 2)
    assert round(categories['transport'], 2) == round((1.50 * 4) + (12.00 * 1), 2)


def test_top_n_expensive():
    """Тест поиска самых дорогих покупок."""
    purchases = [
        {'name': 'Cheap', 'price': 1.0, 'qty': 1},
        {'name': 'Medium', 'price': 5.0, 'qty': 2},
        {'name': 'Expensive', 'price': 10.0, 'qty': 3},
        {'name': 'Average', 'price': 3.0, 'qty': 2}
    ]
    
    top3 = top_n_expensive(purchases, 3)
    
    assert len(top3) == 3
    assert top3[0]['name'] == 'Expensive'  # 10*3 = 30
    assert top3[1]['name'] == 'Medium'     # 5*2 = 10
    assert top3[2]['name'] == 'Average'    # 3*2 = 6


if __name__ == "__main__":
    pytest.main([__file__, "-v"])