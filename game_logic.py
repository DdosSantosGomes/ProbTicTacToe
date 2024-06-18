# We hide the game logic here, since it is fixed. 
# We just import this ugly file into our main game class file and use it there.

board = "board(n,n,n,n,n,n,n,n,n,0).\n" 

marks = "mark(x). mark(n). mark(o).\n"

positions = """
    1/9::pos(1,1); 1/9::pos(2,1); 1/9::pos(3,1); 1/9::pos(4,1); 1/9::pos(5,1); 
               1/9::pos(6,1); 1/9::pos(7,1); 1/9::pos(8,1); 1/9::pos(9,1).

    1/9::pos(1,2); 1/9::pos(2,2); 1/9::pos(3,2); 1/9::pos(4,2); 1/9::pos(5,2); 
               1/9::pos(6,2); 1/9::pos(7,2); 1/9::pos(8,2); 1/9::pos(9,2).

    1/9::pos(1,3); 1/9::pos(2,3); 1/9::pos(3,3); 1/9::pos(4,3); 1/9::pos(5,3); 
               1/9::pos(6,3); 1/9::pos(7,3); 1/9::pos(8,3); 1/9::pos(9,3).
"""

next_move = """
    board(x,S2,S3,S4,S5,S6,S7,S8,S9,B) :- board(n,S2,S3,S4,S5,S6,S7,S8,S9,A), pos(1,B), square1G, turn(B), B is A+1.
    board(S1,x,S3,S4,S5,S6,S7,S8,S9,B) :- board(S1,n,S3,S4,S5,S6,S7,S8,S9,A), pos(2,B), square2G, turn(B), B is A+1.
    board(S1,S2,x,S4,S5,S6,S7,S8,S9,B) :- board(S1,S2,n,S4,S5,S6,S7,S8,S9,A), pos(3,B), square3G, turn(B), B is A+1.
    board(S1,S2,S3,x,S5,S6,S7,S8,S9,B) :- board(S1,S2,S3,n,S5,S6,S7,S8,S9,A), pos(4,B), square4G, turn(B), B is A+1.
    board(S1,S2,S3,S4,x,S6,S7,S8,S9,B) :- board(S1,S2,S3,S4,n,S6,S7,S8,S9,A), pos(5,B), square5G, turn(B), B is A+1.
    board(S1,S2,S3,S4,S5,x,S7,S8,S9,B) :- board(S1,S2,S3,S4,S5,n,S7,S8,S9,A), pos(6,B), square6G, turn(B), B is A+1.
    board(S1,S2,S3,S4,S5,S6,x,S8,S9,B) :- board(S1,S2,S3,S4,S5,S6,n,S8,S9,A), pos(7,B), square7G, turn(B), B is A+1.
    board(S1,S2,S3,S4,S5,S6,S7,x,S9,B) :- board(S1,S2,S3,S4,S5,S6,S7,n,S9,A), pos(8,B), square8G, turn(B), B is A+1.
    board(S1,S2,S3,S4,S5,S6,S7,S8,x,B) :- board(S1,S2,S3,S4,S5,S6,S7,S8,n,A), pos(9,B), square9G, turn(B), B is A+1.

    board(o,S2,S3,S4,S5,S6,S7,S8,S9,B) :- board(n,S2,S3,S4,S5,S6,S7,S8,S9,A), pos(1,B), square1B, turn(B), B is A+1.
    board(S1,o,S3,S4,S5,S6,S7,S8,S9,B) :- board(S1,n,S3,S4,S5,S6,S7,S8,S9,A), pos(2,B), square2B, turn(B), B is A+1.
    board(S1,S2,o,S4,S5,S6,S7,S8,S9,B) :- board(S1,S2,n,S4,S5,S6,S7,S8,S9,A), pos(3,B), square3B, turn(B), B is A+1.
    board(S1,S2,S3,o,S5,S6,S7,S8,S9,B) :- board(S1,S2,S3,n,S5,S6,S7,S8,S9,A), pos(4,B), square4B, turn(B), B is A+1.
    board(S1,S2,S3,S4,o,S6,S7,S8,S9,B) :- board(S1,S2,S3,S4,n,S6,S7,S8,S9,A), pos(5,B), square5B, turn(B), B is A+1.
    board(S1,S2,S3,S4,S5,o,S7,S8,S9,B) :- board(S1,S2,S3,S4,S5,n,S7,S8,S9,A), pos(6,B), square6B, turn(B), B is A+1.
    board(S1,S2,S3,S4,S5,S6,o,S8,S9,B) :- board(S1,S2,S3,S4,S5,S6,n,S8,S9,A), pos(7,B), square7B, turn(B), B is A+1.
    board(S1,S2,S3,S4,S5,S6,S7,o,S9,B) :- board(S1,S2,S3,S4,S5,S6,S7,n,S9,A), pos(8,B), square8B, turn(B), B is A+1.
    board(S1,S2,S3,S4,S5,S6,S7,S8,o,B) :- board(S1,S2,S3,S4,S5,S6,S7,S8,n,A), pos(9,B), square9B, turn(B), B is A+1.

    board(n,S2,S3,S4,S5,S6,S7,S8,S9,B) :- board(n,S2,S3,S4,S5,S6,S7,S8,S9,A), pos(1,B), square1N, turn(B), B is A+1.
    board(S1,n,S3,S4,S5,S6,S7,S8,S9,B) :- board(S1,n,S3,S4,S5,S6,S7,S8,S9,A), pos(2,B), square2N, turn(B), B is A+1.
    board(S1,S2,n,S4,S5,S6,S7,S8,S9,B) :- board(S1,S2,n,S4,S5,S6,S7,S8,S9,A), pos(3,B), square3N, turn(B), B is A+1.
    board(S1,S2,S3,n,S5,S6,S7,S8,S9,B) :- board(S1,S2,S3,n,S5,S6,S7,S8,S9,A), pos(4,B), square4N, turn(B), B is A+1.
    board(S1,S2,S3,S4,n,S6,S7,S8,S9,B) :- board(S1,S2,S3,S4,n,S6,S7,S8,S9,A), pos(5,B), square5N, turn(B), B is A+1.
    board(S1,S2,S3,S4,S5,n,S7,S8,S9,B) :- board(S1,S2,S3,S4,S5,n,S7,S8,S9,A), pos(6,B), square6N, turn(B), B is A+1.
    board(S1,S2,S3,S4,S5,S6,n,S8,S9,B) :- board(S1,S2,S3,S4,S5,S6,n,S8,S9,A), pos(7,B), square7N, turn(B), B is A+1.
    board(S1,S2,S3,S4,S5,S6,S7,n,S9,B) :- board(S1,S2,S3,S4,S5,S6,S7,n,S9,A), pos(8,B), square8N, turn(B), B is A+1.
    board(S1,S2,S3,S4,S5,S6,S7,S8,n,B) :- board(S1,S2,S3,S4,S5,S6,S7,S8,n,A), pos(9,B), square9N, turn(B), B is A+1.
"""

