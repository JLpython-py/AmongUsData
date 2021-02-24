#! python3
# update.py

"""
Update CSV data based on data in Among_Us_Bot database tables
"""

import csv
import logging
import os
import sqlite3

logging.basicConfig(
    level=logging.INFO,
    format=" %(asctime)s - %(levelname)s - %(message)s"
)

DIRECTORY = os.path.join(
    os.path.expanduser("~"), "PythonScripts", "Among_Us_Bot",
    "data", "db"
)
DIRECTORIES = {
    "airship.sqlite": "Airship",
    "mira_hq.sqlite": "MIRA HQ",
    "polus.sqlite": "Polus",
    "the_skeld.sqlite": "The Skeld"
}


class Update:
    """ Update CSV files given the database to reference
"""
    def __init__(self, database):
        directory = os.path.join(DIRECTORY, database)
        assert os.path.exists(directory)
        self.connection = sqlite3.connect(directory)
        self.cursor = self.connection.cursor()
        self.directory = DIRECTORIES[database]
        self.write(
            "actions.csv", self.execute_query("actions")
        )
        self.write(
            "locations.csv", self.execute_query("locations")
        )
        self.write(
            "tasks.csv", self.execute_query("tasks")
        )
        self.write(
            "vents.csv", self.execute_query("vents")
        )

    def execute_query(self, table):
        logging.info(table)
        query = f"""
        SELECT *
        FROM {table}
        """
        self.cursor.execute(query)
        columns = [d[0].title() for d in self.cursor.description]
        data = self.cursor.fetchall()
        return columns, sorted(data)

    def write(self, filename, data):
        with open(
            os.path.join("data", self.directory, filename),
            "w", newline=""
        ) as file:
            writer = csv.writer(file)
            writer.writerow([d.replace('\r\n', '\\n') for d in data[0]])
            for row in data[1]:
                writer.writerow([r.replace('\r\n', '\\n') for r in row])


def main():
    databases = os.listdir(DIRECTORY)
    for mapdb in databases:
        logging.info(mapdb)
        db_update = Update(mapdb)
        db_update.connection.close()


if __name__ == '__main__':
    main()
