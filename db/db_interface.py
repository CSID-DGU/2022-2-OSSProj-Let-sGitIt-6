import sqlite3


class InterfDB:

    def __init__(self, dbname):
        self.__DBNAME = dbname
        self.db = sqlite3.connect(self.__DBNAME)

    def init_db(self):
        with open("./db/schema.sql", 'r') as f:
            self.db.cursor().executescript(f.read())
        self.db.commit()

    def query_db(self, query, args=(), one=False):
        cursor = self.db.execute(query, args)
        result = [dict((cursor.description[idx][0], value) for idx, value in enumerate(row)) \
                  for row in cursor.fetchall()]
        return (result[0] if result else None) if one else result

    def commit(self):
        self.db.commit()

    def is_limit_data(self, score, limit=10):
        num_of_data = self.query_db("select count(score) from user;")[0]['count(score)']

        try:
            last_data = self.query_db("select score from user order by score asc;", one=True)['score']
        except:
            return False

        if num_of_data == limit:
            if score > last_data:
                self.query_db(f"delete from user where score={last_data};")
                self.commit()
                return False
            else:
                return True
        else:
            return False
