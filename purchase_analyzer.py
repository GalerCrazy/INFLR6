import csv
from typing import List, Dict, Any


def read_purchases(path: str) -> List[Dict[str, Any]]:
    """
    Читает файл с покупками и возвращает список валидных записей.
    """
    purchases = []
    
    with open(path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
                
            parts = line.split(';')
            if len(parts) != 5:
                continue
            
            try:
                date, category, name, price_str, qty_str = parts
                
                # Удаляем лишние пробелы
                date = date.strip()
                category = category.strip()
                name = name.strip()
                price_str = price_str.strip()
                qty_str = qty_str.strip()
                
                # Пропускаем строки с пустыми значениями
                if not all([date, category, name, price_str, qty_str]):
                    continue
                
                # Пробуем преобразовать price и qty
                try:
                    price = float(price_str)
                except ValueError:
                    continue
                    
                try:
                    qty = float(qty_str)
                except ValueError:
                    continue
                
                # Проверяем на отрицательные значения
                if price < 0 or qty < 0:
                    continue
                
                # Все проверки пройдены
                purchases.append({
                    'date': date,
                    'category': category,
                    'name': name,
                    'price': price,
                    'qty': qty
                })
                
            except Exception:
                continue
    
    return purchases


def count_errors(path: str) -> int:
    """
    Возвращает количество строк с ошибками.
    """
    total_lines = 0
    valid_lines = 0
    
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            total_lines += 1
            
            if not line:
                continue
                
            parts = line.split(';')
            if len(parts) != 5:
                continue
            
            try:
                date, category, name, price_str, qty_str = parts
                
                # Проверяем непустые значения
                if not all([date.strip(), category.strip(), name.strip(), 
                           price_str.strip(), qty_str.strip()]):
                    continue
                
                # Проверяем числовые значения
                try:
                    price = float(price_str.strip())
                    qty = float(qty_str.strip())
                except ValueError:
                    continue
                
                # Проверяем неотрицательные значения
                if price < 0 or qty < 0:
                    continue
                
                valid_lines += 1
                
            except Exception:
                continue
    
    return total_lines - valid_lines


def total_spent(purchases: List[Dict[str, Any]]) -> float:
    """
    Возвращает общую сумму всех покупок.
    """
    total = 0.0
    for purchase in purchases:
        total += purchase['price'] * purchase['qty']
    return round(total, 2)


def spent_by_category(purchases: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Возвращает сумму трат по категориям.
    """
    categories = {}
    for purchase in purchases:
        category = purchase['category']
        amount = purchase['price'] * purchase['qty']
        categories[category] = categories.get(category, 0) + amount
    
    # Округляем значения
    for category in categories:
        categories[category] = round(categories[category], 2)
    
    return categories


def top_n_expensive(purchases: List[Dict[str, Any]], n: int = 3) -> List[Dict[str, Any]]:
    """
    Возвращает топ-N самых дорогих покупок.
    """
    # Добавляем поле total к каждой покупке
    purchases_with_total = []
    for purchase in purchases:
        purchase_copy = purchase.copy()
        purchase_copy['total'] = purchase['price'] * purchase['qty']
        purchases_with_total.append(purchase_copy)
    
    # Сортируем по убыванию total
    sorted_purchases = sorted(purchases_with_total, 
                            key=lambda x: x['total'], 
                            reverse=True)
    
    # Возвращаем первые N элементов
    return sorted_purchases[:n]


def write_report(purchases: List[Dict[str, Any]], errors: int, out_path: str):
    """
    Записывает отчет в файл.
    """
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("=== ОТЧЕТ О ПОКУПКАХ ===\n\n")
        
        # Статистика
        f.write(f"Количество валидных записей: {len(purchases)}\n")
        f.write(f"Количество ошибочных записей: {errors}\n")
        f.write(f"Общая сумма потраченного: {total_spent(purchases):.2f}\n\n")
        
        # По категориям
        f.write("=== ТРАТЫ ПО КАТЕГОРИЯМ ===\n")
        categories = spent_by_category(purchases)
        for category, amount in sorted(categories.items()):
            f.write(f"{category}: {amount:.2f}\n")
        
        # Топ-3 покупки
        f.write("\n=== ТОП-3 САМЫХ ДОРОГИХ ПОКУПОК ===\n")
        top_purchases = top_n_expensive(purchases, 3)
        for i, purchase in enumerate(top_purchases, 1):
            total = purchase['price'] * purchase['qty']
            f.write(f"{i}. {purchase['date']} | {purchase['category']} | "
                   f"{purchase['name']} | {purchase['price']} x {purchase['qty']} = {total:.2f}\n")