import sqlite3
import pandas as pd
import logging
import matplotlib.pyplot as plt
import os

def setup_logger():
    filehandler = logging.FileHandler("logs.log")
    formatter = logging.Formatter("[%(asctime)s][%(name)s][%(levelname)s] %(message)s")
    filehandler.setFormatter(formatter)
    return filehandler

logger = logging.getLogger("logger")
logger.setLevel(logging.INFO)
logger.addHandler(setup_logger())


def read_csv(filepath):
    try:
        df = pd.read_csv(filepath)
        logger.info("CSV filen har lästs in korrekt")
    except Exception as e:
        logger.error(f"Kunde inte läsa in filen:{e}")
        df = None
    return df


def update_database(df, db_path):
    try:
        with sqlite3.connect(db_path) as conn:
            df.to_sql("patientdata", conn, if_exists = "replace", index = False)
            logger.info("Databasen har uppdaterats")
    except Exception as e:
        logger.error(f"Fel inträffat vid uppdatering av {e}")
        raise
    

def analyze_data(df):
    try:
        df["Datum"] = pd.to_datetime(df["Datum"], errors="coerce")
        df = df.dropna(subset=["Datum"])
        
        for månad, grupp in df.groupby(df["Datum"].dt.to_period("M")):
            common_treatment = grupp["Behandling"].value_counts().idxmax()
            logger.info(f"Vanligaste behandling i {månad}: {common_treatment}")
        
            average_cost = grupp["Kostnad"].mean()
            logger.info(f"Genomsnittlig kostnad: {average_cost} kr")
            
            median = grupp["Kostnad"].median()
            logger.info(f"Mediankostnad i {månad}: {median} kr")
            
        frekvens = df["Behandling"].value_counts()
        logger.info("Totalt antal per behandling:\n" + str(frekvens))
            
        df["Veckodag"] = df["Datum"].dt.day_name()
        treatment_per_day = df["Veckodag"].value_counts()
        logger.info("Antal behandling per veckodag:\n" + str(treatment_per_day))
    except Exception as e:
        logger.error(f"Fel vid analys {e}") 
        
def plot_treatment_per_day(df):
    df["Veckodag"] = df["Datum"].dt.day_name()
    df["Veckodag"].value_counts().plot(kind="bar", title="Behandling per veckodag")
    plt.ylabel("Antal")
    plt.tight_layout()
    plt.savefig("plots/behandlingar_per_veckodag.png")
    plt.clf()
    
def plot_cost_per_month(df):
    df["Månad"] = df["Datum"].dt.to_period("M")
    cost_per_month = df.groupby("Månad")["Kostnad"].mean()
    cost_per_month.index = cost_per_month.index.to_timestamp()
    cost_per_month.plot(marker="o", title="Genomsnittlig kostnad per månad")
    plt.ylabel("Kostnad (kr)")
    plt.xlabel("Månad")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plots/genomsnittlig_kostnad_per_manad.png")
    plt.clf()
    
def plot_treatmentcost(df):
    df.boxplot(column="Kostnad", by="Behandling", rot=45)
    plt.title("Kostnad per behandling")
    plt.suptitle("")  
    plt.ylabel("Kostnad (kr)")
    plt.tight_layout()
    plt.savefig("plots/kostnad_per_behandling.png")
    plt.clf()
    
def plot_pie_chart(df):
    df["Behandling"].value_counts().plot.pie(autopct="%1.1f%%", title="Andel per behandling")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig("plots/andel_per_behandling.png")
    plt.clf()

def visualize_data(df):
    try:
        os.makedirs("plots", exist_ok=True)
        df["Datum"] = pd.to_datetime(df["Datum"])
        
        plot_treatment_per_day(df)
        plot_cost_per_month(df)
        plot_treatmentcost(df)
        plot_pie_chart(df)
        
        logger.info("Visualisering sparades till plots")
    except Exception as e:
        logger.error(f"Fel vid visualisering {e}")  
        
      
def main():
    try: 
        data = read_csv("patientdata.csv")
        if data is not None:
            update_database(data, "data.db")
            analyze_data(data)
            visualize_data(data)
        else:
            logger.error("Ingen data att bearbeta")
    except Exception as e:
        logger.error(f"Fel: {e}") 
        
if __name__ == "__main__": 
    main()    
