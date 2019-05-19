n = 10;
a = [2,7,1,6,9,5,3,4,8,0];

print a;

for i=0:n {
    if (i == n - 1) {
        break;
    }
    k = i;
    l = i + 1;
    for j=l:n {
        if (a[j] < a[k]) {
            k = j;
        }
    }
    if (k != i) {
        tmp = a[k];
        a[k] = a[i];
        a[i] = tmp;
    }
}

print a;
