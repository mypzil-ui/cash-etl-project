import pandas as pd
import random
import os
from datetime import datetime, timedelta

# Конфигурация
NUM_SHOPS = 5  # Количество магазинов
MAX_CASHES_PER_SHOP = 3  # Максимум касс в магазине
MIN_CHECKS = 50  # Минимум чеков на кассу в день
MAX_CHECKS = 200  # Максимум чеков

# Каталог товаров
PRODUCTS = [
    ("Средство для мытья посуды", "Бытовая химия"),
    ("Стиральный порошок", "Бытовая химия"),
    ("Полотенце кухонное", "Текстиль"),
    ("Скатерть", "Текстиль"),
    ("Кастрюля 3л", "Посуда"),
    ("Сковорода", "Посуда"),
    ("Набор вилок", "Кухонная утварь"),
    ("Разделочная доска", "Кухонная утварь"),
    ("Ваза декоративная", "Декор"),
    ("Рамка для фото", "Декор"),
]

def generate_doc_id():
    """Генерирует уникально-буквенный ID чека"""
    return f"DOC-{random.randint(100000, 999999)}"

def generate_csv_for_shop_and_cash(shop_num, cash_num, date):
    """Генерирует CSV для одной кассы одного магазина за один день"""
    num_checks = random.randint(MIN_CHECKS, MAX_CHECKS)
    data = []
    
    for _ in range(num_checks):
        doc_id = generate_doc_id()
        item, category = random.choice(PRODUCTS)
        amount = random.randint(1, 5)
        price = round(random.uniform(50, 500), 2)
        discount = round(random.uniform(0, price * 0.3), 2) if random.random() > 0.7 else 0
        
        data.append({
            'doc_id': doc_id,
            'item': item,
            'category': category,
            'amount': amount,
            'price': price,
            'discount': discount
        })
    
    df = pd.DataFrame(data)
    
    # Создаём папку data, если её нет
    os.makedirs('data', exist_ok=True)
    
    # Сохраняем CSV
    filename = f'data/{shop_num}_{cash_num}.csv'
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"Сгенерирован файл: {filename} ({num_checks} чеков)")

def main():
    today = datetime.now()
    
    for shop in range(1, NUM_SHOPS + 1):
        num_cashes = random.randint(1, MAX_CASHES_PER_SHOP)
        for cash in range(1, num_cashes + 1):
            generate_csv_for_shop_and_cash(shop, cash, today)

if __name__ == '__main__':
    main()