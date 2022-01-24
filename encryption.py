Alphabets = [
                'a','!','@','M','9','N','8','c','d','g',
                'D','E','F','G','H',
                'h','i','j','k',')','l','&','m','n','(','q',
                'r','s','t','u','w','x','y','z','v','e','f','#','$',
                '%','R','+','-','o','p','~','^','C',
                'I','J','K','L','O','3','P','Q','S','1','T','5','U','X','V','W','Y','0',
                'Z','2','b','4','6','A','7','B',
            ]


def encrypt(shift,message):

    if shift > 73:
        shift = shift % 73

    enc_msg = ""

    for i in range( len(message)):

        to_find = message[i]
        j = 0

        while  j < 74:
            if Alphabets[j] == to_find:
                position = j
                break
            j+=1

        if j > 73:
            enc_msg += message[i]
            continue

        position += shift

        if position > 73:
            position -= 73

        enc_msg += Alphabets[position]

    return enc_msg



def decrypt(shift,message):

    if shift > 73:
        shift = shift % 73

    dec_msg = ""

    for i in range( len(message)):

        to_find = message[i]
        j = 0

        while  j < 74:
            if Alphabets[j] == to_find:
                position = j
                break
            j+=1

        if j > 73:
            dec_msg += message[i]
            continue

        position -= shift

        if position < 0 :
            position += 73

        dec_msg += Alphabets[position]

    return dec_msg





# message = input("Enter the message: ")
# choice = input("Type 'Encrypt' to encrypt or 'Decrypt' to decrypt The message: ")
# shift = int(input("Enter the key: "))

# choice = choice.lower()

# if choice == "encrypt":
#     encoded_msg = encrypt(Alphabets, 9, message.lower())
#     print("Encrypted message is : " + encoded_msg)
# elif choice == "decrypt" :
#     decoded_msg = decrypt(Alphabets, 9, message)
#     print(decoded_msg)
# else:
#     print("Give the required inputes properly")
