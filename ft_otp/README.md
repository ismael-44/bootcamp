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
python ft_otp.py [options] file
```
## Examples
#### Generate an encrypted key:
```bash
python ft_otp.py -g key.txt
```
This command will generate an encrypted key and save it in the ./ft_otp.key file. You need to provide a valid file named key.txt containing a length hexadecimal string (at least 64 characters).

#### Generate a time-based OTP code:
```bash
python ft_otp.py -k encrypted_key.txt
```
This command will read the encrypted key from the encrypted_key.txt file and generate a time-based OTP code.

## Important Note
The generated OTP codes are based on the current time and are only valid for a specific duration. Make sure to use the code within the time frame specified.

## ⚠️ Disclaimer

Attention Users! Your commitment to responsible and ethical use is essential. Please read and abide by the following cybersecurity disclaimer:

1. **Educational Purpose**: This repo is intended for educational and research purposes only. It serves as a platform to explore cybersecurity concepts, techniques, and vulnerabilities in a controlled and legal environment. It must not be used for any malicious or unauthorized activities.

2. **Lawful Usage**: Ensure that your usage of the repo complies with all applicable laws, regulations, and ethical guidelines in your jurisdiction. Any actions that infringe upon the privacy, security, or rights of individuals, organizations, or systems are strictly prohibited.

3. **Informed Consent**: Obtain proper authorization and informed consent before conducting any security assessments, vulnerability testing, or penetration testing. Unauthorized access or attempts to exploit vulnerabilities without explicit permission are unlawful and unethical.

4. **Respect for Privacy**: Respect the privacy and confidentiality of others. Do not share or disclose any sensitive information obtained through the repo without proper authorization. Treat personal data with the utmost care and comply with relevant privacy laws and regulations.

5. **Secure Environment**: Use the hacker repository in a secure environment and on systems that you have explicit permission to access. Take appropriate measures to protect your own systems and networks from any unintended consequences or exposure to vulnerabilities.

6. **Accountability**: You are solely responsible for your actions and their consequences when using the repo. The maintainers, contributors, and owners of the repo are not liable for any damages, losses, or legal repercussions resulting from the misuse or unauthorized use of the repo.

7. **Ethical Conduct**: Promote ethical conduct and professionalism in your use of the hacker repository. Do not cause harm, disrupt services, or compromise the integrity of systems or networks. Act responsibly, transparently, and with respect for others' security and privacy.

Remember, the repo is a tool to enhance your understanding of cybersecurity. It is your responsibility to ensure that you use it responsibly and ethically, contributing positively to the field of cybersecurity.

Stay curious, learn responsibly, and help build a safer digital world! 🛡️🔒


If you have any questions or need further assistance, feel free to contact me

Enjoy generating OTP codes with this program!
