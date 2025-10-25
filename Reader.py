import csv

class Reader:
    def __init__(self):
        self.data = []

    def read(self, filename):
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for row in reader:
                self.data.append(row)
