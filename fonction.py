def saisieAliment() :
    test = {}
    test["nom"] = str(input("Entrez le nom de l'aliment : "))
    test["poids"] = int (input("Entrez le poids de la portion de l'apport calorique : "))
    test["calories"] = int (input("Entrez le nombre de kcal : "))
    test["carbs"] = int (input("Entrez le nombre de carbs : "))
    test["protein"] = int (input("Entrez le nombre de protein : "))
    return test

