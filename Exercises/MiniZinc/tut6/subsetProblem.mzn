% Use this editor as a MiniZinc scratch book
set of int: topSet = {3, 4, -2, -4, 5,1,2, 10, 13, -4};
var set of topSet: subSet;
constraint( sum( i in subSet) (i)==0); 
constraint(subSet != {});
solve satisfy;