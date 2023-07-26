%generate

%max two people are allowed on the bridge
{ on_bridge(X): person(X) } = 2.

{ cross(X,Y,T,P, Time): person(X), person(Y), torch(T), point(P) } :- same_point(X,Y, T, P), on_bridge(X), on_bridge(Y), 
cross(Time), Time = max(time(X), time(Y)).

{ cross(X,T,P, Time): person(X), person(Y), torch(T), point(P) } :-  same_point(X,T,P), on_bridge(X),
cross(Time), Time = time(X).

{ same_point(X, Y, T,P): person(X), person(Y),torch(T),  point(P) } :- same_point(X, Y, T, start).
{ same_point(X, Y, T, P): person(X), person(Y),torch(T), point(P) } :- same_point(X, Y, T, end).



%define 
position(X, P, 0) :- init(X,P).
position(X, T, end, Time+Time) :- cross(X,_,T,start,Time).
position(X,T, start, Time+Time) :- cross(X,_,T,end, Time).

%test


%show
#show Time.


