import os
import re
from models.csvtable import CSVTable

divider = "/;/;/"

class CSVFactory:
    # function for loading a .csv file
    # the file is parsed not by a ',' but with a divider like '/;/;/'
    # because a ',' is used in our strings
    def load(path):
        lines = []
        with open(path) as file:
            lines = file.readlines()
            file.close()

        table = None
        for line in lines:
            if table == None:
                table = CSVTable(re.split(divider, line.replace('\n', '')))
            else:
                table.add(re.split(divider, line.replace('\n', '')))

        return table


    # function for creating a .csv file based on a header array
    # first this function checks if a .csv file with this path already exists
    # if this file exists it is loaded instead of created
    def create(path, headers):
        if not os.path.exists(path):
            with open(path, "w") as file:
                file.write(divider.join(map(str, headers)) + '\n')
                file.close()
                return CSVTable(headers)
        else:
            return CSVFactory.load(path)

    # function for saving a CSVTable to a .csv file
    # it takes a path and a table to create/overwrite this file
    def save(path, table):
        headers = table.headers()
        rows = table.all()
        with open(path, "w") as file:
            file.write(divider.join(map(str, headers)) + '\n')
            for row in rows:
                file.write(divider.join(map(str, row)) + '\n')

            file.close()
