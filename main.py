###################################################
# Name: Morel Raphaël
# Contact: morelraphael2@gmail.com
###################################################
import pandas as pd
from datetime import datetime
import sqlite3
import os


quit = False ## Variable qui à true quite la boucle infinie while 
nom_base_de_donnees = 'data_base.db'
nom_table_apj = 'apports_journalier_table'
nom_table_aa = 'apports_aliment_table'
nom_table_tj = 'total_journalier'

#chargement des dataframe si ils existent 
if os.path.exists(nom_base_de_donnees): # si le fichier de data base existe on charge les df
    print("La base de données existe.")
    db_SQLite = sqlite3.connect(nom_base_de_donnees)
    df_apports_journaliers = pd.read_sql('SELECT * FROM ' + nom_table_apj, db_SQLite)
    df_apports_aliment = pd.read_sql('SELECT * FROM ' + nom_table_aa, db_SQLite)
    df_total_journalier = pd.read_sql('SELECT * FROM ' + nom_table_tj, db_SQLite)
else:
    # Création des DataFrame vide
    df_apports_journaliers = pd.DataFrame(columns=['date', 'nom aliment', 'quantite', 'calories', 'glucides', 'proteine'])
    df_apports_aliment = pd.DataFrame(columns=['nom aliment', 'quantite', 'calories', 'glucides', 'proteine'])
    df_total_journalier = pd.DataFrame(columns=['date', 'calories', 'glucides', 'proteine'])



# Fonction pour ajouter un nouvel apport calorique journalier
def calcul_total_journalier(df):
    df_copy = df.copy() #copie le df pour ne pas apporter de modif au df en paramètre
    df_copy['date'] = pd.to_datetime(df_copy['date'])
    # Extraire uniquement la partie de la date correspondant au jour (année-mois-jour)
    df_copy['date'] = df_copy['date'].dt.date
    # Créer un DataFrame vide pour stocker les totaux par jour
    df_sortie = df_copy.groupby('date').sum(numeric_only=True).reset_index()
    return df_sortie

def ajouter_apport():
    date = datetime.now()
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    nom_aliment = input("Entrez le nom de l'aliment : ")
    quantite = float(input("Entrez la quantité (en gramme) : "))

    aliment_info = df_apports_aliment[df_apports_aliment['nom aliment'] == nom_aliment]
    if not aliment_info.empty:
        quantite2 = aliment_info['quantite'].values[0]
        calories = aliment_info['calories'].values[0]*(quantite/quantite2)
        glucides = aliment_info['glucides'].values[0]*(quantite/quantite2)
        proteine = aliment_info['proteine'].values[0]*(quantite/quantite2)
         # Ajout des données dans le DataFrame
        df_apports_journaliers.loc[len(df_apports_journaliers)] = [date, nom_aliment, quantite, calories, glucides, proteine]
        print("Aliment ajouté avec succès !")
    else : 
        print("Aliment non trouvé dans la base de données de nutrition.")

    return calcul_total_journalier(df_apports_journaliers)
    
    

# Fonction pour ajouter un nouvel aliment au DataFrame
    
def ajouter_apport_aliment():
    nom_aliment = input("Entrez le nom de l'aliment : ")
    nom_aliment_minuscule = nom_aliment.lower()
    aliments_existant = [nom.lower() for nom in df_apports_aliment['nom aliment'].values]
    if nom_aliment_minuscule in aliments_existant:
        print("Cet aliment existe déjà dans la base de données.")
        return
    
    quantite = float(input("Entrez la quantité : "))
    calories = float(input("Entrez le nombre de calories: "))
    glucides = float(input("Entrez la quantité de glucide "))
    proteine = float(input("Entrez la quantité de proteine: "))
    
    # Ajout des données dans le DataFrame
    df_apports_aliment.loc[len(df_apports_aliment)] = [nom_aliment, quantite, calories, glucides, proteine]
    print("Aliment ajouté avec succès !")

