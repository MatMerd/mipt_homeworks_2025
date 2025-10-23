from .db import Database

class DBManager:
    _bases = dict()

    @staticmethod
    def openDBConnect(file_path):
        db = DBManager._bases.get(file_path, None)
        if db == None:
            db = Database(file_path)
            DBManager._bases[file_path] = [db, 1]
        else:
            db = db[0]
            DBManager._bases[file_path][1] += 1
        return db
    
    @staticmethod
    def closeDBConnect(file_path):
        db = DBManager._bases.get(file_path, None)
        if db == None or db[1] == 0:
            raise Exception("Database {file_name} is not open")
        elif db[1] > 1:
            DBManager._bases[file_path][1] -=1
        else:
            DBManager._bases.pop(file_path)