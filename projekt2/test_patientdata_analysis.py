from main import read_csv, update_database
import pandas as pd
import sqlite3
import unittest

class TestPatientData(unittest.TestCase):
    
    def test_read_csv(self):
     df = read_csv("testdata.csv") 
     self.assertIn("Datum", df.columns)
     self.assertNotIn("Tid", df.columns) 
     
    def test_read_missing_file(self):
        with self.assertLogs("logger", level = "ERROR") as log_cm:
            df = read_csv("fil_som_inte_finns.csv")
        self.assertTrue(any("Kunde inte läsa in filen" in message for message in log_cm.output), 
                        "felmeddelande loggades inte korrekt")

    def test_update_database(self):
        df = read_csv("testdata.csv")
        update_database(df, "test_data.db")
        with sqlite3.connect("test_data.db") as conn:
            result = pd.read_sql("SELECT * FROM patientdata", conn)
            self.assertEqual(len(result), len(df))

if __name__ == "__main__":
    unittest.main()
