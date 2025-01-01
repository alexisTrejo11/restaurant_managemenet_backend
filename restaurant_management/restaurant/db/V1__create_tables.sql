-- Diner Area
CREATE TABLE menu_items (
     id SERIAL PRIMARY KEY,
     name VARCHAR(255) NOT NULL,
     price DECIMAL(10, 2) NOT NULL,
     description VARCHAR(255),
     category VARCHAR(255) NOT NULL CHECK (category IN ('DRINKS', 'ALCOHOL_DRINKS', 'BREAKFASTS', 'STARTERS', 'MEALS', 'DESSERTS', 'EXTRAS')),
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE menu_extras (
     id SERIAL PRIMARY KEY,
     name VARCHAR(255) NOT NULL,
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tables (
     id SERIAL PRIMARY KEY,
     number INT NOT NULL,
     capacity INT NOT NULL,
     is_available BOOLEAN DEFAULT TRUE,
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Kitchen
CREATE TABLE orders (
     id SERIAL PRIMARY KEY,
     table_id INT NOT NULL,
     status VARCHAR(255) NOT NULL CHECK (status IN ('IN_PROGRESS', 'COMPLETED', 'CANCELLED')),
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
     end_at TIMESTAMP
);

CREATE TABLE order_items (
     id SERIAL PRIMARY KEY,
     menu_item_id INT NOT NULL,
     menu_extra_id INT,
     quantity INT NOT NULL,
     order_id INT NOT NULL,
     notes VARCHAR(255),
     added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
     is_delivered BOOLEAN DEFAULT FALSE
);

CREATE TABLE ingredients (
     id SERIAL PRIMARY KEY,
     menu_item_id INT,
     name VARCHAR(255) NOT NULL,
     unit VARCHAR(10) NOT NULL,
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE stocks(
     id SERIAL PRIMARY KEY,
     ingredient_id INT NOT NULL REFERENCES ingredients(id),
     total_stock INT NOT NULL,
     optimal_stock_quantity INT NOT NULL,
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE stock_transactions (
     id SERIAL PRIMARY KEY,
     ingredient_quantity int NOT NULL,
     stock_id int NOT NULL,
     transaction_type VARCHAR(3) CHECK (transaction_type IN ('IN', 'OUT')),
     date TIMESTAMP,
     ingredient_id int NOT NULL
);

-- Clients
CREATE TABLE reservations (
     id SERIAL PRIMARY KEY,
     name VARCHAR(255) NOT NULL,
     email VARCHAR(255),
     phone_number VARCHAR(255),
     customer_number INT NOT NULL,
     table_id INT NOT NULL,
     reservation_date TIMESTAMP NOT NULL,
     status VARCHAR(255) NOT NULL CHECK (status IN ('BOOKED', 'ATTENDED', 'NOT_ATTENDED', 'CANCELLED')),
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
     cancelled_at TIMESTAMP
);

CREATE TABLE payments (
     id SERIAL PRIMARY KEY,
     order_id int,
     payment_method VARCHAR(255) CHECK (payment_method IN ('CASH, CARD, TRANSACTION')),
     payment_status VARCHAR(255) CHECK (payment_method IN ('PENDING, COMPLETED, CANCELLED')),
     sub_total DECIMAL(10, 2) NOT NULL,
     disccount DECIMAL(10, 2) NOT NULL,
     vat_rate DECIMAL(10, 2) NOT NULL, --0.16
     vat DECIMAL(10, 2) NOT NULL,    --12.00 MXN
     currency_type VARCHAR(255) CHECK (currency_type IN ('MXN', 'USD', 'EUR')),
     total DECIMAL(10, 2) NOT NULL,
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
     paid_at TIMESTAMP
);

ALTER TABLE orders 
    ADD CONSTRAINT order_table_fk
    FOREIGN KEY (table_id) REFERENCES tables(id);

ALTER TABLE stocks 
    ADD CONSTRAINT stock_ingredient_fk
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id);

ALTER TABLE stock_transactions
    ADD CONSTRAINT transaction_stock_fk
    FOREIGN KEY (stock_id) REFERENCES stocks(id);

ALTER TABLE reservations 
    ADD CONSTRAINT reservation_table_fk
    FOREIGN KEY (table_id) REFERENCES tables(id);

ALTER TABLE payments 
     ADD CONSTRAINT payment_order_fk
    FOREIGN KEY (order_id) REFERENCES orders(id);
