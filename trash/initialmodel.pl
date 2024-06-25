0.4 :: cell(1,good,A); 0.3 :: cell(1,neutral,A); 0.3 :: cell(1,bad,A) :- turn(_,A).
0.8 :: cell(2,good,A); 0.1 :: cell(2,neutral,A); 0.1 :: cell(2,bad,A) :- turn(_,A).
0.6 :: cell(3,good,A); 0.25 :: cell(3,neutral,A); 0.15 :: cell(3,bad,A) :- turn(_,A).
0.45 :: cell(4,good,A); 0.25 :: cell(4,neutral,A); 0.3 :: cell(4,bad,A) :- turn(_,A).
0.35 :: cell(5,good,A); 0.3 :: cell(5,neutral,A); 0.35 :: cell(5,bad,A) :- turn(_,A).
0.45 :: cell(6,good,A); 0.15 :: cell(6,neutral,A); 0.4 :: cell(6,bad,A) :- turn(_,A).
0.4 :: cell(7,good,A); 0.25 :: cell(7,neutral,A); 0.35 :: cell(7,bad,A) :- turn(_,A).
0.95 :: cell(8,good,A); 0.05 :: cell(8,neutral,A); 0.0 :: cell(8,bad,A) :- turn(_,A).
0.55 :: cell(9,good,A); 0.05 :: cell(9,neutral,A); 0.4 :: cell(9,bad,A) :- turn(_,A).

turn(x,1).
turn(o,2).
turn(x,3).

board(C,P,B) :- board(C,n,A), cell(C,good,B), turn(P,B), play(C,B), B is A+1.
board(C,o,B) :- board(C,n,A), cell(C,bad,B), turn(x,B), play(C,B), B is A+1.
board(C,x,B) :- board(C,n,A), cell(C,bad,B), turn(o,B), play(C,B), B is A+1.
board(C,n,B) :- board(C,n,A), cell(C,good,B), turn(_,B), play(C,B), B is A+1.
board(C,P,B) :- board(C,P,A), turn(_,B), \+play(C,B), B is A+1.

win1(A) :- board(1,x,A),board(2,x,A),board(3,x,A).
win2(A) :- board(4,x,A),board(5,x,A),board(6,x,A).
win3(A) :- board(7,x,A),board(8,x,A),board(9,x,A).
win4(A) :- board(1,x,A),board(4,x,A),board(7,x,A).
win5(A) :- board(2,x,A),board(5,x,A),board(8,x,A).
win6(A) :- board(3,x,A),board(6,x,A),board(9,x,A).
win7(A) :- board(3,x,A),board(5,x,A),board(7,x,A).
win8(A) :- board(1,x,A),board(5,x,A),board(9,x,A).

lose1(A) :- board(1,o,A),board(2,o,A),board(3,o,A).
lose2(A) :- board(4,o,A),board(5,o,A),board(6,o,A).
lose3(A) :- board(7,o,A),board(8,o,A),board(9,o,A).
lose4(A) :- board(1,o,A),board(4,o,A),board(7,o,A).
lose5(A) :- board(2,o,A),board(5,o,A),board(8,o,A).
lose6(A) :- board(3,o,A),board(6,o,A),board(9,o,A).
lose7(A) :- board(3,o,A),board(5,o,A),board(7,o,A).
lose8(A) :- board(1,o,A),board(5,o,A),board(9,o,A).

win(A) :- win1(A), \+ lose(B), turn(_,B), B < A.
win(A) :- win2(A), \+ lose(B), turn(_,B), B < A.
win(A) :- win3(A), \+ lose(B), turn(_,B), B < A.
win(A) :- win4(A), \+ lose(B), turn(_,B), B < A.
win(A) :- win5(A), \+ lose(B), turn(_,B), B < A.
win(A) :- win6(A), \+ lose(B), turn(_,B), B < A.
win(A) :- win7(A), \+ lose(B), turn(_,B), B < A.
win(A) :- win8(A), \+ lose(B), turn(_,B), B < A.

lose(A) :- lose1(A), \+ win(B), turn(_,B), B < A.

board(1,n,0).
board(2,o,0).
board(3,o,0).
board(4,x,0).
board(5,n,0).
board(6,n,0).
board(7,o,0).
board(8,x,0).
board(9,n,0).

0.25 :: play(1,A); 0.25 :: play(5,A); 0.25 :: play(6,A); 0.25 :: play(9,A) :- turn(_,A).
evidence(play(9,1)).
query(win(3)).