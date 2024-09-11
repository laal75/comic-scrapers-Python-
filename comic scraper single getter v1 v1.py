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
    print(f"All images zipped into: {zip_filename}")

# Main function to scrape and download images
def scrape_images(url, directory='images', zip_filename='images.zip'):
    create_directory(directory)
    image_urls = extract_images_from_url(url)
    
    # Download each image if size is above 500 KB
    for idx, image_url in enumerate(image_urls):
        if not image_url.startswith('http'):
            image_url = f"{url}/{image_url}"  # Handle relative URLs
        image_path = os.path.join(directory, f'image_{idx}.jpg')
        download_image(image_url, image_path, min_size_kb=300)
    
    # Zip the downloaded images
    zip_images(directory, zip_filename)

# Ask the user for the URL and the zip file name
if __name__ == "__main__":
    while True :
        target_url = input("Enter the URL of the website to scrape images from: ")
        zip_name = input("Enter the name for the zip file (e.g., 'my_images.zip'): ")
        scrape_images(target_url, zip_filename=zip_name)
