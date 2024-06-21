% 1 cell 

turn(x,1).
turn(o,2).
turn(x,3).
turn(o,4).


board(n,0).

0.65::square1G(N); 0.05::square1B(N); 0.3::square1N(N).

board(x,B) :- board(n,A), turn(x,B), square1G(B), B is A+1.
board(o,B) :- board(n,A), turn(o,B), square1G(B), B is A+1.

board(o,B) :- board(n,A), turn(x,B), square1B(B), B is A+1.
board(x,B) :- board(n,A), turn(o,B), square1B(B), B is A+1.

board(n,B) :- board(n,A), turn(_,B), square1N(B), B is A+1.

board(x,B) :- board(x,A), turn(_, B), B is A+1.
board(o,B) :- board(o,A), turn(_, B), B is A+1.

x_in_one :- board(x,1). 
x_in_two :- board(n,1), board(x,2).
x_in_one_then_two :- board(x,1), board(x,2). 


win(T) :- board(x,T).
lose(T) :- board(o,T).
tie(T) :- board(n,T). 

% queries
query(x_in_one).
query(x_in_two).
query(win(4)).



% 2 cells

% %% possible turns
turn(o,1).
turn(x,2).
turn(o,3).
turn(x,4).
turn(o,5).
turn(x,6).
turn(o,7).
turn(x,8).
turn(o,9).

board(n,n,0).

1/2::pos(1,1); 1/2::pos(2,1).
1/2::pos(1,2); 1/2::pos(2,2).
1/2::pos(1,3); 1/2::pos(2,3).

0.65::square1G(N); 0.05::square1B(N); 0.3::square1N(N).
0.65::square2G(N); 0.05::square2B(N); 0.3::square2N(N).

board(x,S,B) :- board(n,S,A), pos(1,B), turn(x,B), square1G(B), B is A+1.
board(S,x,B) :- board(S,n,A), pos(2,B), turn(x,B), square1G(B) B is A+1.
board(o,S,B) :- board(n,S,A), pos(1,B), turn(x,B), square1B(B), B is A+1.
board(S,o,B) :- board(S,n,A), pos(2,B), turn(x,B), square1B(B) B is A+1.

board(o,S,B) :- board(n,S,A), pos(1,B), turn(o,B), square1G(B), B is A+1.
board(S,o,B) :- board(S,n,A), pos(2,B), turn(o,B), square1G(B), B is A+1.
board(x,S,B) :- board(n,S,A), pos(1,B), turn(o,B), square1B(B), B is A+1.
board(S,x,B) :- board(S,n,A), pos(2,B), turn(o,B), square1B(B), B is A+1.

win(B) :- board(x,x,B).
lose(B) :- board(o,o,B).

x1_in_one :- board(x,_,1).
x1_in_two :- board(x,_,2).

x_1_in_two_not_one :- board(n,_,1), board(x,_,2).
x_1_in_two_not_one :- board(o,_,1), board(x,_,2).


% % queries
query(x1_in_one).
query(x1_in_two).
query(x_1_in_two_not_one).