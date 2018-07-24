

class DataSet(object):

    def __init__(self):
        self.row = 0
        self.data = {}
        self.max_row = 0
        self.max_column = 0
        self.filled_columns = 0

    def set_current_row(self, row: int):
        if row < 0:
            print("Row number cannot be lower than zero!")
            return
        self.row = row

    def get_current_row(self):
        return self.row

    def next(self):
        self.row += 1

    def previous(self):
        if self.row == 0:
            raise Exception("Cannot go back a row, row is currently 0!")
        self.row -= 1

    def write_column(self, column: int, value):

        if column < 0:
            raise Exception("Column number cannot be less than zero!")

        if self.row not in self.data:
            self.data[self.row] = {}
        if column not in self.data[self.row]:
            self.filled_columns += 1
        self.data[self.row][column] = value

        if self.row > self.max_row:
            self.max_row = self.row
        if column > self.max_column:
            self.max_column = column

    def write(self, row: int, column: int, value):

        if column < 0:
            raise Exception("Column number cannot be less than zero!")
        if row < 0:
            raise Exception("Row number cannot be less than zero!")

        if row not in self.data:
            self.data[row] = {}
        if column not in self.data[row]:
            self.filled_columns += 1
        self.data[row][column] = value

        if row > self.max_row:
            self.max_row = row
        if column > self.max_column:
            self.max_column = column

    def read_column(self, column: int):
        if self.row in self.data:
            if column in self.data[self.row]:
                return self.data[self.row][column]
            else:
                raise Exception("Column #" + str(column) + " has no stored value!")
        else:
            raise Exception("Current row number (#" + str(self.row) + ") has no stored values!")

    def is_row_written(self, row: int):
        return row in self.data

    def is_column_written(self, row: int, column: int):
        return self.is_row_written(row) and column in self.data[row]

    def get_row_count(self):
        return len(self.data)

    def get_max_row(self):
        return self.max_row

    def get_max_column(self):
        return self.max_column

    def save_to_file(self, file_path: str, condense: bool=False):

        # Open the file with write privileges
        fh = open(file_path, "w+")

        # Turn all the rows into lines in the file.
        for key in self.data:
            row = self.data[key]
            line = str(key) + ": "
            if condense:
                line = ""
            i = 0
            for column_index in row:
                sep = ", "
                if i == len(row) - 1:
                    sep = ""
                line += str(row[column_index]).strip() + sep
                i += 1

            fh.write(line.strip() + "\n")

        fh.close()

    def __str__(self):
        return ("Dataset\n" +
                "Size: %s rows, %s columns\n"
                "Existing rows: %s/%s\n"
                "Filled values: %s/%s (%d%%)") % (self.get_max_row() + 1, self.get_max_column() + 1,
                                                  self.get_row_count(), self.get_max_row() + 1,
                                                  str(self.filled_columns),
                                                  str((self.get_max_row() + 1) * (self.get_max_column() + 1)),
                                                  (self.filled_columns /
                                                  ((self.get_max_row() + 1) * (self.get_max_column() + 1))) * 100.0
                                                  )

