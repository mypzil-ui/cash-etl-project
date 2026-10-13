-- Включаем поддержку внешних ключей (в SQLite они по умолчанию отключены)
PRAGMA foreign_keys = ON;

-- Удаляем старые таблицы, если они остались (порядок важен: сначала зависимые)
DROP TABLE IF EXISTS cash_receipt_items;
DROP TABLE IF EXISTS cash_receipts;
DROP TABLE IF EXISTS cash_registers;
DROP TABLE IF EXISTS cash_shops;

-- Таблица магазинов
CREATE TABLE cash_shops (
    shop_id INTEGER PRIMARY KEY,
    shop_name TEXT NOT NULL
);

-- Таблица касс
CREATE TABLE cash_registers (
    cash_id INTEGER PRIMARY KEY AUTOINCREMENT,
    shop_id INTEGER NOT NULL,
    cash_number INTEGER NOT NULL,
    FOREIGN KEY (shop_id) REFERENCES cash_shops(shop_id)
);

-- Таблица чеков
CREATE TABLE cash_receipts (
    receipt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_id TEXT UNIQUE NOT NULL,
    shop_id INTEGER NOT NULL,
    cash_id INTEGER NOT NULL,
    receipt_date DATE DEFAULT (date('now')),
    FOREIGN KEY (shop_id) REFERENCES cash_shops(shop_id),
    FOREIGN KEY (cash_id) REFERENCES cash_registers(cash_id)
);

-- Таблица позиций чека
CREATE TABLE cash_receipt_items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    receipt_id INTEGER NOT NULL,
    item_name TEXT NOT NULL,
    category TEXT NOT NULL,
    amount INTEGER NOT NULL,
    price REAL NOT NULL,
    discount REAL DEFAULT 0,
    FOREIGN KEY (receipt_id) REFERENCES cash_receipts(receipt_id)
);

-- Индексы для ускорения запросов
CREATE INDEX idx_receipts_date ON cash_receipts(receipt_date);
CREATE INDEX idx_receipt_items_category ON cash_receipt_items(category);