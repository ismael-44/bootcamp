#Necesary libraries
import argparse, os, sys, re, requests, urllib3, shutil
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
#Disable unsecure warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Definition of global variables
url_main = None
soup = None
images_list_var = None
link = None
domain = None
link_filtered = []

############### Downloading images ###############

#Download images
def download(path, url):
    url_dict = urlparse(url)
    domain = url_dict.netloc
    protocol = url_dict.scheme
    url_main = (protocol + "://" + domain)
    imagecounter = 0
    print("Downloading images...")
    for i in images_list_var:
        try:
            if i.startswith("/"):
                concatenated = url_main + i
                req = requests.get(concatenated , verify=False).content
            else:
                req = requests.get(i , verify=False).content
            imagename = i.split("/")[-1]
            image_savename = path + "/" + imagename
            if not os.path.exists(image_savename):
                with open(image_savename, 'wb') as f:
                    f.write(req)
                imagecounter = imagecounter+1
                print("Image downloaded. Total:" , imagecounter)
            else:
                print("Duplicated image skipped...")
        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError, requests.exceptions.ConnectTimeout ,requests.exceptions.SSLError) as err:
            print("There has been an error downloading this image")
            print(err)
            print("###############################################")
            continue
    print(imagecounter , "images downloaded on" , path)

############### End of downloading images ###############



############### Local files ###############
#Find and download the images on a local html file

def local_file(url, path):
    with open(url, 'rb') as f:
        contents = f.read()
    html = BeautifulSoup(contents, features="html.parser")
    image_src(html)
    print("Moving local files to the path selected...", images_list_var)
    print(path)
    for i in images_list_var:
        try:
            shutil.copy(str(i), path)
        except(FileExistsError, FileNotFoundError) as e:
            print(e)
            print("Cant move the images to the path folder. Chekc if the foldername doesnt have spaces or special characters")
    print("Files copied")
    exit()
############### End of local files ###############



############### Finding images ###############

#Find images on the parsed html
def image_src(soup):    
    images = soup.find_all('img')
    global images_list_var
    images_list = []
    print("Searching images...")
    for i in images:
        try:
            imgsrc=i['data-srcset']
        except:
            try:
                imgsrc=i['data-src']
            except:
                try:
                    imgsrc=i['data-fallback-src']
                except:
                    try:
                        imgsrc=i['src']
                    except:
                        pass

        if imgsrc.endswith(".jpg") or imgsrc.endswith(".png") or imgsrc.endswith(".gif") or imgsrc.endswith(".bmp"):
            images_list.append(imgsrc)
    images_list_var = images_list

############### End of finding images ###############



############### Recursive ###############
visited = []
def recursive_fun(recursive, path, max_depth, loops):
    global visited
    if recursive == True:
        if (loops in visited):
            return
        visited.append(loops)
        global url_main
        global soup
        global domain
        if not max_depth == 0:  
            link_urls = [link['href'] for link in soup.find_all('a') if 'href' in link.attrs]
            for links in link_urls:
                if links.startswith("/"):
                    concatenated = url_main + links
                    if concatenated.startswith(url_main):
                        if concatenated not in link_filtered:
                            link_filtered.append(concatenated)
                else:
                    if links.startswith(url_main):
                        if links not in link_filtered:
                            link_filtered.append(links)

            for loops in link_filtered:
                url_dict = urlparse(loops)
                domain = url_dict.netloc
                proto = url_dict.scheme
                url_main = (proto + "://" + domain)
                print("Parsing recursively...")
                try:
                    html_to_parse = requests.get(loops, verify=False)
                    html_to_parse.raise_for_status()
                except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError, requests.exceptions.ConnectTimeout ,requests.exceptions.SSLError) as err:
                    print("Error with this link. Skipping..")
                    continue
                soup = BeautifulSoup(html_to_parse.text, 'html.parser')
                image_src(soup)
                download(path, loops)
                recursive_fun(recursive, path, max_depth -1, loops)
                print("Current depth" , max_depth)
        else:
            return

############### End recursive ###############


############### Parsing html code ###############

#Getting the html code to filter
def parse_section(url):
    global url_main
    global soup
    global domain
    url_dict = urlparse(url)
    domain = url_dict.netloc

    proto = url_dict.scheme
    url_main = (proto + "://" + domain)
    print("Parsing html code...")
    try:
        html_to_parse = requests.get(url, verify=False)
        html_to_parse.raise_for_status()
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError, requests.exceptions.ConnectTimeout ,requests.exceptions.SSLError) as err:
        print("#######################################")
        print("## Error trying to get the html code ##")
        print("#######################################")
        print(err)
        sys.exit()
    soup = BeautifulSoup(html_to_parse.text, 'html.parser')

############### End of parsing html code ###############



############### Trying to reach the URL ###############

#Checking if the url responds properly, if not, script exit
def url_responsecheck(url):
    try:
        request = requests.get(url , verify=False)
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError, requests.exceptions.ConnectTimeout ,requests.exceptions.SSLError) as err:
        print("###################################")
        print("## Error trying to reach the url ##")
        print("###################################")
        print(err)
        print("###################################")
        sys.exit()
    if not request.status_code == 200:
        print("The url is not responding properly")
        print(request.status_code)
        sys.exit() 

############### End of trying to reach the URL ###############



############### URL syntax checker ###############

#Checking if the url is valid, if not, script exit
def url_filt(url, path):
    regex = "^((http|https)://)[-a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)$"
    r = re.compile(regex)
    if (re.search(r , url)):
        print("")
    elif os.path.exists(url):
        if not url.endswith(".html"):
            print("Filetype not suported")
            exit()
        local_file(url, path)
    else:
        print("This is not a valid URL or filepath")        
        sys.exit()

############### Enf of URL syntax checker ###############



############### Path Filter ###############

#Cheking if the path exist, if not, you can create, else script exit
def path_filt(path):
    if not os.path.exists(path):
            print("This path doesnt exist")
            while True:
                user = input('Do you want to create it? (Yes / no)')
                if user.capitalize() == 'Yes':
                    try:
                        os.makedirs(path)
                        print("Directory created")
                        break
                    except(PermissionError):
                        print("Dont have permission to create the dir")
                        exit()
                elif user.capitalize() == 'No':
                    print('Use -p option and specify another path')
                    sys.exit()
                else:
                    print('Enter Yes or No')
                    continue

############### End of path filter ###############



############### MAIN ###############

#Recive all the parameters
def main():
    parser = argparse.ArgumentParser(description="Download images form a website")
    parser.add_argument("-r", "--recursive" , help="Do it recursevely", action="store_true" , default=False)
    parser.add_argument("-l" , "--depth" , type=int , help="Max recursive depth" , default=5 , choices=[1,2,3,4,5])
    parser.add_argument("-p", "--path" , help="Folder to save the images. Type absolute path", type=str , default="./data/")
    parser.add_argument("url", help="Provide a valid URL" , type=str)
    args = parser.parse_args()

#Adding arguments to variables
    recursive = args.recursive
    max_depth = args.depth
    path = args.path
    url = args.url

#Calling filter acction functions
    path_filt(path)
    url_filt(url, path)
    url_responsecheck(url)
    parse_section(url)
    recursive_fun(recursive, path, max_depth, url)
    image_src(soup)
    download(path,url)

############### END OF MAIN ###############

#Executing main function
if __name__ == '__main__':
    main()

