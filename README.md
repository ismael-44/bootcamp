# Python Script for Downloading Images from a Website

This Python script is designed to download images from a website. It takes a URL as input and allows for recursive downloading of images from the specified website. Here's a breakdown of the script:

## Necessary Libraries
 
 #### The script begins by importing the required libraries:
``` python
import argparse, os, sys, re, requests, urllib3, shutil
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```
The imported libraries are used for various purposes throughout the script, such as parsing HTML, making HTTP requests, handling URLs, and managing file operations.

## Global Variables

Next, several global variables are defined, including url_main, soup, images_list_var, link, domain, and link_filtered. These variables store important data and are used across different functions in the script.

## Downloading Images

The download function is responsible for downloading images. It takes a path and URL as input, and then iterates over the images_list_var list to download each image using the requests library. The downloaded images are saved in the specified path.

## Local Files

The local_file function is used to find and download images from a local HTML file. It takes a URL and a path as input. The HTML file is read and parsed using BeautifulSoup, and then the images are copied to the specified path using the shutil library.

## Finding Images

The image_src function is responsible for finding images within the parsed HTML. It uses BeautifulSoup to extract all <img> tags and checks their attributes to find image sources (src). Images ending with .jpg, .png, .gif, or .bmp extensions are added to the images_list_var list.

## Recursive Function

The recursive_fun function enables recursive parsing of the website's HTML. It takes parameters like recursive, path, max_depth, and loops. If the recursive flag is set to True, the function starts parsing the HTML of each discovered URL up to the specified max_depth. It maintains a list of visited URLs to avoid revisiting the same URL multiple times.

## Parsing HTML Code

The parse_section function is responsible for parsing the HTML code of the provided URL. It uses the requests library to fetch the HTML content and then utilizes BeautifulSoup to create a parsed HTML object (soup).

## URL Response Check

The url_responsecheck function checks if the provided URL responds properly. It uses the requests library to make a GET request to the URL and verifies that the status code is 200 (OK). If the response is not successful, the script exits.

## URL Syntax Checker

The url_filt function checks if the provided URL is valid. It uses a regular expression to match the URL format. If the URL is a valid file path, it checks if the file is an HTML file and calls the local_file function. If the URL is not valid, the script exits.

## Path Filter

The path_filt function checks if the specified path exists. If the path doesn't exist, the function asks the user if they want to create it. If the user confirms, the directory is created. If the user declines or enters an invalid response, the script exits.

## Main Function

The main function is the entry point of the script. It utilizes the argparse library to parse command-line arguments and assigns them to variables. It then calls the necessary filter and action functions in the specified order to perform the image downloading process.

## Execution of the Script

At the end of the script, the main function is executed if the script is run directly (not imported as a module). This ensures that the image downloading process is triggered when the script is executed from the command line.

To use the script, you need to provide the following command-line arguments:

```python
    -r or --recursive: Use this flag to enable recursive downloading. If not specified, only images from the provided URL will be downloaded.
    -l or --depth: Specify the maximum depth of recursion. The script will follow links up to the specified depth while performing recursive downloading. The default value is 5, and the available choices are 1, 2, 3, 4, and 5.
    -p or --path: Specify the folder where the downloaded images will be saved. Provide the absolute path to the folder. The default path is "./data/".
    url: Provide the URL of the website from which you want to download images.
```
