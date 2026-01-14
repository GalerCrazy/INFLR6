import purchase_analyzer as pa


def main():
    input_file = "purchases.txt"
    output_file = "report.txt"
    
    # Читаем валидные покупки
    purchases = pa.read_purchases(input_file)
    
    # Считаем ошибки
    errors = pa.count_errors(input_file)
    
    # Создаем отчет
    pa.write_report(purchases, errors, output_file)
    
    print(f"Отчет создан: {output_file}")
    print(f"Валидных записей: {len(purchases)}")
    print(f"Ошибок: {errors}")
    print(f"Общая сумма: {pa.total_spent(purchases):.2f}")