#!/usr/bin/python
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
            neighbors = find_neighbors(new_matrix, x, y)
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


def start_game(matrix_len, iterations, speed):
    matrix = [
        [randint(0, 1) for i in xrange(matrix_len)] for i in xrange(matrix_len)
    ]
    signal.signal(signal.SIGINT, signal_handler)
    print 'Press Ctrl+C'
    while iterations > 0:
        system('clear')
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


def print_help():
    print sys.argv[0] + ' -l <matrix_len> -i <iterations> -s <speed>'


def main(argv):
    matrix_len = 8
    iterations = 1000
    speed = 0.3

    try:
        opts, args = getopt.getopt(argv, "l:i:s:")
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-l"):
            matrix_len = int(arg)
        elif opt in ("-i"):
            iterations = arg
        elif opt in ("-s"):
            speed = arg

        start_game(matrix_len, iterations, speed)


if __name__ == "__main__":
    main(sys.argv[1:])
    print_help()
