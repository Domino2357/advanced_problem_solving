%NOTE: in the exercise it is asked to only put at most one of each item in the rucksack
% this can be achieved by changing "array[rucksack] of var 0..1: final"
% and obviously changing the inputs
% rucksack problem exercise 6.3
enum items;
array[items] of int: weights;
array[items] of int: values;
% maximum weight
int: maximum;

% number of chosen items
array[items] of var int: chosen;

% we ought not to have negative amounts
constraint forall(i in items) (chosen[i] >= 0);

% we are not allowed to exceed the maximum
constraint sum(i in items) (chosen[i]*weights[i]) <= maximum;


solve maximize sum(i in items) (chosen[i]*values[i]);

output ["Optimal value assignment: " ++ show(chosen) ]
