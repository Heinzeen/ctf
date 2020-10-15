#Time to coding

The second challenge is worth 200 points and it is called \textbf{Time to Coding}. The description of the challenge says:

>Take a look at the python code file, and find the secret message in the file data.enc.
>Flag format: flag{string}

So it seems like we have to take the data in the file *data.enc* and decrypt it using the information taken from the file *encrypt.py* (both files are given). The encrypted data is a simple string: *BBlZPqpYhG8\kJLhh\_Jh=:\}W<WKXTSZX* while the python file contains an ecnryption function:
```
import base64

def encrypt(data): 
    encrypted=""
    key=0x2F
    pre_enc=""
    for x in data:              #first part
        tmp = ord(x) 
        tmp = tmp ^ key         #just xor with 0x2f
        pre_enc+=chr(tmp)           

    pre_enc=base64.b64encode(pre_enc)   #base64
    encrypted_data=""                   #third part
                                    #invert the string
    for x in range(0, len(pre_enc)):    
        tmp = pre_enc[ len(pre_enc) - 1 -x ]    
        encrypted_data+= chr(ord(tmp) + 5 )
           
    return encrypted_data

```

#solution
To solve this challenge we have to decrypt the data contained in *data.enc*; we can do that by reversing the encryption function and thus creating a decryption function.
The encryption function is divided into three parts. It first makes a xor between every character in the plaintext and 0x2f, then it encodes the string with the base64 encryption and, in the end, it inverts the string.
We can now easily write a python function that does the opposite and give to it as input the ecnrypted function; the decryption function (with an instruction that calls it with the right parameter) is the following:

```
import base64
def decrypt(post_encode):
    decrypted_data=""           #invert the string
    for x in range(0, len(post_encode)):
        tmp = post_encode[ len(post_encode) - 1 -x ]    
        decrypted_data+= chr(ord(tmp) - 5 )
    decrypted_data=base64.b64decode(decrypted_data)
                                #decrypt with base64
    decrypted=""
    key=0x2F
    pre_enc=""
    for x in decrypted_data:        #xor with 0x2f
        tmp = ord(x) 
        tmp = tmp ^ key
        pre_enc+=chr(tmp)
    return pre_enc

msg = "BBlZPqpYhG8\kJLhh_Jh=:}W<WKXTSZX"
original = decrypt(msg)
print(original)
```

Executing this will result in the string **flag{Th1S_is_N0t_safe}** as output, which is our flag.
