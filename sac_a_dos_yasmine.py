import random #pour rendomiser lorsequ'on choisit un element dans la premiere phases. 

#exemple de TD
items = [
#  (poids, valeurs)
    {"objet": "A", "poids": 4, "valeur": 6},
    {"objet": "B", "poids": 2, "valeur": 4},
    {"objet": "C", "poids": 3, "valeur": 5},
    {"objet": "D", "poids": 5, "valeur": 8}
]
# capacite du sac a dos est == 11
capacite = 10


#-----------------------------Calculer le cout de chaque objet---------------------------------------------------------------

# Fonction pour calculer le ratio valeur/poids
def calcul_cout(items):
    for item in items:
        item["cout"] = item["valeur"] / item["poids"]

#---------------------------Randomized construction-------------------------------------------------------------------

def Phase_1(items, capacite, alpha):
    '''1 ere etape: calculer le cout de  chaque objet 
        2 eme etape: ordre decroissant des couts
        3 eme etape: Definir un seuil
        4 eme etape: construire la liste RCL telque: si le cout d'un objet >= seuil 
        5 eme etape: selection aleatoire'''
    

    '''1 ere etape: Calcule du cout de chaque objet'''
    calcul_cout(items) 

    solution = [] # au debut on initialise la solution a l'ensemble vide
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
        seuil = cout_max - alpha * (cout_max - cout_min)
        #print(seuil)
        '''4 eme etape: Construire la RCL'''
        rcl = [i for i in elements_restants if i["cout"] >= seuil]
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
    print(best_value)
    improved = True
    while improved:
        improved = False
        # Étape 1: Ajouter un nouvel objet
        for item in items:
            if item not in best_solution:  
                new_solution = best_solution + [item]
                new_weight = sum(i["poids"] for i in new_solution)
                new_value = sum(i["valeur"] for i in new_solution)
                
                if new_weight <= capacite and new_value > best_value:
                    best_solution = new_solution
                    best_value = new_value
                    improved = True
                    break

        # Étape 2: Supprimer un objet existant
        for item in best_solution:
            new_solution = [i for i in best_solution if i != item]
            new_value = sum(i["valeur"] for i in new_solution)
            
            if new_value > best_value:
                best_solution = new_solution
                best_value = new_value
                improved = True
                break

        # Étape 3: Permuter un objet
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


# Phase 1: Générer une solution initiale
solution_initiale = Phase_1(items, capacite, 0.5)
print(f"Solution initiale: {[item['objet'] for item in solution_initiale]}, Valeur: {sum(item['valeur'] for item in solution_initiale)}")

# Phase 2: Appliquer la recherche locale
solution_finale = recherche_locale(solution_initiale, items, capacite)
print(f"Solution finale: {[item['objet'] for item in solution_finale]}, Valeur: {sum(item['valeur'] for item in solution_finale)}")






























#print(solution_gloutonne)