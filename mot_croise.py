# -*- coding: utf-8 -*-

import time
import argparse
import numpy as np
from constraint_programming import constraint_programming
# python mot_croise.py -g crossword1.txt -d words1.txt
# ajouter tqdm

argparser = argparse.ArgumentParser(
    description='Solves crosswords')

argparser.add_argument(
    '-g',
    '--grid',
    help='path to grid')

argparser.add_argument(
    '-d',
    '--dictionnary',
    help='path to dictionnary')


class CrossWord:
    def __init__(self,args):
        self.dic_path = args.dictionnary
        self.grid_path = args.grid
        self.grid_array,self.word_list,self.grid_width,self.grid_height  = self.parse()
        self.segments, self.croisements,self.croisements_bis=self.get_segments()

    def parse(self):

        with open(self.dic_path, "r") as dict_file:
            word_list = dict_file.readlines()
            word_list = [word[:-1] for word in word_list]
            self.word_list = word_list
            self.alphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
            self.wl_alph=[]
            for el in self.alphabet:
                self.wl_alph.append(el)
            for el in self.word_list:
                self.wl_alph.append(el)

        with open(self.grid_path, "r") as grid_file:
            grid_lines = grid_file.readlines()
        grid_lines = [line[:-1] for line in grid_lines]
        self.grid_width = len(grid_lines[0])
        self.grid_height = len(grid_lines)
        self.grid_array = np.zeros((self.grid_width, self.grid_height))
        for line in range(self.grid_height):
            for column in range(self.grid_width):
                if grid_lines[line][column] == ".":
                    self.grid_array[line][column] = 1

        return self.grid_array,self.word_list,self.grid_width,self.grid_height

    def solve(self):

        # On veut une var du type var = {1: un_mot, 2: un_autre_mot}
        var = {seg:set(self.wl_alph) for seg in self.segments}


        #Contrainte uniaire: impose la longueur des segments= la longueur d'un mot qui existe (restriction de l'espace)
        for s in self.segments:
            size_seg = self.segments[s][0]
            var[s]=set([w for w in self.wl_alph if len(w)==size_seg])
        # Creation du probleme
        print(var)
        P = constraint_programming(var)
        count=0
        NEQ = {(i,j) for i in self.word_list for j in self.word_list if i!=j}
        for w in self.segments:
            for z in self.segments:
                if w!=z:
                    P.addConstraint(w,z,NEQ)
        # Contraintes binaires: pour forcer les mots à s'intersecter correctement selon les croisements que l'on impose
        for c in self.croisements:
            count=count+1
            print(str(count)+ " / "+str(len(self.croisements)))

            # SOLUTION 1: (très gourmande en temps)
            word_list_1 = [p for p in self.word_list if p in var[c[0]] and len(p)>self.croisements[c][0]]
            word_list_2 = [p for p in self.word_list if p in var[c[1]] and len(p)>self.croisements[c][1]]

            BIN = {(i,j) for i in word_list_1 for j in word_list_2 if i[self.croisements[c][0]]==j[self.croisements[c][1]]}
            BIN = {(i,j) for i in word_list_1 for j in word_list_2 if i[self.croisements[c][0]]==j[self.croisements[c][1]]}
            # C0 et c1 ont la propriété d'être identiques en les index relatifs à leur chaine de caractère de croisement
            P.addConstraint(c[0],c[1],BIN)

            count=0
        for c in self.croisements_bis:
            # SOLUTION 2: l'idée est de mettre une contrainte sur croisements_to_add entre un mot et une lettre
            count=count+1
            print(str(count)+ " / "+str(len(self.croisements_bis)))
            BIN = {(i,j) for i in self.word_list for j in self.alphabet if len(i)>self.croisements_bis[c][0] and len(j)>self.croisements_bis[c][0] and i[self.croisements_bis[c][0]]==j[self.croisements_bis[c][1]] }

            P.addConstraint(c[0],c[1],BIN)

        start=time.time()
        solution= P.solve()
        end=time.time()
        print(end-start)

        return solution



    def get_segments(self):
        id_segment = 0

        horizontal_segments = {}
        for k in range(self.grid_height):
            mot_en_cours = False
            longeur_du_mot = 0
            debut = None
            for i in range(self.grid_width):
                if self.grid_array[k][i] == 1 and mot_en_cours == False:
                    mot_en_cours = True
                    longeur_du_mot = 1
                    debut = (k,i)
                elif self.grid_array[k][i] == 1 and mot_en_cours == True:
                    longeur_du_mot += 1
                elif self.grid_array[k][i] == 0 and mot_en_cours == True and longeur_du_mot > 1:
                    mot_en_cours = False
                    id_segment += 1
                    horizontal_segments[id_segment] = [longeur_du_mot, debut, (k,i-1)]
                elif self.grid_array[k][i] == 0 and mot_en_cours == True and longeur_du_mot <= 1:
                    mot_en_cours = False

        vertical_segments = {}
        for i in range(self.grid_width):
            mot_en_cours = False
            longeur_du_mot = 0
            debut = None
            for k in range(self.grid_height):
                if self.grid_array[k][i] == 1 and mot_en_cours == False:
                    mot_en_cours = True
                    longeur_du_mot = 1
                    debut = (k,i)
                elif self.grid_array[k][i] == 1 and mot_en_cours == True:
                    longeur_du_mot += 1
                elif self.grid_array[k][i] == 0 and mot_en_cours == True and longeur_du_mot > 1:
                    mot_en_cours = False
                    id_segment += 1
                    vertical_segments[id_segment] = [longeur_du_mot, debut, (k-1,i)]
                elif self.grid_array[k][i] == 0 and mot_en_cours == True and longeur_du_mot <= 1:
                    mot_en_cours = False

        croisements =[]

        for k in range(self.grid_height):
            for i in range(self.grid_width):
                if self.grid_array[k,i] == 1:
                    horizontal = None
                    vertical = None
                    for id, segment in horizontal_segments.items():
                        if k == segment[1][0] and i>= segment[1][1] and i<= segment[2][1]:
                            horizontal = [id, i]
                    if horizontal is not None:
                        for id, segment in vertical_segments.items():
                            if i == segment[1][1] and k >= segment[1][0] and k <= segment[2][0]:
                                vertical = [id, k]
                        if vertical is not None:
                            croisements.append(horizontal + vertical)
        croisements_up={}
        horizontal_segments.update(vertical_segments)
        segments = horizontal_segments

        for elem in croisements:
            croisements_up[(elem[0],elem[2])]=[elem[1],elem[3]]
        for elem in croisements_up:

            pair = croisements_up[elem]
            # Traitement du cas horizontal
            col_croise = pair[0]
            seg_horiz_length = col_croise-segments[elem[0]][1][1]
            croisements_up[elem][0]=seg_horiz_length
            # Traitement du cas vertical
            vertic_croise=pair[1]
            seg_vertic_length = vertic_croise-segments[elem[1]][1][0]
            croisements_up[elem][1]=seg_vertic_length

        # On doit rajouter des segments d'une lettre pour les intersections et mettre des contraintes dessus sur l'alphabet
        i=0
        segments_to_add={}
        curr_len_seg=len(segments)

        for c in croisements_up:
            i=i+1

            segments_to_add[i+curr_len_seg]=[]
            segments_to_add[i+curr_len_seg]=[1,c[0],c[1],croisements_up[c][0],croisements_up[c][1]]

        croisements_up_to_add={}
        for new_elem in segments_to_add:
            croisements_up_to_add[segments_to_add[new_elem][1],new_elem]=[segments_to_add[new_elem][4],0]
            croisements_up_to_add[segments_to_add[new_elem][0],new_elem]=[segments_to_add[new_elem][3],0]

        for s in segments_to_add:
            segments[s]=segments_to_add[s]

        # On doit ajouter aux croisements les "intersections" d'un segment d'une lettre et des segments normaux
        # de la forme (numero intersection, numero segment, position dans l'inter, 0)
        print(segments)
        print(croisements_up)
        print(croisements_up_to_add)
        return segments, croisements_up,croisements_up_to_add


if __name__ == '__main__':
    args = argparser.parse_args()
    solver = CrossWord(args)
    print(solver.solve())
