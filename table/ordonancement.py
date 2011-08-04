#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import *


class Algo(object):
    def __init__(self, table):
        self.table = table
        
        self.pivot = None


    def algo(self):
        iterator = self.algo_iter()
        L, C = [set(range(len(self.table[0])))], [set(range(len(self.table)))]        
        pos_l = pos_c = 0
        
        while True:
            self.pivot = choixPivot(self.table, L[pos_l], C[pos_c])
            try:
                L, C, pos_l, pos_c = iterator.next()
            except StopIteration:
                break
        L.reverse()
        return goodListe(L), goodListe(C)


    def algo_iter(self):
        T = self.table
        L, C = [set(range(len(T[0])))], [set(range(len(T)))]
        
        pos_l = pos_c = 0

        pile = [-1]
        
        while pile:
            pivot = self.pivot
  
            c0, c1, l0, l1 = decoupage(pivot, pos_l, pos_c, L, C, T)
            new_pos_c, new_pos_l, L, C = maj(pos_c, pos_l, L, C, c0, c1, l0, l1)
  
            #reculer
            if (new_pos_l == pos_l) and (pos_l + 1 >= len(L)):
                pos_c -= 1
                pos_l = pile.pop() + 1
            else:
                if (new_pos_c > pos_c):
                    pile.append(pos_c)
                    pos_c += 1
                pos_l +=  1
            
            yield L, C, pos_l, pos_c


def algo(T):
    return Algo(T).algo()
