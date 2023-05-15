# Stockholm

## Description

This program is a didactic ransomware that demonstrates encryption and decryption functionalities. It allows users to encrypt files in a specified directory using a generated key or decrypt the encrypted files using a provided key.

## Features

- Encryption: The program encrypts files in a specified directory using the RSA algorithm with the generated key.
- Decryption: The program decrypts the encrypted files using the provided key.
- Key Generation: The program generates a private key and saves it in a file named "key.pem" for encryption and decryption operations.

## Installation

To use this program, follow these steps:

1. Install the required dependencies by running the following command: `pip install cryptography pyfiglet`
2. Save the program code in a file with the ".py" extension.
3. Run the program using the command: `python program.py [arguments]`

## 💻 Usage
The program supports the following command-line arguments:

- `-v`, `--version`: Displays the version of the program.
- `-s`, `--silent`: Runs the program in silent mode, suppressing output messages.
- `-r`, `--reverse`: Decrypts all the encrypted content using the specified key.

### Examples

1. Encrypt files in a directory:

```python
python program.py
```

2. Encrypt files in a directory silently:

```python
python program.py -s
```

3. Decrypt files using a key:

```python
python program.py -r key.pem
```

## ⚠️ Disclaimer

This program is for educational purposes only. Use it responsibly and only on systems that you own or have proper authorization to use. The author and OpenAI are not responsible for any misuse or damage caused by this program.
