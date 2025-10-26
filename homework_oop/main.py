import csv
import os

# Б13-403 Т. Вязовик

class Solver:
    def __init__(self, filepath):
        self.db = []
        with open(filepath, 'r', encoding="utf-8") as file:
            reader = csv.reader(file)
            self.fields = next(reader)
            for row in reader:
                self.db.append(dict(zip(self.fields, row)))
        self.commands = []
    def select(self, name, value):
        self.commands.append(("select", name, value))
    def sort(self, name, descending=False):
        self.commands.append(("sort", name, descending))
    def group(self, name):
        self.commands.append(("sort", name, False))
    def execute(self):
        ans = []
        for cmd in self.commands:
            if cmd[0] == "select":
                if cmd[1] not in self.fields:
                    print(f"Unable to find field {cmd[1]}. Maybe you ment one of these?\n", *self.fields)
                    continue
                
                req = []
                for row in self.db:
                    if row[cmd[1]] == cmd[2]:
                        req.append(row.copy())
                ans.append(req)
            elif cmd[0] == "sort":
                if cmd[1] not in self.fields:
                    print(f"Unable to find field {cmd[1]}. Maybe you ment one of these?\n", *self.fields)
                    continue

                self.db = sorted(self.db, key=(lambda row: row[cmd[1]]), reverse=cmd[2])
        self.commands = []
        return ans

class Calc:
    def __init__(self, solver):
        self.solver = solver
    def median(self):
        backup = self.solver.db.copy()
        cmd_backup = self.solver.commands.copy()
        self.solver.commands = []
        self.solver.sort("Size")
        self.solver.execute()
        ans = self.solver.db[len(self.solver.db) // 2]['Size']
        self.solver.db = backup
        self.solver.cmd_backup = cmd_backup
        return ans
    def likest(self):
        backup = self.solver.db.copy()
        cmd_backup = self.solver.commands.copy()
        self.solver.commands = []
        self.solver.sort("Stars")
        self.solver.execute()
        ans = self.solver.db[-1]
        self.solver.db = backup
        self.solver.cmd_backup = cmd_backup
        return ans
    def silent(self):
        backup = self.solver.db.copy()
        cmd_backup = self.solver.commands.copy()
        self.solver.commands = []
        self.solver.select("Language", "")
        ans = self.solver.execute()[0]
        self.solver.db = backup
        self.solver.cmd_backup = cmd_backup
        return ans
    def perflect(self):
        backup = self.solver.db.copy()
        cmd_backup = self.solver.commands.copy()
        self.solver.commands = []
        self.solver.sort("*And here I put my name for commit number field, if I had one*")
        self.solver.execute()
        ans = self.solver.db[-10:]
        self.solver.db = backup
        self.solver.cmd_backup = cmd_backup
        return ans
    def niceones(self):
        backup = self.solver.db.copy()
        cmd_backup = self.solver.commands.copy()
        self.solver.commands = []
        self.solver.select("Stars", "69")
        ans = self.solver.execute()[0]
        self.solver.db = backup
        self.solver.cmd_backup = cmd_backup
        return ans


if __name__ == "__main__":
    print(os.getcwd())
    solver = Solver("./repositories.csv")
    print(solver.db[:5])