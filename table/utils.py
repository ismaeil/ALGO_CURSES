#! /usr/bin/python
# -*- coding: utf-8 -*-

def transposeData(listedelistes):
    """
    L'entrée est la liste des colonnes et la sortie est la liste des lignes ::
    
        entree = [[1, 2, 3, 4, 5],[11, 12, 13, 14, 15],[21, 22, 23, 24, 25]]
        
        sortie = transposeData(entree)
        
        sortie
        
        [[1, 11, 21], [2, 12, 22], [3, 13, 23], [4, 14, 24], [5, 15, 25]]
    """
    nbcolonnes = len(listedelistes)
    nblignes = len(listedelistes[0]) 
    sortie = [[] for i in range(nblignes)]
    
    for col in listedelistes:
        for ligne in range(nblignes):
            sortie[ligne].append(col[ligne])
    return sortie


def customap(liste):
    """
    À partir de : ::
    
        [set([3, 4]), set([0, 1, 2])]
        
    Retourner : ::
    
        [set([0, 1]), set([2, 3, 4])]
        
    """
    resultat = [ "" for i in range(len(liste))]
    aux2 = []
    j = 0
    for i in range(len(liste)):
        aux = list(liste[i])
        for k in range(len(aux)):
            aux2.append(j)
            j += 1
        resultat[i] = set(aux2)
        aux2 = []
    return resultat
  

def reorderTab(table):
    """
    Ordonner la table itérativement.
    On a besoin de deux listes intermédiaires L(n+1) et L(n). on les appellera LL et L
    La sortie est une liste d'ordre
    cette méthode ne travaille que sur les colonnes de la table et ne change pas l'ordre des lignes.

        **Dans une table "démontable", les lignes doivent être ordonnées dans un ordre de démontabilité du treillis associé pour que 
        cette méthode puisse créer une table ordonnée (ie : sans configuration Gamma)**

    Exemple :
        
    = = = =
    0 1 1 1
    0 1 0 1
    1 1 0 0
    = = = =

    se transforme en :
           
    = = = =
    1 1 0 1
    0 1 0 1
    0 0 1 1
    = = = =

    """
    nombre_colonnes = len(table)
    nombre_lignes = len(table[0])
    LL = [set(range(1, nombre_colonnes + 1))]
    liste_aux = range(1, nombre_lignes + 1)
    liste_aux.reverse()
    for i in liste_aux:
        L = []
        for A in LL:
          E0 = set()
          E1 = set()
          for j in list(A):
              if table[j - 1][i - 1] == 0:
                  E0 = E0 | set([j])
              else:
                  E1 = E1 | set([j])
          L.append(E0)
          L.append(E1)
        LL = L
    liste_ordre = goodListe(L)
    #indice mini = 0
    aux = []
    for i in liste_ordre:
        aux.append(i - 1)
    resultat = nouvelOrdre(table, aux)
    return resultat


def goodListe(liste):
    """
    Transforme une liste d'ensembles (éventuellement vides) en en liste d'entiers ::

        [set([]), set([3]), set([]), set([4]), set([1]), set([]), set([]), set([2])]

    se transforme en ::

        [3, 4, 1, 2]

    """
    sortie = []
    for u in liste:
        sortie.extend(u)
    return sortie


def reorderLC(table, ordrel, ordrec):
    """
    On donne la table, un ordre sur les lignes et sur les colonnes et on réordonne !
    entrée : liste de listes + ordre ligne + ordre colonne
    sortie : liste de listes (ordonnée)
    """
    sortie =[[] for i in ordrec]
    for c in range(len(ordrec)):
        for l in range(len(ordrel)):
            sortie[c].append(table[ordrec[c]][ordrel[l]])
    return sortie

