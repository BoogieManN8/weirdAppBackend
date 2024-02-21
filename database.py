import pymysql

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.connection = pymysql.connect(host=host, user=user, password=password, db=database)
        self.cursor = self.connection.cursor()

    def create(self, table, data):
        placeholders = ', '.join(['%s'] * len(data))
        columns = ', '.join(data.keys())
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(sql, list(data.values()))
        self.connection.commit()

    def read(self, table, conditions=None):
        sql = f"SELECT * FROM {table}"
        if conditions:
            sql += " WHERE " + " AND ".join([f"{k} = %s" for k in conditions])
            self.cursor.execute(sql, list(conditions.values()))
        else:
            self.cursor.execute(sql)
        return self.cursor.fetchall()

    def update(self, table, data, conditions):
        data_update = ', '.join([f"{k} = %s" for k in data])
        condition_part = " AND ".join([f"{k} = %s" for k in conditions])
        sql = f"UPDATE {table} SET {data_update} WHERE {condition_part}"
        self.cursor.execute(sql, list(data.values()) + list(conditions.values()))
        self.connection.commit()

    def delete(self, table, conditions):
        condition_part = " AND ".join([f"{k} = %s" for k in conditions])
        sql = f"DELETE FROM {table} WHERE {condition_part}"
        self.cursor.execute(sql, list(conditions.values()))
        self.connection.commit()
        
    # USER
    def create_user(self, id, isGuest, isPremium, userToken, userLevel):
        sql = """
        INSERT INTO users (id, isGuest, isPremium, userToken, userLevel) 
        VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(sql, (id, isGuest, isPremium, userToken, userLevel))
        self.connection.commit()

    def read_user(self, id):
        sql = "SELECT * FROM users WHERE id = %s"
        self.cursor.execute(sql, (id,))
        return self.cursor.fetchone()

    def update_user(self, id, isGuest=None, isPremium=None, userToken=None, userLevel=None):
        updates = []
        parameters = []

        if isGuest is not None:
            updates.append("isGuest = %s")
            parameters.append(isGuest)
        
        if isPremium is not None:
            updates.append("isPremium = %s")
            parameters.append(isPremium)
        
        if userToken is not None:
            updates.append("userToken = %s")
            parameters.append(userToken)
        
        if userLevel is not None:
            updates.append("userLevel = %s")
            parameters.append(userLevel)
        
        sql = "UPDATE users SET " + ", ".join(updates) + " WHERE id = %s"
        parameters.append(id)
        self.cursor.execute(sql, parameters)
        self.connection.commit()

    def delete_user(self, id):
        sql = "DELETE FROM users WHERE id = %s"
        self.cursor.execute(sql, (id,))
        self.connection.commit()


    def close(self):
        self.connection.close()
