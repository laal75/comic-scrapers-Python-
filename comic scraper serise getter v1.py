import requests
from bs4 import BeautifulSoup
import os
import zipfile

# Function to download and save images if they are above a size limit
def download_image(image_url, save_path, min_size_kb=500):
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            # Get image size from headers (Content-Length)
            image_size_kb = int(response.headers.get('Content-Length', 0)) / 1024
            if image_size_kb >= min_size_kb:
                with open(save_path, 'wb') as file:
                    file.write(response.content)
                print(f"Downloaded: {save_path} ({image_size_kb:.2f} KB)")
            else:
                print(f"Skipped: {image_url} (size: {image_size_kb:.2f} KB, below {min_size_kb} KB)")
        else:
            print(f"Failed to download {image_url}")
    except Exception as e:
        print(f"Error downloading {image_url}: {e}")

# Function to scrape images from the webpage
def extract_images_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        image_tags = soup.find_all('img')
        
        # Extract image URLs
        image_urls = [img['src'] for img in image_tags if 'src' in img.attrs]
        return image_urls
    except Exception as e:
        print(f"Error scraping the webpage {url}: {e}")
        return []

# Function to create a directory if it doesn't exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to create a zip file from a directory
def zip_images(directory, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, directory))
    print(f"Images zipped into: {zip_filename}")

# Main function to scrape, download, and zip images for each page separately
def scrape_images_per_page(base_url, start_num, end_num, zip_name_format, min_size_kb=500):
    # Loop through the range of numbers (e.g., 1 to 25)
    for n in range(start_num, end_num + 1):
        url = base_url.replace("{n}", str(n))
        print(f"Scraping images from: {url}")
        
        # Create a directory for the current page's images
        page_directory = f"page_{n}_images"
        create_directory(page_directory)
        
        # Extract and download images from the current page URL
        image_urls = extract_images_from_url(url)
        for idx, image_url in enumerate(image_urls):
            if not image_url.startswith('http'):
                image_url = f"{url}/{image_url}"  # Handle relative URLs
            image_path = os.path.join(page_directory, f'image_{n}_{idx}.jpg')
            download_image(image_url, image_path, min_size_kb=min_size_kb)
        
        # Create a zip file for this page's images with the custom name
        zip_filename = zip_name_format.replace("{n}", str(n)) + ".zip"
        zip_images(page_directory, zip_filename)

# Ask the user for the URL pattern, number range, and the custom zip name format
if __name__ == "__main__":
    base_url = input("Enter the URL pattern (use {n} for the number, e.g., 'https://readallcomics.com/poison-ivy-{n}-2022/'): ")
    start_num = int(input("Enter the starting number: "))
    end_num = int(input("Enter the ending number: "))
    zip_name_format = input("Enter the custom zip name format (use {n} for the number, e.g., 'poison-ivy-{n}'): ")
    
    # Scrape images and zip them for each page with custom zip name
    scrape_images_per_page(base_url, start_num, end_num, zip_name_format)
