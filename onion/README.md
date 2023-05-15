# Onion

This project launchs a hidden service on the tor network!

## Dockerfile Explanation ✨🐳🔧

This Dockerfile is a script that outlines the steps for building a Docker image based on the latest version of NGINX. Let's dive into the details of each instruction:

---

**FROM nginx:latest** 

This line sets the base image as the latest version of NGINX, providing a solid foundation for our custom image.

---

**EXPOSE 4242  
EXPOSE 80** 

These instructions specify that the container will expose ports 4242 and 80, allowing external connections to reach NGINX services running inside the container.

---

**RUN apt update && apt install tor -y  
RUN apt install ssh -y** 

These commands update the package repositories and install the Tor and SSH packages within the container.

---

**RUN useradd -m -d /home/ssh_user -G sudo -s /bin/bash ssh_user  
RUN mkdir -p /home/ssh_user/.ssh** 

Here, a user named "ssh_user" is created with a home directory at "/home/ssh_user". The user is added to the "sudo" group, granting administrative privileges. Additionally, a directory for SSH keys is created under the user's home directory.

---

**COPY authorized_keys /home/ssh_user/.ssh/authorized_keys  
RUN chown ssh_user:ssh_user /home/ssh_user/.ssh/authorized_keys  
RUN chmod 644 /home/ssh_user/.ssh/authorized_keys** 

These instructions copy an SSH authorized_keys file to the container, which allows SSH access with the corresponding private key. The file's ownership is set to the "ssh_user" and its permissions are adjusted to read-only for the owner.

---

**COPY init.sh /  
RUN chmod +x /init.sh** 

This step copies an initialization script named "init.sh" to the root directory ("/") of the container and grants it executable permissions.

---

**COPY index.html /usr/share/nginx/html/index.html  
COPY nginx.conf /etc/nginx/nginx.conf  
COPY sshd_config /etc/ssh/sshd_config  
COPY torrc /etc/tor/torrc** 

These instructions copy various configuration files to their respective locations within the container. The "index.html" file replaces the default NGINX landing page, while the other files adjust the NGINX, SSH, and Tor configurations to meet specific requirements.

---

Each instruction in this Dockerfile contributes to the creation of a customized NGINX image with additional components and configurations.

## 💻 Usage

1. Replace the authorized_keys content with your user public key.
2. Launch the image build (execute this command on the dockerfile folder):
```bash
docker build -t onion .
```
3. Launch this image with docker run. You can use this command:
```bash
docker run -it -p 80:80 -p 4242:4242 --name onion onion
```
4. Open a docker shell
```bash
docker exec -it onion /bin/bash
```
5. Once you are inside, execute init.sh script. Use this command:
```bash
bash /init.sh
```
6. Already all the main services are running. Try to visit your hidden service through tor network. You can user Tor Browser. Paste the hostname on the Browser:
```bash
cat /var/lib/tor/other_hidden_service/hostname
```
7. You can use ssh to connect the docker container:
```bash
ssh -p 4242 ssh_user@localhost
```

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
