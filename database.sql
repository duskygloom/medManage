CREATE TABLE purchase (
    batch VARCHAR(50) PRIMARY KEY,
    title VARCHAR(100),
    amount INT(12),
    price DECIMAL(8, 2),
    purchasedate DATE,
    mfgdate DATE,
    expdate DATE,
    dealer VARCHAR(100)
);

CREATE TABLE sell (
    batch VARCHAR(50) PRIMARY KEY,
    title VARCHAR(100),
    amount INT(12),
    price DECIMAL(8, 2),
    selldate DATE,
    customer VARCHAR(100)
);
