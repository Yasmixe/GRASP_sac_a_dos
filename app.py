import random

# Exemple d'objets avec poids et valeur 
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
#-----------------------------Calculer le cout de chaque objet---------------------------------------------------------------

# Fonction pour calculer le coût (valeur/poids) pour chaque objet
def calcul_cout(items):
    for item in items:
        item["cout"] = item["valeur"] / item["poids"]

#---------------------------Randomized construction-------------------------------------------------------------------
# Phase 1 : Construction de la solution aleatoire
def Phase_1(items, capacite, alpha):
    '''1 ere etape: calculer le cout de  chaque objet 
        2 eme etape: ordre decroissant des couts
        3 eme etape: Definir un seuil
        4 eme etape: construire la liste RCL telque: si le cout d'un objet >= seuil 
        5 eme etape: selection aleatoire'''
#----------------------------------------------------------------------------------------------------------------------
    '''1 ere etape: Calcule du cout de chaque objet'''
    calcul_cout(items)

    solution = []
    capacite_debut = 0 
    rcl = []
    
    while capacite_debut < capacite:
        ''' 2 eme etape: ordre decroissant des couts'''
        elements_restants = [item for item in items if item not in solution]
        elements_restants.sort(key=lambda x: x["cout"], reverse=True)

        if not elements_restants:
            break

        '''3 eme etape: Definir un seuil'''
        cout_max = elements_restants[0]["cout"]
        cout_min = elements_restants[-1]["cout"]
        '''print(cout_min)
        print(cout_max)'''
        '''3 eme etape: definir un seuil: '''
        seuil = cout_min + alpha * (cout_max - cout_min)
        #print(seuil)
        '''4 eme etape: Construire la RCL'''
        rcl = [i for i in elements_restants if i["cout"] <= seuil]
         #print(f'La liste RCL contient : {rcl}')

        '''5 eme etape: selection aleatoire'''
        element_aleatoire = random.choice(rcl)
        
      #print(f'lelement aleatoire que jai choisi est: {element_aleatoire["objet"]}')
        # Vérifier la contrainte de poids
        if capacite_debut + element_aleatoire["poids"] <= capacite:
            solution.append(element_aleatoire)
            capacite_debut += element_aleatoire["poids"]
        else:
            break

    return solution


#------------------------------------Recherche locale------------------------------------------------------------------------------------

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
                #print(f'la nouvelle solution pour ajout est: {new_solution}')
                new_weight = sum(i["poids"] for i in new_solution)
                new_value = sum(i["valeur"] for i in new_solution)
                #print(f'new value pour ajout est: {new_value}')
                # Vérifier si l'ajout ne dépasse pas la capacité et améliore la valeur
                if new_weight <= capacite and new_value > best_value:
                    best_solution = new_solution
                    #print(f'Best solution pour lajout dun objet: {best_solution}')
                    best_value = new_value
                    #print(f'Best value pour lajout dun objet: {best_value} et capacite sac a dos: {new_weight}')
                    improved = True
                    break

        # Étape 2: Supprimer un objet existant
        for item in best_solution:
            new_solution = [i for i in best_solution if i != item]
            #print(f'la nouvelle solution pour suppression est: {new_solution}')
            new_value = sum(i["valeur"] for i in new_solution)
            #print(f'new value pour suppression est: {new_value} et capacite sac a dos: {new_weight}')
            if new_value > best_value:
                best_solution = new_solution
                #print(f'Best solution pour la suppression dun objet: {best_solution}')
                best_value = new_value
                #print(f'Best value pour la suppression dun objet: {best_value}')
                improved = True
                break

        # Étape 3: Permuter un objet
        for item_to_remove in best_solution:
            for item_to_add in items:
                if item_to_add not in best_solution:
                    new_solution = [i for i in best_solution if i != item_to_remove] + [item_to_add]
                    #print(f'la nouvelle solution pour permutation est: {new_solution}')
                    new_weight = sum(i["poids"] for i in new_solution)
                    new_value = sum(i["valeur"] for i in new_solution)
                    #print(f'new value pour permutation est: {new_value} et capacite sac a dos: {new_weight}')
                    if new_weight <= capacite and new_value > best_value:
                        best_solution = new_solution
                        #print(f'Best solution pour la permutation dun objet: {best_solution}')
                        best_value = new_value
                        #print(f'Best value pour la permutation dun objet: {best_value}')
                        improved = True
                        break
            if improved:
                break

    return best_solution

