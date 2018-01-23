

import time
import argparse

argparser = argparse.ArgumentParser(
    description='Solves crosswords')

argparser.add_argument(
    '-g',
    '--grille',
    help='path to grille')

argparser.add_argument(
    '-d',
    '--dictionnaire',
    help='path to  dictionnaire')



class CrossWord:
    def __init__(self,args):
        self.dic_path = args.dictionnaire
        self.grille_path = args.grille

        self.grill_width = None
        self.grill_length = None


    def parse(self):

        with open(self.dic_path, "r") as dict_file:
            word_list = dict_file.readlines()
            word_list = [word[:-1] for word in word_list]

        print(word_list)

        with open(self.grill_path, "r") as grill_file:
            word_list = dict_file.readlines()
            word_list = [word[:-1] for word in word_list]


if __name__ == '__main__':
    args = argparser.parse_args()
    solver = CrossWord(args)
    solver.parse()





