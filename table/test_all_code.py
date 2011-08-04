#! /usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import os
import sys

from ordonancement import algo
from import_export import *
from utils import *

class AlgoTest(unittest.TestCase):
    
    """
    Classe de tests du réordonnancement des tables 0/1.
    """
  
    def test_nouvelOrdre(self):
        """
        ordonne les colonnes dans l'ordre passé en argument à l'aide d'une liste
        ATTENTION : le min de la liste d'ordre est un 0
        """
        t = [[0, 0, 1], [1, 1, 1], [1, 0, 0], [1, 1, 0]]
        self.assertEquals(nouvelOrdre(t, [3, 1, 0, 2]),[[1, 1, 0], [1, 1, 1], [0, 0, 1], [1, 0, 0]])
      
      
    def test_goodListe1(self):
        """
        [set([]), set([3]), set([]), set([4]), set([1]), set([]), set([]), set([2])]
        se transforme en 
        [3, 4, 1, 2]
        """
        t = goodListe([set([]), set([3]), set([]), set([4]), set([1]), set([]), set([]), set([2])])
        self.assertEquals(t, [3, 4, 1, 2])
      
      
      
    def test_goodListe2(self):
        """
        [set([]), set([3, 6]), set([]), set([4]), set([1]), set([]), set([]), set([2])]
        se transforme en 
        [3, 6, 4, 1, 2]
        """
        t = goodListe([set([]), set([3, 6]), set([]), set([4]), set([1]), set([]), set([]), set([2])])
        self.assertEquals(t, [3, 6, 4, 1, 2] )
    
    
    def test_reorderTab1(self):
        """
        0 1 1 1                           1 1 0 1
        0 1 0 1     se transforme en      0 1 0 1
        1 1 0 0                           0 0 1 1
        """
        t = [[0, 0, 1], [1, 1, 1], [1, 0, 0], [1, 1, 0]]
        self.assertEquals(reorderTab(t),[[1, 0, 0], [1, 1, 0], [0, 0, 1], [1, 1, 1]])
  
  
    def test_reorderTab2(self):
        """
        1 0 0 0                           0 0 0 1
        1 1 0 1     se transforme en      1 0 1 1
        1 1 1 0                           0 1 1 1
        """
        t2 = [[1, 1, 1], [0, 1, 1], [0, 0, 1], [0, 1, 0]]
        self.assertEquals(reorderTab(t2),[[0, 1, 0], [0, 0, 1], [0, 1, 1], [1, 1, 1]])
  
  
    def test_comparer_reordertab_et_algo(self):
        """
        0 1 1 1          reorder          1 1 0 1
        0 1 0 1     se transforme en      0 1 0 1
        1 1 0 0                           0 0 1 1
        
        0 1 1 1          algo             1 0 0 1
        0 1 0 1     se transforme en      0 0 1 1
        1 1 0 0                           0 1 1 1
        
        """
        t = [[0, 0, 1], [1, 1, 1], [1, 0, 0], [1, 1, 0]]
        L, C = algo(t)
        self.assertFalse(reorderTab(t) == reorderLC(t, L, C))
  
  
    def test_transposeData(self):
        """
        entree = [[1, 2, 3, 4, 5],[11, 12, 13, 14, 15],[21, 22, 23, 24, 25]]
        sortie = [[1, 11, 21], [2, 12, 22], [3, 13, 23], [4, 14, 24], [5, 15, 25]]
        """
        t = [[1, 2, 3, 4, 5],[11, 12, 13, 14, 15],[21, 22, 23, 24, 25]]
        self.assertEquals(transposeData(t), [[1, 11, 21], [2, 12, 22], [3, 13, 23], [4, 14, 24], [5, 15, 25]])
    
    
    def test_imporTable(self):
        
        f = open(os.path.abspath('../Examples/table1.txt'))
        t = imporTable(f)
        self.assertEquals(t, [[1, 1, 0, 1], [0, 1, 0 ,1], [0, 1, 1, 0], [1, 0, 0, 0], [0, 1, 1, 0], [1, 1, 1, 0]])
  
  
    def test_imporTable_generique(self):
        """
        importer le fichier Examples/table1.txt
        et construire l'objet Table correspondant
        """
        
        f = open(os.path.abspath('../Examples/table1.txt'))
        t, l, c = imporTable_generique(f)
            
        self.assertEquals(t, [[1, 1, 0, 1], [0, 1, 0 ,1], [0, 1, 1, 0], [1, 0, 0, 0], [0, 1, 1, 0], [1, 1, 1, 0]])
        self.assertEquals(l, ["l" + str(i) for i in range(4)])
        self.assertEquals(c, ["c" + str(i) for i in range(6)])
        
        f = open(os.path.abspath('../Examples/tableLC.txt'))
        t, l, c = imporTable_generique(f, True, True)
            
        self.assertEquals(t, [[1, 1, 0, 1], [0, 1, 0 ,1], [0, 1, 1, 0], [1, 0, 0, 0], [0, 1, 1, 0], [1, 1, 1, 0]])
        self.assertEquals(c, [x for x in 'ABCDEF'])
        self.assertEquals(l, [x for x in 'abcd'])
    
        f = open(os.path.abspath('../Examples/tableL.txt'))
        t, l, c = imporTable_generique(f, True, False)
            
        self.assertEquals(t, [[1, 1, 0, 1], [0, 1, 0 ,1], [0, 1, 1, 0], [1, 0, 0, 0], [0, 1, 1, 0], [1, 1, 1, 0]])
        self.assertEquals(c, ["c" + str(i) for i in range(6)])
        self.assertEquals(l, [x for x in 'abcd'])
        
        f = open(os.path.abspath('../Examples/tableC.txt'))
        t, l, c = imporTable_generique(f, False, True)
            
        self.assertEquals(t, [[1, 1, 0, 1], [0, 1, 0 ,1], [0, 1, 1, 0], [1, 0, 0, 0], [0, 1, 1, 0], [1, 1, 1, 0]])
        self.assertEquals(c, [x for x in 'ABCDEF'])
        self.assertEquals(l, ["l" + str(i) for i in range(4)])
    
    
    def test_tabletoliststr(self):
        t = [[1, 2, 3],[11, 12, 13],[21, 22, 23]]
        result = ['1 11 21', '2 12 22', '3 13 23']
        self.assertEquals(tabletoliststr(t), result)
  
  
    def test_reorderLC(self):
  
        t = [[1, 2, 3, 4, 5],[11, 12, 13, 14, 15],[21, 22, 23, 24, 25]]
        result = [[23, 22, 25, 24, 21], [3, 2, 5, 4, 1], [13, 12, 15, 14, 11]]
        self.assertEquals(reorderLC(t, [2, 1, 4, 3, 0], [2, 0, 1]), result)
      
   
    def test_choixPivot(self):

        t = [[1, 1, 0, 1], [0, 1, 0 ,1], [0, 1, 1, 0], [1, 0, 0, 0], [0, 1, 1, 0], [1, 1, 1, 0]]
        pivot = choixPivot(t, set([0, 1, 2, 3]), set([0, 1, 2, 3, 4, 5]))
        elems =  colonnes_element(pivot, set([0, 1, 2, 3, 4, 5]), t)
        self.assertEquals((pivot, elems), (1, set([0, 1, 2, 5, 4])))
    
        pivot = choixPivot(t, set([0, 3, 2]), set([0, 1, 2, 3, 4, 5]))
        elems =  colonnes_element(pivot, set([0, 1, 2, 3, 4, 5]), t)
        self.assertEquals((pivot, elems), (2, set([2, 5, 4])))
      
      
    def test_entasserLigne1(self):

        t = [[1, 1, 0, 1], [0, 1, 0 ,1], [0, 1, 1, 0], [1, 0, 0, 0], [0, 1, 1, 0], [1, 1, 1, 0]]
        c = [set([3]), set([0, 1, 2, 4, 5])]
        self.assertEquals(entasserLigne(t, 1, set([0, 1, 2, 3, 4, 5])), c)
  
  
    def test_entasserLigne2(self):

        t = [[1, 1, 0, 1], [0, 1, 0 ,1], [0, 1, 1, 0], [1, 0, 0, 0], [0, 1, 1, 0], [1, 1, 1, 0]]
        c = [set([0, 3]), set([2, 5])]
        self.assertEquals(entasserLigne(t, 2, set([0, 2, 3, 5])), c)
  
  
    def test_decoupage1(self):
        """
        à partir de indice_colonne, indice_ligne, L (liste d'ensemble), C (liste d'ensemble) et la 
        table ; retourner c0, c1, l0, l1 (ensembles)
        
        Explications:
        1) choisir pivot in L[indice_ligne] tq le nombre de 1 de la ligne pivot soit max dans C[indice_colonne]
        2) c1 = ensemble de colonnes de C[indice_colonne] tq pivot à un 1 sur celles ci
        3) c0 = ...
        4) l1 = ensemble des elts de L[indice_ligne] qui ont des 1 sur ts les element de c1 (EXTENSION du pivot)
        5) l0 = L[indice_ligne] \ l1
        
        Exemple:
       
                 * 0 1 2 3 4 5
               * * * * * * * *
        T =     0* 1 0 0 1 0 1
                1* 1 1 1 0 1 1
                2* 0 0 1 0 1 1
                3* 1 1 0 0 0 0
        
        C = [{2, 3, 4}, {0, 1, 5}]
        L = [{3}, {0, 2}, {1}]
        indice_ligne = 1
        indice_colonne = 0
        pivot = 2 (in L[1] = {0, 2} qui maximise C[0] = {2, 3, 4})
        c1 = {2, 4}
        c0 = {3}
        l1 = {2}
        l0 = {0}
        """
        T = [[1, 1, 0, 1], [0, 1, 0 ,1], [0, 1, 1, 0], [1, 0, 0, 0], [0, 1, 1, 0], [1, 1, 1, 0]]
        indice_ligne = 1
        indice_colonne = 0
        C = [set([2, 3, 4]), set([0, 1, 5])]
        L = [set([3]), set([0, 2]), set([1])]
        c1 = set([2, 4])
        c0 = set([3])
        l1 = set([2])
        l0 = set([0])
        pivot = choixPivot(T, L[indice_ligne], C[indice_colonne])

        self.assertEquals(decoupage(pivot, indice_ligne, indice_colonne, L, C, T), (c0, c1, l0, l1))
  
  
    def test_decoupage2(self):
        """
        comme le test précedent mais en plus on essaye de voir si l'extension se fait vraiment 
        l1 doit donc contenir plus que un élèment
                 * 0 1 2 3 4 5
               * * * * * * * *
        T =     0* 1 0 1 1 1 1
                1* 1 1 1 0 1 1
                2* 0 0 1 1 1 1
                3* 1 1 0 0 0 0
        
        C = [{2, 3, 4}, {0, 1, 5}]
        L = [{3}, {0, 2}, {1}]
        indice_ligne = 1
        indice_colonne = 0
        pivot = 2 (in L[1] = {0, 2} qui maximise C[0] = {2, 3, 4})
        c1 = {2, 3, 4}
        c0 = {}
        l1 = {2, 0}
        l0 = {}
        """
        T = [[1, 1, 0, 1], [0, 1, 0 ,1], [1, 1, 1, 0], [1, 0, 1, 0], [1, 1, 1, 0], [1, 1, 1, 0]]
        indice_ligne = 1
        indice_colonne = 0
        C = [set([2, 3, 4]), set([0, 1, 5])]
        L = [set([3]), set([0, 2]), set([1])]
        c1 = set([2, 4, 3])
        c0 = set([])
        l1 = set([2, 0])
        l0 = set([])
        pivot = choixPivot(T, L[indice_ligne], C[indice_colonne])

        self.assertEquals(decoupage(pivot, indice_ligne, indice_colonne, L, C, T), (c0, c1, l0, l1))
  
  
    def test_decoupage3(self):
        """
                 * 0 1 2 3 4 5
               * * * * * * * *
        T =     0* 1 1 0 0 0 0
                1* 0 0 1 0 1 1
                2* 1 1 1 0 1 1
                3* 1 0 0 1 0 1
        
        C = [{2, 3, 4, 0, 1, 5}]
        L = [{3, 0, 2, 1}]
        indice_ligne = 0
        indice_colonne = 0
        pivot = 2 
        c1 = {2, 5, 4, 1, 0}
        c0 = {3}
        l1 = {2}
        l0 = {1, 3, 0}
    
        """
        T = [[1, 0, 1, 1], [1, 0, 1, 0], [0, 1, 1, 0], [0, 0, 0, 1], [0, 1, 1, 0], [0, 1, 1, 1]]
        indice_ligne = 0
        indice_colonne = 0
        C = [set([2, 3, 4, 0, 1, 5])]
        L = [set([3, 0, 2, 1])]
        c1 = set([0, 2, 5, 4, 1])
        c0 = set([3])
        l1 = set([2])
        l0 = set([1, 3, 0])
        pivot = choixPivot(T, L[indice_ligne], C[indice_colonne])

        self.assertEquals(decoupage(pivot, indice_ligne, indice_colonne, L, C, T), (c0, c1, l0, l1))
    
    
    def test_maj1(self):
        """
        methode auxiliaire pour le programme principal
        cas où c0 et c1 et l1 et l0 sont vides 
        """
        pos_l = 1
        pos_c = 3
        L = [set([1, 2, 3]), set([]), set([21, 22, 23]), set([44])]
        C = [set([35]), set([111, 112, 113]), set([222, 232]), set([]), set([90])]
        l0 = set([])
        l1 = set([])
        c0 = set([])
        c1 = set([])
        LL = [set([1, 2, 3]), set([]), set([21, 22, 23]), set([44])]
        CC = [set([35]), set([111, 112, 113]), set([222, 232]), set([]), set([90])]
        new_pos_l, new_pos_c = 1, 3 
        self.assertEquals(maj(pos_c, pos_l, L, C, c0, c1, l0, l1), (new_pos_c, new_pos_l, LL, CC))
  
  
    def test_maj2(self):
        """
        methode auxiliaire pour le programme principal
        cas où l0 et l1 et c1 et c0 ne sont pas vides 
        """
        pos_l = 2
        pos_c = 1
        L = [set([1, 2, 3]), set([]), set([21, 22, 23]), set([44])]
        C = [set([35]), set([111, 112, 113]), set([222, 232]), set([]), set([90])]
        l0 = set([21, 22])
        l1 = set([23])
        c0 = set([111])
        c1 = set([112, 113])
        LL = [set([1, 2, 3]), set([]), l1, l0, set([44])]
        CC = [set([35]), c0, c1, set([222, 232]), set([]), set([90])]
        new_pos_l, new_pos_c = 3, 2 
        self.assertEquals(maj(pos_c, pos_l, L, C, c0, c1, l0, l1), (new_pos_c, new_pos_l, LL, CC))
      
      
    def test_maj3(self):
        """
        methode auxiliaire pour le programme principal
        cas où c0 et c1 sont vides mais pas l1 et l2 
        """
        pos_l = 0
        pos_c = 3
        L = [set([1, 2, 3]), set([]), set([21, 22, 23]), set([44])]
        C = [set([35]), set([111, 112, 113]), set([222, 232]), set([]), set([90])]
        l0 = set([1])
        l1 = set([2, 3])
        c0 = set([])
        c1 = set([])
        LL = [l1, l0, set([]), set([21, 22, 23]), set([44])]
        CC = [set([35]), set([111, 112, 113]), set([222, 232]), set([]), set([90])]
        new_pos_l, new_pos_c = 1, 3 
        self.assertEquals(maj(pos_c, pos_l, L, C, c0, c1, l0, l1), (new_pos_c, new_pos_l, LL, CC))
      
      
    def test_maj4(self):
        """
        methode auxiliaire pour le programme principal
        cas où l0 et l1 sont vides mais pas c1 et c2 
        """
        pos_l = 1
        pos_c = 2
        L = [set([1, 2, 3]), set([]), set([21, 22, 23]), set([44])]
        C = [set([35]), set([111, 112, 113]), set([222, 232]), set([]), set([90])]
        l0 = set([])
        l1 = set([])
        c0 = set([222])
        c1 = set([232])
        LL = [set([1, 2, 3]), set([]), set([21, 22, 23]), set([44])]
        CC = [set([35]), set([111, 112, 113]), c0, c1, set([]), set([90])]
        new_pos_l, new_pos_c = 1, 3 
        self.assertEquals(maj(pos_c, pos_l, L, C, c0, c1, l0, l1), (new_pos_c, new_pos_l, LL, CC))
      
      
    def test_maj5(self):
        """
        methode auxiliaire pour le programme principal
        seul l0 est vide 
        """
        pos_l = 2
        pos_c = 2
        L = [set([1, 2, 3]), set([]), set([21, 22, 23]), set([44])]
        C = [set([35]), set([111, 112, 113]), set([222, 232]), set([]), set([90])]
        l0 = set([])
        l1 = set([21, 22, 23])
        c0 = set([222])
        c1 = set([232])
        LL = [set([1, 2, 3]), set([]), set([21, 22, 23]), set([44])]
        CC = [set([35]), set([111, 112, 113]), c0, c1, set([]), set([90])]
        new_pos_l, new_pos_c = 2, 3 
        self.assertEquals(maj(pos_c, pos_l, L, C, c0, c1, l0, l1), (new_pos_c, new_pos_l, LL, CC))
    
    
    def test_algo1(self):
        """
        à partir d'une table, on rend la liste des lignes et des colonnes après application de l'algo
        Si on veux, on peut appliquer la méthode nouvelOrdreLC pour réordonner ainsi la table.
        Exemple :
        à partir de :
            c0 c1 c2 c3 c4 c5
        l0* 1  0  0  1  0  1
        l1* 1  1  1  0  1  1
        l2* 0  0  1  0  1  1
        l3* 1  1  0  0  0  0
         qui est t = [[1, 1, 0, 1], [0, 1, 0 ,1], [0, 1, 1, 0], [1, 0, 0, 0], [0, 1, 1, 0], [1, 1, 1, 0]]
        
        rendre l'ordre de 
            c3 c1 c0 c2 c4 c5
        l3* 0  1  1  0  0  0
        l0* 1  0  1  0  0  1
        l2* 0  0  0  1  1  1
        l1* 0  1  1  1  1  1
        
        la sortie doit donc être : L, C = [3, 0, 2, 1], [3, 1, 0, 2, 4, 5]
        """
        t = [[1, 1, 0, 1], [0, 1, 0 ,1], [0, 1, 1, 0], [1, 0, 0, 0], [0, 1, 1, 0], [1, 1, 1, 0]]
        L, C = [3, 0, 2, 1], [3, 1, 0, 2, 4, 5]
        self.assertEquals(algo(t), (L, C))
      
      
    def test_algo2(self):
        """
        cette fois la table est déjà ordonnée !
        0 0 0 0 0
        0 0 0 0 1
        0 0 0 1 1
        0 0 1 1 1
        0 1 1 1 1
        1 1 1 1 1
        """
        t = [
        [0, 0, 0, 0, 0, 1], 
        [0, 0, 0, 0, 1, 1], 
        [0, 0, 0, 1, 1, 1], 
        [0, 0, 1, 1, 1, 1], 
        [0, 1, 1, 1, 1, 1], 
        ]
        L, C = [0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4]
        self.assertEquals(algo(t), (L, C))
      
      
    def test_algo3(self):
        """
        cette fois la table est desordonnée !
        1 1 1 1 1
        1 1 1 1 0
        1 1 1 0 0
        1 1 0 0 0
        1 0 0 0 0
        0 0 0 0 0
        """
        t = [
        [1, 1, 1, 1, 1, 0], 
        [1, 1, 1, 1, 0, 0], 
        [1, 1, 1, 0, 0, 0], 
        [1, 1, 0, 0, 0, 0], 
        [1, 0, 0, 0, 0, 0], 
        ]
        L, C = [5, 4, 3, 2, 1, 0], [4, 3, 2, 1, 0]
        self.assertEquals(algo(t), (L, C))
      
      
    def test_algo4(self):
        """
        cette fois la table il y a des sépartions ligne sans colonnes et colonnes sans lignes 
        avec changement d'ordre en retour...(cas général me parait-il)
        1 1 0 0 1 0
        1 0 0 0 1 0
        0 0 1 1 1 1 
        1 1 1 1 1 1
        """
        t = [
        [1, 1, 0, 1], 
        [1, 0, 0, 1], 
        [0, 0, 1, 1], 
        [0, 0, 1, 1], 
        [1, 1, 1, 1], 
        [0, 0, 1, 1], 
     
        ]
        L, C = [1, 0, 2, 3], [1, 0, 2, 3, 5, 4]
        self.assertEquals(algo(t), (L, C))
    
    
    def test_creerTable(self):
        """
        on testera seulement si le nombre de ligne et de colonnes et bon et
         si les élèments ne contiennet que des 0 et des 1
        """
        T = creerTable(5, 3)
        self.assertEqual(len(T), 3)
        self.assertEqual(len(T[0]), 5)
        for i in range(5):
            for j in range(3):
                self.assertTrue(T[j][i] in (0, 1))
                
                
    def test_customap(self):
        l = customap([set([3, 4]), set([0, 1, 2])])
        self.assertEqual(l, [set([0, 1]), set([2, 3, 4])])
        
      
    def test_tabletostr(self):
        table, label_ligne, label_colonne = imporTable_generique(open(os.path.abspath('../Examples/table_7_10.txt')), True, True)
        ordre_ligne = [set([0, 1]), set([2, 3]), set([4, 5, 6])]
        ordre_colonne = [set([0, 1, 2]), set([3, 4]), set([5, 6, 7, 8, 9])]
        chaine = tabletostr(table, label_ligne, label_colonne, ordre_ligne, ordre_colonne)
        result = "        A B C | D E | I J F G H \na       1 0 1 | 1 1 | 1 1 1 0 1 \nb       0 1 1 | 1 1 | 0 1 1 0 0 \n--------------------------------\nc       1 0 0 | 1 1 | 1 1 1 0 0 \nd       0 1 1 | 0 1 | 0 0 1 0 1 \n--------------------------------\ne       1 1 1 | 0 1 | 0 0 0 0 1 \nf       1 0 0 | 0 1 | 1 0 0 0 1 \ng       0 0 0 | 0 1 | 1 0 1 1 0 \n"
        self.assertEqual(chaine, result)
        
        
    def test_colonnes_element(self):
        pivot = 1
        colonnes_autorisees = [1, 2, 3]
        T = [[1, 1, 0], [0, 0, 1], [1, 1, 1], [1, 1, 0], [0, 0, 1]]
        result = set([2, 3])
        self.assertEqual(colonnes_element(pivot, colonnes_autorisees, T), result)
    
if __name__ == '__main__':
    unittest.main()

