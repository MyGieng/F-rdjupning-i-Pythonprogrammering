Tandvårdsanalys med python 

Ett dataflödesprojekt i python som analyserar och visualiserar fiktiv tandvårdsdata. Projektet omfattar hela processen från datainläsnig till analys och visualisering.

Funktioner 

Inläsning av CSV fil med felhantering
Lagring i SQLite databas
Analys av data 
Visualisering med stapeldiagram, linjediagram, boxplot och cirkeldiagram
Loggning av alla viktiga steg och felmeddelanden
Enhetstester med unittest

Struktur 

Projektet är uppbyggd med en main() funktion som styr hela flödet som i sin tur är uppdelad i separata funktioner: read_Csv, update_database, analyze_data, visualize_data. Fel hanteras med try/except. Koden är lätt att underhålla och kan automatiseras om önskas. 

Förutsättningar för att komma igång 

Python 
Bibliotek: pandas, matplotlib, Sqlite3, unittest.

Körning

Se till att python och bibliotek är installerade. För att installera biblioteken använd exempelvis "pip install (biblioteken)". Placera CSV filen i samma fil som koden. Kör programmet med "python patientdata_analysis.py. Visualiseringar sparas i plots och under logs.log kan resultaten ses från analysen. 
