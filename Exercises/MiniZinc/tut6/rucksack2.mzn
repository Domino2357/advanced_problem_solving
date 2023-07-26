%NOTE: in the exercise it is asked to only put at most one of each item in the rucksack
% this can be achieved by changing "array[rucksack] of var 0..1: final"
% and obviously changing the inputs

%rucksack
enum rucksack = {item1, item2, item3, item4};
array[rucksack] of int: values = [54, 106, 254, 295];
array[rucksack] of int: weights = [20, 40, 85, 110];
%number of final values
array[rucksack] of var int: final;
%max capacity
int: capacity;

%computation
constraint(forall (i in rucksack) (final[i] >= 0));
constraint(sum(i in rucksack) (final[i]*weights[i])<= capacity);

solve maximize (sum(i in rucksack) (final[i]*values[i]));

