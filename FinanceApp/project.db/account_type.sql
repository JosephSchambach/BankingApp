CREATE TABLE account_type (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, account_type TEXT NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id));