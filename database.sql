create database medmanage;
use medmanage;


create table stock (
    batch varchar(50),
    medname varchar(100),
    quantity int(12),
    pricerate decimal(8, 2),
    dealer varchar(100),
    buydate date,
    mfgdate date,
    expdate date
);


create table sold (
    batch varchar(50),
    medname varchar(100),
    quantity int(12),
    pricerate decimal(8, 2),
    dealer varchar(100),
    buydate date,
    mfgdate date,
    expdate date
);


create table dumpbin (
    batch varchar(50),
    medname varchar(100),
    quantity int(12),
    pricerate decimal(8, 2),
    dealer varchar(100),
    buydate date,
    mfgdate date,
    expdate date
);


create table sell (
    batch varchar(50) primary key,
    medname varchar(100),
    quantity int(12),
    pricerate decimal(8, 2),
    customer varchar(100),
    selldate date
);