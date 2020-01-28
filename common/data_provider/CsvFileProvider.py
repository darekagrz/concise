import csv


class CsvFileProvider:

    def __init__(self, datafile=None):
        self.datafile = datafile

    def get_list_by_column(self, column, unique=False):
        column_data = []
        if self.datafile is not None:
            csv_file = open(self.datafile, 'rt')
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                column_data.append(str(row[column]))
        else:
            raise Exception('File is not declared')

        if unique:
            return list(dict.fromkeys(column_data))

        return list(column_data)

    def set_data_file(self, datafile):
        self.datafile = datafile
