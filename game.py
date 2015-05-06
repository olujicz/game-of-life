#!/usr/bin/python
from random import randint
from time import sleep
from os import system
from copy import deepcopy
import sys
import signal
import getopt


def find_neighbors(matrix, x, y, dist=1):
    counter = 0
    me = matrix[x][y]
    neighbors = [
        row[max(0, y-dist):y+dist+1] for row in matrix[max(0, x-1):x+dist+1]
    ]
    for row in neighbors:
        for cell in row:
            if cell == 1:
                counter += 1
    if me == 1:
        counter -= 1

    return counter, neighbors


class Matrix:
    def __init__(self, matrix_len):
        self.matrix_len = matrix_len
        self.matrix = [
            [randint(0, 1) for i in xrange(self.matrix_len)]
            for i in xrange(self.matrix_len)
        ]

    def get(self):
        return self.matrix

    def printWorld(self):
        output = ""
        for row in self.matrix:
            for cell in row:
                if cell == 1:
                    output += " O"
                else:
                    output += " ."
            output += '\n'
        print output


class MatrixFuture(Matrix):
    def __init__(self, matrix):
        self.current_matrix = matrix
        self.matrix = deepcopy(self.current_matrix)
        for x in range(0, len(self.matrix)):
            for y in range(0, len(self.matrix)):
                me = self.matrix[x][y]
                neighbors = find_neighbors(self.current_matrix, x, y)
                if me == 0:
                    if neighbors[0] == 3:
                        me = 1
                else:
                    if neighbors[0] < 2:
                        me = 0
                    elif neighbors[0] in range(2, 3):
                        me = 1
                    elif neighbors[0] > 3:
                        me = 0

                self.matrix[x][y] = me


class PygameWorld:
    try:
        pygame = __import__('pygame')
    except ImportError:
        print "For graphic mode you need pygame module."
        sys.exit()

    def __init__(self, matrix):
        self.matrix = matrix

        self.blocksize = 10
        width = len(matrix[0]) * self.blocksize
        height = len(matrix) * self.blocksize
        display = (width, height)
        self.green = (0, 255, 0)

        self.pygame.init()
        self.pygame.display.set_caption("The game of life")
        self.screen = self.pygame.display.set_mode(display, 0, 32)

    def show(self, matrix):
        self.matrix = matrix
        status = False
        x = y = 0
        for row in self.matrix:
            for item in row:
                self.screen.fill(
                    (self.green[0]*item/1,
                     self.green[1]*item/1,
                     self.green[2]*item/1),
                    (x, y, self.blocksize - 2, self.blocksize - 2))
                y += self.blocksize
            x += self.blocksize
            y = 0
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
                sys.exit()
            elif event.type == self.pygame.KEYDOWN:
                if event.key == self.pygame.K_ESCAPE:
                    self.pygame.quit()
                    sys.exit()
                elif event.key == self.pygame.K_SPACE:
                    status = True
        self.pygame.display.update()
        return status


def signal_handler(signal, frame):
    print '\nYou pressed Ctrl+C!'
    sys.exit(0)


def start_game(matrix_len, iterations, speed, graphic):
    matrix = Matrix(matrix_len)
    signal.signal(signal.SIGINT, signal_handler)
    if graphic:
        pyWorld = PygameWorld(matrix.get())
        print "Press Escape to close."
        print "Press Space to reset."
    while iterations > 0:
        if graphic:
            state = pyWorld.show(matrix.get())
            if state:
                matrix = Matrix(matrix_len)
        else:
            system('clear')
            matrix.printWorld()
        matrix_future = MatrixFuture(matrix=matrix.get())
        if matrix.get() == matrix_future.get():
            print "\nGame over :D\nRestarting in 5 sec..."
            sleep(5)
            matrix = Matrix(matrix_len)
        else:
            matrix = matrix_future
        sleep(speed)
        iterations -= 1


def usage():
    print sys.argv[0] + \
        ' -l <matrix_len> -i <iterations> -s <speed> -g (optional graphic)'
    sys.exit()


def intOrFload(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


def main(argv):
    matrix_len = 8
    iterations = 1000
    speed = 0.3
    graphic = False

    try:
        opts, args = getopt.getopt(argv, "hl:i:s:g")
        if not opts:
            usage()
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt == '-l':
            matrix_len = int(arg)
        elif opt == '-i':
            iterations = int(arg)
        elif opt == '-s':
            speed = intOrFload(arg)
        elif opt == '-g':
            graphic = True
        else:
            usage()

    start_game(matrix_len, iterations, speed, graphic)

if __name__ == "__main__":
    main(sys.argv[1:])
