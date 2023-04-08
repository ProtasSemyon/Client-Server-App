CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    brand VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER NOT NULL
);

CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    contact_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL
);

CREATE TABLE product_suppliers (
    product_supplier_id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    supplier_id INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);


INSERT INTO customers (customer_id, first_name, last_name, email, phone)
VALUES
    (1, 'Сергей', 'Иванов', 'ivanovsergei@mail.ru', '555-1234'),
    (2, 'Анна', 'Петрова', 'petrovaanna@gmail.com', '555-5678'),
    (3, 'Дмитрий', 'Сидоров', 'dmitriysidorov@hotmail.com', '555-9012'),
    (4, 'Елена', 'Кузнецова', 'kuznetsova.elena@gmail.com', '555-3456'),
    (5, 'Иван', 'Смирнов', 'ivan_smirnov@yahoo.com', '555-7890');

INSERT INTO orders (customer_id, order_date, total_amount)
VALUES
    (1, '2022-02-01', 256.50),
    (1, '2022-03-15', 124.99),
    (2, '2022-02-28', 789.00),
    (3, '2022-04-02', 45.75),
    (4, '2022-03-07', 167.85),
    (5, '2022-03-21', 679.99),
    (5, '2022-04-02', 235.50);


INSERT INTO products (product_id, product_name, brand, category, description, price, stock_quantity)
VALUES 
    (1,'Laptop 15.6 inch', 'Dell', 'Laptops', 'Dell Inspiron 15 3000 Series, 15.6 inch HD, Intel Core i5-7200U, 8GB DDR4 RAM, 256GB SSD, Windows 10 Home', 699.99, 50),
    (2,'Smartphone 6.2 inch', 'Samsung', 'Smartphones', 'Samsung Galaxy S21, 6.2 inch, 5G, 8GB RAM, 128GB storage, Phantom Gray', 799.99, 100),
    (3,'Tablet 10.2 inch', 'Apple', 'Tablets', 'Apple iPad 10.2 inch, 8th generation, 32GB, Wi-Fi, Space Gray', 329.99, 30),
    (4,'Smartwatch', 'Apple', 'Wearable Technology', 'Apple Watch Series 6, GPS, 44mm Space Gray Aluminum Case with Black Sport Band', 429.99, 20),
    (5,'Wireless Earbuds', 'Sony', 'Audio Accessories', 'Sony WF-1000XM4 true wireless earbuds, noise cancelling, 8 hours battery life, black', 279.99, 50);

INSERT INTO suppliers (supplier_name, contact_name, email, phone)
VALUES
    ('ABC Electronics', 'John Doe', 'johndoe@abcelectronics.com', '555-1234'),
    ('XYZ Electronics', 'Jane Smith', 'janesmith@xyz.com', '555-5678'),
    ('Tech Company', 'Bob Johnson', 'bjohnson@techco.com', '555-4321'),
    ('TechMart', 'Alice Brown', 'abrown@techmart.com', '555-8765'),
    ('ElectroWorld', 'Mike Wilson', 'mwilson@electroworld.com', '555-1111');

INSERT INTO product_suppliers (product_id, supplier_id) 
VALUES
(2, 5),
(1, 2),
(4, 4),
(5, 1),
(1, 4),
(3, 3),
(2, 3),
(1, 5),
(3, 4),
(4, 2);
