CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY ,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(200) NOT NULL,
    password VARCHAR(200) NOT NULL,
    company_name VARCHAR(200) NOT NULL
);"""

CREATE_SEQUENCES_TABLE = """CREATE TABLE IF NOT EXISTS sequences (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    num_steps INT NOT NULL,
    description VARCHAR(100) ARRAY,
    user_id int,
    FOREIGN KEY(user_id) REFERENCES users(id)
);"""

CREATE_PREFERENCES_TABLE = """CREATE TABLE IF NOT EXISTS preferences(
    id SERIAL PRIMARY KEY,
    language VARCHAR(50) NOT NULL,
    user_id int FOREIGN KEY REFRENCES users(id)
);"""


INSERT_INTO_SEQUENCE_TABLE = """INSERT INTO sequences (title, num_steps, description)
VALUES (%s, %s, %s) RETURNING id;
"""

INSERT_INTO_USERS_TABLE = """INSERT INTO users (name, email, password, company_name)
VALUES (%s, %s, %s, %s);
"""

UPDATE_INTO_SEQUENCE_TABLE = """UPDATE sequences SET title = %s, num_steps = %s, description = %s WHERE id = %s"""


GET_SEQUENCE_DATA = """SELECT * FROM sequences WHERE id = %s"""



