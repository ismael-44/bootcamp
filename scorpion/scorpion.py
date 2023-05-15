import sys
from PIL import Image
from PIL.ExifTags import TAGS

def show_metadata(image_path):
    try:

        with Image.open(image_path) as img:
        #Show basic metadata
            print(" ")
            print(" ")
            print(f"Image: {image_path}")
            print(f"Format: {img.format}")
            print(f"Size: {img.size}")
            print(f"Mode: {img.mode} ")

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

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Provide at least one image")
    else:
        for image_path in sys.argv[1:]:
            if image_path.endswith(('jpg', 'png' , 'bmp' , 'gif' )):
                show_metadata(image_path)
            else:
                print("Filetype not suported")