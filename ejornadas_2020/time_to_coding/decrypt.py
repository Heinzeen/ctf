import base64
def decrypt(post_encode):
    decrypted_data="" 
    for x in range(0, len(post_encode)):
        tmp = post_encode[ len(post_encode) - 1 -x ]    
        decrypted_data+= chr(ord(tmp) - 5 )
    decrypted_data=base64.b64decode(decrypted_data)

    decrypted=""
    key=0x2F
    pre_enc=""
    for x in decrypted_data:
        tmp = ord(x) 
        tmp = tmp ^ key
        pre_enc+=chr(tmp)
    return pre_enc

msg = "BBlZPqpYhG8\kJLhh_Jh=:}W<WKXTSZX"    #data.enc
original = decrypt(msg)
print(original)