# Phase 1: Générer une solution initiale
'''for i in [0, 0.2, 0.4, 0.5, 0.6, 0.8, 1]:
    solution_initiale = Phase_1(items, capacite, i)
    print(f"Solution initiale: {[item['objet'] for item in solution_initiale]}, Valeur: {sum(item['valeur'] for item in solution_initiale)}")

    # Phase 2: Appliquer la recherche locale
    solution_finale = recherche_locale(solution_initiale, items, capacite)
    print(f"Solution finale: {[item['objet'] for item in solution_finale]}, Valeur: {sum(item['valeur'] for item in solution_finale)}")

#print(solution_gloutonne)'''

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
#print(solution_finale)
print(f"\nMeilleure solution trouvée : {[item['objet'] for item in solution_finale]}, Valeur : {valeur_finale}")


#path relinking.

#-------------------------------------------------------------------------------------------------------------------------------------
def path_linking(solution_1, solution_2, items, capacite):
    """
    Combine deux solutions pour explorer des solutions intermédiaires
    et effectuer une recherche locale sur celles-ci.
    """
    # Étape 1: Calculer les objets communs entre les deux solutions
    objets_communs = [item for item in solution_1 if item in solution_2]
    
    # Étape 2: Ajouter des objets de solution_2 qui ne sont pas dans solution_1
    objets_uniques = [item for item in solution_2 if item not in solution_1]
    
    # Étape 3: Construire une solution intermédiaire basée sur les objets communs
    solution_intermediaire = objets_communs[:]
    
    # Ajouter les objets uniques à la solution intermédiaire tout en respectant la capacité
    poids_total = sum(item["poids"] for item in solution_intermediaire)
    for item in objets_uniques:
        if poids_total + item["poids"] <= capacite:
            solution_intermediaire.append(item)
            poids_total += item["poids"]
    
    # Étape 4: Appliquer une recherche locale pour améliorer la solution intermédiaire
    solution_amelioree = recherche_locale(solution_intermediaire, items, capacite)
    
    return solution_amelioree

def grasp_with_path_linking(items, capacite, max_iterations):
    best_solution = None
    best_value = 0
    solutions = []  # Stocke toutes les solutions finales pour le path linking

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
        
        # Ajouter la solution actuelle à la liste des solutions
        solutions.append(solution_finale)

    # Phase de Path Linking
    print("\nPhase de Path Linking :")
    for i in range(len(solutions)):
        for j in range(i + 1, len(solutions)):
            # Combiner deux solutions avec path linking
            solution_pl = path_linking(solutions[i], solutions[j], items, capacite)
            valeur_pl = sum(item["valeur"] for item in solution_pl)
            print(f"  Solution path linking : {[item['objet'] for item in solution_pl]}, Valeur : {valeur_pl}")
            
            # Mettre à jour la meilleure solution trouvée
            if valeur_pl > best_value:
                best_solution = solution_pl
                best_value = valeur_pl
                print(f"  Nouvelle meilleure solution trouvée : {[item['objet'] for item in best_solution]}, Valeur : {best_value}")

    return best_solution, best_value


# Exécution de GRASP avec Path Linking
max_iterations = 15  # Nombre d'itérations maximum
solution_finale, valeur_finale = grasp_with_path_linking(items, capacite, max_iterations)

print(f"\nMeilleure solution trouvée avec Path Linking : {[item['objet'] for item in solution_finale]}, Valeur : {valeur_finale}")
