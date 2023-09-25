import numpy as np

from outils_analyse.fits import gaussian_fit, gaus, round_any
from outils_analyse.identification_des_pics import determiner_indexes_maximums_scipy
from outils_analyse.lecture_des_fichiers import lire_csv_a_3_colonnes, crop_pour_conserver_que_la_partie_avec_rampe
from outils_analyse.conversion_temps_en_potentiel import \
    calculer_facteur_conversion_temps_en_potentiel_avec_mesure_rampe
import matplotlib.pyplot as plt
import os
import matplotlib
"""
------------------------------------------------------------------------------

Copy pastez le code de l'analyse légère pour un pic ici. À partir des résultat
de l'analyse légère, compléter le code pour faire l'analyse complète

_____________________________________________________________________________
"""
# Grosseur du text dans les figures
matplotlib.rcParams.update({'font.size': 18})
"""
------------------------------------------------------------------------------

Lire le fichier des résultats et transformer les valeurs en un array numpy

_____________________________________________________________________________
"""
path = "C:/Users/Ariette/Documents/5e session physique/PhysEx/F&H/Données/Acquisition 4 (U1 = 3.5V).csv"
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
                                                               hauteur_minimum=None, distance_minumum=150)

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



"""
------------------------------------------------------------------------------

Faire une régression gaussienne sur chacun des pics et calculer le potentiel de contact.
Pour arrondir les valeurs selons leur incertitudes, regardez la documentation de sigfig.

Les résultats devraient être similaire à 
Pic 1: Moyenne: 2.04 ± 0.02 STD: -0.44 ± 0.02 Amplitude: 0.083 ± 0.004
Pic 2: Moyenne: 6.91 ± 0.01 STD: 0.82 ± 0.01 Amplitude: 0.459 ± 0.006
Pic 3: Moyenne: 12.00 ± 0.01 STD: 1.09 ± 0.01 Amplitude: 0.96 ± 0.01
Pic 4: Moyenne: 17.14 ± 0.01 STD: 1.26 ± 0.01 Amplitude: 1.365 ± 0.007


_____________________________________________________________________________
"""


# Définir les régions des pics (des nouvelles array)

liste_fit = []
liste_x = []
for indx_pic in liste_des_indexes_des_pics:
    if indx_pic < 50:
        array_cropped = valeurs_avec_bonnes_unites_determination_des_pics[indx_pic-45:indx_pic+45]
    else:
        array_cropped = valeurs_avec_bonnes_unites_determination_des_pics[indx_pic -50:indx_pic + 50]
    x = array_cropped[:, 0]
    y = array_cropped[:, 1]
    mu = valeurs_avec_bonnes_unites_determination_des_pics[indx_pic, 0]
    a = valeurs_avec_bonnes_unites_determination_des_pics[indx_pic, 1]
    fit = gaussian_fit(x,y, a, mu, 1)
    liste_fit.append(fit)
    liste_x.append(x)



# Mettres les paramètres des fits gaussiens pour chaque pic [Amplitude, Moyenne, STD]
peak1 = liste_fit[0]# Arrray de 3 éléments
peak2 = liste_fit[1] # Arrray de 3 éléments
peak3 = liste_fit[2] # Arrray de 3 éléments
peak4 = liste_fit[3] # Arrray de 3 éléments

"""
_____________________________________________________________________________
"""
# Ne pas modifier cette section!!!

def rounding_peaks(peaks):
    all_values = []
    for i in range(0, 3):
        all_values.append(round_any(peaks[0][i], uncertainty=peaks[1][i]))

    return all_values

print("Pic 1:", f"Moyenne: {rounding_peaks(peak1)[1]}",
      f"STD: {rounding_peaks(peak1)[2]}",
      f"Amplitude: {rounding_peaks(peak1)[0]}")
print("Pic 2:", f"Moyenne: {rounding_peaks(peak2)[1]}",
      f"STD: {rounding_peaks(peak2)[2]}",
      f"Amplitude: {rounding_peaks(peak2)[0]}")
print("Pic 3:", f"Moyenne: {rounding_peaks(peak3)[1]}",
      f"STD: {rounding_peaks(peak3)[2]}",
      f"Amplitude: {rounding_peaks(peak3)[0]}")
print("Pic 4:", f"Moyenne: {rounding_peaks(peak4)[1]}",
      f"STD: {rounding_peaks(peak4)[2]}",
      f"Amplitude: {rounding_peaks(peak4)[0]}")

"""
------------------------------------------------------------------------------

Faire un graphique digne d'un article qui contient l'ensemble des données de courants en fonction de la tension,
les emplacements approximatifs des maximums et les différents fits gaussiens effectués.

Ça devrait ressembler à la figure exemple_de_fichiers/exemple_graphique_f_et_h
_____________________________________________________________________________
"""
plt.figure()
plt.title("Figure 7: Pics d'ionisations du mercure avec les paramètres d'acquisitions du Tableau 5.")
plt.plot(valeurs_avec_bonnes_unites_determination_des_pics[:, 0],
         valeurs_avec_bonnes_unites_determination_des_pics[:, 1])
plt.scatter(valeurs_avec_bonnes_unites_determination_des_pics[liste_des_indexes_des_pics, 0],
            valeurs_avec_bonnes_unites_determination_des_pics[liste_des_indexes_des_pics, 1],
            label="Estimation des pics")
plt.xlabel("Tension entre G1 et le ground [V]")
plt.ylabel('Courant du pico [nA]')

# les gaussiennes
test = liste_fit[0][0][0]
y1 = gaus(liste_x[0], liste_fit[0][0][0], liste_fit[0][0][1], liste_fit[0][0][2])
y2 = gaus(liste_x[1], liste_fit[1][0][0], liste_fit[1][0][1], liste_fit[1][0][2])
y3 = gaus(liste_x[2], liste_fit[2][0][0], liste_fit[2][0][1], liste_fit[2][0][2])
y4 = gaus(liste_x[3], liste_fit[3][0][0], liste_fit[3][0][1], liste_fit[3][0][2])
plt.plot(liste_x[0], y1, label=f'Y = {rounding_peaks(peak1)[0]} * np.exp(-(x - {rounding_peaks(peak1)[1]}) ** 2 / (2 * {rounding_peaks(peak1)[2]} ** 2))')
plt.plot(liste_x[1], y2, label=f'Y = {rounding_peaks(peak2)[0]} * np.exp(-(x - {rounding_peaks(peak2)[1]}) ** 2 / (2 * {rounding_peaks(peak2)[2]} ** 2))')
plt.plot(liste_x[2], y3, label=f'Y = {rounding_peaks(peak3)[0]} * np.exp(-(x - {rounding_peaks(peak3)[1]}) ** 2 / (2 * {rounding_peaks(peak3)[2]} ** 2))')
plt.plot(liste_x[3], y4, label=f'Y = {rounding_peaks(peak4)[0]} * np.exp(-(x - {rounding_peaks(peak4)[1]}) ** 2 / (2 * {rounding_peaks(peak4)[2]} ** 2))')
plt.legend()
plt.show()

