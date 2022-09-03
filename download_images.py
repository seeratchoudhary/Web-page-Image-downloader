from bs4 import BeautifulSoup
# importing BeautifulSoup library to crawl the website

import requests
import os


def create_folder():
    """Creates a folder in the current directory of the name provided by the user."""
    folder_name = ""
    try:
        folder_name = input("Enter the folder name to store the images:- ")
        os.mkdir(folder_name)
    except FileExistsError:
	    # if folder exists with that name, ask another name
        print("Folder Already Exist with that name!")
        create_folder()
    return folder_name


def download_images(images, folder_name):
    """Downloads all the images from the website."""
    # initial count is zero
    count = 0
    # print total images found in URL
    print(f"Total {len(images)} Image Found!")

    # checking if images is not zero
    if len(images) != 0:
        for i, image in enumerate(images):
            # From image tag ,Fetch image Source URL
                # 1.data-srcset
                # 2.data-src
                # 3.data-fallback-src
                # 4.src
            # Here we will use exception handling

            # first we will search for "data-srcset" in img tag
            image_link = image.get("data-srcset") or image.get("data-src") or image.get("data-fallback-src") or image.get("src")
            if not image_link:
                print("No image found in this tag")
                continue
            # After getting Image Source URL
            # We will try to get the content of image
            try:
                response_content = requests.get(image_link).content
                try:
                    # possibility of decode
                    response_content = str(response_content, 'utf-8')
                except UnicodeDecodeError:
                    # After checking above condition, Image Download start
                    with open(f"{folder_name}/images{i+1}.jpg", "wb+") as f:
                        f.write(response_content)
                    # counting number of image downloaded
                    count += 1
                else:
                    print("Invalid image content")
            except Exception as e:
                print("Exception occured while downloading image: ", e)
        # There might be possible, that all
        # images not download
        # if all images download
        if count == len(images):
            print("All Images Downloaded!")
        # if all images not download
        else:
            print(f"Total {count} Images Downloaded Out of {len(images)}")

# MAIN FUNCTION START
def main(url):
    # content of URL
    r = requests.get(url)
    # Parse HTML Code
    soup = BeautifulSoup(r.text, 'html.parser')
    # find all images in URL
    images = soup.findAll('img')
    # Call folder create function
    folder_name = create_folder()
    # image downloading start
    download_images(images, folder_name)

# take url
url = input("Enter URL:- ")
# CALL MAIN FUNCTION
main(url)
