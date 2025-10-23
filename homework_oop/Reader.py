import csv

class CsvReader:
    def read(self):
        data = []
        with open('repositories.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                data.append(row)
        return data

