print "if inline";
if (2 < 3) print "2 < 3";

print "if block";
if (3 < 4) {
    print "3 < 4";

}

print "if/else (3 < 2)";

if (3 < 2) 
    print "this should not print";
else
    print "this should print";

print "if/else block ( 3 < 2) ";

if (3 < 2) {
    print "this should not print";
    print "this should not print too";
} else {
    print "this should print";
    print "this should print too";
}

print "nested if/else";

if (2==2) {
    if (2==1) {
        print "this should print";        
    } else {
        print "this should not print";
    }
    print "this should print too";
}