def modifier_apport_aliment():
    nom_aliment = input("Entrez le nom de l'aliment à modifier : ")
    aliment_info = df_apports_aliment[df_apports_aliment['nom aliment'] == nom_aliment]
    
    if not aliment_info.empty:
        print("Apport actuel de l'aliment :")
        print(aliment_info)
        
        new_quantite = float(input("Entrez la nouvelle quantité : "))
        new_calories = float(input("Entrez le nouveau nombre de calories : "))
        new_glucides = float(input("Entrez la nouvelle quantité de glucides : "))
        new_proteine = float(input("Entrez la nouvelle quantité de protéines : "))
        
        # Modifier les valeurs dans le DataFrame
        df_apports_aliment.loc[df_apports_aliment['nom aliment'] == nom_aliment, 'quantite'] = new_quantite
        df_apports_aliment.loc[df_apports_aliment['nom aliment'] == nom_aliment, 'calories'] = new_calories
        df_apports_aliment.loc[df_apports_aliment['nom aliment'] == nom_aliment, 'glucides'] = new_glucides
        df_apports_aliment.loc[df_apports_aliment['nom aliment'] == nom_aliment, 'proteine'] = new_proteine
        
        print("Apport modifié avec succès !")
    else:
        print("Cet aliment n'existe pas dans la base de données.")   

def supprimer_apport_aliment():
    nom_aliment = input("Entrez le nom de l'aliment à supprimer : ")
    aliment_info = df_apports_aliment[df_apports_aliment['nom aliment'] == nom_aliment]
     
    if not aliment_info.empty:
        print("Informations sur l'aliment à supprimer :")
        print(aliment_info)
        df_apports_aliment.drop(df_apports_aliment[df_apports_aliment['nom aliment'] == nom_aliment].index, inplace=True)
    else:
        print("Cet aliment n'existe pas dans la base de données.")

def supprimer_apport_journalier():
    date = input("Entrez la date de l'apport à supprimer (format YYYY-MM-DD) : ")
    apport_info = df_apports_journaliers[df_apports_journaliers['date'] == date]
    
    if not apport_info.empty:
        print("Apport journalier trouvé pour la date spécifiée :")
        print(apport_info)
        
        confirmation = input("Voulez-vous vraiment supprimer cet apport ? (Oui/Non) : ").lower()
        
        if confirmation == "oui":
            # Supprimer l'apport du DataFrame
            df_apports_journaliers.drop(df_apports_journaliers[df_apports_journaliers['date'] == date].index, inplace=True)
            print("Apport journalier supprimé avec succès !")
        elif confirmation == "non":
            print("Suppression annulée.")
        else:
            print("Réponse invalide. Suppression annulée.")
    else:
        print("Aucun apport trouvé pour la date spécifiée.")


while not quit : 
    print ("0 : Quitter")
    print ("1 : Enregistrer un nouvel aliment")
    print ("2 : Ajouter un apport journalier")
    print ("3 : Recap journalier")
    print ("4 : afficher apport des aliments")
    print ("5 : Modifier les apports d'un aliment")
    print ("6 : supprimer un aliment")
    print ("7 : supprimer un apport journalier")
    print ("8 : afficher date")
    choix = int (input("Faire un choix  : \n"))

    if (choix== 0):
        quit = True
        db_SQLite = sqlite3.connect(nom_base_de_donnees)
        df_apports_journaliers.to_sql(nom_table_apj, db_SQLite, index=False, if_exists='replace')
        df_apports_aliment.to_sql(nom_table_aa, db_SQLite, index=False, if_exists='replace')
        df_total_journalier.to_sql(nom_table_tj, db_SQLite,index=False, if_exists='replace')
        db_SQLite.close()

    elif (choix== 1):
        ajouter_apport_aliment()


        
    elif (choix== 2):
       df_total_journalier = ajouter_apport()
    
    elif (choix == 3):
        print(df_apports_journaliers)
        print(df_total_journalier)
        
        
    
    elif (choix== 4):
        print(df_apports_aliment)

                
    elif(choix == 5):
        modifier_apport_aliment()


    elif(choix == 6): 
        supprimer_apport_aliment()

    elif(choix==7): 
        supprimer_apport_journalier()
            
    elif (choix == 8) : 
        print("Date : {}".format(datetime.now()) )


    else : 
        print("Choix invalide")




### verifier que l'alliment n'existe pas avant d'en rajouter un aux apport nutri
### gestion d'un choix invalide dans le menue de nav
### problème d'enregistrement dans les DB a cause de la date

        