from main import read_csv, update_database
import pandas as pd
import sqlite3
import unittest

class TestDatabaseUpdate(unittest.TestCase):

    def test_update_database(self):
        df = read_csv("cars_data.csv")
        update_database(df, "test_data.db")
        with sqlite3.connect("test_data.db") as conn:
            result = pd.read_sql("SELECT * FROM cars_data", conn)
            self.assertEqual(len(result), len(df))

if __name__ == "__main__":
    unittest.main()
