a = zeros(3,2);
print "a = zeros(3, 2) ||| ", a;

b = ones(3,2);
print "b = ones(3, 2) ||| ", b;

c = eye(3,2);
print "c = eye(3, 2) ||| ", c;

print "a .+ 1 ||| ", a .+ 1;
print "a .- 1 ||| ", a .- 1;
print "b .* 3 ||| ", b .* 3;
print "c ./ 2 ||| ", c ./ 2;

d = [1,2];
print "d = [1,2] ||| ", d;
e = [[1,2],[3,4]];
print "e = [[1,2],[3,4]] ||| ", e;

d[0] = 3;
print "d[0] = 3; ||| ", d;

e[0] = d;
f = 3;
print "e[0] = d; f = 3; ||| ", e, f;
e[0] = [-10, -f];
print "e[0] = [-10, -f]; ||| ", e;


f = [[4,5],[6,7]];
print "f = [[4,5],[6,7]] ||| ", f;
print "e * f ||| ", e .* f;
print "e * f' ||| ", e .* f';
