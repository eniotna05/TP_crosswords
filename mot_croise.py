import time
import argparse
import numpy as np

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


    def parse(self):

        with open(self.dic_path, "r") as dict_file:
            word_list = dict_file.readlines()
            word_list = [word[:-1] for word in word_list]

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

if __name__ == '__main__':
    args = argparser.parse_args()
    solver = CrossWord(args)
    solver.parse()





