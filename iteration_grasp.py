import random

# Exemple d'objets avec poids et valeur (plus grand jeu de données)
items = [
    {"objet": "A", "poids": 5, "valeur": 10},
    {"objet": "B", "poids": 3, "valeur": 7},
    {"objet": "C", "poids": 4, "valeur": 8},
    {"objet": "D", "poids": 2, "valeur": 6},
    {"objet": "E", "poids": 1, "valeur": 5},
    {"objet": "F", "poids": 9, "valeur": 15},
    {"objet": "G", "poids": 6, "valeur": 9},
    {"objet": "H", "poids": 7, "valeur": 12},
    {"objet": "I", "poids": 8, "valeur": 14},
    {"objet": "J", "poids": 3, "valeur": 9},
]

capacite = 20  # Capacité du sac à dos

# Fonction pour calculer le coût (valeur/poids) pour chaque objet
def calcul_cout(items):
    for item in items:
        item["cout"] = item["valeur"] / item["poids"]

# Phase 1 : Construction de la solution avec GRASP
def Phase_1(items, capacite, alpha):
    calcul_cout(items)
    
    solution = []
    capacite_debut = 0
    rcl = []
    
    while capacite_debut < capacite:
        # Trier les objets restants par leur ratio valeur/poids
        elements_restants = [item for item in items if item not in solution]
        elements_restants.sort(key=lambda x: x["cout"], reverse=True)

        if not elements_restants:
            break

        # Calcul du seuil pour la RCL (Restricted Candidate List)
        cout_max = elements_restants[0]["cout"]
        cout_min = elements_restants[-1]["cout"]
        seuil = cout_min + alpha * (cout_max - cout_min)
        
        # Sélectionner les éléments dans la RCL
        rcl = [i for i in elements_restants if i["cout"] >= seuil]
        
        # Choisir un élément aléatoire de la RCL
        element_aleatoire = random.choice(rcl)
        
        # Vérifier si l'ajout de l'objet ne dépasse pas la capacité
        if capacite_debut + element_aleatoire["poids"] <= capacite:
            solution.append(element_aleatoire)
            capacite_debut += element_aleatoire["poids"]
        else:
            break

    return solution

# Recherche locale pour améliorer la solution
def recherche_locale(solution, items, capacite):
    best_solution = solution[:]
    best_value = sum(item["valeur"] for item in best_solution)
    
    improved = True
    while improved:
        improved = False
        
        # Ajouter un nouvel objet
        for item in items:
            if item not in best_solution:
                new_solution = best_solution + [item]
                new_weight = sum(i["poids"] for i in new_solution)
                new_value = sum(i["valeur"] for i in new_solution)
                
                # Vérifier si l'ajout ne dépasse pas la capacité et améliore la valeur
                if new_weight <= capacite and new_value > best_value:
                    best_solution = new_solution
                    best_value = new_value
                    improved = True
                    break

        # Supprimer un objet
        for item in best_solution:
            new_solution = [i for i in best_solution if i != item]
            new_value = sum(i["valeur"] for i in new_solution)
            
            # Vérifier si la nouvelle solution est meilleure
            if new_value > best_value:
                best_solution = new_solution
                best_value = new_value
                improved = True
                break

        # Échanger un objet
        for item_to_remove in best_solution:
            for item_to_add in items:
                if item_to_add not in best_solution:
                    new_solution = [i for i in best_solution if i != item_to_remove] + [item_to_add]
                    new_weight = sum(i["poids"] for i in new_solution)
                    new_value = sum(i["valeur"] for i in new_solution)
                    
                    if new_weight <= capacite and new_value > best_value:
                        best_solution = new_solution
                        best_value = new_value
                        improved = True
                        break
            if improved:
                break

    return best_solution

# Critère d'arrêt : nombre d'itérations
def grasp(items, capacite, max_iterations):
    best_solution = None
    best_value = 0

    for iteration in range(max_iterations):
        print(f"\nItération {iteration + 1} :")
        # Choisir un alpha aléatoire pour la construction de la solution
        alpha_value = random.uniform(0, 1)
        solution_initiale = Phase_1(items, capacite, alpha_value)
        
        # Améliorer la solution avec la recherche locale
        solution_finale = recherche_locale(solution_initiale, items, capacite)
        
        # Calculer la valeur finale
        valeur_finale = sum(item["valeur"] for item in solution_finale)
        print(f"  Valeur de la solution finale : {valeur_finale}")
        print(f"  Solution : {[item['objet'] for item in solution_finale]}")

        # Mettre à jour la meilleure solution trouvée
        if valeur_finale > best_value:
            best_solution = solution_finale
            best_value = valeur_finale
            print(f"  Meilleure solution trouvée jusqu'à maintenant : {[item['objet'] for item in best_solution]}, Valeur : {best_value}")

    return best_solution, best_value

# Exécution de GRASP
max_iterations = 15  # Nombre d'itérations maximum
solution_finale, valeur_finale = grasp(items, capacite, max_iterations)

print(f"\nMeilleure solution trouvée : {[item['objet'] for item in solution_finale]}, Valeur : {valeur_finale}")
