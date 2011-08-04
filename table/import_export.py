#! /usr/bin/python
# -*- coding: utf-8 -*-

from utils import *

import random

def imporTable(fichier):
    """
    Importer un fichier et construire la table correspondant
    
    **Cette méthode stipule que le fichier ne contient pas les labels, ce dernier cas est
    géré dans la méthode imporTable_generique**
    
    Exemple: ::
    
        f = open('Examples/table1.txt')
        
        t = imporTable(f)
        
        t
        
        [[1, 1, 0, 1], [0, 1, 0, 1], [0, 1, 1, 0], [1, 0, 0, 0], [0, 1, 1, 0], [1, 1, 1, 0]]
        
    """
  
    sortie = [[int(x) for x in ligne.split()] for ligne in fichier]
    return transposeData(sortie)
  
  
def imporTable_generique(fichier, label_lignes=False, label_colonnes=False):
    """
    Fonction très proche de la fonction *imporTable_generique* du code avec No curses
    
    """
  
    if label_colonnes:
        label_table_colonnes = fichier.readline().split()
    
    sortie = []
    label_table_lignes = []
    for ligne in fichier:
        elems = ligne.split()
        if label_lignes:
            label_table_lignes.append(elems.pop(0))
        else:
            label_table_lignes.append("l" + str(len(label_table_lignes)))
        
        sortie.append([int(x) for x in elems])

    if not label_colonnes:
        label_table_colonnes = ["c" + str(x) for x in range(len(sortie[0]))]
    
    return transposeData(sortie), label_table_lignes, label_table_colonnes


def tabletoliststr(table):
    """
    Lecture en ligne de la table
    
    Résultat = liste de lignes en chaînes de caractères 
         
    = = =
    1 1 0
    0 1 0
    1 1 1
    = = =
    
    se transforme en : ::
    
        ["1 1 0", "0 1 0", "1 1 1"]
        
    """
    sortie = []
    nbligne = len(table[0])
    nbcol = len(table)
    
    aux = ""
    for i in range(nbligne):
        for j in range(nbcol - 1):
            aux += str(table[j][i]) + " "
        aux += str(table[nbcol - 1][i])
        sortie.append(aux)
        aux = ""
    return sortie


def tabletostr(table, label_ligne, label_colonne, ordre_ligne, ordre_colonne):
    """
    À partir d'une table avec ou pas des labels, on procède à la lecture de la table et on crée une chaîne de
    caractères qui fait que l'affichage en est rendu facile.
    
    *ordre_ligne* et *ordre_colonne* permettent de créer un découpage en lignes et colonnes
    
    Cette fonction ne sert qu'à la visualisation d'une table.
    
    Le *return* peut tout  à fait être remplacé par un *print*.
    
    EXEMPLE : ::
        
        table, label_ligne, label_colonne = imporTable_generique(open('Examples/table_7_10.txt'), True, True)
        
        ordre_ligne = [set([0, 1]), set([2, 3]), set([4, 5, 6])]
        
        ordre_colonne = [set([0, 1, 2]), set([3, 4]), set([5, 6, 7, 8, 9])]
        
        print(tabletostr(table, label_ligne, label_colonne, ordre_ligne, ordre_colonne))
        
    """
    label_l = [label_ligne[i] for i in goodListe(ordre_ligne)]
    label_c = [label_colonne[i] for i in goodListe(ordre_colonne)]
    ordre_l = customap(ordre_ligne)
    ordre_c = customap(ordre_colonne)
    t = reorderLC(table, goodListe(ordre_ligne), goodListe(ordre_colonne))
    
    nb_ligne = len(label_l) + 1
    
    #trouver les indices pour couper les colonnes
    indice_separation_colonnes = []
    for ens in ordre_c[:-1]:
        indice_separation_colonnes.append(list(ens).pop())
      
    #trouver les indices pour couper les lignes
    indice_separation_lignes = []
    for ens in ordre_l[:-1]:
        indice_separation_lignes.append(list(ens).pop())
      
    sortie = " " * nb_ligne
    for j, y in enumerate(label_c):
        sortie += y + " "
        # séparer label colonnes
        # si les labels colonnes existent
        if set(label_c) != set([""]):
            if j in indice_separation_colonnes:
                  sortie += "| "
                  
    sortie += "\n"
    
    for i, x in enumerate(label_l):
        sortie += x.ljust(nb_ligne)
        nb_cols = len(x.ljust(nb_ligne))
        for j, y in enumerate(label_c):
            sortie += str(t[j][i]).center(len(y)) + " "
            nb_cols += len(str(t[j][i]).center(len(y)) + " ")
            # séparer colonnes t
            if j in indice_separation_colonnes:
                sortie += "| "
                nb_cols += 2
        # séparer lignes t
        if i in indice_separation_lignes:
            sortie += "\n" + ("-" * nb_cols)
        sortie += "\n"
      
    return sortie
  

def creerTable(nb_l, nb_c):
    """
    Créer une table aléatoire à partir qui a nb_l lignes et nb_c colonnes.
    
    Exemple : ::
    
        table = creerTable(2, 5)
        
        table
        
        [[0, 1], [0, 1], [0, 0], [1, 1], [0, 0]]
        
    """
    listecolonnes = [[] for j in range(nb_c)]
    for j in range(nb_c):
        for i in range(nb_l):
            listecolonnes[j].append(random.randint(0, 1))
      
    return listecolonnes
