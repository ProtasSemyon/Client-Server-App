INSERT INTO customers (first_name, last_name, email, phone)
VALUES
    ('Сергей', 'Иванов', 'ivanovsergei@mail.ru', '555-1234'),
    ('Анна', 'Петрова', 'petrovaanna@gmail.com', '555-5678'),
    ('Дмитрий', 'Сидоров', 'dmitriysidorov@hotmail.com', '555-9012'),
    ('Елена', 'Кузнецова', 'kuznetsova.elena@gmail.com', '555-3456'),
    ('Иван', 'Смирнов', 'ivan_smirnov@yahoo.com', '555-7890');

INSERT INTO orders (customer_id, order_date, total_amount)
VALUES
    (1, '2022-02-01', 256.50),
    (1, '2022-03-15', 124.99),
    (2, '2022-02-28', 789.00),
    (3, '2022-04-02', 45.75),
    (4, '2022-03-07', 167.85),
    (5, '2022-03-21', 679.99),
    (5, '2022-04-02', 235.50);

INSERT INTO order_items (order_id, product_id, quantity, price) 
VALUES
  (1, 1, 2, 399.99),
  (1, 3, 1, 59.99),
  (2, 2, 1, 299.99),
  (2, 5, 2, 49.99),
  (3, 4, 1, 799.99),
  (4, 1, 1, 399.99),
  (4, 3, 3, 59.99),
  (4, 5, 1, 49.99),
  (5, 2, 2, 299.99);


INSERT INTO products (product_name, brand, category, description, price, stock_quantity)
VALUES 
    ('Laptop 15.6 inch', 'Dell', 'Laptops', 'Dell Inspiron 15 3000 Series, 15.6 inch HD, Intel Core i5-7200U, 8GB DDR4 RAM, 256GB SSD, Windows 10 Home', 699.99, 50),
    ('Smartphone 6.2 inch', 'Samsung', 'Smartphones', 'Samsung Galaxy S21, 6.2 inch, 5G, 8GB RAM, 128GB storage, Phantom Gray', 799.99, 100),
    ('Tablet 10.2 inch', 'Apple', 'Tablets', 'Apple iPad 10.2 inch, 8th generation, 32GB, Wi-Fi, Space Gray', 329.99, 30),
    ('Smartwatch', 'Apple', 'Wearable Technology', 'Apple Watch Series 6, GPS, 44mm Space Gray Aluminum Case with Black Sport Band', 429.99, 20),
    ('Wireless Earbuds', 'Sony', 'Audio Accessories', 'Sony WF-1000XM4 true wireless earbuds, noise cancelling, 8 hours battery life, black', 279.99, 50);

INSERT INTO suppliers (supplier_name, contact_name, email, phone)
VALUES
    ('ABC Electronics', 'John Doe', 'johndoe@abcelectronics.com', '555-1234'),
    ('XYZ Electronics', 'Jane Smith', 'janesmith@xyz.com', '555-5678'),
    ('Tech Company', 'Bob Johnson', 'bjohnson@techco.com', '555-4321'),
    ('TechMart', 'Alice Brown', 'abrown@techmart.com', '555-8765'),
    ('ElectroWorld', 'Mike Wilson', 'mwilson@electroworld.com', '555-1111');
