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
     payment_method VARCHAR(255) CHECK (payment_method IN ('CASH', 'CARD', 'TRANSACTION')),
     payment_status VARCHAR(255) CHECK (payment_method IN ('PENDING', 'COMPLETED', 'CANCELLED')),
     sub_total DECIMAL(10, 2) NOT NULL,
     disccount DECIMAL(10, 2) NOT NULL,
     vat_rate DECIMAL(10, 2) NOT NULL, --0.16
     vat DECIMAL(10, 2) NOT NULL,    --12.00 MXN
     currency_type VARCHAR(255) CHECK (currency_type IN ('MXN', 'USD', 'EUR')),
     total DECIMAL(10, 2) NOT NULL,
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
     paid_at TIMESTAMP
);

CREATE TABLE payment_items (
    id SERIAL PRIMARY KEY,                          
    payment_id INT NOT NULL,                      
    menu_item_id INT NOT NULL,                    
    order_item_id INT NOT NULL,                   
    menu_item_extra_id INT,                       
    price NUMERIC(10, 2) NOT NULL,                
    quantity INT NOT NULL CHECK (quantity > 0),   
    total NUMERIC(10, 2) NOT NULL,                
    CONSTRAINT fk_payment FOREIGN KEY (payment_id) REFERENCES public.payments (id) ON DELETE CASCADE
);

-- Create enum types for gender and role
CREATE TYPE user_gender AS ENUM ('male', 'female', 'other');
CREATE TYPE user_role AS ENUM ('admin', 'staff', 'customer');

-- Create users table
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone_number VARCHAR(15),
    hashed_password VARCHAR(255) NOT NULL,
    gender user_gender NOT NULL,
    birth_date DATE NOT NULL,
    role user_role NOT NULL,
    joined_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN NOT NULL DEFAULT true,
    is_verified BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_phone ON users(phone_number);
CREATE INDEX idx_users_created_at ON users(created_at);

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';


CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();


ALTER TABLE users 
    ADD CONSTRAINT users_birth_date_check 
    CHECK (birth_date <= CURRENT_DATE - INTERVAL '18 years');

ALTER TABLE users 
    ADD CONSTRAINT users_email_check 
    CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

ALTER TABLE users 
    ADD CONSTRAINT users_phone_check 
    CHECK (phone_number IS NULL OR phone_number ~ '^\+?1?\d{9,15}$');


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
