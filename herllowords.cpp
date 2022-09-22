#include <iostream>
#include <string>
#include <cmath>
#include <stdlib.h>

using namespace std;

/*
https://cplusplus.com/reference/cstdio/printf/
https://www.tutorialspoint.com/c_standard_library/c_function_scanf.htm
*/



int test() {
    int a = 1, b=2;
    double b_flt = 2.1;

    return 1 + 2;
}

int main() {
    const int xx = 20;
    const double lightSpeed = 3e8; //valid

    char x;
    // cout << "type something:"; 
    // cin >> x; // same line as the previous
    // cout << x; // newline

    /*
    entering the wrong variable doesnt throw an error
    but defaults the variable entry 
    to something like 0

    for char, as if I"m gonna use that
    it's the first letter of an assumed 
    string entered
    */

    // operator shenanigans
    int c = 69;
    cout << c << " <3 \n" << c ++ ; // aha this is how ya do it
    // cout doesn't newline
    c +=2;
    cout << c << "\n" ;
    cout << "bool:" << (c < xx) << "\n";
    // && and || for the logical ops

    // strings: concat; 
    string strand = "strangles";
    strand = strand += " yes"; 
    cout << strand << " -|- " << strand.append(" and I appended this.");
    cout << "\n" << strand.length();
    cout << "\n" << strand[0] << "\n";
    // awwwwwww
    for (int i = 0; i < 10; i++) {
        // ah, loop syntax
        cout << strand[i];
    }
    
    for (int i = 0; i < 54; i++) {
        if (i < 20) {
            cout << i;
        } else if (i == 20) { // double equals lmao
            cout << i << "B";
        } else {
            cout << i;
        }
    }
    string result = (xx > 10) ? "True" : "False";
    cout << result;

    // swtiches (ahaaaa)
    


    return 10; //ends func yes

    // skipping this bit just cuz
    cout << "so is this bit being used?";
    cout << test;
    return 0; //ends func ??
}
/*multi line comment
*/