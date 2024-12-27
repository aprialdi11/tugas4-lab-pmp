CREATE DATABASE musik;

USE musik;

CREATE TABLE lagu (
    id INT AUTO_INCREMENT PRIMARY KEY,
    judul VARCHAR(255) NOT NULL,
    penyanyi VARCHAR(255) NOT NULL,
    genre VARCHAR(100) NOT NULL,
    tahun_rilis YEAR NOT NULL
);