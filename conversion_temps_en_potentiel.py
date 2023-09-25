from typing import Tuple
import numpy as np


def calculer_facteur_conversion_temps_en_potentiel_avec_mesure_rampe(valeurs: np.array,
                                                                     indice_colonne_temps: int,
                                                                     indice_colonne_rampe) -> Tuple[float, float]:
    """
    Pour déterminer la facteur de conversion temps-potentiel, le taux de variation du potentiel de la rampe
    en fonction du temps est calculé pour l'ensemble des points (sauf les deux aux extrémités car il leur manque
    un voisin pour calculer le taux de variation instantané.). Ensuite, la valeur moyenne est calculé ainsi que
    la déviation standard.

    Attention! Le taux de variation est calculé sur l'entièreté de l'array numpy.

    :param valeurs: array numpy contenant au moins la colonne du temps et la colonne du potentiel de la rampe
    :param indice_colonne_temps: indice associé à la colonne du temps dans l'array numpy
    :param indice_colonne_rampe: indice associé à la colonne du potentiel de la rampe dans l'array numpy
    :return:
    """
    # ici on prend delta_t_i = t_i+1 - t_i-1. Nous perdons donc les 2 éléments aux extrémités.
    deltas_t = valeurs[2:, indice_colonne_temps] - valeurs[:-2, indice_colonne_temps]
    deltats_V = valeurs[2:, indice_colonne_rampe] - valeurs[:-2, indice_colonne_rampe]
    gradient = deltats_V / deltas_t

    return gradient.mean(), gradient.std()




