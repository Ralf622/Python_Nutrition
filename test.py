import pandas as pd
from datetime import datetime
import sqlite3
import os


quit = False ## Variable qui à true quite la boucle infinie while 
nom_base_de_donnees = 'data_base.db'
nom_table_apj = 'apports_journalier_table'
nom_table_apn = 'apports_nutritionnels_table'

#chargement des dataframe si ils existent 
if os.path.exists(nom_base_de_donnees): # si le fichier de data base existe on charge les df
    print("La base de données existe.")
    db_SQLite = sqlite3.connect(nom_base_de_donnees)
    df_apports_journalier = pd.read_sql('SELECT * FROM ' + nom_table_apj, db_SQLite)
    df_apports_nutritionnels = pd.read_sql('SELECT * FROM ' + nom_table_apn, db_SQLite)
else:
    # Création des DataFrame vide
    df_apports_journalier = pd.DataFrame(columns=['date', 'nom aliment', 'quantite', 'calories', 'glucides', 'proteine'])
    df_apports_nutritionnels = pd.DataFrame(columns=['nom aliment', 'quantite', 'calories', 'glucides', 'proteine'])


# Fonction pour ajouter un nouvel apport calorique journalier

def ajouter_apport():
    date = datetime.now()
    nom_aliment = input("Entrez le nom de l'aliment : ")
    quantite = float(input("Entrez la quantité (en gramme) : "))

    aliment_info = df_apports_nutritionnels[df_apports_nutritionnels['nom aliment'] == nom_aliment]
    
    if not aliment_info.empty:
        quantite2 = aliment_info['quantite'].values[0]
        calories = aliment_info['calories'].values[0]*(quantite/quantite2)
        glucides = aliment_info['glucides'].values[0]*(quantite/quantite2)
        proteine = aliment_info['proteine'].values[0]*(quantite/quantite2)
           # Ajout des données dans le DataFrame
    df_apports_journalier.loc[len(df_apports_journalier)] = [date, nom_aliment, quantite, calories, glucides, proteine]
    print("Aliment ajouté avec succès !")
 


# Fonction pour ajouter un nouvel aliment au DataFrame
    
def ajouter_apport_nutritionnel():
    nom_aliment = input("Entrez le nom de l'aliment : ")
    quantite = float(input("Entrez la quantité : "))
    calories = float(input("Entrez le nombre de calories: "))
    glucides = float(input("Entrez la quantité de glucide "))
    proteine = float(input("Entrez la quantité de proteine: "))
    
    # Ajout des données dans le DataFrame
    df_apports_nutritionnels.loc[len(df_apports_nutritionnels)] = [nom_aliment, quantite, calories, glucides, proteine]
    print("Aliment ajouté avec succès !")


#Phase d'initialisation de l'application 
    



while not quit : 
    print ("0 : Quitter")
    print ("1 : Enregistrer un nouvel aliment")
    print ("2 : Ajouter un apport journalier")
    print ("3 : Recap journalier")
    print ("4 : afficher apport des aliments")
    print ("5 : Modifier les apports d'un aliment")
    print ("6 : afficher date")
    choix = int (input("Faire un choix  : \n"))

    if (choix== 0):
        quit = True
        db_SQLite = sqlite3.connect(nom_base_de_donnees)
        df_apports_journalier.to_sql(nom_table_apj, db_SQLite, index=False, if_exists='replace')
        df_apports_nutritionnels.to_sql(nom_table_apn, db_SQLite, index=False, if_exists='replace')
        db_SQLite.close()

    if (choix== 1):
        ajouter_apport_nutritionnel()


        
    if (choix== 2):
        ajouter_apport()
    
    if (choix == 3):
        print(df_apports_journalier)
        
        
    
    if (choix== 4):
        print(df_apports_nutritionnels)

                
    if(choix == 5):
        print("choix 5")

            
    if (choix == 6) : 
        print("Date : {}".format(datetime.now()) )


### a faire
### calcul des totaux journalier 
        
        