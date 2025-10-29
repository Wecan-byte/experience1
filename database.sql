-- 校园二手物品管理系统 数据库建表脚本
CREATE DATABASE IF NOT EXISTS campus_used_goods CHARACTER SET utf8mb4;
USE campus_used_goods;

-- 删除已存在的表（按外键依赖顺序）
DROP TABLE IF EXISTS logs;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(50),
    address VARCHAR(200),
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    seller_id INT,
    location VARCHAR(200),
    status VARCHAR(20),
    FOREIGN KEY (seller_id) REFERENCES users(user_id)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    buyer_id INT,
    product_id INT,
    order_time DATETIME,
    status VARCHAR(20),
    FOREIGN KEY (buyer_id) REFERENCES users(user_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE logs (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    action VARCHAR(100),
    details TEXT,
    log_time DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
