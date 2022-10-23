CREATE TABLE visitors (id SERIAL PRIMARY KEY, time TIMESTAMP);
CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT, name TEXT, role INTEGER);
CREATE TABLE courses (id SERIAL PRIMARY KEY, course_name TEXT, par INT, lenght INT, holes INT, city TEXT, postcode INT, adress TEXT, created_at TIMESTAMP, rated INT, hardness INT);
CREATE TABLE reviews (id SERIAL PRIMARY KEY, course_id INTEGER REFERENCES courses, rating INT);
CREATE TABLE shape (id SERIAL PRIMARY KEY, course_id INTEGER REFERENCES courses, fit INT);