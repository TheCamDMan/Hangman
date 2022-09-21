# Citation for the following program:
# Date: 8/7/2022
# Adapted from:
# Source URL: https://docs.python.org/3/howto/sockets.html
# Source URL: https://realpython.com/python-sockets/#troubleshooting
# List of words gathered from Wikipedia:
#   Source URL: https://simple.wikipedia.org/wiki/Wikipedia:List_of_1000_basic_words#:~:text=Wikipedia%3AList%20of%201000%20basic%20words.%201%20A.%20a%2C,develop%2C%20die%2C%20different%2C%20difficult%2C%20dinner%2C%20...%20More%20items

import socket
import random


# initialize the host, port, how to quit the game, and the list of words
HOST = "localhost"
PORT = 6666
END_GAME = b"/q"
WORD_LIST = [
    "about",
    "above",
    "across",
    "act",
    "active",
    "activity",
    "baby",
    "back",
    "bad",
    "bag",
    "ball",
    "bank",
    "base",
    "basket",
    "bath",
    "clothes",
    "cloud",
    "cloudy",
    "close",
    "coffee",
    "fail",
    "fall",
    "false",
    "into",
    "introduce",
    "invent",
    "juice",
    "jump",
    "last",
    "late",
    "lately",
]

# initialize the list and string that hold the guesses
correct_guesses = []
incorrect_guesses = ""

# this will display the spaces for the characters of the word
# so the user will know how many letters there are
player_display = ""

# track how many turns player has taken
turn = 0

# chose a random word from the list
chosen_word = WORD_LIST[random.randint(0, len(WORD_LIST) - 1)]

# creates the spaces for the word to display
for i in range(len(chosen_word)):
    player_display += "_"
    correct_guesses.append(None)
player_display += "\n"

# holds the different images of the hangman at different phases
boards = [
    "     ------ \n    |/     |\n    |      |\n    |\n    |\n    |\n"
    "    |\n    |\n    |\n____|____\n\n",
    "     ------ \n    |/     |\n    |      |\n    |     ( )\n    |\n    |\n    |\n"
    "    |\n    |\n    |\n____|____\n\n",
    "     ------ \n    |/     |\n    |      |\n    |     ( )\n    |      |\n    |\n"
    "    |\n    |\n    |\n____|____\n\n",
    "     ------ \n    |/     |\n    |      |\n    |     ( )\n    |    / |\n    |\n"
    "    |\n    |\n    |\n____|____\n\n",
    "     ------ \n    |/     |\n    |      |\n    |     ( )\n    |    / | \ \n    |\n"
    "    |\n    |\n    |\n____|____\n\n",
    "     ------ \n    |/     |\n    |      |\n    |     ( )\n    |    / | \ \n    |    /\n"
    "    |\n    |\n    |\n____|____\n\n",
    "     ------ \n    |/     |\n    |      |\n    |     ( )\n    |    / | \ \n    |    /   \ \n"
    "    |\n    |\n    |\n____|____\n\n",
]

# first image is the first in the list of boards
curr_board = boards[0]

# sets up the socket, connects to the host via the desired port, and listens
serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serv_sock.bind((HOST, PORT))
serv_sock.listen(1)
(client_sock, address) = serv_sock.accept()


def validate_guess(letter, word):
    """
    Validates a letter guessed by the user against the word chosen by game
    Returns True if letter is correct, returns False if letter is incorrect
    """
    if letter in word:
        return True


def add_next_letter(letter, correct_guesses, word):
    """
    Adds a letter to the player's correct guesses
    """
    index = word.index(letter)
    correct_guesses[index] = letter
    return correct_guesses


def check_winner(word, guesses):
    """
    Returns True if winner of the game, otherwise False
    """
    if None in guesses:
        return False
    if word == "".join(guesses):
        return True
    return False


def wrong_guess(letter, incorrect_guesses):
    """
    Adds a letter to the incorrect guesses
    """
    incorrect_guesses += letter
    return incorrect_guesses


def check_loser(guesses):
    """
    Returns True if the player has lost the game
    """
    return len(guesses) == 6


# the loop of the server
while True:

    # get the letter from the client
    req = client_sock.recv(4096)

    # reprompt if the user enters invalid character
    if not req.decode().isalpha:
        continue

    # closes server if the user enters the end game token /q
    if req == END_GAME:
        client_sock.sendall(b"server done")
        client_sock.close()
        serv_sock.close()
        break

    # client sends the start string if the game is just starting
    if req.decode() == "start":
        curr_board += player_display
        client_sock.sendall(curr_board.encode())
        continue

    # if the guess is valid
    if validate_guess(req.decode(), chosen_word):

        # add guess to the correct guesses
        correct_guesses = add_next_letter(req.decode(), correct_guesses, chosen_word)

        # check for the win condition
        if check_winner(chosen_word, correct_guesses):

            # build the player display
            player_display = ""
            for each in correct_guesses:
                if each == None:
                    player_display += "_"
                else:
                    player_display += each
            player_display += "\n"

            # build the data to be sent to the client
            curr_board = (
                boards[turn]
                + player_display
                + "Incorrect Guesses: "
                + incorrect_guesses
                + "\nCongrats! You Won!"
            )

            # send data to client and close the socket connections
            client_sock.sendall(curr_board.encode())
            client_sock.close()
            serv_sock.close()
            break

        # buld the player display based on what was guessed correctly
        player_display = ""
        for each in correct_guesses:
            if each == None:
                player_display += "_"
            else:
                player_display += each
        player_display += "\n"

        # builds the correct image and UI based on turn of the player
        curr_board = (
            boards[turn] + player_display + "Incorrect Guesses: " + incorrect_guesses
        )
        # send to the server
        client_sock.sendall(curr_board.encode())

    else:
        # add wrong guess to incorrect guesses string
        incorrect_guesses = wrong_guess(req.decode(), incorrect_guesses)

        # check for losing condition
        if check_loser(incorrect_guesses):

            # build the losing board and display
            curr_board = (
                boards[len(boards) - 1]
                + chosen_word
                + "\n"
                + "Incorrect Guesses: "
                + incorrect_guesses
                + "\nSorry! You Lost!"
            )

            # send to client and close socket
            client_sock.sendall(curr_board.encode())
            client_sock.close()
            serv_sock.close()
            break

        # increment the player turn
        turn += 1

        # build the display for the word and spaces
        player_display = ""
        for each in correct_guesses:
            if each == None:
                player_display += "_"
            else:
                player_display += each
        player_display += "\n"

        # build the board and send to the client
        curr_board = boards[turn] + player_display + "Guesses: " + incorrect_guesses
        client_sock.sendall(curr_board.encode())