win_condition = """
    win(B) :- board(x,x,x,S4,S5,S6,S7,S8,S9,B).
    win(B) :- board(S1,S2,S3,x,x,x,S7,S8,S9,B).
    win(B) :- board(S1,S2,S3,S4,S5,S6,x,x,x,B).
    win(B) :- board(x,S2,S3,x,S5,S6,x,S8,S9,B).
    win(B) :- board(S1,x,S3,S4,x,S6,S7,x,S9,B).
    win(B) :- board(S1,S2,x,S4,S5,x,S7,S8,x,B).
    win(B) :- board(x,S2,S3,S4,x,S6,S7,S8,x,B).
    win(B) :- board(x,S2,S3,S4,x,S6,S7,S8,x,B).
"""

lose_condition = """
    lose(B) :- board(o,o,o,S4,S5,S6,S7,S8,S9,B).
    lose(B) :- board(S1,S2,S3,o,o,o,S7,S8,S9,B).
    lose(B) :- board(S1,S2,S3,S4,S5,S6,o,o,o,B).
    lose(B) :- board(o,S2,S3,o,S5,S6,o,S8,S9,B).
    lose(B) :- board(S1,o,S3,S4,o,S6,S7,o,S9,B).
    lose(B) :- board(S1,S2,o,S4,S5,o,S7,S8,o,B).
    lose(B) :- board(o,S2,S3,S4,o,S6,S7,S8,o,B).
    lose(B) :- board(o,S2,S3,S4,o,S6,S7,S8,o,B).
"""