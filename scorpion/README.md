# Image Metadata Viewer

This script allows you to view the metadata of an image file. It utilizes the Python Imaging Library (PIL) to extract and display the metadata information.

## Usage

To run the script, execute it in your Python environment and provide one or more image file paths as command-line arguments. The script will display the metadata information for each image.

```shell
python script.py image1.jpg image2.png image3.bmp
```
## Script Explanation
The script begins by importing the necessary modules:

```python
import sys
from PIL import Image
from PIL.ExifTags import TAGS
```

- sys module is imported to access command-line arguments.
- Image class from the PIL module is used to work with images.
- TAGS dictionary from PIL.ExifTags is imported to map the EXIF tag IDs to their corresponding tag names.

### Next, a function named show_metadata is defined to display the metadata of an image file:

```python
def show_metadata(image_path):
    try:
        with Image.open(image_path) as img:
            # Show basic metadata
            print(" ")
            print(" ")
            print(f"Image: {image_path}")
            print(f"Format: {img.format}")
            print(f"Size: {img.size}")
            print(f"Mode: {img.mode} ")
            
            # Retrieve EXIF data
            exif_data = img.getexif()

            if exif_data:
                print("Exif data:")
                for tag, value in exif_data.items():
                    tag = TAGS.get(tag, tag)
                    data = exif_data.get(tag)
                    if isinstance(data, bytes):
                        data = data.decode()
                    print(f"{tag}: {value}")
            else:
                print("No EXIF data found")
                print("..................")
                
    except OSError:
        print(f"Could not open file {image_path}")
```
- The show_metadata function takes an image_path argument representing the path of the image file.
- Inside the function, the image is opened using Image.open(image_path) and assigned to the img variable.
- Basic metadata such as image format, size, and mode are printed.
- The EXIF data is retrieved using img.getexif().
- If EXIF data is found, it is iterated over, and each tag and its corresponding value are printed.
- If no EXIF data is found, a corresponding message is displayed.
- In case of an OSError when opening the file, an error message is printed.

### Finally, the main execution code checks the command-line arguments and calls the show_metadata function for each valid image file:

```python
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Provide at least one image")
    else:
        for image_path in sys.argv[1:]:
            if image_path.endswith(('jpg', 'png', 'bmp', 'gif')):
                show_metadata(image_path)
            else:
                print("Filetype not supported")
```
The if __name__ == '__main__': condition ensures that the code inside it is only executed when the script is run directly, not when imported as a module.

It checks if the number of command-line arguments is sufficient, and if not, it displays a corresponding message.

For each image file provided as a command-line argument, the show_metadata function is called, but only for image file types ending with 'jpg', 'png', 'bmp', or 'gif'. Other file type

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
