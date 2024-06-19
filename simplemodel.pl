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
% turn(x,0).
% turn(o,1).
% turn(x,2).
% turn(o,3).
% turn(x,4).
% turn(o,5).
% turn(x,6).
% turn(o,7).
% turn(x,8).
% turn(o,9).
% 
% board(n,n,0).
% 
% 1/2::pos(1,1); 1/2::pos(2,1).
% 
% 1/2::pos(1,2); 1/2::pos(2,2).
% 
% 1/2::pos(1,3); 1/2::pos(2,3).
% 
% board(x,_,B) :- board(n,_,A), pos(1,B), turn(x,B), B is A+1.
% board(_,x,B) :- board(_,n,A), pos(2,B), turn(x,B), B is A+1.
% 
% board(o,_,B) :- board(n,_,A), pos(1,B), turn(o,B), B is A+1.
% board(_,o,B) :- board(_,n,A), pos(2,B), turn(o,B), B is A+1.
% 
% win(B) :- board(x,x,B).
% lose(B) :- board(o,o,B).
% 
% 
% % queries
% query(board(o,n,1)).
% query(win(2)).
% query(lose(2)).