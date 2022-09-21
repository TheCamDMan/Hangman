# Hangman: Server / Client

## by Cameron Blankenship (@TheCamDMan)

### San Diego, CA

---

### Description

This is a game of Hangman played in the command line with an ASCII UI. 
The game is a demonstration of the Client/Server architecture utilizing the Python socket library.

---

### How to Use

The point of hangmans is to guess a secret word before the gallows can draw a full person. If the head, body, arms, and legs get completed, 
the game is over.

Upon start-up, the terminal will display an empty gallows, and a line with as many spaces as there are letters in the secret word.
Use the keyboard to guess a letter that you think is in the secret word.

As the game goes on, letters that are guessed correctly are filled in, and those that are incorrect are displayed so that you don't double guess a letter.

Quit the game by entering "/q" when prompted for a letter.

Good Luck!

---

## Installation

1.  Download the required client and server python files from the repository.

2a. Open two terminals and enter "python (or python3) server.py" in one, then "python client.py" in the other.

2b. If using bash terminal, open one terminal and enter "python server.py &" to run the server in the background, then "python client.py".

---

## Background

This program was assigned to me during Intro to Computer Networks as a portfolio project during my time at Oregon 
State University while pursuing my Bachelor's of Science in Computer Science.

This class served to give an introduction to the different protocols used in the OSI Model and how data is passed through the layers.
We demonstrated our understanding of the concepts by implementing reliable data transfer, a program emulating Traceroute using the ping command, 
and a client-server program using sockets for communication.

---

## Version

### v.1

This is the first public distribution of this program.

---

## Framework Used

This program was written using the socket library in Python.

---

## Credits

Portfolio Project for Oregon State University


