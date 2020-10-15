#include <stdio.h>
#include <string.h>



int main(){
    char* msg = "rxms{xqfedafmfqftueftuzs}";

    printf("len = %ld\n", strlen(msg));

    char plain[strlen(msg) + 1];
    int i;
    int j;
    for(i = strlen(msg) - 1; i >= 0; i--){
        char new;
        if(msg[i] < 123)   
            if(msg[i] - 12 >= 97)
                new = msg[i] - 12;
            else
                new = msg[i] - 12 + 26;
            
        else
            new = msg[i];
        plain[i] = new;
        
    }
    plain[strlen(msg)] = 0;                 //string terminator
    printf("plain = %s\n",plain);


    return 0;
}