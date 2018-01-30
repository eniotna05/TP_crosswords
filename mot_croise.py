import time
import argparse
import numpy as np

# python mot_croise.py -g crossword1.txt -d words1.txt

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

        self.grid_width = None
        self.grid_height = None
        self.grid_array = None

        self.word_list=None


    def parse(self):

        with open(self.dic_path, "r") as dict_file:
            word_list = dict_file.readlines()
            word_list = [word[:-1] for word in word_list]
            self.word_list = word_list

        print(word_list)

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

        print(self.grid_array)

    def solve(self):

        segments,croisements=get_segments()
        letters=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        words=self.word_list

        # On veut une var du type var = {1: un_mot, 2: un_autre_mot}
        var = {seg:set(words) for seg in segments}

        # Création du probleme
        P = constraint_programming(var)

        #Contrainte uniaire: impose la longueur des segments= la longueur d'un mot qui existe (restriction de l'espace)
        for s in segments:
            var[str(s)]=set([w for w in words if len(w)==len(s)])

        # Contraintes binaires: pour forcer les mots à s'intersecter correctement selon les croisements que l'on impose
        BIN = {(i,j) for i in segments for j in segments if i==j}

        # Imaginons par exemple que seg1[i]=seg2[j] (les deux mots se croisent, en l'indice i pour seg1 et j pour seg2)
        # Il suffit alors de boucler sur les segments en ajoutant les contraintes ainsi de suite puis de faire:
        P.addConstraint(seg1[i],seg2[j],BIN)

        return P.solve()

    def get_segments(self):
        """
        Cette fonction transforme self.words en un tableau de segments [0,0...0] de la taille des mots que l'on cherche
        Elle retourne aussi là où les mots se croisent (quels indices respectifs)

        """
        segments=[]

        return segments, croisements

if __name__ == '__main__':
    args = argparser.parse_args()
    solver = CrossWord(args)
    solver.parse()
