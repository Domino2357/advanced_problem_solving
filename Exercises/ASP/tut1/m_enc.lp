%find the perfect matching for a graph

%generate
%{ matching(X,Y) } = 1 :- matching(X,Y).

%define
0{matching(X,Y)}1 :- edge(X,Y).
matching(X,Y) :- matching(Y,X).

%test
:- matching(X,Y), matching(X,Z), Y != Z.

show matching/2.