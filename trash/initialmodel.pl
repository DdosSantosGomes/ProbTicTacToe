board(n,n,n,n,n,n,n,n,n,0).

0.6 :: cell(g,1,A); 0.3 :: cell(n,1,A); 0.1 :: cell(b,1,A) :- turn(_,A).
0.6 :: cell(g,2,A); 0.3 :: cell(n,2,A); 0.1 :: cell(b,2,A) :- turn(_,A).
0.7 :: cell(g,3,A); 0.15 :: cell(n,3,A); 0.15 :: cell(b,3,A) :- turn(_,A).
0.45 :: cell(g,4,A); 0.15 :: cell(n,4,A); 0.4 :: cell(b,4,A) :- turn(_,A).
0.6 :: cell(g,5,A); 0.15 :: cell(n,5,A); 0.25 :: cell(b,5,A) :- turn(_,A).
0.75 :: cell(g,6,A); 0.15 :: cell(n,6,A); 0.1 :: cell(b,6,A) :- turn(_,A).
0.7 :: cell(g,7,A); 0.3 :: cell(n,7,A); 0.0 :: cell(b,7,A) :- turn(_,A).
0.3 :: cell(g,8,A); 0.05 :: cell(n,8,A); 0.65 :: cell(b,8,A) :- turn(_,A).
0.55 :: cell(g,9,A); 0.3 :: cell(n,9,A); 0.15 :: cell(b,9,A) :- turn(_,A).

turn(x,1).
turn(o,2).
turn(x,3).

choose(1,1).
choose(2,1).
choose(3,1).
choose(4,1).
choose(5,1).
choose(6,1).
choose(7,1).
choose(8,1).
choose(9,1).

choose(N,B) :- choose(N,A), cell(n,N,A), B is A+1.

