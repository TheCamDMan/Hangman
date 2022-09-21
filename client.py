# Citation for the following program:
# Date: 8/7/2022
# Adapted from:
# Source URL: https://docs.python.org/3/howto/sockets.html
# Source URL: https://internalpointers.com/post/making-http-requests-sockets-python

import socket

# the chosen port number
PORT = 6666

# creates a socket that can be reused
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# connects socket to local host with chosen port number
s.connect(("localhost", PORT))

# print welcome message and send to server
print("Welcome to Hangman!\nEnter '/q' to quit")
s.sendall(b"start")

# get and print the response from the server
response = s.recv(4096)
print(response.decode())

# game loop
while True:

    # get input from the user
    guess = input("Go ahead and guess a letter: ")

    # reprompt player if nothing is entered
    if len(guess) == 0:
        continue

    # send the end game token to the server
    if guess == "/q":
        s.sendall(b"/q")

        # get response and close the socket
        response = s.recv(4096)
        if response.decode() == "server done":
            print("Thanks for playing!")
            s.close()
            break

    # send the guess as binary to the host
    s.sendall(guess.encode())

    # get the response from the server
    response = s.recv(4096)

    # print the response to the server
    print(response.decode())

    # checking reponse for a win or loss
    if (
        "Sorry! You Lost!" in response.decode()
        or "Congrats! You Won!" in response.decode()
    ):
        # if win or lose, close the socket connection
        s.close
        break
