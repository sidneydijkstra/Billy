
class CSVTable():
    def __init__(self, columnHeaders):
        self.columnHeaders = columnHeaders
        self.rows = []


    # header util
    def headers(self):
        return self.columnHeaders

    # row util
    def add(self, row):
        self.rows.append(row)

    def get(self, limit=10, startTop=True):
        if len(self.rows) <= limit:
            return self.rows
        return self.rows[0:limit] if startTop else self.rows[len(self.rows)-limit:len(self.rows)]

    def pick(self, start, end):
        if end <= len(self.rows) and end >= 0 and start <= len(self.rows) and start >= 0:
            return self.rows[start:end]
        return None

    def find(self, header, value): # TODO
        index = -1
        for i in range(len(self.columnHeaders)):
            if self.columnHeaders[i] == header:
                index = i
                break

        if index == -1:
            return None

        for row in self.rows:
            if row[index] == value:
                return row

    def update(self, header, value, content):
        index = -1
        for i in range(len(self.columnHeaders)):
            if self.columnHeaders[i] == header:
                index = i
                break

        if index == -1:
            return

        for i in range(len(self.rows)):
            if self.rows[i][index] == value:
                self.rows[i] = content
                return




    def all(self):
        return self.rows

    # util
    def show(self):
        print("Table:")
        print(self.columnHeaders)
        print("Content:")
        for row in self.rows:
            print(row)
