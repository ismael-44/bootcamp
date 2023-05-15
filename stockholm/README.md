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

## 💻 Usage

Feel free to explore the individual project directories to learn more about the specific topics covered and the techniques employed. You can clone the repository and access the project files to review the code, documentation, and any accompanying materials.

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
