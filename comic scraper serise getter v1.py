import requests
from bs4 import BeautifulSoup
import os
import zipfile
import shutil
import time

# Max retries for image download and page scraping
MAX_RETRIES = 3

# Function to download and save images, with optional size constraint and retry logic
def download_image(image_url, save_path, min_size_kb=None, retry_count=0):
    try:
        response = requests.get(image_url, stream=True, timeout=10)
        if response.status_code == 200:
            # Get image size from headers (Content-Length)
            image_size_kb = int(response.headers.get('Content-Length', 0)) / 1024 if response.headers.get('Content-Length') else None

            # Check if the image meets the minimum size requirement
            if min_size_kb is None or (image_size_kb and image_size_kb >= min_size_kb):
                with open(save_path, 'wb') as file:
                    file.write(response.content)
                print(f"Downloaded: {save_path} ({image_size_kb:.2f} KB)" if image_size_kb else f"Downloaded: {save_path}")
            else:
                print(f"Skipped: {image_url} (size: {image_size_kb:.2f} KB, below {min_size_kb} KB)")
        else:
            print(f"Failed to download {image_url}")
            if retry_count < MAX_RETRIES:
                print(f"Retrying {image_url}... Attempt {retry_count + 1}")
                time.sleep(2)  # Delay before retry
                return download_image(image_url, save_path, min_size_kb, retry_count + 1)
            else:
                print(f"Max retries reached for {image_url}. Skipping this image.")
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
        print(f"Error downloading {image_url}: {e}")
        if retry_count < MAX_RETRIES:
            print(f"Retrying {image_url}... Attempt {retry_count + 1}")
            time.sleep(2)  # Delay before retry
            return download_image(image_url, save_path, min_size_kb, retry_count + 1)
        else:
            print(f"Max retries reached for {image_url}. Skipping this image.")

# Function to filter out unwanted images (logo or banner)
def is_valid_image(image_url):
    lower_url = image_url.lower()
    return "logo" not in lower_url and "banner" not in lower_url

# Function to scrape images from the webpage, with retry logic
def extract_images_from_url(url, retry_count=0):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None  # Return None if the page is missing
        soup = BeautifulSoup(response.text, 'html.parser')
        image_tags = soup.find_all('img')

        # Extract image URLs and filter out logos and banners
        image_urls = [img['src'] for img in image_tags if 'src' in img.attrs and is_valid_image(img['src'])]
        return image_urls
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
        print(f"Error scraping the webpage {url}: {e}")
        if retry_count < MAX_RETRIES:
            print(f"Retrying {url}... Attempt {retry_count + 1}")
            time.sleep(2)  # Delay before retry
            return extract_images_from_url(url, retry_count + 1)
        else:
            print(f"Max retries reached for {url}. Skipping this comic.")
            return None

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

# Function to clean up folders after zipping
def cleanup_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
        print(f"Cleaned up folder: {directory}")

# Main function to scrape, download, zip images, and clean up folders
def scrape_images_per_page_with_optional_year(base_url, start_num, end_num, year, zip_name_format, min_size_kb=None, zero_padding=0):
    for n in range(start_num, end_num + 1):
        # Format the issue number with the specified zero padding
        formatted_issue = f"{n:0{zero_padding}d}"
        current_year = year if year else ""  # Use the year if provided, otherwise empty
        
        url = base_url.replace("{n}", formatted_issue).replace("{year}", str(current_year)) if year else base_url.replace("{n}", formatted_issue).replace("-{year}", "")
        
        print(f"Scraping images from: {url}")
        image_urls = extract_images_from_url(url)
        
        if image_urls is None:
            print(f"Skipping comic {formatted_issue}. Unable to load page.")
            continue
        
        # Create a directory for the current page's images
        page_directory = f"page_{formatted_issue}_images"
        create_directory(page_directory)
        
        # Extract and download images from the current page URL
        for idx, image_url in enumerate(image_urls):
            if not image_url.startswith('http'):
                image_url = f"{url}/{image_url}"  # Handle relative URLs
            image_path = os.path.join(page_directory, f'image_{formatted_issue}_{idx}.jpg')
            download_image(image_url, image_path, min_size_kb=min_size_kb)
        
        # Create a zip file for this page's images with the custom name
        zip_filename = zip_name_format.replace("{n}", formatted_issue).replace("{year}", str(current_year)) + ".zip"
        zip_images(page_directory, zip_filename)

        # Clean up the folder after zipping
        cleanup_directory(page_directory)

# Ask the user for the URL pattern, number range, and the custom zip name format
if __name__ == "__main__":
    base_url = input("Enter the URL pattern (use {n} for the number and {year} for the year, e.g., 'https://readallcomics.com/scooby-apocalypse-{n}-{year}/'): ")
    start_num = int(input("Enter the starting number: "))
    end_num = int(input("Enter the ending number: "))
    year_input = input("Enter the starting year (leave blank if there is no year): ")
    year = int(year_input) if year_input else None
    zip_name_format = input("Enter the custom zip name format (use {n} for the number and {year} for the year, e.g., 'scooby-apocalypse-{n}-{year}'): ")
    
    # Ask how many leading zeroes the user wants
    zero_padding = int(input("How many digits should the issue number have? (Enter 1 for no zero padding, 2 for 01, 3 for 001): "))

    # Ask the user for the minimum size constraint for images (if left blank, no constraint)
    min_size_input = input("Enter the minimum image size in KB (leave blank for no size constraint): ")
    min_size_kb = int(min_size_input) if min_size_input else None

    # Scrape images, zip them, and clean up folders for each page
    scrape_images_per_page_with_optional_year(base_url, start_num, end_num, year, zip_name_format, min_size_kb=min_size_kb, zero_padding=zero_padding)
