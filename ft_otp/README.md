# OTP Code Generator

This program is an OTP (One-Time Password) code generator written in Python. It allows you to generate time-based OTP codes using an encrypted key. The program supports both HOTP (HMAC-based One-Time Password) and TOTP (Time-based One-Time Password) algorithms.

## Prerequisites

Before using the program, you need to ensure that you have the following dependencies installed:

- Python 3.x
- `cryptography` library

You can install the `cryptography` library using the following command:

```bash
pip install cryptography
```
## Usage

The program accepts command-line arguments to perform different actions. Here are the available options:

- `-g` or `--save`: Generate an encrypted key. This key is required to generate time-based OTP codes. You need to provide a valid file containing a length hexadecimal string (at least 64 characters) to generate the key. The encrypted key will be saved in the `./ft_otp.key` file.

- `-k` or `--generate`: Generate a time-based OTP code using the encrypted key. You need to provide a valid file containing the encrypted key generated using the `-g` option.

- `file`: Provide a valid file path as an argument. This file will be used for generating or reading the encrypted key.

To run the program, use the following command:

```bash
python otp_code_generator.py [options] file
```
## Examples
#### Generate an encrypted key:
```bash
python otp_code_generator.py -g key.txt
```
This command will generate an encrypted key and save it in the ./ft_otp.key file. You need to provide a valid file named key.txt containing a length hexadecimal string (at least 64 characters).

#### Generate a time-based OTP code:
```bash
python otp_code_generator.py -k encrypted_key.txt
```
This command will read the encrypted key from the encrypted_key.txt file and generate a time-based OTP code.

## Important Note
The generated OTP codes are based on the current time and are only valid for a specific duration. Make sure to use the code within the time frame specified.

## Disclaimer
This program is for educational purposes only. It should not be used for any malicious activities. The author is not responsible for any misuse or unauthorized use of this program.

If you have any questions or need further assistance, feel free to contact me

Enjoy generating OTP codes with this program!
