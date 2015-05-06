#!/usr/bin/python
import pygame
from random import randint
from time import sleep
from os import system
from copy import deepcopy
import sys
import signal
import getopt


def signal_handler(signal, frame):
    print '\nYou pressed Ctrl+C!'
    sys.exit(0)


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


def newStep(current_matrix, matrix_len):
    new_matrix = deepcopy(current_matrix)
    for x in range(0, matrix_len):
        for y in range(0, matrix_len):
            me = new_matrix[x][y]
            neighbors = find_neighbors(current_matrix, x, y)
            if me == 1:
                if neighbors[0] < 2:
                    me = 0
                elif neighbors[0] in range(2, 3):
                    me = 1
                elif neighbors[0] > 3:
                    me = 0
            else:
                if neighbors[0] == 3:
                    me = 1
            new_matrix[x][y] = me

    return new_matrix, current_matrix


def printWorld(matrix):
    output = ""
    for row in matrix:
        for cell in row:
            if cell == 1:
                output += " O"
            else:
                output += " ."
        output += '\n'
    print output


def pygameWorld(matrix):
    blocksize = 16
    width = len(matrix[0]) * blocksize
    height = len(matrix) * blocksize
    display = (width, height)
    green = (0, 255, 0)

    pygame.init()
    pygame.display.set_caption("The game of life")
    screen = pygame.display.set_mode(display, 0, 32)

    x = y = 0
    for row in matrix:
        for item in row:
            screen.fill(
                (green[0]*item/1, green[1]*item/1, green[2]*item/1),
                (x, y, blocksize - 2, blocksize - 2))
            y += blocksize
        x += blocksize
        y = 0
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
                return


def start_game(matrix_len, iterations, speed, graphic):
    matrix = [
        [randint(0, 1) for i in xrange(matrix_len)] for i in xrange(matrix_len)
    ]
    signal.signal(signal.SIGINT, signal_handler)
    print 'Press Ctrl+C'
    while iterations > 0:
        system('clear')
        if graphic:
            pygameWorld(matrix)
        else:
            printWorld(matrix)
        matrix, current_matrix = newStep(matrix, matrix_len)
        if matrix == current_matrix:
            print "\nGame over :D\nRestarting in 5 sec..."
            sleep(5)
            matrix = [
                [randint(0, 1) for i in xrange(matrix_len)]
                for i in xrange(matrix_len)
            ]
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
