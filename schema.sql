CREATE TABLE visitors (id SERIAL PRIMARY KEY, time TIMESTAMP);
CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);
CREATE TABLE courses (id SERIAL PRIMARY KEY, name TEXT, par INT, lenght INT, holes INT, adress TEXT);