import sqlite3
import pandas as pd
import logging

#sätta upp logger 
def setup_logger():
    filehandler = logging.FileHandler("logs.log")
    formatter = logging.Formatter("[%(asctime)s][%(name)s][%(levelname)s] %(message)s")
    filehandler.setFormatter(formatter)
    return filehandler

#loggerinställningar 
logger = logging.getLogger("logger")
logger.setLevel(logging.INFO)
logger.addHandler(setup_logger())

#läsa in data
def read_csv(filepath):
    try:
        df = pd.read_csv(filepath)
        logger.info("CSV filen har lästs in korrekt")
    except Exception as e:
        logger.error(f"fel vid inläsning av CSV filen {e}")
        df = None
    return df

#uppdatera SQLite databas
def update_database(df, db_path):
    try:
        with sqlite3.connect(db_path) as conn:
            df.to_sql("cars_data", conn, if_exists = "replace", index = False)
            logger.info("Databas uppdaterades")
    except Exception as e:
        logger.error(f"Fel vid uppdatering av {e}")
        raise
    
#huvudfunktion
def main():
    try :
        data = read_csv("cars_data.csv")
        update_database(data, "data.db")
    except Exception as e:
        logger.error(f"Fel: {e}")
        
        
if __name__ == "__main__":
    main()
