a = [1,2,3];
b = [[1,2,3],[4,5,6]];

print a;
print b;

i = 1;

if (2 == 2) {
    i *= 7.0;
}

# this is not allowed
# a[0] = 7.0;

# but this is, since the type can change dynamically
a[0] = i;

print a;
