#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses

from table.import_export import imporTable_generique
from table.utils import *
from table.ordonancement import Algo

def lignes_tableaux(table, L, C, labels_lignes, labels_colonnes, pos_l, pos_c):

    shape_colonne = [" " * max([len(label) for label in labels_lignes]), " "]

    corresp_colonnes = [0 for colonne in labels_colonnes]

    for i, elems in enumerate(C):
       elems = list(elems)
       elems.sort()


       if i == pos_c or i == pos_c + 1:
           shape_colonne[-1] = "|"
       else:
           shape_colonne[-1] = "!"

       for elem in elems:
           shape_colonne.append(" " * len(labels_colonnes[elem]))
           corresp_colonnes[elem] = len(shape_colonne) - 1
           shape_colonne.append(" ")

       if i == pos_c:
           shape_colonne[-1] = "|"
       else:
           shape_colonne[-1] = "!"

    shape_ligne = [" " * max([len(label) for label in labels_lignes]), " "]
    ligne_actu = list(shape_colonne)
    for i, corresp in enumerate(corresp_colonnes):
       ligne_actu[corresp] = labels_colonnes[i]
    shape_ligne[0] = "".join(ligne_actu)

    corresp_lignes = [0 for ligne in labels_lignes]

    for i, elems in enumerate(reversed(L)):
       elems = list(elems)
       elems.sort()


       if i == (len(L) - 1 - pos_l) or i == (len(L) - pos_l):
           shape_ligne[-1] = "~" * sum([len(x) for x in shape_colonne])
       else:
           shape_ligne[-1] = "-" * sum([len(x) for x in shape_colonne])

       for elem in elems:

           ligne_actu = list(shape_colonne)
           ligne_actu[0] = labels_lignes[elem].ljust(len(ligne_actu[0]))
           for i, corresp in enumerate(corresp_colonnes):
               ligne_actu[corresp] = str(table[i][elem]).center(len(ligne_actu[corresp]))

           shape_ligne.append("".join(ligne_actu))

           corresp_lignes[elem] = len(shape_ligne) - 1
           shape_ligne.append(" ")

       if i == (len(L) - 1 - pos_l):
           shape_ligne[-1] = "~" * sum([len(x) for x in shape_colonne])
       else:
           shape_ligne[-1] = "-" * sum([len(x) for x in shape_colonne])


    return shape_ligne, corresp_lignes


class Screen(object):
    def __init__(self):
        self.screen = curses.initscr()

    def init(self):
        curses.noecho()
        curses.cbreak()
    def finish(self):
        curses.nocbreak()
        curses.echo()
        curses.endwin()  
        
              
    def draw(self, s):
        self.screen.clear()
        y, x = 0, 0
        for l in s:
            self.screen.addstr(y, x, s[y], curses.A_NORMAL)
            y += 1

    def draw_inverse(self, y, s):
        self.screen.addstr(y, 0, s[y], curses.A_REVERSE)

class Keys(object):
    def __init__(self, screen):
        self.screen = screen

    def press(self, pos_actu, possible_lines):
        key = self.screen.getch()
        if chr(key) == 'i':
            return (pos_actu - 1) % len(possible_lines)
        elif chr(key) == 'k':
            return (pos_actu + 1) % len(possible_lines)
        elif chr(key) == ' ':        
            return None
        
        return pos_actu

if __name__ == "__main__":
    table, labels_lignes, labels_colonnes =  imporTable_generique(open('./Examples/table_10_20.txt'), False, False)

    algo = Algo(table)
    iterator = algo.algo_iter()

    screen = Screen()
    keys = Keys(screen.screen)
    screen.init()

        
    L, C = [set(range(len(table[0])))], [set(range(len(table)))]        
    pos_l = pos_c = 0
    
    while True:
        possible_lines = []
        for l in L[pos_l]:
            colonnes_utiles = colonnes_element(l, C[pos_c], table)
            est_max = True
            for l2 in L[pos_l]:
                colonnes_utiles2 = colonnes_element(l2, C[pos_c], table)
                if colonnes_utiles != colonnes_utiles2 and colonnes_utiles.issubset(colonnes_utiles2):
                    est_max = False
                    break
            if est_max:
                possible_lines.append(l)
        
        possible_lines.sort()
        pos_actu = 0
        while True:
            s, corresp_ligne = lignes_tableaux(table, L, C, labels_lignes, labels_colonnes, pos_l, pos_c)
            screen.draw(s)
            screen.draw_inverse(corresp_ligne[possible_lines[pos_actu]], s)
            screen.screen.addstr(len(s) + 1, 4, str([labels_lignes[x] for x in possible_lines]))
            touch = keys.press(pos_actu, possible_lines)
            if touch is None:
                algo.pivot = possible_lines[pos_actu]
                break
            else:
                pos_actu = touch
            
        # algo.pivot = choixPivot(table, L[pos_l], C[pos_c])
        try:
            L, C, pos_l, pos_c = iterator.next()
        except StopIteration:
            break
