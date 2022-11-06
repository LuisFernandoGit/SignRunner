import random

SIGNS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "NH", "O", "P", "Q", "R", "S",
         "T", "U", "V", "W", "X", "Y", "Z"]

def read_input(str):
    str = str.split(",")
    return str[0], str[1]

def make_input(tup):
    return str(tup[0]) + "," + str(tup[1])

class Game:
    def __init__(self, id):
        self.sign_index = 0
        self.letter = "0"
        self.hand = "0"
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.flag = False
        self.wins = [0,0]

    def get_player_move(self, p):
        if self.moves[p] != None:
            p = read_input(self.moves[p])
            pL = p[0]
            pH = p[1]
            return pL, pH
        else:
            return "", ""

    def play(self, player, move):
        self.moves[player] = move

    def connected(self):
        return self.ready

    def isReady(self):
        return self.flag

    def sign_chosen(self):
        return self.sign_index, self.hand

    def setSign(self):
        self.sign_index = random.randint(0, len(SIGNS) - 1)
        self.letter = SIGNS[self.sign_index]
        while self.hand == "0":
            if random.randint(0, 1) == 0:
                self.hand = 'Right'
            if random.randint(0, 1) == 1:
                self.hand = 'Left'
        self.flag = True

    def winner(self):
        winner = -1
        if self.moves[0] != None and self.moves[1] != None:
            p1 = read_input(self.moves[0])
            p1L = p1[0]
            p1H = p1[1]
            p2 = read_input(self.moves[1])
            p2L = p2[0]
            p2H = p2[1]

            if p1L == self.letter and p1H == self.hand:
                winner = 0
            elif p2L == self.letter and p2H == self.hand:
                winner = 1

        return winner

    def reset(self):
        if self.letter != "0" and self.hand != "0":
            index = self.winner()
            self.wins[index] += 1
            self.letter = "0"
            self.hand = "0"
            self.flag = False