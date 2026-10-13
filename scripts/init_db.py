import sqlite3
import os
import sys

# Определяем пути
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'cash.db')
SQL_PATH = os.path.join(BASE_DIR, 'sql', 'create_tables.sql')

print("=" * 60)
print("Инициализация базы данных Cash ETL")
print("=" * 60)
print(f"📁 Базовая директория: {BASE_DIR}")
print(f"💾 Путь к БД: {DB_PATH}")
print(f"📄 Путь к SQL: {SQL_PATH}")
print()

# Проверяем, что SQL-файл существует
if not os.path.exists(SQL_PATH):
    print(f"❌ ОШИБКА: SQL-файл не найден: {SQL_PATH}")
    print("   Убедись, что файл sql/create_tables.sql существует")
    sys.exit(1)

print("✅ SQL-файл найден")

# Читаем SQL-скрипт
try:
    with open(SQL_PATH, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    print(f"✅ SQL-скрипт прочитан ({len(sql_script)} символов)")
except Exception as e:
    print(f"❌ Ошибка чтения SQL-файла: {e}")
    sys.exit(1)

# Создаём базу и выполняем скрипт
try:
    # Удаляем старую базу, если она есть (для чистой инициализации)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"🗑  Удалена старая база: {DB_PATH}")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Включаем поддержку внешних ключей
    cursor.execute("PRAGMA foreign_keys = ON;")
    print("✅ Внешние ключи включены")
    
    # Выполняем SQL-скрипт
    cursor.executescript(sql_script)
    print("✅ SQL-скрипт выполнен")
    
    # Проверяем, что таблицы созданы
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = cursor.fetchall()
    
    print(f"\n📊 Созданные таблицы ({len(tables)} шт.):")
    for table in tables:
        print(f"   ✓ {table[0]}")
    
    conn.close()
    
    print(f"\n{'=' * 60}")
    print(f"🎉 База данных успешно создана!")
    print(f"📍 Файл: {DB_PATH}")
    print(f"{'=' * 60}")
    
except Exception as e:
    print(f"\n❌ ОШИБКА при создании базы данных: {e}")
    print(f"   Тип ошибки: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    sys.exit(1)