board(x,S2,S3,S4,S5,S6,S7,S8,S9,B) :- board(n,S2,S3,S4,S5,S6,S7,S8,S9,A), turn(x,B), cell(g,1,B), B is A+1.
board(o,S2,S3,S4,S5,S6,S7,S8,S9,B) :- board(n,S2,S3,S4,S5,S6,S7,S8,S9,A), turn(o,B), cell(g,1,B), B is A+1.
board(x,S2,S3,S4,S5,S6,S7,S8,S9,B) :- board(n,S2,S3,S4,S5,S6,S7,S8,S9,A), turn(o,B), cell(b,1,B), B is A+1.
board(o,S2,S3,S4,S5,S6,S7,S8,S9,B) :- board(n,S2,S3,S4,S5,S6,S7,S8,S9,A), turn(x,B), cell(b,1,B), B is A+1.
board(n,S2,S3,S4,S5,S6,S7,S8,S9,B) :- board(n,S2,S3,S4,S5,S6,S7,S8,S9,A), turn(_,B), cell(n,1,B), B is A+1.
board(S1,x,S3,S4,S5,S6,S7,S8,S9,B) :- board(S1,n,S3,S4,S5,S6,S7,S8,S9,A), turn(x,B), cell(g,2,B), B is A+1.
board(S1,o,S3,S4,S5,S6,S7,S8,S9,B) :- board(S1,n,S3,S4,S5,S6,S7,S8,S9,A), turn(o,B), cell(g,2,B), B is A+1.
board(S1,x,S3,S4,S5,S6,S7,S8,S9,B) :- board(S1,n,S3,S4,S5,S6,S7,S8,S9,A), turn(o,B), cell(b,2,B), B is A+1.
board(S1,o,S3,S4,S5,S6,S7,S8,S9,B) :- board(S1,n,S3,S4,S5,S6,S7,S8,S9,A), turn(x,B), cell(b,2,B), B is A+1.
board(S1,n,S3,S4,S5,S6,S7,S8,S9,B) :- board(S1,n,S3,S4,S5,S6,S7,S8,S9,A), turn(_,B), cell(n,2,B), B is A+1.
board(S1,S2,x,S4,S5,S6,S7,S8,S9,B) :- board(S1,S2,n,S4,S5,S6,S7,S8,S9,A), turn(x,B), cell(g,3,B), B is A+1.
board(S1,S2,o,S4,S5,S6,S7,S8,S9,B) :- board(S1,S2,n,S4,S5,S6,S7,S8,S9,A), turn(o,B), cell(g,3,B), B is A+1.
board(S1,S2,x,S4,S5,S6,S7,S8,S9,B) :- board(S1,S2,n,S4,S5,S6,S7,S8,S9,A), turn(o,B), cell(b,3,B), B is A+1.
board(S1,S2,o,S4,S5,S6,S7,S8,S9,B) :- board(S1,S2,n,S4,S5,S6,S7,S8,S9,A), turn(x,B), cell(b,3,B), B is A+1.
board(S1,S2,n,S4,S5,S6,S7,S8,S9,B) :- board(S1,S2,n,S4,S5,S6,S7,S8,S9,A), turn(_,B), cell(n,3,B), B is A+1.
board(S1,S2,S3,x,S5,S6,S7,S8,S9,B) :- board(S1,S2,S3,n,S5,S6,S7,S8,S9,A), turn(x,B), cell(g,4,B), B is A+1.
board(S1,S2,S3,o,S5,S6,S7,S8,S9,B) :- board(S1,S2,S3,n,S5,S6,S7,S8,S9,A), turn(o,B), cell(g,4,B), B is A+1.
board(S1,S2,S3,x,S5,S6,S7,S8,S9,B) :- board(S1,S2,S3,n,S5,S6,S7,S8,S9,A), turn(o,B), cell(b,4,B), B is A+1.
board(S1,S2,S3,o,S5,S6,S7,S8,S9,B) :- board(S1,S2,S3,n,S5,S6,S7,S8,S9,A), turn(x,B), cell(b,4,B), B is A+1.
board(S1,S2,S3,n,S5,S6,S7,S8,S9,B) :- board(S1,S2,S3,n,S5,S6,S7,S8,S9,A), turn(_,B), cell(n,4,B), B is A+1.
board(S1,S2,S3,S4,x,S6,S7,S8,S9,B) :- board(S1,S2,S3,S4,n,S6,S7,S8,S9,A), turn(x,B), cell(g,5,B), B is A+1.
board(S1,S2,S3,S4,o,S6,S7,S8,S9,B) :- board(S1,S2,S3,S4,n,S6,S7,S8,S9,A), turn(o,B), cell(g,5,B), B is A+1.
board(S1,S2,S3,S4,x,S6,S7,S8,S9,B) :- board(S1,S2,S3,S4,n,S6,S7,S8,S9,A), turn(o,B), cell(b,5,B), B is A+1.
board(S1,S2,S3,S4,o,S6,S7,S8,S9,B) :- board(S1,S2,S3,S4,n,S6,S7,S8,S9,A), turn(x,B), cell(b,5,B), B is A+1.
board(S1,S2,S3,S4,n,S6,S7,S8,S9,B) :- board(S1,S2,S3,S4,n,S6,S7,S8,S9,A), turn(_,B), cell(n,5,B), B is A+1.
board(S1,S2,S3,S4,S5,x,S7,S8,S9,B) :- board(S1,S2,S3,S4,S5,n,S7,S8,S9,A), turn(x,B), cell(g,6,B), B is A+1.
board(S1,S2,S3,S4,S5,o,S7,S8,S9,B) :- board(S1,S2,S3,S4,S5,n,S7,S8,S9,A), turn(o,B), cell(g,6,B), B is A+1.
board(S1,S2,S3,S4,S5,x,S7,S8,S9,B) :- board(S1,S2,S3,S4,S5,n,S7,S8,S9,A), turn(o,B), cell(b,6,B), B is A+1.
board(S1,S2,S3,S4,S5,o,S7,S8,S9,B) :- board(S1,S2,S3,S4,S5,n,S7,S8,S9,A), turn(x,B), cell(b,6,B), B is A+1.
board(S1,S2,S3,S4,S5,n,S7,S8,S9,B) :- board(S1,S2,S3,S4,S5,n,S7,S8,S9,A), turn(_,B), cell(n,6,B), B is A+1.
board(S1,S2,S3,S4,S5,S6,x,S8,S9,B) :- board(S1,S2,S3,S4,S5,S6,n,S8,S9,A), turn(x,B), cell(g,7,B), B is A+1.
board(S1,S2,S3,S4,S5,S6,o,S8,S9,B) :- board(S1,S2,S3,S4,S5,S6,n,S8,S9,A), turn(o,B), cell(g,7,B), B is A+1.
board(S1,S2,S3,S4,S5,S6,x,S8,S9,B) :- board(S1,S2,S3,S4,S5,S6,n,S8,S9,A), turn(o,B), cell(b,7,B), B is A+1.
board(S1,S2,S3,S4,S5,S6,o,S8,S9,B) :- board(S1,S2,S3,S4,S5,S6,n,S8,S9,A), turn(x,B), cell(b,7,B), B is A+1.
board(S1,S2,S3,S4,S5,S6,n,S8,S9,B) :- board(S1,S2,S3,S4,S5,S6,n,S8,S9,A), turn(_,B), cell(n,7,B), B is A+1.
board(S1,S2,S3,S4,S5,S6,S7,x,S9,B) :- board(S1,S2,S3,S4,S5,S6,S7,n,S9,A), turn(x,B), cell(g,8,B), B is A+1.
board(S1,S2,S3,S4,S5,S6,S7,o,S9,B) :- board(S1,S2,S3,S4,S5,S6,S7,n,S9,A), turn(o,B), cell(g,8,B), B is A+1.
board(S1,S2,S3,S4,S5,S6,S7,x,S9,B) :- board(S1,S2,S3,S4,S5,S6,S7,n,S9,A), turn(o,B), cell(b,8,B), B is A+1.
board(S1,S2,S3,S4,S5,S6,S7,o,S9,B) :- board(S1,S2,S3,S4,S5,S6,S7,n,S9,A), turn(x,B), cell(b,8,B), B is A+1.
board(S1,S2,S3,S4,S5,S6,S7,n,S9,B) :- board(S1,S2,S3,S4,S5,S6,S7,n,S9,A), turn(_,B), cell(n,8,B), B is A+1.
board(S1,S2,S3,S4,S5,S6,S7,S8,x,B) :- board(S1,S2,S3,S4,S5,S6,S7,S8,n,A), turn(x,B), cell(g,9,B), B is A+1.
board(S1,S2,S3,S4,S5,S6,S7,S8,o,B) :- board(S1,S2,S3,S4,S5,S6,S7,S8,n,A), turn(o,B), cell(g,9,B), B is A+1.
board(S1,S2,S3,S4,S5,S6,S7,S8,x,B) :- board(S1,S2,S3,S4,S5,S6,S7,S8,n,A), turn(o,B), cell(b,9,B), B is A+1.
board(S1,S2,S3,S4,S5,S6,S7,S8,o,B) :- board(S1,S2,S3,S4,S5,S6,S7,S8,n,A), turn(x,B), cell(b,9,B), B is A+1.
board(S1,S2,S3,S4,S5,S6,S7,S8,n,B) :- board(S1,S2,S3,S4,S5,S6,S7,S8,n,A), turn(_,B), cell(n,9,B), B is A+1.


query(board(x,n,n,n,n,n,n,n,n,1)).
query(board(x,n,n,n,n,n,n,n,n,2)).
query(cell(g,1,1)).
query(cell(g,1,2)).
