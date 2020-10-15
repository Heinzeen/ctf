#Rotate away
The first challenge is worth 100 points and it is called **Rotate away**. The description of the challenge says:

>Rotate every damn day of the year

>rxms{xqfedafmfqftueftuzs}

>Flag format: flag{string}


##Solution

Both the name of the challenge and the first row of the description give us an hint about what we have to do; these references to the word *rotate* makes me think about **Caesar's cipher**. The third row of the description tells us that the flag starts with the word *flag*; it's easy to see that the first part of the string in the second row of the description (i.e. *rxms*) is the word *flag* where every character has been shifted by 12 position. It is reasonable to think that the second string is the flag, with every character shifted by 12 positions; to check this hypothesis I created a C program to shift the string and check the resulting string:


```
#include <stdio.h>
#include <string.h>

int main(){
    char* msg = "rxms{xqfedafmfqftueftuzs}";

    printf("len = %ld\n", strlen(msg));

    char plain[strlen(msg) + 1];
    int i;
    int j;
                            //iterate through the string
    for(i = strlen(msg) - 1; i >= 0; i--){  
        char new;
        if(msg[i] < 123)    //do not rotate the parenthesis
                        //manage the out-of-bound rotation
            if(msg[i] - 12 >= 97)  
                new = msg[i] - 12;
            else
                new = msg[i] - 12 + 26;
            
        else
            new = msg[i];
        plain[i] = new;
        
    }
    plain[strlen(msg)] = 0;         //string terminator
    printf("plain = %s\n",plain);


    return 0;
}
```

The output of the program is **plain = flag{letsrotatethisthing}**, which is the flag.
