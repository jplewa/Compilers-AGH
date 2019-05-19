n = 10;
a = [2,7,1,6,9,5,3,4,8,0];

print a;

for i=1:n {
    x = a[i];
    j = i - 1;
    while (j >= 0) {
        if (a[j] <= x)
            break;
        k = j + 1;
        a[k] = a[j];
        j -= 1;
    }
    k = j + 1;
    a[k] = x;
}

print a;
