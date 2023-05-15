import argparse, hashlib, os, hmac, base64, struct, time, re
from cryptography.fernet import Fernet, InvalidToken

#Global variables
key = None

def newkeycheck(file):
    global key
    try:
        with open(file) as opfil:
            key = opfil.read()
            regex = r'^[0-9a-fA-F]{64,}$'
            r = re.compile(regex)
            if re.match(r, key):
                print("")
            else:
                print("This string is not an hex string")
                exit()
    except(OSError, FileNotFoundError,) as e:
        print("Error trying to open file")
        print(e)
        exit()

def cifkey(key):
    destiny = "./ft_otp.key"
    cif_key = Fernet.generate_key()
    with open ("./master.key" , 'wb') as master:
        master.write(cif_key)
        print("Master key saved on ./master.key")
    f = Fernet(cif_key)
    encoded_key = key.encode()
    encrypted_key = f.encrypt(encoded_key)
    encrypted_key = encrypted_key.decode()
    if os.path.exists(destiny):
        with open(destiny, 'w') as f:
            f.write(encrypted_key)
            print("New key saved on ./ft_otp.key")

def readkey(file):
    try:
        with open ("./master.key", "r") as master:
            cif_key = master.read()
        with open (file, 'r') as key:
            encrypt = key.read()
        f = Fernet(cif_key)
        decrypted = f.decrypt(encrypt)
        decrypted = decrypted.decode('utf-8')
        return decrypted
    except(InvalidToken, FileNotFoundError, IsADirectoryError, TypeError) as e:
        print("Error trying to decrypt")
        print(e)
        exit()

def get_hotp_token(secret, intervals_no):
    key = base64.b85decode(secret)
    #decoding our key
    msg = struct.pack(">Q", intervals_no)
    #conversions between Python values and C structs represente
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = o = h[19] & 15
    #Generate a hash using both of these. Hashing algorithm is HMAC
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    #unpacking
    return h

def get_totp_token(secret):
    #ensuring to give the same otp for 30 seconds
    x =str(get_hotp_token(secret,intervals_no=int(time.time())//30))
    #adding 0 in the beginning till OTP has 6 digits
    while len(x)!=6:
        x+='0'
    return x
    
def main():
    parser = argparse.ArgumentParser(description="Password generator")
    parser.add_argument("-g", "--save" , help="Using a length hexadecimal string (at least 64 characters) generate an encrypted key. This key is needed to generate based time OTP codes", action="store_true")
    parser.add_argument("-k" , "--generate" , help="Generate time based OTP code, using the encrypt key. If you dont have key, generate one using -g ", action="store_true")
    parser.add_argument("file", help="Provide a valid file" , type=str)
    args = parser.parse_args()
    if not (args.save or args.generate):
        parser.error('No action requested, add -g or -k option')

#Adding arguments to variables
    file = args.file
    gen = args.generate
    save = args.save

#Calling functions
    if gen == True:
        decrypted = readkey(file)
        print(get_totp_token(decrypted))

    elif save == True:   
        newkeycheck(file)
        cifkey(key)

if __name__ == '__main__':
    main()

