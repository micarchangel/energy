CREATE TABLE abonents (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(150),
    address TEXT,
    account_number VARCHAR(50) UNIQUE
);

CREATE TABLE meters (
    id SERIAL PRIMARY KEY,
    serial_number VARCHAR(50),
    type VARCHAR(50),
    install_date DATE,
    abonent_id INT REFERENCES abonents(id) ON DELETE CASCADE
);

CREATE TABLE readings (
    id SERIAL PRIMARY KEY,
    meter_id INT REFERENCES meters(id) ON DELETE CASCADE,
    reading_date DATE,
    value NUMERIC(10,2)
);

CREATE TABLE tariffs (
    id SERIAL PRIMARY KEY,
    zone VARCHAR(50),
    value NUMERIC(10,4),
    start_date DATE
);

CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    abonent_id INT REFERENCES abonents(id) ON DELETE CASCADE,
    pay_date DATE,
    amount NUMERIC(10,2),
    period VARCHAR(20)
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    login TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'operator', 'inspector', 'cashier'))
);

CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    action TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Пример пользователя-админа
INSERT INTO users (login, password_hash, role)
VALUES ('admin', 'admin_hash', 'admin');
