CREATE TABLE visitors (id SERIAL PRIMARY KEY, time TIMESTAMP);
CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);
CREATE TABLE courses (id SERIAL PRIMARY KEY, course_name TEXT, par INT, lenght INT, holes INT, city TEXT, postcode INT, adress TEXT, created_at TIMESTAMP);
CREATE TABLE polls (id SERIAL PRIMARY KEY,topic TEXT,created_at TIMESTAMP);
CREATE TABLE choices (id SERIAL PRIMARY KEY,poll_id INTEGER REFERENCES polls,choice TEXT);
CREATE TABLE answers (id SERIAL PRIMARY KEY,choice_id INTEGER REFERENCES choices,sent_at TIMESTAMP);