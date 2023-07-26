%people
person(a;b;c;d).
torch(t).
% Facts
time(a,1).
time(b,2).
time(c,5).
time(d,10).
point(start; end).
%everyone starts at one end of the bridge
init(a;b;c;d;t, start).
%the goal is that all people reach the end
goal(a;b;c;d, end).