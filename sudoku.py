#!/usr/bin/python3
import copy
import sys

possible = set((1, 2, 3, 4, 5, 6, 7, 8, 9))

# A blank is a row/column, along with its square.
# The row/column intersect at a blank.
class blank(object):
    # initialize a blank instance
    def __init__(self, location, square, row, column):
        # a tuple of the blank location, such as 0,5
        self.location = location
        # a set of numbers in the square
        self.square = square
        # a set of numbers in the row
        self.row = row
        # a set of numbers in the column
        self.column = column

    def get_candidates(self):
        return possible - self.row - self.column - self.square


class board(object):
    def __init__(self):
        # keyed by position tuple, first number is row, second is column
        self.boxes = {}
        self.load()

    # return true if the board is solved.
    def solved(self):
        for v in self.boxes.values():
            if v == 0:
                return False
        return True

    def get_rows(self):
        # create an empty rows list
        rows = []
        # start counting from 0 to 8
        for row_num in range(9):
            # create an empty list for holding the numbers in the row
            row_data = []
            for k, v in self.boxes.items():
                if k[0] == row_num:
                    row_data.append(v)
            rows.append(row_data)
        return rows

    # given x/y coordinates return the set of numbers in the containing square
    def get_square(self, x, y):

        # returns the box tuple for the containing square
        def square_coordinates(num):
            one = (0, 1, 2)
            two = (3, 4, 5)
            three = (6, 7, 8)
            if num in one:
                return one
            elif num in two:
                return two
            return three

        squareset = set()
        for xloc in square_coordinates(x):
            for yloc in square_coordinates(y):
                addr = (xloc, yloc)
                if self.boxes[(xloc, yloc)] != 0:
                    squareset.add(self.boxes[(xloc, yloc)])
        return squareset

    def make_blanks(self, boxes):
        # Loop over boxes, looking for a blank (0)
        blanks = []
        for x in range(9):
            for y in range(9):
                if boxes[(x, y)] == 0:
                    # Found a blank, make a blank instance
                    blanks.append(
                        blank(
                            (x, y),
                            set([v for k, v in boxes.items() if k[0] == x]),
                            set([v for k, v in boxes.items() if k[1] == y]),
                            self.get_square(x, y)
                        )
                    )
        return blanks

    # based on the current state of the board, fill out what I can.
    def solve(self):

        # find blanks with only one possibility and fill in the answer.
        def fill(bxs):
            # returns progress
            blanks = self.make_blanks(bxs)
            progress = 0
            for blank in blanks:
                poss = blank.get_candidates()
                if len(poss) == 1:
                    bxs[blank.location] = poss.pop()
                    progress += 1
            return progress

        # keep filling in as long as you are making progress
        while fill(self.boxes) > 0:
            continue

        if self.solved():
            return

        # we went through all blanks and none had "known" solutions.
        depth = 2
        print('this board requires guessing, we must go deeper', depth)
        for blank in self.make_blanks(self.boxes):
            poss = blank.get_candidates()
            if len(poss) == depth:
                # TODO: sort out how to keep track of mutiple solutions
                for guess in poss:
                    print('guessing %d for %s' % (guess, blank.location))
                    boxes_copy = copy.deepcopy(self.boxes)
                    boxes_copy[blank.location] = guess

                    progress = fill(boxes_copy)
                    if progress == 0:
                        continue

                    self.boxes = copy.deepcopy(boxes_copy)
                    self.solve()

    def add_box(self, key, value):
        # check if key is a tuple
        if not isinstance(key, tuple):
            raise ValueError("key is not a tuple")

        # make sure the tuple has length 2
        if len(key) != 2:
            raise ValueError("key must have a length of 2")

        # make sure the tuple has only numbers in there
        for n in key:
            if not isinstance(n, int) or n > 8:
                raise ValueError("either not a number or greater than 8")

        # make sure the value is an int
        if not isinstance(value, int):
            raise ValueError("not a number yo!")

        # make sure the value is between 1 and 9
        if not (value >= 0 and value < 10):
            raise ValueError("Your value is not between 1 and 9")

        # your box looks good, add it
        self.boxes[key] = value

    def load(self):
        with open("board.txt") as f:
            lines = f.readlines()

        for line_number, line in enumerate(lines):
            # remove the invisible newline
            stripped = line.rstrip("\n")
            if len(stripped) != 9:
                raise ValueError(
                    "Line %d does not have 9 values, it is %d" %
                    (line_number, len(stripped)))
            for character_number, num in enumerate(line.rstrip("\n")):
                if num == "0":
                    raise ValueError("Use underscore for an unknown value")

                if num == "-":
                    num = 0
                self.add_box((line_number, character_number), int(num))

    def print(self):
        # get the rows
        for row_number, row in enumerate(self.get_rows()):
            # horizontal line
            if row_number % 3 == 0:
                print('+-------+-------+-------+')
            print('| ', end='')
            # We are walking across the charecters
            for box_number, box in enumerate(row):
                # TODO: don't print 0, change that to ' '
                if box == 0:
                    box = ' '
                if (box_number + 1) % 3 == 0:
                    print(box, end=' | ')
                else:
                    print(box, end=' ')

            print()
        print('+-------+-------+-------+')


def main():
    # create a board instance, which will load from board.txt
    myboard = board()

    # unsolved board
    myboard.print()

  #  while myboard.solved(myboard.boxes) != True:
    myboard.solve()

    # solved board
    myboard.print()


if __name__ == "__main__":
    main()
