n = 10;
a = [2,7,1,6,9,5,3,4,8,0];

print a;

n -= 1;
while (1 == 1) {
    for i=0:n {
        j = i + 1;
        if (a[i] > a[j]) {
            tmp = a[i];
            a[i] = a[j];
            a[j] = tmp;
        }
    }
    n -= 1;
    if (n == 0)
        break;
}

print a;
