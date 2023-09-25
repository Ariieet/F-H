"""
------------------------------------------------------------------------------

Pour vous faciliter la vie, vous pouvez utiliser le code présent dans le dossier
outils_analyse.

_____________________________________________________________________________
"""
"""
------------------------------------------------------------------------------

Mettres vois import ici

_____________________________________________________________________________
"""
from outils_analyse.identification_des_pics import determiner_indexes_maximums_scipy
from outils_analyse.lecture_des_fichiers import lire_csv_a_3_colonnes, crop_pour_conserver_que_la_partie_avec_rampe
from outils_analyse.conversion_temps_en_potentiel import \
    calculer_facteur_conversion_temps_en_potentiel_avec_mesure_rampe
import matplotlib.pyplot as plt
import os
import matplotlib
# Grosseur du text dans les figures
matplotlib.rcParams.update({'font.size': 18})
"""
------------------------------------------------------------------------------

Lire le fichier des résultats et transformer les valeurs en un array numpy

_____________________________________________________________________________
"""
path = "C:/Users/Ariette/Documents/5e session physique/PhysEx/F&H/PHY-3002-Frank-et-Hertz-main/PHY-3002-Frank-et-Hertz-main/exemples_de_fichiers/exemple_de_donnees.csv"
# Mettre vos valuers extraites à la place du None.
valeurs_en_array = lire_csv_a_3_colonnes(path, 9)  # Array de trois colonnes

"""
_____________________________________________________________________________
"""
# Ne pas modifier cette section!!!

# La figure obtenue devrait correspondre à celle de figures_exemple/lecture_des_donnes_brutes
plt.figure()
plt.plot(valeurs_en_array[:, 0], valeurs_en_array[:, 2], label="Tensions du pico")
plt.plot(valeurs_en_array[:, 0], valeurs_en_array[:, 1], label="Tensions entre la G1 et le ground")
plt.xlabel("Temps [s]")
plt.ylabel("Tension [V]")
plt.legend()
plt.show()

"""
------------------------------------------------------------------------------

Retirer les valeurs qui se trouvent à l'extérieur de l'activation du générateur de rampe.
Ne pas oublier de mettre le début de la rampe comme étant t=0.

_____________________________________________________________________________
"""
# Mettre vos données croppé remise à t_0=0 dans cette variable
valeurs_cropped_debutant_par_t0 = crop_pour_conserver_que_la_partie_avec_rampe(valeurs_en_array, 2, 0.05, 0.1)  # Array de trois colonnes
valeurs_cropped_debutant_par_t0[:,0] = valeurs_cropped_debutant_par_t0[:,0] + abs(valeurs_cropped_debutant_par_t0[0,0]) # metrre temps à 0

"""
_____________________________________________________________________________
"""
# Ne pas modifier cette section!!!

# La figure obtenue devrait correspondre à celle de figures_exemple/donnes_cropped
plt.figure()
plt.plot(valeurs_cropped_debutant_par_t0[:, 0], valeurs_cropped_debutant_par_t0[:, 2],
         label="Tensions du pico")
plt.plot(valeurs_cropped_debutant_par_t0[:, 0], valeurs_cropped_debutant_par_t0[:, 1],
         label="Tensions entre la G1 et le ground")
plt.xlabel("Temps [s]")
plt.ylabel("Tension [V]")
plt.legend()
plt.show()
"""
------------------------------------------------------------------------------

Calculer la pente de la tension du générateur de rampe et son incertitude.
Afficher cette valeur et son incertitude, puis convertir les valeurs de temps
en valeurs de tension. La valeur devrait être près de: Pente =  -0.44003644585609436 +- 0.031069057062268257 V/s

Ensuite, convertissez les valeurs de tensions du pico en valeur de courant, en considérant que l'échelle
du pico utilisé est de 3nA. 
_____________________________________________________________________________
"""
# Afficher la pente et son incertitude
facteur_valeur, facteur_incertitude = calculer_facteur_conversion_temps_en_potentiel_avec_mesure_rampe(valeurs_cropped_debutant_par_t0, 0, 2)

# Convertir le temps en tension avec la pente
valeurs_cropped_debutant_par_t0[:,0] = valeurs_cropped_debutant_par_t0[:,0]* abs(facteur_valeur)

# Mettre vos données avec les bonnes unités à la place et vos informations par rapport à la pente ici
valeurs_avec_bonnes_unites = valeurs_cropped_debutant_par_t0  # Array de trois colonnes


"""
_____________________________________________________________________________
"""
# Ne pas modifier cette section!!!

print("Pente = ", f"{facteur_valeur} +- {facteur_incertitude}")

# La figure obtenue devrait correspondre à celle de figures_exemple/donnes_avec_bonnes_unités
plt.figure()
plt.plot(valeurs_avec_bonnes_unites[:, 0], valeurs_avec_bonnes_unites[:, 1],
         label="Courant du pico")
plt.xlabel("Tension entre G1 et le ground [V]")
plt.ylabel("Courant mesuré [nA]")
plt.legend()
plt.show()
"""
------------------------------------------------------------------------------

Déterminer l'emplacement approximatif des maximums. Ça devrait être
environ: Estimation des pics: [ 1.9844797  6.902538  11.950019  17.083782 ] V

_____________________________________________________________________________
"""
valeurs_avec_bonnes_unites_determination_des_pics = valeurs_avec_bonnes_unites  # Array de trois colonnes
liste_des_indexes_des_pics = determiner_indexes_maximums_scipy(valeurs_avec_bonnes_unites_determination_des_pics, 1,
                                                               hauteur_minimum=None, distance_minumum=75)

# On obtient les minimums en plus des maximus
print(valeurs_avec_bonnes_unites_determination_des_pics.max())

"""
_____________________________________________________________________________
"""
# Ne pas modifier cette section!!!

print("Estimation des pics:", valeurs_avec_bonnes_unites_determination_des_pics[liste_des_indexes_des_pics, 0])

# La figure obtenue devrait correspondre à celle de figures_exemple/estimation_des_pics
plt.figure()
plt.plot(valeurs_avec_bonnes_unites_determination_des_pics[:, 0],
         valeurs_avec_bonnes_unites_determination_des_pics[:, 1],
         label="Courant du pico")
plt.xlabel("Tension entre G1 et le ground [V]")
plt.scatter(valeurs_avec_bonnes_unites_determination_des_pics[liste_des_indexes_des_pics, 0],
            valeurs_avec_bonnes_unites_determination_des_pics[liste_des_indexes_des_pics, 1],
            label="Estimation des pics")
plt.ylabel("Courant mesuré [nA]")
plt.legend()
plt.show()