def choixPivot(table, ensemble_ligne, ensemble_colonne):
    """
    On entend par pivot la ligne qui a le plus grand poid

    Exemple :
                     
    == == == == == ==
    1  0  0  1  0  1
    1  1  1  0  1  1
    0  0  1  0  1  1
    1  1  0  0  0  0
    == == == == == ==

    qui est ::

        t = [[1, 1, 0, 1], [0, 1, 0 ,1], [0, 1, 1, 0], [1, 0, 0, 0], [0, 1, 1, 0], [1, 1, 1, 0]]

    on a ::

        choixPivot(t, set([0, 1, 3]), set([0, 1, 2, 3, 4, 5])) = 1 

    car le poid de la ligne 1 est (selon les colonnes : set([0, 1, 2, 3, 4, 5])) cinq et est supérieur ou égal au poid des autres lignes. 
    le choix du pivot est fait parmi les lignes autorisées et les colonnes autorisées
    
    Retourner la ligne pivot et l'ensemble des colonnes où elle a des 1

    **ATTENTION :**
        
        **cette méthode donne bien un élèment maximal, mais elle ne tient pas compte des autres
        élèments maximaux qui n'ont pas un poid maximal (ceci est par contre le cas dans le 
        code de la méthode avec curses)**
        
        **Par exemple, dans la table suivante :**

             
        = = =
        1 0 1
        0 1 0
        = = =

        **les deux lignes sont maximales (aucune n'est incluse dans l'autre) même si la première a plus de 
        poid que la seconde.
        La méthode actuelle ne tient pas compte de ce fait !**
        
    """
    resultat = -1
    somme = 0
    for k in ensemble_ligne:
        aux = sum(table[i][k] for i in ensemble_colonne)
        if aux >= somme:
            somme = aux
            resultat = k
    
    return resultat
 
 
def entasserLigne(table, ligne, colonnes_autorisees):
    """
    Entasser une ligne selon un ensemble de colonnes revient à mettre tous ses 1 à droite et ses zero 
    à gauche en changeant ainsi l'ordre des colonnes autorisées.
    """
    zero, un = [], []
    for i in colonnes_autorisees:
        if table[i][ligne] == 0:
            zero.append(i)
        else:
            un.append(i)
    nouvel_ordre_colonnes_autorisees = [set(zero), set(un)] # il peut y avir des ensembles vides
    
    return nouvel_ordre_colonnes_autorisees
 
 
def decoupage(pivot, indice_ligne, indice_colonne, L, C, T):
    """
    À partir de pivot indice_colonne, indice_ligne, L (liste d'ensemble), C (liste d'ensemble) et la 
    table ; retourner c0, c1, l0, l1 (ensembles)
    
        Cette méthode est très proche de la méthode *decoupage* utilisée dans la version non cureses de l'algorithme.
        
        Le prototype de la fonction change tout de même entre les deux versions (Curses et Non Curses)
  
    """
    c1 = colonnes_element(pivot, C[indice_colonne], T)
    c0 = C[indice_colonne] - c1
    l1, l0 = [], []
    aux = 0
    for i in L[indice_ligne]:
        for j in c1:
            aux += T[j][i]
        
        if aux == len(c1):
            l1.append(i)
            aux = 0
        else:
            l0.append(i)
            aux = 0
  
    l1, l0 = set(l1), set(l0)
    return c0, c1, l0, l1
  
 
def maj(pos_c, pos_l, L, C, c0, c1, l0, l1):
    """
    Méthode auxiliaire pour le programme principal
    Elle fait des mises à jour de variables intermédiaires.
    """
    if (c0 != set([]) and c1 != set([])):
        C = C[:pos_c] + [c0, c1] + C[pos_c + 1:]
        new_pos_c = pos_c + 1
    else:
        new_pos_c = pos_c
      
    if (l0 != set([]) and l1 != set([])):
        L = L[:pos_l] + [l1, l0] + L[pos_l + 1:]
        new_pos_l = pos_l + 1
    else:
        new_pos_l = pos_l
    
    return new_pos_c, new_pos_l, L, C


def nouvelOrdre(table, liste):
    """
    Réordonner les colonnes suivant la liste en tant qu'index
    
    Exemple :
    
        Le résultat du réordonnancement de ::
        
            [[0, 0, 1], [1, 1, 1], [1, 0, 0], [1, 1, 0]]
            
        suivant la table ::
        
            [3, 1, 0, 2]
        
        est ::
        
            [[1, 1, 0], [1, 1, 1], [0, 0, 1], [1, 0, 0]]
        
    """
    result = []
    for i in liste:
        result.append(table[i])
    return result


def colonnes_element(pivot, colonnes_autorisees, T):
    """
    Fonction auxiliaire qui retournes parmis les colonnes autorisés, celles qui contiennent un 1 sur la ligne pivot
    """
    return set([j for j in colonnes_autorisees if T[j][pivot] == 1])


