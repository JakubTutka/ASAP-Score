import mysql.connector
import hashlib

class mysql_users:

    def __init__(self):

        self.connection = mysql.connector.connect(
            user = "root",
            password = "root",
            host = '127.0.0.1',
            database = 'asap_score',
            auth_plugin = 'mysql_native_password'
        )

        self.cursor = self.connection.cursor()

    def register(self, username, password, email):

        hashed_password = hashlib.sha256(bytes(password, encoding="ascii")).hexdigest()

        user_data = {
            'username' : username,
            'hashed_password' : hashed_password,
            'email' : email
        }
        register_query = "INSERT INTO users (username, hashed_password, email) VALUES (%(username)s, %(hashed_password)s, %(email)s)"

        self.cursor.execute(register_query, user_data)
        self.connection.commit()


    def deleta_all_users(self):

        query = "TRUNCATE TABLE users;"
        self.cursor.execute(query)
        self.connection.commit()


