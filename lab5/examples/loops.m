print "for block";
for i = 1:3 {
    print i;
    print i+1;
}

print "for inline";
for j = 2:7 print j*2;

print "nested for";
for i = 1:10 {
    a = 1;
    for j = 1:i
        a *= j;
    print a;
}

print "for break (from 1 to 10, breaks at 5)";
for i = 1:10 {
    print i;
    if (i==5) break;
}

print "for continue (from 1 to 10, does not print 5)";
for i = 1:10 {
    if (i==5) continue;
    print i;
}

print "while block";
while (i > 1) {
    print i;
    i -= 1;
}

print "while break (until 1, breaks at 5";
i = 10;
while (i > 1) {
    if (i == 5) break;
    print i;
    i -= 1;
}

i = 11;
print "while continue (until 1, does not print 5";
while (i > 1) {
    i -= 1;
    if (i == 5) continue;
    print i;
}

print "while inline (inifnite)";
# while (1<2) print "OJEJ";
