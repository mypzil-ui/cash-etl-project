import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cash.db')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("=" * 60)
print("ПРОВЕРКА БАЗЫ ДАННЫХ")
print("=" * 60)

# Магазины
cursor.execute("SELECT COUNT(*) FROM cash_shops")
print(f"\n Магазинов: {cursor.fetchone()[0]}")

# Кассы
cursor.execute("SELECT COUNT(*) FROM cash_registers")
print(f" Касс: {cursor.fetchone()[0]}")

# Чеки
cursor.execute("SELECT COUNT(*) FROM cash_receipts")
print(f"🧾 Чеков: {cursor.fetchone()[0]}")

# Позиции
cursor.execute("SELECT COUNT(*) FROM cash_receipt_items")
print(f"📦 Позиций товаров: {cursor.fetchone()[0]}")

# Пример данных
print("\n" + "=" * 60)
print("ПРИМЕРЫ ДАННЫХ:")
print("=" * 60)

print("\n Магазины (первые 5):")
cursor.execute("SELECT * FROM cash_shops LIMIT 5")
for row in cursor.fetchall():
    print(f"   ID: {row[0]}, Название: {row[1]}")

print("\n🧾 Чеки (первые 5):")
cursor.execute("SELECT * FROM cash_receipts LIMIT 5")
for row in cursor.fetchall():
    print(f"   ID: {row[0]}, Doc: {row[1]}, Дата: {row[4]}")

print("\n📦 Позиции (первые 5):")
cursor.execute("SELECT * FROM cash_receipt_items LIMIT 5")
for row in cursor.fetchall():
    print(f"   ID: {row[0]}, Товар: {row[2]}, Кол-во: {row[4]}, Цена: {row[5]}")

conn.close()
print("\n✅ Проверка завершена!")
