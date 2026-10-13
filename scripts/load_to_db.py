import sqlite3
import pandas as pd
import os
import re
from datetime import datetime

# Путь к базе данных SQLite (файл cash.db в корне проекта)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cash.db')


def get_connection():
    """Создаёт подключение к SQLite базе"""
    conn = sqlite3.connect(DB_PATH)
    # Включаем поддержку внешних ключей
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def get_or_create_shop(conn, shop_num):
    """Получает или создаёт магазин"""
    cursor = conn.cursor()
    cursor.execute("SELECT shop_id FROM cash_shops WHERE shop_id = ?", (shop_num,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute(
            "INSERT INTO cash_shops (shop_id, shop_name) VALUES (?, ?)",
            (shop_num, f"Магазин {shop_num}")
        )
        conn.commit()
        return shop_num


def get_or_create_cash(conn, shop_id, cash_num):
    """Получает или создаёт кассу"""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT cash_id FROM cash_registers WHERE shop_id = ? AND cash_number = ?",
        (shop_id, cash_num)
    )
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute(
            "INSERT INTO cash_registers (shop_id, cash_number) VALUES (?, ?)",
            (shop_id, cash_num)
        )
        conn.commit()
        return cursor.lastrowid


def load_csv_to_db(filepath, shop_num, cash_num):
    """Загружает CSV в БД"""
    conn = get_connection()
    
    try:
        shop_id = get_or_create_shop(conn, shop_num)
        cash_id = get_or_create_cash(conn, shop_id, cash_num)
        
        df = pd.read_csv(filepath)
        
        cursor = conn.cursor()
        
        # Создаём чек (используем первый doc_id как идентификатор)
        doc_id = str(df['doc_id'].iloc[0])
        cursor.execute("""
            INSERT INTO cash_receipts (doc_id, shop_id, cash_id, receipt_date)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(doc_id) DO NOTHING
        """, (doc_id, shop_id, cash_id, datetime.now().date().isoformat()))
        
        # Получаем ID чека
        cursor.execute("SELECT receipt_id FROM cash_receipts WHERE doc_id = ?", (doc_id,))
        receipt_id = cursor.fetchone()[0]
        
        # Загружаем позиции чека
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO cash_receipt_items 
                (receipt_id, item_name, category, amount, price, discount)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                receipt_id,
                str(row['item']),
                str(row['category']),
                int(row['amount']),
                float(row['price']),
                float(row['discount'])
            ))
        
        conn.commit()
        print(f"✓ Загружен файл: {filepath} ({len(df)} позиций)")
        
    except Exception as e:
        print(f" Ошибка при загрузке {filepath}: {e}")
        conn.rollback()
    finally:
        conn.close()


def main():
    # Проверяем, что база существует
    if not os.path.exists(DB_PATH):
        print(f" База данных не найдена: {DB_PATH}")
        print("  Сначала запусти: python scripts/init_db.py")
        return
    
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    processed_dir = os.path.join(data_dir, 'processed')
    os.makedirs(processed_dir, exist_ok=True)
    
    # Паттерн для имени файла: {{shop_num}}_{{cash_num}}.csv
    pattern = re.compile(r'^(\d+)_(\d+)\.csv$')
    
    files_loaded = 0
    files_skipped = 0
    
    for filename in os.listdir(data_dir):
        match = pattern.match(filename)
        if match:
            shop_num = int(match.group(1))
            cash_num = int(match.group(2))
            filepath = os.path.join(data_dir, filename)
            
            # Проверяем, не обработан ли уже файл
            processed_path = os.path.join(processed_dir, filename)
            if os.path.exists(processed_path):
                print(f"⏭  Пропущен (уже обработан): {filename}")
                files_skipped += 1
                continue
            
            load_csv_to_db(filepath, shop_num, cash_num)
            files_loaded += 1
            
            # Перемещаем файл в processed
            os.rename(filepath, processed_path)
            print(f"  → Перемещён в: {processed_path}")
    
    print(f"\n Загружено файлов: {files_loaded}")
    print(f"⏭ Пропущено файлов: {files_skipped}")

if __name__ == '__main__':
    main()