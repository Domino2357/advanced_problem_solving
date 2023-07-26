%define graph

node(1..4).

edge(1,2).
edge(1,3).
edge(2,4).
edge(3,4).
%edge(4,3).
edge(X,Y) :- edge(Y,X).
