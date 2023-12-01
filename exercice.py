from ortools.sat.python import cp_model
#import time

def generer_emploi_du_temps(enseignants, salles, cours_liste, horaires, jours):
    # Créer le modèl
    model = cp_model.CpModel()
   
    # Création des variables de décision représentant l'affectation des enseignants aux cours, salles, horaires et jours.
    # Chaque variable est un booléen indiquant la présence d'un enseignant dans une salle pour un cours, un horaire et un jour spécifiques.  
    emploi_du_temps = {(ens, salle, cours, horaire, jour): model.NewBoolVar(f'{ens}_{salle}_{cours}_{horaire}_{jour}')
                       for ens in enseignants
                       for salle in salles
                       for cours in cours_liste
                       for horaire in horaires
                       for jour in jours}

    # Ajouter les contraintes pour garantir la faisabilité de l'emploi du temps

    # Contraintes sur le nombre de cours par enseignant, salle, cours, horaire, jour
    for ens in enseignants:
        for horaire in horaires:
            for jour in jours:
                model.Add(sum(emploi_du_temps[(ens, salle, cours, horaire, jour)] for salle in salles for cours in cours_liste) <= 1)
    
    # Contraintes sur le nombre de cours par salle, horaire, jour
    for salle in salles:
        for horaire in horaires:
            for jour in jours:
                model.Add(sum(emploi_du_temps[(ens, salle, cours, horaire, jour)] for ens in enseignants for cours in cours_liste) <= 1)

    # Contraintes sur le nombre de cours par cours, horaire, jour
    for cours in cours_liste:
        for horaire in horaires:
            for jour in jours:
                model.Add(sum(emploi_du_temps[(ens, salle, cours, horaire, jour)] for ens in enseignants for salle in salles) <= 1)

    # Contraintes sur le nombre de cours par cours, enseignant, horaire
    for cours in cours_liste:
        for ens in enseignants:
            for horaire in horaires:
                model.Add(sum(emploi_du_temps[(ens, salle, cours, horaire, jour)] for salle in salles for jour in jours) == 1)

    # Contraintes sur le nombre de cours par enseignant, horaire, jour
    for horaire in horaires:
        for ens in enseignants:
            for jour in jours:
                model.Add(sum(emploi_du_temps[(ens, salle, cours, horaire, jour)] for salle in salles for cours in cours_liste) <= 1)

    # Ajouter la contrainte spécifique aux salles (au plus un cours par salle et par horaire)
    for salle in salles:
        for horaire in horaires:
            for jour in jours:
                model.Add(sum(emploi_du_temps[(ens, salle, cours, horaire, jour)] for ens in enseignants for cours in cours_liste) <= 1)

    # Résoudre le modèle
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
 
    # Imprimer le statut de la résolution
   # print(solver.ResponseStats())

    # Afficher le message d'incompatibilité si le problème est non réalisable
    if status == cp_model.INFEASIBLE:
        print("Le problème est non réalisable. Vérifiez vos contraintes.")
    else:
        # Afficher les résultats
        for ens in enseignants:
            for salle in salles:
                for cours in cours_liste:
                    for horaire in horaires:
                        for jour in jours:
                            if solver.Value(emploi_du_temps[(ens, salle, cours, horaire, jour)]) == 1:
                               print("Enseignant {}, Salle {}, Cours {}, Horaire {}, Jour {}".format(ens, salle, cours, horaire, jour))

#ts = time.time()
if __name__ == "__main__":
    # Définition des enseignants, des salles, des cours, des horaires et des jours
    enseignants = ['e1', 'e2', 'e3','e4','e5']
    salles = ['s1', 's2', 's3','s4','s5']
    cours_liste = ['c1', 'c2', 'c3','c4','c5']
    horaires = ['h1', 'h2', 'h3','h4','h5']
    jours = ['Lundi', 'Mardi', 'Mercredi','Jeudi','Vendredi']
    # Appel de la fonction pour générer l'emploi du temps
    generer_emploi_du_temps(enseignants, salles, cours_liste, horaires, jours)
#    print("Time required is:", time.time() - ts)
