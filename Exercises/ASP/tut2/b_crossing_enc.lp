%encoding

%define
leftSide(X, 0) :- p(X).
leftSide(X, 0) :- torch(X).

%at most two people cross at every move
1{cross(X, S): p(X), step(S)}2 :- S=1..5.
1{cross(X, S): torch(X), step(S)}1 :- S=1..5.

%when a person crosses, she is on the other side
leftSide(X, S) :- cross(X, S), rightSide(X, S-1), step(S) .
rightSide(X, S) :- cross(X, S), leftSide(X, S-1), step(S).
leftSide(X, S) :- not cross(X, S), leftSide(X, S-1), step(S).
rightSide(X,S) :- not cross(X,S), rightSide(X, S-1), step(S).

%
cost(C, S) :-C= #max {T: cross(X,S), p(X), step(S), t(X, T)}, S=1..5.
finalCost(F) :- F= #sum {C, S: cost(C,S), step(S)}.
%test

%people can only cross if the torch is on the same side
:- cross(X, S), p(X), rightSide(X, S), leftSide(Y, S), torch(Y), step(S).
:- cross(X, S), p(X), leftSide(X, S), rightSide(Y, S), torch(Y), step(S).
%people need to be on the same side to cross
:- cross(X,S), cross(Y, S), p(X), p(Y), leftSide(X, S), rightSide(Y,S), step(S).
:- cross(X,S), cross(Y, S), p(X), p(Y), rightSide(X, S), leftSide(Y,S), step(S).
%people need to cross with the torch
:- cross(X,S), not cross(Y,S), p(X), torch(Y).
%at the end everyone needs to be on the other side
:- leftSide(X, S), S==5, step(S), p(X).

#minimize{F: finalCost(F)}.